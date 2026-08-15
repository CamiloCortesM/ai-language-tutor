#!/usr/bin/env python3
"""Spaced-repetition scheduler (FSRS) + streak. Stdlib only.

Data: student/<active>/cards.json, student/<active>/progress.json.
Commands:
  due                    print due cards as JSON
  grade <id> <1-4>       apply a review grade (1 Again, 2 Hard, 3 Good, 4 Easy)
  add                    add cards from a JSON array on stdin
  img <id> <query>       fetch a CC image (Openverse) for a card -> student/<lang>/img/
  streak                 update and print the streak (call once per study day)
  stats                  deck counts
  selfcheck              run internal assertions on temp data

ponytail: simplified FSRS-4.5 with default weights; swap in py-fsrs and the
optimizer only if a learner accumulates thousands of reviews.
"""
import json
import math
import sys
import uuid
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STUDENT = ROOT / "student"


def lang_dir():
    """Active language folder inside student/ (one folder per language studied)."""
    active = STUDENT / "active.txt"
    if active.exists():
        d = STUDENT / active.read_text().strip()
        if d.is_dir():
            return d
    dirs = [d for d in STUDENT.iterdir()
            if d.is_dir() and not d.name.startswith(".")] if STUDENT.exists() else []
    if len(dirs) == 1:
        return dirs[0]
    sys.exit("no active language folder — write its name to student/active.txt (e.g. 'english')")


def cards_path():
    return lang_dir() / "cards.json"


def progress_path():
    return lang_dir() / "progress.json"

W = [0.4872, 1.4003, 3.7145, 13.8206, 5.1618, 1.2298, 0.8975, 0.031,
     1.6474, 0.1367, 1.0461, 2.1072, 0.0793, 0.3246, 1.587, 0.2272, 2.8755]
FACTOR = 19 / 81  # forgetting-curve constant; interval ≈ S at 90% retention


def load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def retrievability(card, today):
    t = (today - date.fromisoformat(card["last_review"])).days
    return (1 + FACTOR * t / max(card["S"], 0.1)) ** -0.5


def review(card, grade, today):
    if card.get("last_review") is None:
        card["S"] = W[grade - 1]
        card["D"] = min(10.0, max(1.0, W[4] - math.exp(W[5] * (grade - 1)) + 1))
    else:
        r = retrievability(card, today)
        d, s = card["D"], card["S"]
        if grade == 1:
            card["S"] = min(s, W[11] * d ** -W[12] * ((s + 1) ** W[13] - 1) * math.exp(W[14] * (1 - r)))
            card["lapses"] = card.get("lapses", 0) + 1
        else:
            hard = W[15] if grade == 2 else 1.0
            easy = W[16] if grade == 4 else 1.0
            card["S"] = s * (1 + math.exp(W[8]) * (11 - d) * s ** -W[9]
                             * (math.exp(W[10] * (1 - r)) - 1) * hard * easy)
        delta = -W[6] * (grade - 3)
        card["D"] = min(10.0, max(1.0, d + delta * (10 - d) / 9))
    card["reps"] = card.get("reps", 0) + 1
    card["last_review"] = today.isoformat()
    interval = 0 if grade == 1 else max(1, round(card["S"]))
    card["due"] = (today + timedelta(days=interval)).isoformat()
    return interval


def validate_card(card):
    if not isinstance(card, dict):
        raise ValueError("each card must be a JSON object")
    front, answer, hint = card.get("front"), card.get("answer"), card.get("hint")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("each card needs a non-empty answer")
    if not isinstance(hint, str) or not hint.strip():
        raise ValueError("each card needs a non-empty L1 hint")
    if not isinstance(front, str) or front.count("___") != 1:
        raise ValueError("each card front needs exactly one ___")
    if sum(ch.isalnum() for ch in front.replace("___", "")) < 3:
        raise ValueError("each card front needs meaningful sentence context around ___")


def cmd_due(today):
    deck = load(cards_path(), {"cards": []})["cards"]
    due = [c for c in deck if c.get("due") is None or c["due"] <= today.isoformat()]
    print(json.dumps(due, indent=2, ensure_ascii=False))


def cmd_grade(card_id, grade, today):
    data = load(cards_path(), {"cards": []})
    for card in data["cards"]:
        if card["id"] == card_id:
            interval = review(card, grade, today)
            save(cards_path(), data)
            print(json.dumps({"id": card_id, "next_due": card["due"], "interval_days": interval}))
            return
    sys.exit(f"no card with id {card_id}")


