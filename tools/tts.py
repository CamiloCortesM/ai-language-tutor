#!/usr/bin/env python3
"""Text-to-speech with cache and graceful fallback. Stdlib only.

Provider picked by TUTOR_TTS env var, or auto-detected (free first):
  edge        FREE neural voices — `pip install edge-tts`, no key, no account
              (voice via TUTOR_TTS_VOICE, default "en-US-AndrewNeural")
  openai      needs OPENAI_API_KEY      (model gpt-4o-mini-tts; default voice "nova")
  elevenlabs  needs ELEVENLABS_API_KEY  (voice id via TUTOR_TTS_VOICE, default "Rachel")
  say         macOS built-in — no key, no cost, robotic (last resort)

Usage:
  python3 tools/tts.py say "Hello there"      synthesize and play
  python3 tools/tts.py file "Hello" out.mp3   synthesize to a file
  python3 tools/tts.py check                  print the active provider

Audio is cached in student/.tts-cache/ keyed by provider+voice+text, so a
repeated sentence (flashcards repeat a lot) is never billed twice.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "student" / ".tts-cache"

DEFAULT_VOICE = {"edge": "en-US-AndrewNeural", "openai": "nova",
                 "elevenlabs": "21m00Tcm4TlvDq8ikWAM"}  # 21m0… = Rachel


def provider():
    p = os.environ.get("TUTOR_TTS")
    if p:
        return p
    if importlib.util.find_spec("edge_tts"):
        return "edge"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ELEVENLABS_API_KEY"):
        return "elevenlabs"
    return "say"


def synth(text, voice=None):
    """Return a Path to an mp3 for `text`, or None when only `say` is available."""
    prov = provider()
    if prov == "say":
        return None
    voice = voice or os.environ.get("TUTOR_TTS_VOICE") or DEFAULT_VOICE.get(prov)
    key = hashlib.sha1(f"{prov}:{voice}:{text}".encode()).hexdigest()[:16]
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / f"{key}.mp3"
    if out.exists():
        return out
    if prov == "edge":
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--text", text,
                            "--voice", voice, "--write-media", str(out)],
                           capture_output=True)
        if r.returncode != 0 or not out.exists():
            return None  # offline or edge hiccup -> caller falls back
        return out
    if prov == "openai":
        req = urllib.request.Request(
            "https://api.openai.com/v1/audio/speech",
            data=json.dumps({"model": "gpt-4o-mini-tts", "voice": voice,
                             "input": text}).encode(),
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                     "Content-Type": "application/json"})
    elif prov == "elevenlabs":
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
            data=json.dumps({"text": text,
                             "model_id": "eleven_multilingual_v2"}).encode(),
            headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                     "Content-Type": "application/json"})
    else:
        sys.exit(f"unknown TTS provider: {prov}")
    with urllib.request.urlopen(req, timeout=60) as r:
        out.write_bytes(r.read())
    return out


def play(text):
    path = synth(text)
    if path:  # play the mp3, per platform
        if sys.platform == "darwin" and shutil.which("afplay"):
            return subprocess.run(["afplay", str(path)], check=False)
        for p in ("mpv", "ffplay"):
            if shutil.which(p):
                cmd = [p, "--no-video", str(path)] if p == "mpv" else \
                      [p, "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)]
                return subprocess.run(cmd, check=False)
        if sys.platform == "win32":
            ps = ("Add-Type -AssemblyName PresentationCore;"
                  f"$p=New-Object System.Windows.Media.MediaPlayer;$p.Open([uri]'{path}');$p.Play();"
                  "while(!$p.NaturalDuration.HasTimeSpan){Start-Sleep -m 100};"
                  "Start-Sleep -Seconds ([math]::Ceiling($p.NaturalDuration.TimeSpan.TotalSeconds))")
            return subprocess.run(["powershell", "-NoProfile", "-c", ps], check=False)
        print(path)  # no player found: hand back the file path
        return
    # no synth provider at all -> the OS's built-in robotic voice
    if sys.platform == "darwin" and shutil.which("say"):
        subprocess.run(["say", text], check=False)
    elif sys.platform == "win32":
        ps = ("Add-Type -AssemblyName System.Speech;"
              "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(" + json.dumps(text) + ")")
        subprocess.run(["powershell", "-NoProfile", "-c", ps], check=False)
    elif shutil.which("spd-say"):
        subprocess.run(["spd-say", "-w", text], check=False)
    elif shutil.which("espeak"):
        subprocess.run(["espeak", text], check=False)
    else:
        sys.exit("no audio output found — pip3 install edge-tts and use the browser apps")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "check":
        print(provider())
    elif args[0] == "say":
        play(args[1])
    elif args[0] == "file":
        path = synth(args[1])
        if not path:
            sys.exit("no premium provider configured")
        shutil.copy(path, args[2])
        print(args[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
