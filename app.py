from flask import Flask, jsonify, Response
import datetime as dt
import os, socket
from zoneinfo import ZoneInfo

app = Flask(__name__)

ZONES = {
    "mexico_df": ("Ciudad de México", "America/Mexico_City"),
    "argentina": ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    "venezuela": ("Caracas", "America/Caracas"),
    "colombia": ("Bogotá", "America/Bogota"),
    "suiza": ("Zúrich", "Europe/Zurich"),
}

def now_iso_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat()

def local_times():
    data = {}
    for key, (label, tz) in ZONES.items():
        t = dt.datetime.now(ZoneInfo(tz))
        data[key] = {
            "label": label,
            "tz": tz,
            "iso": t.isoformat(),
            "display": t.strftime("%Y-%m-%d %H:%M:%S"),
        }
    return data

PAGE = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>COAFINA 2025 · Mini app en Flask</title>
<style>
  :root {{ font-family: ui-sans-serif, system-ui; }}
  body {{ margin: 0; background: #0f1221; color: #e8e8ff; }}
  .wrap {{ max-width: 880px; margin: 6vh auto; padding: 24px; }}
  .card {{ background:#171a2e; border:1px solid #2a2f55; border-radius:14px; padding:22px; box-shadow:0 8px 30px rgba(0,0,0,.35); }}
  h1 {{ margin: 0 0 8px 0; font-size: 28px; }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-top:16px; }}
  .kpi {{ background:#10132a; border:1px solid #252b51; padding:14px; border-radius:12px; }}
  .muted {{ opacity:.8; font-size:14px }}
  a {{ color:#8ab4ff; text-decoration:none }}
  .btn {{ display:inline-block; padding:10px 14px; border-radius:10px; background:#2a2f55; border:1px solid #3b4280 }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>🚀 Flask + Docker listo para Render</h1>
      <p class="muted">Ejemplo para <strong>COAFINA 2025</strong> — 
        <a href="https://laconga.redclara.net/hackathon/" target="_blank" rel="noreferrer">laconga.redclara.net/hackathon/</a>
      </p>
      <p class="muted">Contenedor escuchando en <code>$PORT</code>. Host <code>{socket.gethostname()}</code>, puerto <code>{os.getenv("PORT","10000")}</code>.</p>

      <div class="grid" id="times">
        <!-- Tarjetas de zonas horarias -->
        <div class="kpi"><div class="muted">Ciudad de México</div><div id="mexico_df" style="font-size:22px;margin-top:4px;">…</div></div>
        <div class="kpi"><div class="muted">Buenos Aires</div><div id="argentina"  style="font-size:22px;margin-top:4px;">…</div></div>
        <div class="kpi"><div class="muted">Caracas</div><div id="venezuela"  style="font-size:22px;margin-top:4px;">…</div></div>
        <div class="kpi"><div class="muted">Bogotá</div><div id="colombia"   style="font-size:22px;margin-top:4px;">…</div></div>
        <div class="kpi"><div class="muted">Zúrich</div><div id="suiza"      style="font-size:22px;margin-top:4px;">…</div></div>
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
      for (const key of Object.keys(j.local_times)) {{
        const el = document.getElementById(key);
        if (el) el.textContent = j.local_times[key].display;
      }}
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
    return jsonify(
        server_utc=now_iso_utc(),
        local_times=local_times()
    )

@app.get("/healthz")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
