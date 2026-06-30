"""Email send tool — SMTP based, off by default."""
from __future__ import annotations
import os, smtplib
from email.mime.text import MIMEText

from backend.tools.base import BaseTool, ToolPermission


class EmailTool(BaseTool):
    name = "email_send"
    description = "Send an email via SMTP. Args: to, subject, body."
    permissions = ToolPermission(network=True)

    async def run(self, to: str, subject: str, body: str) -> dict:
        host = os.getenv("SMTP_HOST")
        if not host:
            raise RuntimeError("SMTP_HOST not configured")
        port = int(os.getenv("SMTP_PORT", "587"))
        user, pw = os.getenv("SMTP_USER", ""), os.getenv("SMTP_PASSWORD", "")
        sender = os.getenv("SMTP_FROM", user)
        msg = MIMEText(body)
        msg["From"], msg["To"], msg["Subject"] = sender, to, subject
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            if user:
                s.login(user, pw)
            s.send_message(msg)
        return {"sent": True, "to": to}
