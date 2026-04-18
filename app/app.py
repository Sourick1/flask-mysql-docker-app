import os
import time
import logging
from flask import Flask, request, jsonify, render_template_string
import mysql.connector
from mysql.connector import Error

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ── DB Config from env vars ───────────────────────────────────────────────────
DB_CONFIG = {
    "host":     os.getenv("MYSQL_HOST", "db"),
    "port":     int(os.getenv("MYSQL_PORT", 3306)),
    "user":     os.getenv("MYSQL_USER", "flaskuser"),
    "password": os.getenv("MYSQL_PASSWORD", "flaskpass"),
    "database": os.getenv("MYSQL_DATABASE", "messagesdb"),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_connection(retries: int = 10, delay: int = 3):
    """Return a MySQL connection, retrying until MySQL is ready."""
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                logger.info("MySQL connection established.")
                return conn
        except Error as e:
            logger.warning("Attempt %d/%d – MySQL not ready: %s", attempt, retries, e)
            time.sleep(delay)
    raise RuntimeError("Could not connect to MySQL after multiple retries.")


def init_db():
    """Create the messages table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            content   TEXT        NOT NULL,
            author    VARCHAR(100) DEFAULT 'Anonymous',
            created_at TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Database initialised.")


# ── HTML Frontend (inline template) ──────────────────────────────────────────
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Flask Messages Board </title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #0f0f1a;
      --surface:   #1a1a2e;
      --surface2:  #16213e;
      --accent:    #7c3aed;
      --accent2:   #a855f7;
      --glow:      rgba(124, 58, 237, 0.35);
      --text:      #e2e8f0;
      --muted:     #94a3b8;
      --border:    rgba(124, 58, 237, 0.2);
      --success:   #10b981;
      --error:     #ef4444;
    }

    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      background-image:
        radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(168,85,247,0.1) 0%, transparent 50%);
    }

    header {
      background: rgba(26, 26, 46, 0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 1.25rem 2rem;
      display: flex;
      align-items: center;
      gap: 1rem;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    header .logo {
      width: 40px; height: 40px;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.2rem;
      box-shadow: 0 0 20px var(--glow);
    }
    header h1 { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.5px; }
    header span { color: var(--accent2); }

    .badge {
      margin-left: auto;
      padding: 0.3rem 0.8rem;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    main { max-width: 860px; margin: 0 auto; padding: 2.5rem 1.5rem; }

    /* ── Form card ── */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 2rem;
      transition: box-shadow .3s;
    }
    .card:hover { box-shadow: 0 0 30px var(--glow); }

    .card h2 {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .card h2::before {
      content: '';
      display: inline-block;
      width: 4px; height: 1.2em;
      background: linear-gradient(180deg, var(--accent), var(--accent2));
      border-radius: 2px;
    }

    .form-row { display: flex; gap: 1rem; flex-wrap: wrap; }
    .form-group { display: flex; flex-direction: column; gap: 0.4rem; flex: 1; min-width: 180px; }

    label { font-size: 0.8rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }

    input[type="text"], textarea {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      color: var(--text);
      font-family: inherit;
      font-size: 0.95rem;
      transition: border-color .2s, box-shadow .2s;
      outline: none;
      resize: none;
    }
    input[type="text"]:focus, textarea:focus {
      border-color: var(--accent2);
      box-shadow: 0 0 0 3px rgba(168,85,247,0.15);
    }

    button[type="submit"] {
      margin-top: 1rem;
      padding: 0.8rem 2rem;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border: none;
      border-radius: 10px;
      color: #fff;
      font-family: inherit;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform .15s, box-shadow .15s;
      box-shadow: 0 4px 15px var(--glow);
    }
    button[type="submit"]:hover  { transform: translateY(-2px); box-shadow: 0 6px 25px var(--glow); }
    button[type="submit"]:active { transform: translateY(0); }

    /* ── Toast ── */
    #toast {
      position: fixed; bottom: 2rem; right: 2rem;
      padding: 0.9rem 1.4rem;
      border-radius: 12px;
      font-size: 0.9rem;
      font-weight: 600;
      opacity: 0;
      transform: translateY(10px);
      transition: opacity .3s, transform .3s;
      pointer-events: none;
      z-index: 9999;
    }
    #toast.show { opacity: 1; transform: translateY(0); }
    #toast.success { background: var(--success); color: #fff; }
    #toast.error   { background: var(--error);   color: #fff; }

    /* ── Messages list ── */
    .messages-header {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 1.2rem;
    }
    .messages-header h2 { font-size: 1.1rem; font-weight: 600; display: flex; align-items: center; gap: 0.6rem; }
    #refreshBtn {
      padding: 0.5rem 1.1rem;
      background: transparent;
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--muted);
      font-family: inherit;
      font-size: 0.82rem;
      cursor: pointer;
      transition: border-color .2s, color .2s;
    }
    #refreshBtn:hover { border-color: var(--accent2); color: var(--accent2); }

    #msgList { display: flex; flex-direction: column; gap: 0.85rem; }

    .msg-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      display: flex;
      gap: 1rem;
      align-items: flex-start;
      animation: slideIn .3s ease;
      transition: transform .2s, box-shadow .2s;
    }
    .msg-item:hover { transform: translateX(4px); box-shadow: 0 0 20px var(--glow); }

    @keyframes slideIn {
      from { opacity: 0; transform: translateY(8px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .msg-avatar {
      width: 38px; height: 38px; min-width: 38px;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-weight: 700;
      font-size: 0.85rem;
    }

    .msg-body { flex: 1; }
    .msg-meta { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.3rem; }
    .msg-author { font-weight: 600; font-size: 0.9rem; }
    .msg-time { font-size: 0.75rem; color: var(--muted); }
    .msg-content { font-size: 0.92rem; color: var(--text); line-height: 1.55; }

    .empty-state {
      text-align: center; padding: 3rem 1rem;
      color: var(--muted); font-size: 0.95rem;
    }
    .empty-state .emoji { font-size: 2.5rem; display: block; margin-bottom: 0.7rem; }

    footer {
      text-align: center;
      padding: 2rem;
      color: var(--muted);
      font-size: 0.8rem;
      border-top: 1px solid var(--border);
      margin-top: 3rem;
    }
  </style>
</head>
<body>

<header>
  <div class="logo">💬</div>
  <h1>Flask <span>Messages</span> Board</h1>
  <span class="badge">MySQL · Docker</span>
</header>

<main>
  <!-- Post a message -->
  <div class="card">
    <h2>Post a Message</h2>
    <form id="msgForm">
      <div class="form-row">
        <div class="form-group" style="flex:0 0 200px">
          <label for="author">Author</label>
          <input type="text" id="author" placeholder="Your name" maxlength="100"/>
        </div>
        <div class="form-group">
          <label for="content">Message</label>
          <textarea id="content" rows="3" placeholder="What's on your mind?"></textarea>
        </div>
      </div>
      <button type="submit">✉️ &nbsp;Send Message now</button>
    </form>
  </div>

  <!-- Messages feed -->
  <div class="messages-header">
    <h2>💬 &nbsp;Messages</h2>
    <button id="refreshBtn" onclick="loadMessages()">⟳ &nbsp;Refresh</button>
  </div>
  <div id="msgList"><p class="empty-state"><span class="emoji">⏳</span>Loading…</p></div>
</main>

<div id="toast"></div>

<footer>Flask + MySQL + Docker &nbsp;·&nbsp; Built by Antigravity</footer>

<script>
  const toast = document.getElementById('toast');

  function showToast(msg, type = 'success') {
    toast.textContent = msg;
    toast.className = 'show ' + type;
    setTimeout(() => { toast.className = ''; }, 3000);
  }

  async function loadMessages() {
    const list = document.getElementById('msgList');
    list.innerHTML = '<p class="empty-state"><span class="emoji">⏳</span>Loading…</p>';
    try {
      const res = await fetch('/messages');
      const data = await res.json();
      if (!data.messages || data.messages.length === 0) {
        list.innerHTML = '<p class="empty-state"><span class="emoji">🌵</span>No messages yet. Be the first!</p>';
        return;
      }
      list.innerHTML = '';
      data.messages.forEach(m => {
        const initial = (m.author || 'A')[0].toUpperCase();
        const dt = new Date(m.created_at).toLocaleString();
        const item = document.createElement('div');
        item.className = 'msg-item';
        item.innerHTML = `
          <div class="msg-avatar">${initial}</div>
          <div class="msg-body">
            <div class="msg-meta">
              <span class="msg-author">${escHtml(m.author)}</span>
              <span class="msg-time">${dt}</span>
            </div>
            <div class="msg-content">${escHtml(m.content)}</div>
          </div>`;
        list.appendChild(item);
      });
    } catch (e) {
      list.innerHTML = '<p class="empty-state"><span class="emoji">❌</span>Failed to load messages.</p>';
    }
  }

  document.getElementById('msgForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const author  = document.getElementById('author').value.trim() || 'Anonymous';
    const content = document.getElementById('content').value.trim();
    if (!content) { showToast('Message cannot be empty!', 'error'); return; }

    try {
      const res = await fetch('/messages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author, content })
      });
      const data = await res.json();
      if (res.ok) {
        showToast('Message sent! 🎉');
        document.getElementById('content').value = '';
        loadMessages();
      } else {
        showToast(data.error || 'Error sending message.', 'error');
      }
    } catch (err) {
      showToast('Network error.', 'error');
    }
  });

  function escHtml(str) {
    return String(str)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  loadMessages();
</script>
</body>
</html>"""


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/messages", methods=["GET"])
def get_messages():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, content, author, created_at FROM messages ORDER BY created_at DESC LIMIT 100")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert datetime to ISO string for JSON
        for r in rows:
            if r.get("created_at"):
                r["created_at"] = r["created_at"].isoformat()
        return jsonify({"messages": rows})
    except Exception as e:
        logger.error("GET /messages error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/messages", methods=["POST"])
def post_message():
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    author  = (data.get("author")  or "Anonymous").strip()

    if not content:
        return jsonify({"error": "content is required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (content, author) VALUES (%s, %s)",
            (content, author)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "created", "id": new_id}), 201
    except Exception as e:
        logger.error("POST /messages error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
