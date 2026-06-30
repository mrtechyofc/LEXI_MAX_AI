"""Calendar tool — minimal local ICS file backend for now."""
from __future__ import annotations
import os
from datetime import datetime
import uuid

from backend.tools.base import BaseTool, ToolPermission

ICS_FILE = os.path.abspath("./data/calendar.ics")


class CalendarTool(BaseTool):
    name = "calendar_add"
    description = "Add an event to LEXI's local calendar. Args: title, start_iso, end_iso, notes."
    permissions = ToolPermission(filesystem_write=True)

    async def run(self, title: str, start_iso: str, end_iso: str, notes: str = "") -> dict:
        os.makedirs(os.path.dirname(ICS_FILE), exist_ok=True)
        if not os.path.exists(ICS_FILE):
            with open(ICS_FILE, "w") as f:
                f.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//LEXI//EN\n")
        uid = uuid.uuid4().hex
        block = (
            f"BEGIN:VEVENT\nUID:{uid}\nSUMMARY:{title}\n"
            f"DTSTART:{datetime.fromisoformat(start_iso).strftime('%Y%m%dT%H%M%S')}\n"
            f"DTEND:{datetime.fromisoformat(end_iso).strftime('%Y%m%dT%H%M%S')}\n"
            f"DESCRIPTION:{notes}\nEND:VEVENT\n"
        )
        with open(ICS_FILE, "a") as f:
            f.write(block)
        return {"uid": uid, "ics_path": ICS_FILE}
