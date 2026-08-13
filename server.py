"""
=====================================================================
  IKON COMPUTER EDUCATION & TRAINING INSTITUTE
  Universal Backend Server  -  Python 3.6+
  Works on Windows, macOS, Linux  (zero external dependencies)
=====================================================================
  GET  /              -> serves index.html
  GET  /style.css     -> serves static files
  POST /register      -> saves registration to JSON + CSV
  GET  /admin         -> password-protected dashboard
  POST /admin         -> admin login
  GET  /admin/logout  -> clear session
  GET  /admin/export  -> download registrations as CSV
=====================================================================
"""

# ── stdlib only ───────────────────────────────────────────────────────
import sys
import io
import os
import json
import csv
import secrets
import socket
import signal
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from http import server as http_server

# ── Force UTF-8 on all platforms (critical for Windows cp1252) ────────
def _fix_encoding(stream):
    """Re-wrap a stream in UTF-8 if it supports reconfiguration."""
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        # Python < 3.7 or stream doesn't support reconfigure
        try:
            return io.TextIOWrapper(stream.buffer, encoding="utf-8", errors="replace")
        except AttributeError:
            pass  # Already a compatible stream (e.g. StringIO in tests)
    return stream

sys.stdout = _fix_encoding(sys.stdout)
sys.stderr = _fix_encoding(sys.stderr)

# ── Config (override via environment variables if needed) ─────────────
BASE_DIR       = Path(__file__).resolve().parent
PREFERRED_PORT = int(os.environ.get("IKON_PORT",           3000))
ADMIN_PASSWORD =     os.environ.get("IKON_ADMIN_PASSWORD", "ikon2026")
DATA_FILE      = BASE_DIR / "registrations.json"
CSV_FILE       = BASE_DIR / "registrations.csv"
SHEET_NAME     = "Registrations"

IST_OFFSET = timedelta(hours=5, minutes=30)   # Indian Standard Time

# ── Lookup tables ─────────────────────────────────────────────────────
COURSE_LABELS = {
    "java":       "Java Programming",
    "python":     "Python Development",
    "dbms":       "DBMS",
    "networking": "Computer Networking",
    "combo":      "Combo (Multiple Courses)",
}
MODE_LABELS = {
    "online":  "Online",
    "offline": "Offline",
}
CSV_HEADERS = [
    "S.No", "Timestamp (IST)", "Full Name",
    "Email", "Phone", "Course", "Mode", "Message",
]
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css":  "text/css; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".ico":  "image/x-icon",
    ".png":  "image/png",
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg":  "image/svg+xml",
    ".woff": "font/woff",
    ".woff2":"font/woff2",
    ".txt":  "text/plain; charset=utf-8",
    ".pdf":  "application/pdf",
}

# ── Helpers ───────────────────────────────────────────────────────────

def ist_now() -> str:
    utc  = datetime.now(timezone.utc)
    ist  = utc + IST_OFFSET
    return ist.strftime("%d/%m/%Y %I:%M %p IST")


def load_registrations() -> list:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_registration(entry: dict) -> dict:
    records = load_registrations()
    entry["id"] = len(records) + 1
    records.append(entry)

    # JSON
    DATA_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # CSV  (rewrite whole file to keep consistent)
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_HEADERS)
        for r in records:
            w.writerow([
                r.get("id",       ""),
                r.get("timestamp",""),
                r.get("name",     ""),
                r.get("email",    ""),
                r.get("phone",    ""),
                COURSE_LABELS.get(r.get("course",""), r.get("course","")),
                MODE_LABELS.get(  r.get("mode",  ""), r.get("mode",  "")),
                r.get("message",  ""),
            ])

    return entry


