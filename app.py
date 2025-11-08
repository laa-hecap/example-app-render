from flask import Flask, jsonify, Response
import datetime, os, socket

app = Flask(__name__)

PAGE = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Mini app en Flask</title>
<style>
  :root {{ font-family: ui-sans-serif, system-ui; }}
  body {{ margin: 0; background: #0f1221; color: #e8e8ff; }}
  .wrap {{ max-width: 780px; margin: 6vh auto; padding: 24px; }}
  .card {{ background:#171a2e; border:1px solid #2a2f55; border-radius:14px; padding:22px; box-shadow:0 8px 30px rgba(0,0,0,.35); }}
  h1 {{ margin: 0 0 8px 0; font-size: 28px; }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin-top:16px; }}
  .kpi {{ background:#10132a; border:1px solid #252b51; padding:14px; border-radius:12px; }}
  .muted {{ opacity:.8; font-size:14px }}
  a {{ color:#8ab4ff; text-decoration:none }}
  .btn {{ display:inline-block; padding:10px 14px; border-radius:10px; background:#2a2f55; border:1px solid #3b4280 }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1> Flask + Docker listo para Render</h1>
      <p class="muted">Contenedor escuchando en <code>$PORT</code> para Render.</p>
      <div class="grid">
        <div class="kpi"><div class="muted">Hora del servidor</div><div id="now" style="font-size:22px;margin-top:4px;">…</div></div>
        <div class="kpi"><div class="muted">Host</div><div style="font-size:22px;margin-top:4px;">{socket.gethostname()}</div></div>
        <div class="kpi"><div class="muted">Puerto</div><div style="font-size:22px;margin-top:4px;">{os.getenv("PORT","10000")}</div></div>
      </div>
      <p style="margin-top:18px">
        <a class="btn" href="/healthz">/healthz</a>
        <a class="btn" href="/api/time">/api/time</a>
        <a class="btn" href="https://render.com/docs" target="_blank" rel="noreferrer">Docs Render</a>
      </p>
    </div>
  </div>
<script>
  async function tick(){{
    try {{
      const r = await fetch('/api/time');
      const j = await r.json();
      document.getElementById('now').textContent = j.now_iso.replace('T',' ').split('.')[0];
    }} catch(e) {{}}
  }}
  tick(); setInterval(tick, 1000);
</script>
</body></html>
"""

@app.get("/")
def home():
    return Response(PAGE, mimetype="text/html")

@app.get("/api/time")
def api_time():
    return jsonify(now_iso=datetime.datetime.utcnow().isoformat()+"Z")

@app.get("/healthz")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    # Para ejecución local: python app.py
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
