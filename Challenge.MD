# 100-Day Challenge: Python, Cybersecurity & Frontend Development

A single merged curriculum — combining the strongest ideas from two draft plans, resequenced into a genuine easy → hard progression, with a frontend development track woven in throughout (rather than bolted on at the end), so every tool you build eventually gets a real interface.

## How it's organized
- **20 weeks × 5 days = 100 days.** Weekends are for review/catch-up (not counted).
- **Daily time**: 20-45 min early on, 45-90 min in Phase 3-4.
- **Frontend is integrated, not separate**: roughly 1 day per week is frontend-focused, and by Phase 2 you're wiring the backend tools you already built to real UIs.
- **Ethics note** (carried from both source plans): every tool here is for learning, defense, and testing systems you own or are authorized to test. Anything framed as an "attack" tool (e.g. brute-forcer, MITM detector) is for understanding and defending against the technique, run only in your own lab.

---

## Phase 1 — Foundations (Days 1–20)
*Core Python, first security concepts, and HTML/CSS/JS basics.*

### Week 1: Python Security Basics
- **Day 1**: Random password generator (length, symbols, entropy check)
- **Day 2**: Hash calculator (MD5/SHA1/SHA256) for any input string or file
- **Day 3**: Caesar cipher encrypt/decrypt
- **Day 4**: Password strength checker (length, char classes, common-password list)
- **Day 5**: Simple port scanner against localhost (common ports only)

### Week 2: Files, Data & First Web Page
- **Day 6**: File integrity checker using SHA-256 (detect changed files in a folder)
- **Day 7**: File-type detector using magic bytes
- **Day 8**: Log file parser — extract IPs and timestamps with regex
- **Day 9**: **Frontend**: Build a static HTML/CSS page that displays your password-strength checker's results (no JS yet — just structure and styling)
- **Day 10**: **Frontend**: Add vanilla JavaScript to that page so the strength check runs live in the browser as the user types

### Week 3: Networking Basics
- **Day 11**: Subnet calculator (CIDR → IP range)
- **Day 12**: DNS resolver showing all record types for a domain
- **Day 13**: WHOIS lookup tool
- **Day 14**: Ping sweep to find live hosts on your own LAN
- **Day 15**: **Frontend**: Basic responsive layout (flexbox/grid) — build a "network toolkit" landing page linking out to each tool's description

### Week 4: Crypto Basics & First Static Project
- **Day 16**: XOR cipher file encrypter/decrypter
- **Day 17**: Base64 encode/decode utility with a CLI
- **Day 18**: EXIF/metadata stripper for images
- **Day 19**: **Frontend**: JS fundamentals deep-dive — DOM manipulation, events, fetch() basics (no backend yet, just mock data)
- **Day 20**: **Milestone Project**: Combine Days 1–19 into one static "Security Toolkit" webpage (HTML/CSS/JS only, client-side) that showcases at least 3 tools interactively

---

## Phase 2 — Intermediate Tools + Backend/Frontend Integration (Days 21–45)
*Real scanners and crypto tools, plus your first backend (Flask) and your first UI framework (React).*

### Week 5: Web Security Scanning
- **Day 21**: URL validator with basic security checks (suspicious params, obvious XSS/SQLi patterns)
- **Day 22**: SQL injection *detector* (flags risky-looking input in URL params — detection, not exploitation)
- **Day 23**: XSS payload detector (pattern-based)
- **Day 24**: HTTP security headers analyzer (CSP, HSTS, X-Frame-Options, etc.)
- **Day 25**: SSL/TLS certificate validator and expiry checker

### Week 6: Malware Analysis Basics
- **Day 26**: String extractor from binary files
- **Day 27**: File entropy calculator (flag likely-packed/encrypted files)
- **Day 28**: PE file header analyzer (Windows executables)
- **Day 29**: Simple process/service monitor (list running processes, flag unusual ones)
- **Day 30**: YARA rule tester against sample files

