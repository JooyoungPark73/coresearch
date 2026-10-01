"""Source retrieval tests. All network boundaries are mocked; file I/O is real."""
import hashlib
import importlib.util
import io
import json
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sources", ROOT / "skills/coresearch/scripts/fetch_sources.py")
sources = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sources)
PDF = b"%PDF-1.4\ntransport fixture, not a scientific paper\n%%EOF\n"
PUBLIC = (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
PRIVATE = (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 443))


class Response:
    def __init__(self, body=PDF, status=200, headers=None):
        self.body = io.BytesIO(body)
        self.status = status
        self.headers = headers or {}

    def getheader(self, name):
        return self.headers.get(name)

    def read1(self, size):
        return self.body.read(size)


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.manifest = self.root / "sources.json"
        self.source = {"id": "paper-1", "title": "Example", "url": "https://example.org/paper.pdf", "access": "open", "doi": "test-only"}
        self.manifest.write_text(json.dumps([self.source]))

    def fetch(self, *responses, max_bytes=1000):
        connections = []
        for response in responses:
            connection = MagicMock()
            connection.getresponse.return_value = response
            connections.append(connection)
        factory = patch.object(sources, "PublicHTTPSConnection", side_effect=connections)
        with factory:
            result = sources.download(self.source["url"], self.root / "paper.pdf", max_bytes=max_bytes, timeout=1)
        for connection in connections:
            connection.close.assert_called_once()
        return result

    def test_manifest_preserves_metadata(self):
        self.assertEqual(sources.load_sources(self.manifest), [self.source])

    def test_invalid_manifests(self):
        cases = [[], {}, ["x"], [dict(self.source, id="../escape")], [dict(self.source, id="UPPER")],
                 [dict(self.source, title="")], [dict(self.source, access="unknown")],
                 [dict(self.source, url="http://example.org/x")], [self.source, self.source]]
        for data in cases:
            with self.subTest(data=data):
                self.manifest.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    sources.load_sources(self.manifest)

    def test_unsafe_url_syntax(self):
        for url in (None, "file:///etc/passwd", "http://example.org/x", "https://user:secret@example.org/x",
                    "https://example.org:8080/x", "https://example.org/\nx", "https://example.org\\evil/x",
                    "https://[::1%eth0]/x", "https://example.org/ü", "https:///x"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                sources.checked_url(url)

    def test_public_connection_pins_resolved_address_and_verifies_hostname(self):
        context = MagicMock()
        connection = sources.PublicHTTPSConnection("example.org", timeout=2, context=context)
        raw = MagicMock()
        with patch.object(sources.socket, "getaddrinfo", return_value=[PUBLIC]) as dns, patch.object(sources.socket, "socket", return_value=raw):
            connection.connect()
        dns.assert_called_once_with("example.org", 443, type=socket.SOCK_STREAM)
        raw.connect.assert_called_once_with(PUBLIC[-1])
        raw.settimeout.assert_called_once_with(2)
        context.wrap_socket.assert_called_once_with(raw, server_hostname="example.org")

    def test_mixed_public_private_answers_fail_before_connect(self):
        connection = sources.PublicHTTPSConnection("example.org", timeout=1)
        with patch.object(sources.socket, "getaddrinfo", return_value=[PUBLIC, PRIVATE]), patch.object(sources.socket, "socket") as sock:
            with self.assertRaises(OSError):
                connection.connect()
        sock.assert_not_called()

    def test_nonpublic_address_classes(self):
        for ip in ("10.0.0.1", "169.254.169.254", "0.0.0.0", "224.0.0.1", "192.0.2.1", "::1", "::ffff:127.0.0.1", "ff02::1"):
            address = (socket.AF_INET6 if ":" in ip else socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))
            with self.subTest(ip=ip), patch.object(sources.socket, "getaddrinfo", return_value=[address]), patch.object(sources.socket, "socket") as sock:
                with self.assertRaises(OSError):
                    sources.PublicHTTPSConnection("example.org", timeout=1).connect()
                sock.assert_not_called()

    def test_connection_failure_closes_socket(self):
        raw = MagicMock()
        raw.connect.side_effect = TimeoutError("timed out")
        with patch.object(sources.socket, "getaddrinfo", return_value=[PUBLIC]), patch.object(sources.socket, "socket", return_value=raw):
            with self.assertRaises(TimeoutError):
                sources.PublicHTTPSConnection("example.org", timeout=1).connect()
        raw.close.assert_called_once()

    def test_download_provenance_and_bytes(self):
        result = self.fetch(Response(headers={"Content-Length": str(len(PDF))}))
        self.assertEqual((self.root / "paper.pdf").read_bytes(), PDF)
        self.assertEqual(result["sha256"], hashlib.sha256(PDF).hexdigest())
        self.assertEqual(result["bytes"], len(PDF))
        self.assertEqual(result["final_url"], self.source["url"])
        self.assertFalse((self.root / "paper.part").exists())

    def test_relative_redirect(self):
        result = self.fetch(Response(status=302, headers={"Location": "/final.pdf"}), Response())
        self.assertEqual(result["final_url"], "https://example.org/final.pdf")

    def test_redirect_scheme_revalidated(self):
        with self.assertRaises(ValueError):
            self.fetch(Response(status=302, headers={"Location": "file:///etc/passwd"}))
        self.assertFalse((self.root / "paper.pdf").exists())

    def test_redirect_private_dns_revalidated(self):
        first = MagicMock()
        first.getresponse.return_value = Response(status=302, headers={"Location": "https://127.0.0.1/x"})
        actual = sources.PublicHTTPSConnection
        with patch.object(sources, "PublicHTTPSConnection", side_effect=[first, actual("127.0.0.1", timeout=1)]), patch.object(sources.socket, "getaddrinfo", return_value=[PRIVATE]):
            with self.assertRaises(OSError):
                sources.download(self.source["url"], self.root / "paper.pdf", max_bytes=1000, timeout=1)

    def test_redirect_limit(self):
        with self.assertRaises(ValueError):
            self.fetch(*[Response(status=302, headers={"Location": "/again"}) for _ in range(6)])

    def test_redirect_missing_location(self):
        with self.assertRaises(ValueError):
            self.fetch(Response(status=302))

    def test_html_mislabeled_as_pdf_is_rejected(self):
        with self.assertRaises(ValueError):
            self.fetch(Response(b"<html>not a paper</html>", headers={"Content-Type": "application/pdf"}))
        self.assertFalse((self.root / "paper.part").exists())
        self.assertFalse((self.root / "paper.pdf").exists())

    def test_signature_checks_small_chunks(self):
        response = Response()
        read = response.read1
        response.read1 = lambda size: read(min(size, 1))
        self.assertEqual(self.fetch(response)["bytes"], len(PDF))

    def test_excessive_header_and_stream(self):
        for headers in ({"Content-Length": "10000"}, {}):
            with self.subTest(headers=headers), self.assertRaises(ValueError):
                self.fetch(Response(headers=headers), max_bytes=10)
            self.assertFalse((self.root / "paper.pdf").exists())
            self.assertFalse((self.root / "paper.part").exists())

    def test_truncated_response(self):
        with self.assertRaises(ValueError):
            self.fetch(Response(headers={"Content-Length": str(len(PDF) + 1)}))
        self.assertFalse((self.root / "paper.part").exists())

    def test_empty_invalid_length_and_http_failure(self):
        for response in (Response(b""), Response(headers={"Content-Length": "-1"}), Response(status=404)):
            with self.subTest(response=response), self.assertRaises(ValueError):
                self.fetch(response)

    def test_existing_file_or_part_is_not_overwritten(self):
        for name in ("paper.pdf", "paper.part"):
            path = self.root / name
            path.write_bytes(b"keep")
            with self.assertRaises(FileExistsError):
                self.fetch(Response())
            self.assertEqual(path.read_bytes(), b"keep")
            path.unlink()

    def test_read_timeout_cleans_partial_download(self):
        response = Response()
        response.read1 = MagicMock(side_effect=[b"%PDF-", TimeoutError("timeout")])
        with self.assertRaises(TimeoutError):
            self.fetch(response)
        self.assertFalse((self.root / "paper.part").exists())

    def test_dry_run_never_connects_or_writes(self):
        output = self.root / "absent"
        with patch.object(sources.socket, "getaddrinfo", side_effect=AssertionError("network")):
            self.assertEqual(sources.main([str(self.manifest), "--output", str(output), "--dry-run"]), 0)
        self.assertFalse(output.exists())

    def test_invalid_limits_rejected(self):
        for flags in (["--max-bytes", "4"], ["--timeout", "nan"], ["--timeout", "inf"], ["--timeout", "0"]):
            with self.subTest(flags=flags):
                self.assertEqual(sources.main([str(self.manifest), "--output", str(self.root / "absent"), *flags]), 2)
        self.assertFalse((self.root / "absent").exists())

    def test_partial_collection_reports_each_source_without_verification(self):
        self.manifest.write_text(json.dumps([self.source, dict(self.source, id="missing")]))
        connection = MagicMock()
        connection.getresponse.side_effect = [Response(), Response(status=404)]
        output = self.root / "papers"
        with patch.object(sources, "PublicHTTPSConnection", return_value=connection):
            result = sources.main([str(self.manifest), "--output", str(output)])
        self.assertEqual(result, 1)
        report = json.loads((output / "report.json").read_text())
        first, second = report["sources"]
        self.assertEqual(first["source"], self.source)
        self.assertEqual(first["status"], "downloaded")
        self.assertEqual(second["status"], "error")
        self.assertIn("finished_at", report)
        self.assertEqual(first["sha256"], hashlib.sha256((output / first["file"]).read_bytes()).hexdigest())
        self.assertNotIn("verified", json.dumps(report))
        self.assertFalse((output / "missing.pdf").exists())
        self.assertEqual(sources.main([str(self.manifest), "--output", str(output)]), 2)
        self.assertEqual(json.loads((output / "report.json").read_text()), report)

    def test_interrupted_collection_preserves_pending_report(self):
        output = self.root / "papers"
        with patch.object(sources, "download", side_effect=KeyboardInterrupt):
            self.assertEqual(sources.main([str(self.manifest), "--output", str(output)]), 130)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(report["sources"][0]["status"], "pending")


if __name__ == "__main__":
    unittest.main()
