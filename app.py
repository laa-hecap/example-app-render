from flask import Flask, jsonify, Response
import datetime as dt, os, socket
from zoneinfo import ZoneInfo

app = Flask(__name__, static_folder="static")

# Edita aquí: agrega o quita ciudades. (máximo 9 sin tocar el HTML)
ZONES = {
    "mexico_df": ("Ciudad de México", "America/Mexico_City"),
    "argentina": ("Buenos Aires", "America/Argentina/Buenos_Aires"),
    "venezuela": ("Caracas", "America/Caracas"),
    "colombia":  ("Bogotá", "America/Bogota"),
    "suiza":     ("Zúrich", "Europe/Zurich"),
    "bolivia":   ("La Paz", "America/La_Paz"),
    "ecuador":   ("Quito", "America/Guayaquil"),
    "peru":      ("Lima", "America/Lima"),
    "paraguay":  ("Asunción", "America/Asuncion"),
}

def now_iso_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat()

def local_times():
    out = {}
    for key, (label, tz) in ZONES.items():
        t = dt.datetime.now(ZoneInfo(tz))
        out[key] = {"label": label, "tz": tz, "iso": t.isoformat(),
                    "display": t.strftime("%Y-%m-%d %H:%M:%S")}
    return out

# Construimos las tarjetas según ZONES para que sea fácil ampliarlo
cards_html = "\n".join(
    f'''<div class="kpi"><div class="muted">{label}</div>
        <div id="{key}" class="time">…</div></div>'''
    for key, (label, _tz) in ZONES.items()
)

PAGE = f"""<!doctype html>
<html><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>CoAfina 2025 · Mini app</title>
<style>
  :root {{
    --bg:#0b1120; --card:#121832; --border:#2b3160;
    --accent:#b79df2; --accent2:#6a5acd; --text:#fff; --muted:rgba(255,255,255,.85);
  }}
  * {{ box-sizing:border-box }}
  body {{ margin:0; background:var(--bg); color:var(--text); font-family:ui-sans-serif,system-ui; }}
  a {{ color:var(--accent); text-decoration:none }}
  .wrap {{ max-width:1040px; margin:6vh auto 22vh; padding:24px }}
  .card {{
    background: linear-gradient(180deg, rgba(183,157,242,.12), rgba(0,0,0,0)) , var(--card);
    border:1px solid var(--border); border-radius:18px; padding:26px;
    box-shadow:0 18px 50px rgba(0,0,0,.35);
  }}
  h1 {{ margin:0 0 10px; font-size:38px }}
  .muted {{ color:var(--muted); font-size:14px }}
  .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:14px; margin-top:18px }}
  .kpi {{ background:#0f1430; border:1px solid var(--border); padding:16px; border-radius:14px }}
  .time {{ font-size:22px; margin-top:6px }}
  .btn {{ display:inline-block; padding:10px 14px; border-radius:12px; background:#1a2050; border:1px solid var(--border) }}
  .badge {{ display:inline-block; padding:6px 10px; border-radius:999px; background:#1d2150; border:1px solid var(--accent2); font-size:12px }}
  /* Logo grande, centrado abajo */
  .footer-logo {{
    position: fixed; left:50%; bottom:24px; transform:translateX(-50%);
    display:flex; flex-direction:column; align-items:center; gap:8px; opacity:.98;
  }}
  .footer-logo img {{ width: 240px; height:auto; filter:drop-shadow(0 8px 22px rgba(0,0,0,.45)) }}
  .footer-logo span {{ font-size:12px; color:var(--muted) }}
  @media (max-width:600px) {{
    h1 {{ font-size:28px }}
    .footer-logo img {{ width: 180px }}
  }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <div class="badge">Ejemplo para CoAfina 2025</div>
      <h1>¡Volvemos a sonar juntos!</h1>
      <p class="muted">Demo Flask + Docker listo para Render ·
        <a href="https://laconga.redclara.net/hackathon/" target="_blank" rel="noreferrer">laconga.redclara.net/hackathon/</a>
      </p>
      <p class="muted">Host <code>{socket.gethostname()}</code> · Puerto <code>{os.getenv("PORT","10000")}</code> · Escuchando en <code>$PORT</code>.</p>

      <div class="grid" id="times">
        {cards_html}
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
    const r = await fetch('/api/time').catch(()=>null);
    if(!r) return;
    const j = await r.json();
    for (const key in j.local_times) {{
      const el = document.getElementById(key);
      if (el) el.textContent = j.local_times[key].display;
    }}
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
