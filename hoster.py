#!/usr/bin/env python3
"""Simple file hoster.

- Creates a few sample files/folders next to this script.
- Serves the script directory over HTTP so files can be downloaded via a browser.

Usage:
  python hoster.py
  python hoster.py --port 8000 --bind 0.0.0.0
"""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def ensure_sample_content(base_dir: Path) -> None:
    """Create a minimal set of files/folders to download."""
    downloads_dir = base_dir / "downloads"
    sub_dir = downloads_dir / "folder"

    sub_dir.mkdir(parents=True, exist_ok=True)

    (downloads_dir / "hello.txt").write_text(
        "Hello! Ini file contoh.\nBuka folder ini dari browser untuk download.\n",
        encoding="utf-8",
    )
    (sub_dir / "inside.txt").write_text(
        "Ini file di dalam subfolder.\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Host file/folder sederhana via browser")
    parser.add_argument("--port", type=int, default=8000, help="Port HTTP (default: 8000)")
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="Bind address (default: 127.0.0.1; pakai 0.0.0.0 untuk akses dari device lain)",
    )
    parser.add_argument(
        "--no-create",
        action="store_true",
        help="Jangan buat file/folder contoh otomatis",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    base_dir = Path(__file__).resolve().parent
    if not args.no_create:
        ensure_sample_content(base_dir)

    handler = lambda *a, **kw: SimpleHTTPRequestHandler(*a, directory=str(base_dir), **kw)  # noqa: E731

    httpd = ThreadingHTTPServer((args.bind, args.port), handler)

    url_host = "localhost" if args.bind in {"127.0.0.1", "::1", "localhost"} else args.bind
    print(f"Serving folder: {base_dir}")
    print(f"Open in browser: http://{url_host}:{args.port}/")
    print(f"Downloads folder: http://{url_host}:{args.port}/downloads/")
    print("Press Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
