"""Self-contained local console page for the KYVERNEX AI server."""
from __future__ import annotations


def build_local_ai_page() -> bytes:
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KYVERNEX Local AI</title>
<style>
body{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:24px;background:#111827;color:#e5e7eb}
h1{margin:0 0 6px}p{color:#9ca3af}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:#1f2937;padding:16px;border-radius:12px}textarea,select,button,pre{width:100%;box-sizing:border-box}textarea{min-height:180px;padding:12px;background:#0f172a;color:#e5e7eb;border:1px solid #374151;border-radius:8px}button,select{padding:10px;margin-top:10px;border-radius:8px;border:0}button{cursor:pointer;font-weight:700}pre{white-space:pre-wrap;word-break:break-word;background:#0f172a;padding:12px;border-radius:8px;min-height:120px}.ok{color:#86efac}.bad{color:#fca5a5}@media(max-width:700px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<h1>KYVERNEX Local AI</h1>
<p>Loopback-only console for the governed AI bridge.</p>
<div class="grid">
<section class="card"><h2>Status</h2><button onclick="loadHealth()">Refresh health</button><pre id="health">Not loaded</pre></section>
<section class="card"><h2>Manifest</h2><select id="format"><option>canonical</option><option>openai</option><option>anthropic</option><option>gemini</option></select><button onclick="loadManifest()">Load manifest</button><pre id="manifest">Not loaded</pre></section>
</div>
<section class="card" style="margin-top:16px"><h2>Invoke</h2><textarea id="request">{"input":{"message":"ciao"},"context":{"source":"local-console"}}</textarea><button onclick="invoke()">Send governed request</button><pre id="response">Waiting</pre></section>
<script>
const show=(id,data,ok=true)=>{const e=document.getElementById(id);e.textContent=JSON.stringify(data,null,2);e.className=ok?'ok':'bad'};
async function readJson(url,options){const r=await fetch(url,options);let data;try{data=await r.json()}catch{data={status:'FAILED',error:'non-JSON response'}}return [r.ok,data]}
async function loadHealth(){try{const [ok,data]=await readJson('/health');show('health',data,ok)}catch(e){show('health',{status:'FAILED',error:String(e)},false)}}
async function loadManifest(){try{const f=document.getElementById('format').value;const [ok,data]=await readJson('/manifest?format='+encodeURIComponent(f));show('manifest',data,ok)}catch(e){show('manifest',{status:'FAILED',error:String(e)},false)}}
async function invoke(){let body;try{body=JSON.parse(document.getElementById('request').value)}catch(e){show('response',{status:'FAILED',error:'invalid JSON: '+e.message},false);return}try{const [ok,data]=await readJson('/invoke',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});show('response',data,ok)}catch(e){show('response',{status:'FAILED',error:String(e)},false)}}
loadHealth();
</script>
</body>
</html>"""
    return html.encode("utf-8")
