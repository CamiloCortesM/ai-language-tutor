#!/usr/bin/env python3
"""Local server for the HTML apps. Stdlib only.

Serves apps/ statically plus a tiny JSON API over student/ data.
On every result POST it writes student/.event-<app>.json so the tutor can
wait on that file and resume the session automatically.

Usage:
  python3 tools/serve.py [port]  start (default port 8765)
  python3 tools/serve.py status  check this project's server
  python3 tools/serve.py stop    stop this project's server
  python3 tools/serve.py selfcheck

API:
  GET  /api/deck      due cards
  POST /api/deck      {"results":[{"id":..,"grade":1-4},..]} -> grades cards, event
  GET  /api/progress  streak/level/vocab/errors summary for the dashboard
  GET  /api/quiz      contents of student/quiz-current.json (tutor writes it)
  POST /api/quiz      quiz results -> event
  GET  /api/text      contents of student/reading-current.json (tutor writes it)
  POST /api/text      {"addWord": ..} -> queued for the tutor, event
  GET  /api/dictation contents of student/dictation-current.json (tutor writes it)
  GET  /api/img/<f>   card image from student/<lang>/img/
"""
import json
import os
import re
import secrets
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import srs
import tts

ROOT = Path(__file__).resolve().parent.parent
STUDENT = ROOT / "student"
APPS = ROOT / "apps"
CONTROL = STUDENT / ".serve.json"


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def read_control():
    try:
        data = read_json(CONTROL, None)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("port"), int) \
            or not isinstance(data.get("token"), str):
        return None
    return data


def control_request(action, method="GET", timeout=2):
    data = read_control()
    if data is None:
        raise RuntimeError("no server control file")
    token = urllib.parse.quote(data["token"])
    url = f"http://127.0.0.1:{data['port']}/api/{action}?token={token}"
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def server_status():
    try:
        result = control_request("health")
    except (OSError, RuntimeError, urllib.error.URLError, json.JSONDecodeError):
        return None
    return read_control() if result.get("ok") else None


def stop_server():
    if read_control() is None:
        print("server not running")
        return 0
    try:
        control_request("shutdown", method="POST")
    except (OSError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"server did not respond; control file kept: {exc}", file=sys.stderr)
        return 1
    for _ in range(40):
        if not CONTROL.exists():
            break
        time.sleep(0.05)
    if CONTROL.exists():
        print("shutdown requested but not confirmed", file=sys.stderr)
        return 1
    print("server stopped")
    return 0


def write_event(app, payload):
    STUDENT.mkdir(exist_ok=True)
    out = {"app": app, "at": datetime.now().isoformat(timespec="seconds"), **payload}
    (STUDENT / f".event-{app}.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n")


def lang_dir():
    """Active language folder, or None when no student data exists yet."""
    try:
        return srs.lang_dir()
    except SystemExit:
        return None


def due_cards(limit=None):
    d = lang_dir()
    if d is None:
        return []
    deck = read_json(d / "cards.json", {"cards": []})["cards"]
    today = date.today().isoformat()
    due = [c for c in deck if c.get("due") is None or c["due"] <= today]
    # most-overdue reviews first, brand-new cards last
    due.sort(key=lambda c: (c.get("due") is None, c.get("due") or ""))
    return due[:limit] if limit else due


