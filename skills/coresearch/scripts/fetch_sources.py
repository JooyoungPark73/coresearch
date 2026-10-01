#!/usr/bin/env python3
"""Fetch explicit open-access PDF URLs with transport provenance, not claim verification."""
from __future__ import annotations

import argparse
import hashlib
import http.client
import ipaddress
import json
import math
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit

MAX_BYTES = 25 * 1024 * 1024
REDIRECTS = {301, 302, 303, 307, 308}


def checked_url(url: str):
    if not isinstance(url, str) or not url.isascii() or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url):
        raise ValueError("URL must be ASCII with no whitespace or control characters")
    parts = urlsplit(url)
    if (parts.scheme != "https" or not parts.hostname or parts.username is not None
            or parts.password is not None or parts.port not in (None, 443)
            or "%" in parts.hostname or "\\" in url):
        raise ValueError("URL must use HTTPS on port 443 without credentials")
    return parts


def load_sources(path: Path) -> list[dict]:
    sources = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(sources, list) or not sources:
        raise ValueError("manifest must be a nonempty JSON array")
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        identifier = source.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", identifier):
            raise ValueError("source id must be a lowercase slug of 1-80 characters")
        if identifier in seen:
            raise ValueError(f"duplicate source id: {identifier}")
        seen.add(identifier)
        if not isinstance(source.get("title"), str) or not source["title"].strip():
            raise ValueError(f"missing title: {identifier}")
        if source.get("access") != "open":
            raise ValueError(f"source must be curated as open access: {identifier}")
        checked_url(source.get("url"))
    return sources


class PublicHTTPSConnection(http.client.HTTPSConnection):
    """Resolve once, reject any nonpublic answer, and pin the TLS socket to that IP."""

    def connect(self):
        addresses = socket.getaddrinfo(self.host, self.port, type=socket.SOCK_STREAM)
        if not addresses:
            raise OSError("host has no addresses")
        for *_, address in addresses:
            ip = ipaddress.ip_address(address[0])
            mapped = getattr(ip, "ipv4_mapped", None)
            for candidate in (ip, mapped) if mapped else (ip,):
                if not candidate.is_global or candidate.is_multicast or candidate.is_reserved:
                    raise OSError("refusing nonpublic address")
        last_error = None
        for family, kind, protocol, _, address in addresses:
            raw = socket.socket(family, kind, protocol)
            try:
                raw.settimeout(self.timeout)
                raw.connect(address)
                self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
                return
            except OSError as error:
                raw.close()
                last_error = error
        raise last_error or OSError("connection failed")


def download(url: str, destination: Path, *, max_bytes: int, timeout: float) -> dict:
    temporary = destination.with_suffix(".part")
    if destination.exists() or destination.is_symlink() or temporary.exists() or temporary.is_symlink():
        raise FileExistsError(f"preserving existing download: {destination}")
    created = False
    try:
        for redirects in range(6):
            parts = checked_url(url)
            connection = PublicHTTPSConnection(parts.hostname, timeout=timeout)
            try:
                target = parts.path or "/"
                if parts.query:
                    target += "?" + parts.query
                connection.request("GET", target, headers={"User-Agent": "coresearch/2", "Accept": "application/pdf"})
                response = connection.getresponse()
                if response.status in REDIRECTS:
                    location = response.getheader("Location")
                    if not location or redirects == 5:
                        raise ValueError("missing redirect location or redirect limit exceeded")
                    url = urljoin(url, location)
                    continue
                if response.status != 200:
                    raise ValueError(f"HTTP {response.status}")
                length = response.getheader("Content-Length")
                if length is not None and (not length.isdecimal() or int(length) > max_bytes):
                    raise ValueError("invalid or excessive Content-Length")
                digest = hashlib.sha256()
                size = 0
                prefix = b""
                with temporary.open("xb") as stream:
                    created = True
                    while chunk := response.read1(min(65536, max_bytes - size + 1)):
                        size += len(chunk)
                        if size > max_bytes:
                            raise ValueError("PDF exceeds byte limit")
                        prefix = (prefix + chunk)[:5]
                        if len(prefix) == 5 and prefix != b"%PDF-":
                            raise ValueError("response does not have a PDF signature")
                        stream.write(chunk)
                        digest.update(chunk)
                if prefix != b"%PDF-":
                    raise ValueError("response does not have a PDF signature")
                if length is not None and size != int(length):
                    raise ValueError("truncated response")
                # The caller owns a fresh output directory; do not reuse old artifacts.
                temporary.rename(destination)
                return {"final_url": url, "bytes": size, "sha256": digest.hexdigest()}
            finally:
                connection.close()
    finally:
        if created:
            temporary.unlink(missing_ok=True)
    raise ValueError("redirect limit exceeded")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_report(output: Path, report: dict) -> None:
    temporary = output / ".report.tmp"
    temporary.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(output / "report.json")


def collect(sources: list[dict], output: Path, *, max_bytes: int, timeout: float) -> int:
    output.mkdir(parents=True)  # Exclusive: an existing directory is never reused.
    report = {"started_at": now(), "sources": [{"source": source, "status": "pending"} for source in sources]}
    write_report(output, report)
    failures = 0
    for entry in report["sources"]:
        source = entry["source"]
        try:
            entry.update(download(source["url"], output / f"{source['id']}.pdf", max_bytes=max_bytes, timeout=timeout))
            entry.update(status="downloaded", file=f"{source['id']}.pdf")
        except (OSError, ValueError, http.client.HTTPException) as error:
            entry.update(status="error", error=str(error))
            failures += 1
        entry["finished_at"] = now()
        write_report(output, report)
        print(f"{source['id']}: {entry['status']}")
    report["finished_at"] = now()
    write_report(output, report)
    return int(failures > 0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--dry-run", action="store_true", help="validate only; no network or writes")
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    parser.add_argument("--timeout", type=float, default=30, help="socket timeout in seconds, not a process deadline")
    args = parser.parse_args(argv)
    try:
        if args.max_bytes < 5 or not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError("max-bytes must be at least 5 and timeout must be finite and positive")
        sources = load_sources(args.manifest)
        if args.output.exists() or args.output.is_symlink():
            raise FileExistsError(f"output must be a new directory: {args.output}")
        if args.dry_run:
            print(f"Validated {len(sources)} sources; no network or writes.")
            return 0
        return collect(sources, args.output, max_bytes=args.max_bytes, timeout=args.timeout)
    except (OSError, ValueError) as error:
        print(f"fetch_sources: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrupted; report retains completed and pending sources.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