### Week 7: Auth, Forensics & Your First Backend
- **Day 31**: TOTP-based 2FA code generator
- **Day 32**: Browser/log history metadata extractor
- **Day 33**: **Backend**: Intro to Flask — build a `/health` and `/hash` API endpoint that reuses your Day-2 hash calculator
- **Day 34**: **Backend**: Turn your Day-4 password strength checker into a Flask API endpoint (`POST /check-password`)
- **Day 35**: **Frontend**: Connect Day 9-10's JS page to your new Flask API with `fetch()` — first real full-stack loop

### Week 8: Network Security Tools
- **Day 36**: ARP scanner for local network discovery
- **Day 37**: Packet sniffer using scapy (capture-only, your own traffic)
- **Day 38**: MITM/ARP-spoofing *detector* (defensive)
- **Day 39**: Simple firewall rule parser/generator
- **Day 40**: **Frontend**: Style your Flask app's pages properly — introduce a CSS framework or design system basics (spacing, typography scale, color tokens)

### Week 9: React Fundamentals
- **Day 41**: React setup — components, props, first static component tree
- **Day 42**: React state with `useState` — rebuild the password checker UI as a component
- **Day 43**: React `useEffect` + fetch — call your Flask hash API from a React component
- **Day 44**: Build a reusable `<ToolCard>` component and render your toolkit as a grid of cards
- **Day 45**: **Milestone Project**: Full-stack password/hash toolkit — Flask backend + React frontend, deployed locally

---

## Phase 3 — Advanced Security + Real Dashboards (Days 46–75)
*Deeper cryptography, web app security, cloud concepts, and building dashboards that visualize security data.*

### Week 10: Advanced Cryptography
- **Day 46**: RSA key pair generator + encrypt/decrypt
- **Day 47**: AES-256 file encryption (PyCryptodome)
- **Day 48**: Digital signature generator + verifier
- **Day 49**: Diffie-Hellman key exchange simulator
- **Day 50**: Local encrypted password manager (CLI, AES-encrypted vault file)

### Week 11: Web Application Security
- **Day 51**: JWT decoder/validator (and a demo of what happens with a weak secret)
- **Day 52**: OAuth 2.0 client flow (simplified, against a sandbox provider)
- **Day 53**: API rate limiter (token bucket or sliding window)
- **Day 54**: CORS misconfiguration checker
- **Day 55**: CSRF token generator + validator with expiry

### Week 12: Malware Concepts & Detection (Defensive Focus)
- **Day 56**: Reverse-shell *detector* — pattern-match suspicious outbound connection code in sample scripts (defensive/static-analysis angle, not a working shell)
- **Day 57**: Persistence-mechanism *auditor* — scan startup/cron/registry entries and flag anything unexpected
- **Day 58**: Process-injection indicator scanner (static heuristics)
- **Day 59**: Basic rootkit indicator checker (hidden process/port comparison)
- **Day 60**: Anti-tamper file watcher (tripwire-style, alerts on change)

### Week 13: Cloud & Container Security
- **Day 61**: Docker image vulnerability scanner (wraps an existing CVE database/API)
- **Day 62**: Dockerfile security linter (flags root user, latest tags, secrets in layers)
- **Day 63**: AWS IAM policy analyzer (flag overly permissive policies)
- **Day 64**: S3/GCS bucket public-access checker
- **Day 65**: Kubernetes manifest security policy checker

### Week 14: React Dashboards
- **Day 66**: React Router — multi-page app shell for your growing toolkit
- **Day 67**: Build a scan-results table component (sortable, filterable) fed by mock data
- **Day 68**: Connect the table to a real backend endpoint (e.g., your Day-61 Docker scanner results)
- **Day 69**: Add loading/error states and optimistic UI for long-running scans
- **Day 70**: Auth-gate the dashboard with a simple login screen (JWT from Day 51)