def cmd_add(today):
    new = json.loads(sys.stdin.read())
    if isinstance(new, dict):
        new = [new]
    if not isinstance(new, list):
        sys.exit("cards must be a JSON object or array")
    try:
        for card in new:
            validate_card(card)
    except ValueError as e:
        sys.exit(f"invalid card: {e}")
    data = load(cards_path(), {"cards": []})
    for card in new:
        card.setdefault("id", uuid.uuid4().hex[:8])
        card.setdefault("last_review", None)
        card.setdefault("due", today.isoformat())
        card.setdefault("reps", 0)
        card.setdefault("lapses", 0)
        data["cards"].append(card)
    save(cards_path(), data)
    print(f"added {len(new)} card(s), deck now {len(data['cards'])}")


def cmd_img(card_id, query):
    import urllib.parse
    import urllib.request
    if not query:
        sys.exit("usage: img <card-id> <search query>")
    data = load(cards_path(), {"cards": []})
    card = next((c for c in data["cards"] if c["id"] == card_id), None)
    if card is None:
        sys.exit(f"no card with id {card_id}")
    ua = {"User-Agent": "learning-language-tutor/1.0"}
    api = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": query, "page_size": 3, "mature": "false"})
    hits = json.loads(urllib.request.urlopen(
        urllib.request.Request(api, headers=ua), timeout=15).read())["results"]
    if not hits:
        sys.exit(f"no images found for {query!r}")
    pick = hits[0]
    raw = urllib.request.urlopen(
        urllib.request.Request(pick.get("thumbnail") or pick["url"], headers=ua),
        timeout=30).read()
    out = lang_dir() / "img" / f"{card_id}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    card["image"] = out.name
    if pick.get("attribution"):
        card["image_credit"] = pick["attribution"]
    save(cards_path(), data)
    print(json.dumps({"id": card_id, "image": str(out.relative_to(ROOT))}, ensure_ascii=False))


def cmd_streak(today):
    p = load(progress_path(), {"streak": 0, "last_active": None, "level": None, "unit": 1, "history": []})
    last = p.get("last_active")
    if last != today.isoformat():
        if last == (today - timedelta(days=1)).isoformat():
            p["streak"] = p.get("streak", 0) + 1
        else:
            p["streak"] = 1
        p["last_active"] = today.isoformat()
        save(progress_path(), p)
    print(json.dumps({"streak": p["streak"], "last_active": p["last_active"]}))


def cmd_stats(today):
    deck = load(cards_path(), {"cards": []})["cards"]
    due = sum(1 for c in deck if c.get("due") is None or c["due"] <= today.isoformat())
    print(json.dumps({"cards": len(deck), "due": due,
                      "new": sum(1 for c in deck if c.get("last_review") is None)}))


def selfcheck():
    today = date(2026, 1, 1)
    card = {"id": "t1", "last_review": None}
    review(card, 3, today)
    assert card["due"] == "2026-01-05", card["due"]  # Good on a new card ≈ 4 days (S0=3.71)
    s_before = card["S"]
    review(card, 3, date.fromisoformat(card["due"]))
    assert card["S"] > s_before  # stability grows on success
    assert review(card, 1, date.fromisoformat(card["due"])) == 0  # Again → due today
    assert card["lapses"] == 1
    easy = {"id": "t2", "last_review": None}
    review(easy, 4, today)
    assert easy["S"] > 10  # Easy on a new card ≈ 11 days
    assert 1.0 <= card["D"] <= 10.0
    validate_card({"front": "Can I ___ your pen?", "answer": "borrow", "hint": "pedir prestado"})
    for invalid in ({"front": "___!", "answer": "borrow", "hint": "pedir prestado"},
                    {"front": "x___", "answer": "borrow", "hint": "pedir prestado"},
                    {"front": "Can I ___ your pen?", "answer": "borrow"},
                    {"front": "I borrow your pen.", "answer": "borrow", "hint": "pedir prestado"}):
        try:
            validate_card(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid card accepted: {invalid}")
    print("selfcheck OK")


def main():
    args = sys.argv[1:]
    today = date.today()
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "due":
        cmd_due(today)
    elif cmd == "grade":
        cmd_grade(args[1], int(args[2]), today)
    elif cmd == "add":
        cmd_add(today)
    elif cmd == "img":
        if len(args) < 3:
            sys.exit("usage: img <card-id> <search query>")
        cmd_img(args[1], " ".join(args[2:]))
    elif cmd == "streak":
        cmd_streak(today)
    elif cmd == "stats":
        cmd_stats(today)
    elif cmd == "selfcheck":
        selfcheck()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