def find_free_port(preferred: int) -> int:
    """Return preferred port if free, otherwise find the next available one."""
    for port in range(preferred, preferred + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free port found in range %d-%d" % (preferred, preferred + 99))


# ── HTML builders ─────────────────────────────────────────────────────

def _html(body: str, title: str = "Ikon Admin", status: int = 200):
    """Wrap a content block in a minimal full HTML document."""
    return status, f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@700;800&display=swap" rel="stylesheet">
</head>
<body style="margin:0;font-family:'Inter',sans-serif">
{body}
</body>
</html>"""


LOGIN_CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:linear-gradient(135deg,#0d1b3e,#1a3a6e);min-height:100vh;
     display:flex;align-items:center;justify-content:center}
.card{background:#fff;border-radius:20px;padding:44px 40px;width:100%;
      max-width:400px;box-shadow:0 30px 80px rgba(0,0,0,.4);text-align:center}
.icon{font-size:44px;margin-bottom:12px}
h1{font-size:22px;font-weight:700;margin-bottom:4px;color:#1a1a2e}
.sub{font-size:13px;color:#8892a4;margin-bottom:28px}
input{width:100%;padding:13px 16px;border:1.5px solid #e8edf5;border-radius:10px;
      font-size:15px;font-family:inherit;outline:none;margin-bottom:14px;
      transition:border .2s,box-shadow .2s}
input:focus{border-color:#1a73e8;box-shadow:0 0 0 3px rgba(26,115,232,.12)}
.btn{width:100%;padding:13px;background:linear-gradient(135deg,#1a73e8,#0d47a1);
     color:#fff;border:none;border-radius:10px;font-size:15px;font-weight:700;
     cursor:pointer;font-family:inherit;transition:.2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(26,115,232,.4)}
.err{color:#d32f2f;font-size:13px;margin-bottom:12px;
     background:#ffebee;border-radius:8px;padding:8px 12px}
</style>
"""

def login_page(error: str = "") -> tuple:
    err = f'<p class="err">{error}</p>' if error else ""
    body = f"""
{LOGIN_CSS}
<div class="card">
  <div class="icon">&#127891;</div>
  <h1>Admin Panel</h1>
  <p class="sub">Ikon Computer Education &amp; Training Institute</p>
  {err}
  <form method="POST" action="/admin">
    <input type="password" name="password" placeholder="Enter admin password" required autofocus>
    <button class="btn" type="submit">Login</button>
  </form>
</div>"""
    return _html(body, "Admin Login — Ikon Institute")


DASHBOARD_CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#f4f7ff;color:#1a1a2e;min-height:100vh}

/* Sidebar */
.sidebar{position:fixed;top:0;left:0;bottom:0;width:230px;
         background:linear-gradient(180deg,#0d1b3e,#1a3a6e);
         padding:28px 16px;display:flex;flex-direction:column;z-index:10}
.brand{color:#fff;font-family:'Outfit',sans-serif;font-size:17px;font-weight:800;
       padding-bottom:22px;border-bottom:1px solid rgba(255,255,255,.1)}
.brand span{color:#FFB347}
.nav{margin-top:20px;display:flex;flex-direction:column;gap:4px;flex:1}
.nav a{color:rgba(255,255,255,.6);padding:10px 12px;border-radius:10px;
       font-size:14px;text-decoration:none;transition:.2s;display:block}
.nav a:hover,.nav a.active{background:rgba(255,255,255,.12);color:#fff}
.logout{color:rgba(255,255,255,.5);font-size:13px;text-align:center;
        text-decoration:none;padding:10px;border-radius:8px;
        transition:.2s;margin-top:auto;display:block}
.logout:hover{background:rgba(200,0,0,.25);color:#ff8a8a}

/* Main */
.main{margin-left:230px;padding:28px 32px}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:28px;flex-wrap:wrap;gap:12px}
.page-title{font-family:'Outfit',sans-serif;font-size:24px;font-weight:800}
.page-sub{font-size:13px;color:#8892a4;margin-top:3px}
.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.btn{padding:9px 18px;border-radius:9px;font-size:14px;font-weight:600;
     cursor:pointer;text-decoration:none;border:none;font-family:inherit;
     display:inline-flex;align-items:center;gap:6px;transition:.2s;white-space:nowrap}
.btn-blue{background:linear-gradient(135deg,#1a73e8,#0d47a1);color:#fff;
          box-shadow:0 4px 12px rgba(26,115,232,.3)}
.btn-blue:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(26,115,232,.4)}
.btn-out{background:#fff;color:#1a1a2e;border:1.5px solid #e8edf5}
.btn-out:hover{border-color:#1a73e8;color:#1a73e8}
.search{padding:9px 14px;border:1.5px solid #e8edf5;border-radius:9px;
        font-size:14px;font-family:inherit;outline:none;width:220px;transition:.2s;background:#fff}
.search:focus{border-color:#1a73e8;box-shadow:0 0 0 3px rgba(26,115,232,.1)}

/* KPI */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:18px;margin-bottom:24px}
.kpi{background:#fff;border:1px solid #e8edf5;border-radius:16px;padding:22px 24px;transition:.2s}
.kpi:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(26,115,232,.1)}
.kpi-label{font-size:11px;color:#8892a4;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.kpi-val{font-family:'Outfit',sans-serif;font-size:38px;font-weight:800;
         background:linear-gradient(135deg,#1a73e8,#FF6B35);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.kpi-sub{font-size:12px;color:#34C759;margin-top:4px;font-weight:500}

/* Course chips */
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
.chip{background:#fff;border:1px solid #e8edf5;border-radius:12px;
      padding:12px 18px;min-width:150px;transition:.2s}
.chip:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(26,115,232,.1)}
.chip-num{font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;color:#1a73e8}
.chip-label{font-size:12px;color:#8892a4;margin-top:2px}

/* Table card */
.tcard{background:#fff;border:1px solid #e8edf5;border-radius:16px;overflow:hidden}
.thead-bar{padding:16px 22px;display:flex;align-items:center;justify-content:space-between;
           border-bottom:1px solid #e8edf5;gap:12px;flex-wrap:wrap}
.ttitle{font-weight:700;font-size:15px}
.cnt{background:#e8f0fe;color:#1a73e8;border-radius:100px;padding:3px 10px;font-size:13px;font-weight:600}
.twrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:14px}
th{background:#f8faff;padding:11px 15px;text-align:left;font-size:11px;font-weight:700;
   color:#8892a4;text-transform:uppercase;letter-spacing:.7px;
   white-space:nowrap;border-bottom:1px solid #e8edf5}
td{padding:12px 15px;border-bottom:1px solid #f0f4ff;vertical-align:middle}
tr:last-child td{border:none}
tr:hover td{background:#f8faff}
.badge{background:#e8f0fe;color:#1a73e8;border-radius:100px;
       padding:3px 10px;font-size:12px;font-weight:600;white-space:nowrap}
.msg-cell{max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
          color:#8892a4;font-size:13px}
.empty{text-align:center;padding:48px;color:#8892a4;font-size:15px}

@media(max-width:768px){
  .sidebar{display:none}
  .main{margin-left:0;padding:16px}
}
</style>
"""


def dashboard_page(records: list) -> tuple:
    total    = len(records)
    courses: dict = {}
    for r in records:
        label = COURSE_LABELS.get(r.get("course",""), r.get("course","Unknown"))
        courses[label] = courses.get(label, 0) + 1

    # KPI: most popular course
    popular = max(courses, key=courses.get) if courses else "—"

    chips_html = "".join(
        f'<div class="chip"><div class="chip-num">{v}</div>'
        f'<div class="chip-label">{k}</div></div>'
        for k, v in courses.items()
    ) or '<span style="color:#8892a4;font-size:14px">No registrations yet</span>'

    # Table rows (newest first)
    rows_html = ""
    for i, r in enumerate(reversed(records)):
        sno = total - i
        rows_html += (
            f"<tr>"
            f"<td>{sno}</td>"
            f"<td style='white-space:nowrap'>{r.get('timestamp','')}</td>"
            f"<td><strong>{_esc(r.get('name',''))}</strong></td>"
            f"<td>{_esc(r.get('email',''))}</td>"
            f"<td>{_esc(r.get('phone',''))}</td>"
            f"<td><span class='badge'>{COURSE_LABELS.get(r.get('course',''), r.get('course',''))}</span></td>"
            f"<td>{MODE_LABELS.get(r.get('mode',''), r.get('mode',''))}</td>"
            f"<td class='msg-cell' title='{_esc(r.get('message',''))}'>{_esc(r.get('message','')) or '—'}</td>"
            f"</tr>"
        )
    if not rows_html:
        rows_html = '<tr><td colspan="8" class="empty">No registrations yet. They will appear here automatically.</td></tr>'

    now_str = ist_now()

    body = f"""
{DASHBOARD_CSS}
<!-- Sidebar -->
<aside class="sidebar">
  <div class="brand">IKON<span>CE</span> Admin</div>
  <nav class="nav">
    <a href="/admin" class="active">Dashboard</a>
    <a href="#regtable" onclick="document.getElementById('regtable').scrollIntoView({{behavior:'smooth'}});return false">Registrations</a>
    <a href="/admin/export">Export CSV</a>
    <a href="/" target="_blank">View Website</a>
  </nav>
  <a href="/admin/logout" class="logout">Logout</a>
</aside>

<!-- Main -->
<main class="main">
  <div class="topbar">
    <div>
      <div class="page-title">Registrations Dashboard</div>
      <div class="page-sub">Ikon Computer Education &amp; Training Institute</div>
    </div>
    <div class="actions">
      <input class="search" id="s" type="search" placeholder="Search name, email, course..." oninput="filter(this.value)">
      <a href="/admin/export" class="btn btn-blue">Download CSV</a>
      <a href="/admin/logout" class="btn btn-out">Logout</a>
    </div>
  </div>

  <!-- KPI cards -->
  <div class="kpi-grid">
    <div class="kpi">
      <div class="kpi-label">Total Registrations</div>
      <div class="kpi-val">{total}</div>
      <div class="kpi-sub">All time</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Most Popular Course</div>
      <div class="kpi-val" style="font-size:18px">{popular}</div>
      <div class="kpi-sub">Highest enrolments</div>
    </div>
    <div class="kpi">
      <div class="kpi-label">Last Updated</div>
      <div class="kpi-val" style="font-size:18px">{now_str}</div>
      <div class="kpi-sub">Auto-refreshes on reload</div>
    </div>
  </div>

  <!-- Course breakdown -->
  <div style="font-weight:700;font-size:14px;margin-bottom:10px">Course Breakdown</div>
  <div class="chips">{chips_html}</div>

  <!-- Table -->
  <div class="tcard" id="regtable">
    <div class="thead-bar">
      <span class="ttitle">All Registered Candidates</span>
      <span class="cnt">{total} entries</span>
    </div>
    <div class="twrap">
      <table>
        <thead>
          <tr>
            <th>#</th><th>Timestamp</th><th>Name</th><th>Email</th>
            <th>Phone</th><th>Course</th><th>Mode</th><th>Message</th>
          </tr>
        </thead>
        <tbody id="tb">{rows_html}</tbody>
      </table>
    </div>
  </div>
</main>

<script>
function filter(q) {{
  var rows = document.querySelectorAll('#tb tr');
  var term = q.toLowerCase();
  rows.forEach(function(r) {{
    r.style.display = r.textContent.toLowerCase().indexOf(term) !== -1 ? '' : 'none';
  }});
}}
</script>"""
    return _html(body, "Dashboard — Ikon Admin")


def _esc(text: str) -> str:
    """HTML-escape user content to prevent XSS."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


# ── HTTP Handler ──────────────────────────────────────────────────────

class IkonHandler(http_server.BaseHTTPRequestHandler):

    _sessions: set = set()    # In-memory session tokens

    # ── Logging ──────────────────────────────────────────────────────
    def log_message(self, fmt, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {args[0]}  {args[1]}  {args[2]}")

    def log_error(self, fmt, *args):
        pass   # Suppress noisy socket errors from browser keep-alive

    # ── Helpers ──────────────────────────────────────────────────────
    def _send(self, status: int, content_type: str, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _html_resp(self, status: int, html: str):
        self._send(status, "text/html; charset=utf-8", html.encode("utf-8"))

    def _json_resp(self, status: int, data: dict):
        self._send(status, "application/json; charset=utf-8",
                   json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _redirect(self, location: str, cookie: str = ""):
        self.send_response(302)
        self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()

    def _is_authed(self) -> bool:
        cookie = self.headers.get("Cookie", "")
        return any(tok in cookie for tok in self.__class__._sessions)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length > 0 else b""

    # ── OPTIONS (CORS preflight) ──────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ── GET ───────────────────────────────────────────────────────────
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip("/") or "/"

        # ── Admin routes ──────────────────────────────────────────────
        if path in ("/admin", "/admin/"):
            if self._is_authed():
                status, html = dashboard_page(load_registrations())
                self._html_resp(status, html)
            else:
                status, html = login_page()
                self._html_resp(status, html)
            return

        if path == "/admin/logout":
            self._redirect("/admin", "session=; Max-Age=0; Path=/; HttpOnly; SameSite=Strict")
            return

        if path == "/admin/export":
            if not self._is_authed():
                self._redirect("/admin")
                return
            records = load_registrations()
            buf = io.StringIO()
            w   = csv.writer(buf)
            w.writerow(CSV_HEADERS)
            for r in records:
                w.writerow([
                    r.get("id",       ""),
                    r.get("timestamp",""),
                    r.get("name",     ""),
                    r.get("email",    ""),
                    r.get("phone",    ""),
                    COURSE_LABELS.get(r.get("course",""), r.get("course","")),
                    MODE_LABELS.get(  r.get("mode",  ""), r.get("mode",  "")),
                    r.get("message",  ""),
                ])
            body = ("\ufeff" + buf.getvalue()).encode("utf-8")
            stamp = datetime.now().strftime("%Y%m%d_%H%M")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition",
                             f'attachment; filename="ikon_registrations_{stamp}.csv"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # ── Static files ──────────────────────────────────────────────
        rel = "index.html" if path == "/" else path.lstrip("/")
        file_path = (BASE_DIR / rel).resolve()

        # Security: don't allow path traversal outside BASE_DIR
        try:
            file_path.relative_to(BASE_DIR)
        except ValueError:
            self._html_resp(403, "<h1>403 Forbidden</h1>")
            return

        if file_path.is_file():
            mime = MIME_TYPES.get(file_path.suffix.lower(), "application/octet-stream")
            data = file_path.read_bytes()
            self._send(200, mime, data)
        else:
            self._html_resp(404, "<h1>404 Not Found</h1>")

    # ── POST ──────────────────────────────────────────────────────────
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path.rstrip("/") or "/"

        # ── Admin login ───────────────────────────────────────────────
        if path in ("/admin", "/admin/"):
            body   = self._read_body()
            params = urllib.parse.parse_qs(body.decode("utf-8", errors="replace"))
            pwd    = params.get("password", [""])[0]

            if pwd == ADMIN_PASSWORD:
                token = secrets.token_hex(24)
                self.__class__._sessions.add(token)
                self._redirect("/admin",
                               f"session={token}; Path=/; HttpOnly; SameSite=Strict")
            else:
                status, html = login_page("Incorrect password. Please try again.")
                self._html_resp(status, html)
            return

        # ── Registration ──────────────────────────────────────────────
        if path == "/register":
            try:
                raw  = self._read_body()
                data = json.loads(raw.decode("utf-8"))

                entry = {
                    "timestamp": ist_now(),
                    "name":      str(data.get("name",    "")).strip(),
                    "email":     str(data.get("email",   "")).strip(),
                    "phone":     str(data.get("phone",   "")).strip(),
                    "course":    str(data.get("course",  "")).strip(),
                    "mode":      str(data.get("mode",    "")).strip(),
                    "message":   str(data.get("message", "")).strip(),
                }

                # Basic validation
                if not entry["name"] or not entry["email"]:
                    self._json_resp(400, {"status": "error", "message": "Name and email are required."})
                    return

                saved = save_registration(entry)
                course_label = COURSE_LABELS.get(saved["course"], saved["course"])
                print(f"[REG #{saved['id']}] {saved['name']} | {course_label} | {saved['timestamp']}")
                self._json_resp(200, {"status": "success", "id": saved["id"]})

            except (json.JSONDecodeError, UnicodeDecodeError) as ex:
                print(f"[ERR] Invalid request body: {ex}")
                self._json_resp(400, {"status": "error", "message": "Invalid JSON body."})
            except OSError as ex:
                print(f"[ERR] Could not save registration: {ex}")
                self._json_resp(500, {"status": "error", "message": "Server storage error."})
            return

        # ── Student login check ───────────────────────────────────────
        if path == "/login-check":
            try:
                raw  = self._read_body()
                data = json.loads(raw.decode("utf-8"))
                email      = str(data.get("email",       "")).strip().lower()
                phone_last4= str(data.get("phone_last4", "")).strip()

                if not email or not phone_last4:
                    self._json_resp(400, {"status": "error", "message": "Email and PIN required."})
                    return

                records = load_registrations()
                # Find by email (case-insensitive)
                match = next(
                    (r for r in records if r.get("email","").strip().lower() == email),
                    None
                )

                if match is None:
                    self._json_resp(200, {"status": "not_found"})
                    return

                # Validate PIN = last 4 digits of phone
                phone = str(match.get("phone","")).strip()
                if not phone.endswith(phone_last4):
                    self._json_resp(200, {"status": "wrong_pin"})
                    return

                # Return safe record (no sensitive data beyond what they registered)
                safe = {
                    "id":        match.get("id"),
                    "name":      match.get("name"),
                    "email":     match.get("email"),
                    "phone":     phone[:3] + "****" + phone[-2:] if len(phone) > 5 else "****",
                    "course":    COURSE_LABELS.get(match.get("course",""), match.get("course","")),
                    "mode":      MODE_LABELS.get(  match.get("mode",  ""), match.get("mode",  "")),
                    "timestamp": match.get("timestamp"),
                }
                print(f"[LOGIN] Student login: {match.get('name')} ({email})")
                self._json_resp(200, {"status": "found", "record": safe})

            except (json.JSONDecodeError, UnicodeDecodeError):
                self._json_resp(400, {"status": "error", "message": "Invalid request."})
            except Exception as ex:
                print(f"[ERR] login-check error: {ex}")
                self._json_resp(500, {"status": "error", "message": "Server error."})
            return

        self._json_resp(404, {"status": "error", "message": "Not found."})


# ── Graceful shutdown ─────────────────────────────────────────────────

def _make_shutdown(srv):
    def _handler(signum, frame):
        print("\n[INFO] Shutting down server...")
        srv.shutdown()
    return _handler


# ── Entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    os.chdir(BASE_DIR)

    port = find_free_port(PREFERRED_PORT)
    if port != PREFERRED_PORT:
        print(f"[INFO] Port {PREFERRED_PORT} busy, using {port} instead.")

    httpd = http_server.HTTPServer(("", port), IkonHandler)

    # Graceful Ctrl+C / SIGTERM on all platforms
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(sig, _make_shutdown(httpd))
        except (OSError, ValueError):
            pass   # Some signals unavailable on certain platforms

    print("")
    print("==========================================================")
    print("  IKON Computer Education & Training Institute")
    print("  Internship Registration Server")
    print("==========================================================")
    print(f"  Website  -->  http://localhost:{port}")
    print(f"  Admin    -->  http://localhost:{port}/admin")
    print(f"  Password -->  {ADMIN_PASSWORD}")
    print(f"  Export   -->  http://localhost:{port}/admin/export")
    print("==========================================================")
    print("  Press Ctrl+C to stop.")
    print("")

    # Auto-open the website in the default browser
    import webbrowser
    import threading
    threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")