def progress_payload():
    d = lang_dir()
    if d is None:
        return {"streak": 0, "language": None, "level": None, "unit": 1,
                "levelPct": 0, "knownWords": 0, "dueCount": 0,
                "topErrors": [], "history": [0]}
    p = read_json(d / "progress.json",
                  {"streak": 0, "level": None, "unit": 1, "history": []})
    known_path = d / "known_words.txt"
    known = len([l for l in known_path.read_text().splitlines() if l.strip()]) \
        if known_path.exists() else 0
    errors = []
    err_path = d / "errors.md"
    if err_path.exists():
        for line in err_path.read_text().splitlines():
            m = re.match(r"^(\d+)[x×]\s*\|\s*([^|]+?)\s*\|\s*(.+)$", line.strip())
            if m:
                errors.append({"count": int(m.group(1)), "label": m.group(2),
                               "example": m.group(3)})
    errors.sort(key=lambda e: -e["count"])
    history = [h["known_words"] for h in p.get("history", []) if "known_words" in h]
    return {
        "streak": p.get("streak", 0), "language": d.name, "level": p.get("level"),
        "unit": p.get("unit", 1), "levelPct": round((p.get("unit", 1) - 1) / 12 * 100),
        "knownWords": known, "dueCount": len(due_cards()),
        "topErrors": errors[:3], "history": history or [known],
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APPS), **kwargs)

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/health":
            token = (urllib.parse.parse_qs(parsed.query).get("token") or [""])[0]
            if not secrets.compare_digest(token, self.server.shutdown_token):
                return self._json({"error": "forbidden"}, 403)
            return self._json({"ok": True})
        if self.path.startswith("/api/tts"):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            text = (qs.get("text") or [""])[0].strip()
            try:
                path = tts.synth(text) if text else None
            except Exception:
                path = None
            if path is None:  # no premium provider or synth failed -> app falls back to browser voice
                self.send_response(204)
                self.end_headers()
                return
            body = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/deck":
            # ponytail: fixed 30-card session cap; make it configurable if anyone asks
            self._json({"cards": due_cards(limit=30), "totalDue": len(due_cards())})
        elif self.path == "/api/progress":
            self._json(progress_payload())
        elif self.path == "/api/quiz":
            quiz = read_json(STUDENT / "quiz-current.json", None)
            self._json(quiz or {"error": "no quiz prepared"}, 200 if quiz else 404)
        elif self.path == "/api/text":
            text = read_json(STUDENT / "reading-current.json", None)
            self._json(text or {"error": "no text prepared"}, 200 if text else 404)
        elif self.path == "/api/dictation":
            dic = read_json(STUDENT / "dictation-current.json", None)
            self._json(dic or {"error": "no dictation prepared"}, 200 if dic else 404)
        elif self.path.startswith("/api/img/"):
            d = lang_dir()
            name = Path(urllib.parse.unquote(self.path[len("/api/img/"):])).name  # basename only — no traversal
            f = d / "img" / name if d else None
            if f and f.is_file():
                body = f.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._json({"error": "no image"}, 404)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/shutdown":
            token = (urllib.parse.parse_qs(parsed.query).get("token") or [""])[0]
            if not secrets.compare_digest(token, self.server.shutdown_token):
                return self._json({"error": "forbidden"}, 403)
            self._json({"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._json({"error": "bad json"}, 400)
        if self.path == "/api/deck":
            d = lang_dir()
            if d is None:
                return self._json({"error": "no student data yet"}, 400)
            data = read_json(d / "cards.json", {"cards": []})
            today = date.today()
            graded = 0
            for r in body.get("results", []):
                for card in data["cards"]:
                    if card.get("id") == r.get("id"):
                        srs.review(card, int(r["grade"]), today)
                        graded += 1
            srs.save(d / "cards.json", data)
            write_event("flashcards", {"graded": graded, **body})
            self._json({"ok": True, "graded": graded})
        elif self.path == "/api/quiz":
            write_event("quiz", body)
            self._json({"ok": True})
        elif self.path == "/api/text":
            write_event("reader", body)
            self._json({"ok": True})
        else:
            self._json({"error": "unknown endpoint"}, 404)

    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass


def selfcheck():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.shutdown_token = secrets.token_urlsafe(24)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    token = urllib.parse.quote(server.shutdown_token)
    with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/api/health?token={token}", timeout=2) as response:
        assert json.loads(response.read()) == {"ok": True}
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/api/shutdown?token={token}", method="POST")
    with urllib.request.urlopen(request, timeout=2) as response:
        assert json.loads(response.read()) == {"ok": True}
    thread.join(timeout=2)
    server.server_close()
    assert not thread.is_alive()
    print("server selfcheck OK")


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else None
    if command == "stop":
        raise SystemExit(stop_server())
    if command == "status":
        data = server_status()
        print(f"server running on http://localhost:{data['port']}" if data else "server not running")
        raise SystemExit(0 if data else 1)
    if command == "selfcheck":
        selfcheck()
        return

    running = server_status()
    if running:
        print(f"server already running on http://localhost:{running['port']}")
        return
    if CONTROL.exists():
        CONTROL.unlink()

    port = int(command) if command else 8765
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.shutdown_token = secrets.token_urlsafe(24)
    port = server.server_address[1]
    STUDENT.mkdir(exist_ok=True)
    CONTROL.write_text(json.dumps({
        "pid": os.getpid(), "port": port, "token": server.shutdown_token,
        "root": str(ROOT),
    }, indent=2) + "\n")
    print(f"serving apps/ on http://localhost:{port} — run 'python3 tools/serve.py stop' to stop",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        current = read_control()
        if current and secrets.compare_digest(current["token"], server.shutdown_token):
            CONTROL.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
