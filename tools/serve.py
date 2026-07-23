#!/usr/bin/env python3
"""Local server for the HTML apps. Stdlib only.

Serves apps/ statically plus a tiny JSON API over student/ data.
On every result POST it writes student/.event-<app>.json so the tutor can
wait on that file and resume the session automatically.

Usage: python3 tools/serve.py [port]     (default 8765)

API:
  GET  /api/deck      due cards
  POST /api/deck      {"results":[{"id":..,"grade":1-4},..]} -> grades cards, event
  GET  /api/progress  streak/level/vocab/errors summary for the dashboard
  GET  /api/quiz      contents of student/quiz-current.json (tutor writes it)
  POST /api/quiz      quiz results -> event
  GET  /api/text      contents of student/reading-current.json (tutor writes it)
  POST /api/text      {"addWord": ..} -> queued for the tutor, event
"""
import json
import re
import sys
import urllib.parse
from datetime import date, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import srs
import tts

ROOT = Path(__file__).resolve().parent.parent
STUDENT = ROOT / "student"
APPS = ROOT / "apps"


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


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


def due_cards():
    d = lang_dir()
    if d is None:
        return []
    deck = read_json(d / "cards.json", {"cards": []})["cards"]
    today = date.today().isoformat()
    return [c for c in deck if c.get("due") is None or c["due"] <= today]


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
            self._json({"cards": due_cards()})
        elif self.path == "/api/progress":
            self._json(progress_payload())
        elif self.path == "/api/quiz":
            quiz = read_json(STUDENT / "quiz-current.json", None)
            self._json(quiz or {"error": "no quiz prepared"}, 200 if quiz else 404)
        elif self.path == "/api/text":
            text = read_json(STUDENT / "reading-current.json", None)
            self._json(text or {"error": "no text prepared"}, 200 if text else 404)
        else:
            super().do_GET()

    def do_POST(self):
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


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"serving apps/ on http://localhost:{port} — Ctrl-C to stop")
    server.serve_forever()


if __name__ == "__main__":
    main()
