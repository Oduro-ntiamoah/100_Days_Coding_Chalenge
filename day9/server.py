"""Password strength checker backend for the Day 9.

This file serves the password checker interface and processes password strength requests.
Run this file from the day9 folder: python server.py
Then open http://127.0.0.1:8000 in your browser.
"""

from __future__ import annotations

import json
import string
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

UPPER_CASE_LETTERS = string.ascii_uppercase
LOWER_CASE_LETTERS = string.ascii_lowercase
NUMBERS = string.digits
PUNCTUATION = string.punctuation

COMMON_PASSWORDS_1 = [
    "123456", "password", "123456789", "12345678", "12345", "111111", "1234567", "sunshine", "qwerty",
    "iloveyou", "princess", "admin", "welcome", "666666", "abc123", "football", "123123", "monkey",
    "654321", "Admin", "charlie", "aa123456", "donald", "password1", "qwerty123", "letmein", "1234",
    "123", "1q2w3e4r", "123456a", "123qwe", "zxcvbnm", "asdfghjkl", "qazwsx", "1qaz2wsx", "qwertyuiop",
    "password123"
]


def load_common_passwords() -> set[str]:
    passwords = set(COMMON_PASSWORDS_1)
    try:
        remote = urlopen(
            "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
            timeout=5,
        )
        remote_text = remote.read().decode("utf-8", errors="ignore")
        passwords.update(line.strip() for line in remote_text.splitlines() if line.strip())
    except Exception:
        pass
    return passwords


COMMON_PASSWORDS = load_common_passwords()


def get_strength_label(score: int) -> str:
    if score == 6:
        return "Strong"
    if score >= 4:
        return "Moderate"
    if score >= 2:
        return "Weak"
    return "Very Weak"


def get_risk_label(score: int) -> str:
    if score >= 5:
        return "Low risk"
    if score >= 3:
        return "Medium risk"
    return "High risk"


def check_password_strength(password: str) -> dict:
    password = password or ""
    length = len(password)
    has_upper = any(char in UPPER_CASE_LETTERS for char in password)
    has_lower = any(char in LOWER_CASE_LETTERS for char in password)
    has_number = any(char in NUMBERS for char in password)
    has_punctuation = any(char in PUNCTUATION for char in password)
    is_common = password.lower() in COMMON_PASSWORDS

    criteria = {
        "length": length >= 8,
        "upper_case": has_upper,
        "lower_case": has_lower,
        "number": has_number,
        "punctuation": has_punctuation,
        "common_password": not is_common,
    }

    score = sum(1 for value in criteria.values() if value)
    data = {
        "password": password,
        "length": length,
        "score": score,
        "max_score": 6,
        "strength": get_strength_label(score),
        "risk": get_risk_label(score),
        "criteria": criteria,
        "meter": [index < score for index in range(6)],
    }
    return data


class PasswordStrengthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index.html":
            index_path = Path(__file__).resolve().parent / "index.html"
            try:
                html = index_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)
            except Exception as e:
                self.send_error(500, f"Could not read index.html: {str(e)}")
            return

        self.send_error(404, "Not found")

    def do_POST(self):
        if self.path != "/api/check-password":
            self.send_error(404, "Not found")
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0

        password = ""

        if content_length > 0:
            try:
                raw_body = self.rfile.read(content_length)
                body_text = raw_body.decode("utf-8", errors="ignore")
                
                # Try to parse as form data first
                try:
                    form_data = parse_qs(body_text)
                    password = form_data.get("password", [""])[0]
                except Exception:
                    # Try JSON if form parsing fails
                    try:
                        data = json.loads(body_text)
                        password = data.get("password", "")
                    except Exception:
                        password = ""
            except Exception:
                password = ""

        payload = check_password_strength(password)
        self._send_html(payload)

    def _send_html(self, payload: dict):
        """Generate and send HTML response with password analysis results."""
        password = payload.get("password", "")
        score = payload.get("score", 0)
        max_score = payload.get("max_score", 6)
        strength = payload.get("strength", "Very Weak")
        risk = payload.get("risk", "High risk")
        criteria = payload.get("criteria", {})

        # Determine badge class
        badge_class = ""
        if strength == "Strong":
            badge_class = ""
        elif strength in ["Moderate", "Weak"]:
            badge_class = "warning"
        else:
            badge_class = "danger"

        # Determine risk box styling
        if score >= 5:
            risk_bg = "#f0fdf4"
            risk_border = "#10b981"
            risk_color = "#10b981"
        elif score >= 3:
            risk_bg = "#fffbeb"
            risk_border = "#f59e0b"
            risk_color = "#f59e0b"
        else:
            risk_bg = "#fef2f2"
            risk_border = "#ef4444"
            risk_color = "#ef4444"

        # Build check items HTML
        check_items = ""
        check_labels = {
            "length": "Length is at least 8 characters",
            "upper_case": "Contains uppercase letters",
            "lower_case": "Contains lowercase letters",
            "number": "Contains numbers",
            "punctuation": "Contains punctuation",
            "common_password": "Is not a common password",
        }

        for key, label in check_labels.items():
            passed = criteria.get(key, False)
            status_class = "pass" if passed else "fail"
            mark_text = "✓" if passed else "✕"
            status_text = "Pass" if passed else "Fail"
            check_items += f"""                    <div class="check-item {status_class}" data-check="{key}">
                        <div class="left">
                            <div class="mark">{mark_text}</div>
                            <div class="label">{label}</div>
                        </div>
                        <div class="status">{status_text}</div>
                    </div>
"""

        # Build meter segments
        segments = "".join([
            f'                    <div class="segment {"active" if i < score else ""}"></div>\n'
            for i in range(6)
        ])

        # Build HTML response
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker Results</title>
    <style>
        :root {{
            --primary-color: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text: #1f2937;
            --text-light: #6b7280;
            --border-color: #e5e7eb;
            --bg-white: #ffffff;
            --bg-light: #f9fafb;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f4f6;
            color: var(--text);
            display: grid;
            place-items: center;
            padding: 32px 20px;
        }}

        .page-shell {{
            width: min(980px, 100%);
            background: var(--bg-white);
            border: 2px solid var(--border-color);
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .topbar {{
            padding: 16px 24px;
            border-bottom: 2px solid var(--border-color);
            background: var(--bg-light);
        }}

        .topbar span {{
            display: inline-block;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text);
        }}

        .content {{
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
        }}

        .main-panel,
        .side-panel {{
            padding: 32px;
        }}

        .main-panel {{
            border-right: 2px solid var(--border-color);
            background: var(--bg-white);
        }}

        .eyebrow {{
            margin: 0 0 12px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--primary-color);
            letter-spacing: 0.05em;
        }}

        h1 {{
            margin: 0;
            font-size: clamp(2rem, 3vw, 3rem);
            line-height: 1.2;
            color: var(--text);
        }}

        .input-wrap {{
            margin-top: 20px;
        }}

        input[type="text"] {{
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            background: var(--bg-light);
            border: 2px solid var(--border-color);
            color: var(--text);
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s ease;
        }}

        input[type="text"]:focus {{
            border-color: var(--primary-color);
            background: var(--bg-white);
        }}

        button {{
            margin-top: 12px;
            padding: 10px 20px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s ease;
        }}

        button:hover {{
            background: #2563eb;
        }}

        .strength-header {{
            margin-top: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .strength-label {{
            font-size: 0.875rem;
            color: var(--text-light);
            font-weight: 600;
        }}

        .badge {{
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            background: #d1fae5;
            color: var(--success);
            border: 2px solid var(--success);
            letter-spacing: 0.05em;
        }}

        .badge.warning {{
            background: #fef3c7;
            color: var(--warning);
            border-color: var(--warning);
        }}

        .badge.danger {{
            background: #fee2e2;
            color: var(--danger);
            border-color: var(--danger);
        }}

        .meter {{
            margin-top: 16px;
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
        }}

        .segment {{
            height: 10px;
            border-radius: 4px;
            background: var(--border-color);
            border: none;
            transition: background-color 0.2s ease;
        }}

        .segment.active {{
            background: var(--success);
        }}

        .segment.warning {{
            background: var(--warning);
        }}

        .segment.danger {{
            background: var(--danger);
        }}

        .checklist {{
            margin-top: 24px;
            display: grid;
            gap: 12px;
        }}

        .check-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 14px 16px;
            border-radius: 8px;
            background: var(--bg-light);
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
        }}

        .check-item.pass {{
            border-color: var(--success);
            background: #f0fdf4;
        }}

        .check-item.fail {{
            border-color: var(--danger);
            background: #fef2f2;
        }}

        .left {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 1;
        }}

        .left .mark {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            background: var(--success);
            color: var(--bg-white);
            border: none;
            font-weight: 700;
            font-size: 0.875rem;
            flex-shrink: 0;
        }}

        .check-item.fail .mark {{
            background: var(--danger);
        }}

        .check-item .label {{
            font-size: 0.95rem;
            color: var(--text);
            font-weight: 500;
        }}

        .status {{
            font-size: 0.75rem;
            text-transform: uppercase;
            color: var(--success);
            font-weight: 700;
            white-space: nowrap;
            letter-spacing: 0.05em;
        }}

        .check-item.fail .status {{
            color: var(--danger);
        }}

        .side-panel {{
            background: var(--bg-light);
        }}

        .score-box {{
            padding: 24px;
            border-radius: 8px;
            background: var(--bg-white);
            border: 2px solid var(--border-color);
        }}

        .score {{
            margin: 0;
            color: var(--text-light);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .score-value {{
            margin: 12px 0 0;
            font-size: clamp(2.5rem, 4vw, 4rem);
            font-weight: 800;
            line-height: 1;
            color: var(--text);
        }}

        .score-value span {{
            font-size: 1rem;
            color: var(--text-light);
            margin-left: 4px;
            font-weight: 600;
        }}

        .risk-box {{
            margin-top: 16px;
            padding: 16px;
            border-radius: 8px;
            border: 2px solid {risk_border};
        }}

        .risk-box h3 {{
            margin: 0 0 8px;
            font-size: 0.75rem;
            text-transform: uppercase;
            color: var(--text-light);
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .risk-box p {{
            margin: 0;
            font-size: 1.05rem;
            font-weight: 600;
            color: {risk_color};
        }}

        .notes {{
            margin-top: 16px;
            padding: 16px;
            border-radius: 8px;
            background: var(--bg-white);
            border: 2px solid var(--border-color);
        }}

        .notes h3 {{
            margin: 0 0 12px;
            font-size: 0.75rem;
            color: var(--text-light);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .notes ul {{
            margin: 0;
            padding-left: 20px;
            color: var(--text);
            line-height: 1.6;
            font-size: 0.95rem;
        }}

        .notes li {{
            margin-bottom: 8px;
        }}

        @media (max-width: 760px) {{
            .content {{
                grid-template-columns: 1fr;
            }}

            .main-panel {{
                border-right: none;
                border-bottom: 2px solid var(--border-color);
            }}

            .main-panel,
            .side-panel {{
                padding: 24px 20px;
            }}

            .check-item {{
                align-items: flex-start;
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="page-shell">
        <div class="topbar">
            <span>Password Strength Checker</span>
        </div>

        <div class="content">
            <main class="main-panel">
                <p class="eyebrow">Security report</p>
                <h1>Your password is {strength.lower()}.</h1>

                <div class="input-wrap">
                    <form method="post" action="/api/check-password">
                        <input name="password" type="text" placeholder="Type a password..." value="{password}" />
                        <button type="submit">Check Password</button>
                    </form>
                </div>

                <div class="strength-header">
                    <div class="strength-label">Overall strength</div>
                    <div class="badge {badge_class}">{strength}</div>
                </div>

                <div class="meter" aria-label="Password strength meter">
{segments}                </div>

                <div class="checklist">
{check_items}                </div>
            </main>

            <aside class="side-panel">
                <div class="score-box">
                    <p class="score">Score</p>
                    <div class="score-value">{score}<span>/{max_score}</span></div>
                </div>

                <div class="risk-box" style="background-color: {risk_bg};">
                    <h3>Risk level</h3>
                    <p>{risk}</p>
                </div>

                <div class="notes">
                    <h3>Tips</h3>
                    <ul>
                        <li>Use a unique password for each account.</li>
                        <li>Prefer long phrases with symbols and numbers.</li>
                        <li>Consider a password manager for better security.</li>
                    </ul>
                </div>
            </aside>
        </div>
    </div>
</body>
</html>"""

        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return  # Suppress logging


def run_server(host: str = "127.0.0.1", port: int = 8000):
    server = ThreadingHTTPServer((host, port), PasswordStrengthHandler)
    print(f"Password strength server running at http://{host}:{port}")
    print(f"Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")


if __name__ == "__main__":
    run_server()