### Week 15: Data Visualization for Security Data
- **Day 71**: Intro to a charting library (Recharts/Chart.js) — bar chart of vulnerabilities by severity
- **Day 72**: Timeline chart of log events (from your Day-8 log parser output)
- **Day 73**: Network graph visualization of hosts discovered by your ARP scanner
- **Day 74**: Real-time-feeling dashboard using polling (or WebSockets if you're ready) for live scan status
- **Day 75**: **Milestone Project**: Full security dashboard — Flask/FastAPI backend, React frontend, at least 2 chart types, auth-gated

---

## Phase 4 — Mastery: Full-Stack Capstones (Days 76–100)
*Automation, a taste of ML in security, and shipping complete, polished full-stack tools.*

### Week 16: Security Automation
- **Day 76**: SIEM-style log aggregator (ingest multiple log formats into one schema)
- **Day 77**: Automated security report generator (PDF/HTML output from scan results)
- **Day 78**: Incident-response playbook runner (sequenced automated checks + notifications)
- **Day 79**: Threat-intel feed parser (pull an open feed, normalize IOCs)
- **Day 80**: Wire Day 76–79 tools together into one scheduled pipeline (cron or a simple task queue)

### Week 17: Machine Learning in Security (Intro Level)
- **Day 81**: Phishing URL classifier — basic feature extraction + logistic regression
- **Day 82**: Spam/ham email classifier (scikit-learn, small labeled dataset)
- **Day 83**: Anomaly-based log classifier (flag outlier request patterns)
- **Day 84**: Password-strength predictor trained on a breached-password frequency list
- **Day 85**: **Frontend**: Build a simple UI to submit a URL/email/log line and show the model's prediction with confidence

### Week 18: Full-Stack Security Apps
- **Day 86**: Build a real user auth system (signup/login, hashed passwords, sessions) — apply everything from Weeks 7 & 11
- **Day 87**: Add role-based access control (RBAC) to that app (admin vs viewer)
- **Day 88**: Secure cookie handling + CSRF protection wired into the real app
- **Day 89**: Build a honeypot service with logging, and a React page that visualizes attempted hits
- **Day 90**: Rate-limit and harden the app's public endpoints (apply Day 53)

### Week 19: Polish, Testing & Deployment
- **Day 91**: Write unit tests for your 3 most important tools (hash checker, scanner, auth)
- **Day 92**: Add input validation and error handling across your API endpoints
- **Day 93**: Accessibility and responsive-design pass on your dashboard (keyboard nav, contrast, mobile layout)
- **Day 94**: Containerize the full-stack app with Docker Compose (frontend + backend + db)
- **Day 95**: Deploy it (a free-tier host is fine) and set up basic CI (lint + test on push)

### Week 20: Grand Finale
- **Day 96**: Plan your capstone — pick one theme (e.g., "mini-SIEM", "pentest toolkit", "personal security suite") and scope it
- **Day 97**: Build the capstone backend — combine at least 4 tools from earlier days behind one API
- **Day 98**: Build the capstone frontend — dashboard, charts, and auth, using everything from Phase 2–3
- **Day 99**: Write documentation (README, architecture diagram, setup instructions) and a short demo script
- **Day 100**: 🏆 **Ship it** — final polish, record a demo, publish the repo

---

## Rules
1. Code (or at least touch the project) daily — 2-day skip limit before you have to catch up
2. Push to GitHub daily, one commit minimum
3. Comment code and keep a running `notes.md` of what you learned
4. Every backend tool eventually gets a frontend — don't let the UI lag more than 2 weeks behind the logic
5. Review the previous week every Sunday

## Suggested stack
```bash
# Python
pip install cryptography pycryptodome scapy requests beautifulsoup4 \
            flask fastapi pyjwt python-dotenv dnspython pandas \
            scikit-learn yara-python paramiko

# Frontend
npm install react react-router-dom recharts axios
```

## Resources
- **Books**: *Black Hat Python*, *Violent Python*
- **Practice**: TryHackMe, HackTheBox, OverTheWire (for the security side)
- **Frontend**: MDN Web Docs, React docs, web.dev
- **Reference**: OWASP Top 10, OWASP ASVS

---
*Every tool in this plan is for learning, defense, and testing systems you own or are authorized to test. Use it ethically.*