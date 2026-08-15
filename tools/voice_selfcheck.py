#!/usr/bin/env python3
"""Verify the durable interface of the external voice handoff."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VOICE = (ROOT / "portable" / "voice-tutor.md").read_text()
PROFILE_TEMPLATE = (ROOT / "student.example" / "profile.md").read_text()

required_sections = (
    "## Learner handoff instructions",
    "### Validate before write-back",
    "### Activity-rules checklist",
    "## Controller protocol",
    "## Level language policy",
    "## Lesson-type constraints",
    "## Feedback rules",
    "## LESSON REPORT JSON",
)
required_report_fields = (
    "lesson",
    "completed",
    "partial_reason",
    "duration_minutes",
    "performance",
    "corrections",
    "did_well",
    "pronunciation",
    "words_struggled",
    "level_impression",
)

for section in required_sections:
    assert section in VOICE, f"missing voice contract section: {section}"
for field in required_report_fields:
    assert f'"{field}"' in VOICE, f"missing report field: {field}"

assert "same chat" in VOICE, "post-call report recovery must stay in the same chat"
assert "Activity complete. You can end the call now." in VOICE, "missing closing signal"
assert "Generate the LESSON REPORT JSON now" in VOICE, "missing post-call report command"
assert "placement-speaking" in VOICE, "missing placement speaking type"
assert "not_assessed" in VOICE, "missing non-assessment level value"
assert "Complete STEP_i only when its exact `complete_when` condition is met" in VOICE
assert "external | none" in PROFILE_TEMPLATE, "voice routes must be external or none"

print("voice selfcheck OK")
