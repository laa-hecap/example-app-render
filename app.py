from flask import Flask, jsonify, Response
import datetime as dt
import os, socket
from zoneinfo import ZoneInfo

app = Flask(__name__, static_folder="static")

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
<title>CoAfina 2025 · Mini app</title>
<style>
  /* Colores aproximados al afiche: fondo azul muy oscuro + acentos morado/lila */
  :root {{
    --bg: #0b1120;         /* fondo principal */
    --card: #141a2e;       /* tarjetas */
    --border: #263159;     /* bordes */
    --accent: #b79df2;     /* acento lila */
    --accent-2: #6a5acd;   /* morado */
    --text: #ffffff;       /* texto principal */
    --muted: rgba(255,255,255,.8);
  }}
  * {{ box-sizing: border-box }}
  body {{ margin: 0; background: var(--bg); color: var(--text); }}
  a {{ color: var(--accent); text-decoration: none }}
  .wrap {{ max-width: 980px; margin: 6vh auto 14vh; padding: 24px; }}
  .card {{
    background: linear-gradient(180deg, rgba(183,157,242,.08), rgba(0,0,0,0)) , var(--card);
    border: 1px solid var(--border);
    border-radius: 16px; padding: 22px;
    box-shadow: 0 10px 32px rgba(0,0,0,.35);
  }}
  h1 {{ margin: 0 0 8px 0; font-size: 34px; letter-spacing:.3px }}
  .muted {{ color: var(--muted); font-size: 14px }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin-top:16px }}
  .kpi {{ background:#0f1530; border:1px solid var(--border); padding:14px; border-radius:12px }}
  .btn {{ display:inline-block; padding:10px 14px; border-radius:10px; background:#1c2350; border:1px solid var(--border) }}
  .badge {{ display:inline-block; padding:6px 10px; border-radius:999px; background: #1d2150; border:1px solid var(--accent-2); color:#fff; font-size:12px }}
  /* Logo pegado al centro inferior */
  .footer-logo {{
    position: fixed; left: 50%; bottom: 18px; transform: translateX(-50%);
    display: flex; flex-direction: column; align-items: center; gap: 6px;
    opacity: .95;
  }}
  .footer-logo img {{ width: 120px; height: auto; filter: drop-shadow(0 6px 14px rgba(0,0,0,.45)); }}
  .footer-logo span {{ font-size: 12px; color: var(--muted) }}
  @media (max-width: 520px) {{
    h1 {{ font-size: 26px }}
    .footer-logo img {{ width: 96px }}
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="badge">Ejemplo para COAFINA 2025</div>
      <h1>¡Volvemos a sonar juntos!</h1>
      <p class="muted">
        Demo con Flask + Docker listo para Render ·
        <a href="https://laconga.redclara.net/hackathon/" target="_blank" rel="noreferrer">laconga.redclara.net/hackathon/</a>
      </p>
      <p class="muted">Host <code>{socket.gethostname()}</code> · Puerto <code>{os.getenv("PORT","10000")}</code> · Escuchando en <code>$PORT</code>.</p>

      <div class="grid" id="times">
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

  <div class="footer-logo">
    <img src="/static/logo.png" alt="Logo CoAfina" />
    <span>&copy; 2025</span>
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
    }} catch (e) {{}}
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
    return jsonify(server_utc=now_iso_utc(), local_times=local_times())

@app.get("/healthz")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
