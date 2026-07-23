const promptEl = document.querySelector('#prompt');
const validateBtn = document.querySelector('#validate');
const scoreEl = document.querySelector('#score');
const statusEl = document.querySelector('#status');
const contextCheck = document.querySelector('#contextCheck');
const contractCheck = document.querySelector('#contractCheck');
const traceCheck = document.querySelector('#traceCheck');
const inferenceCheck = document.querySelector('#inferenceCheck');
const actsEl = document.querySelector('#acts');
const traceEl = document.querySelector('#trace');
const modeNote = document.querySelector('#modeNote');
const API_URL = (window.KYVERNEX_API_URL || '').replace(/\/$/, '');

const implicit = /\b(procedi|come prima|quello precedente|ultima versione|stesse regole)\b/i;
const adversarial = /\b(inventa|ignora i dati|fabbrica|senza prove)\b/i;
const patterns = [
  ['READ', /\b(leggi|analizza|controlla|review|read|analy[sz]e)\b/i],
  ['CLASSIFY', /\b(analizza|classifica|separa|analy[sz]e|classify)\b/i],
  ['SUMMARIZE', /\b(riassumi|sintetizza|summary|summari[sz]e)\b/i],
  ['VERIFY', /\b(verifica|controlla|prove|verify|evidence)\b/i],
  ['COMPARE', /\b(confronta|compare|differenze)\b/i],
  ['EXTRACT', /\b(estrai|extract|elenca)\b/i],
  ['GENERATE', /\b(crea|scrivi|genera|inventa|write|generate)\b/i],
  ['TRANSLATE', /\b(traduci|translate)\b/i],
];

function localAnalyze(text) {
  const clean = text.trim();
  const acts = patterns.filter(([, regex]) => regex.test(clean)).map(([name]) => name);
  const hasImplicit = implicit.test(clean);
  const isAdversarial = adversarial.test(clean);
  const mentionsObject = /\b(pdf|documento|file|testo|articolo|contratto|report)\b/i.test(clean);
  let status = 'VALID';
  let css = 'good';
  let score = 96;
  let context = 'NOT REQUIRED';
  let contract = 'VALID';
  let unsupported = '0';
  const trace = [];

  if (!clean) {
    return { acts: ['QUESTION'], status: 'INVALID INPUT', css: 'bad', score: 0, context: 'MISSING', contract: 'INVALID', unsupported: '0', trace: ['Input assente: pipeline interrotta.'] };
  }

  trace.push('Input preservato e normalizzato.');
  if (hasImplicit) {
    context = 'MISSING';
    contract = 'PARTIAL';
    status = 'CLARIFICATION REQUIRED';
    css = 'warn';
    score = 58;
    trace.push('Riferimento implicito rilevato.');
    trace.push('Nessuna fonte canonica collegata nel browser.');
  }
  if (mentionsObject && !/\b(incolla|seguente|qui sotto)\b/i.test(clean)) {
    contract = 'PARTIAL';
    status = status === 'CLARIFICATION REQUIRED' ? status : 'OBJECT REQUIRED';
    css = 'warn';
    score = Math.min(score, 72);
    trace.push('Oggetto documentale citato ma non disponibile.');
  }
  if (isAdversarial) {
    status = 'REJECTED';
    css = 'bad';
    score = 18;
    contract = 'REFUSED';
    unsupported = 'BLOCKED';
    trace.push('Richiesta di conclusione non supportata rilevata.');
  }
  if (!acts.length && !hasImplicit && !isAdversarial) {
    contract = 'PARTIAL';
    status = 'COGNITIVE ACT UNKNOWN';
    css = 'warn';
    score = 45;
    trace.push('Atto cognitivo non classificato.');
  }
  return { acts: acts.length ? acts : ['QUESTION'], status, css, score, context, contract, unsupported, trace };
}

function apiResult(payload) {
  const translation = payload.translation || {};
  const validation = payload.validation || {};
  const kernel = payload.kernel || {};
  const valid = validation.valid === true;
  const completed = kernel.status === 'COMPLETED';
  const status = completed ? 'COMPLETED' : (kernel.status || translation.status || 'UNKNOWN');
  const css = completed && valid ? 'good' : (status.includes('REJECT') || status.includes('ERROR') ? 'bad' : 'warn');
  const unknowns = translation.unknowns || [];
  const ambiguities = translation.ambiguities || [];
  const score = completed && valid ? 100 : Math.max(20, 100 - ((unknowns.length + ambiguities.length) * 15) - ((kernel.errors || []).length * 20));
  const trace = [];

  if (payload.analysis_id) trace.push(`Analysis ID: ${payload.analysis_id}`);
  if (payload.fingerprint) trace.push(`Fingerprint: ${payload.fingerprint}`);
  if (payload.created_at) trace.push(`Created: ${payload.created_at}`);
  if (typeof payload.duration_ms === 'number') trace.push(`Duration: ${payload.duration_ms} ms`);

  (payload.timeline || []).forEach(item => {
    trace.push(`${String(item.step).padStart(2, '0')} · ${item.event} · ${item.status}`);
  });
  (kernel.trace || []).forEach(item => {
    trace.push(typeof item === 'string' ? item : JSON.stringify(item));
  });

  return {
    acts: translation.acts || ['QUESTION'],
    status,
    css,
    score,
    context: ambiguities.length ? 'AMBIGUOUS' : (unknowns.length ? 'MISSING' : 'BOUND/NOT REQUIRED'),
    contract: translation.status || (valid ? 'VALID' : 'INVALID'),
    unsupported: (kernel.errors || []).length,
    trace: trace.length ? trace : ['Nessuna traccia restituita.'],
  };
}

function render(result) {
  scoreEl.textContent = `${result.score}/100`;
  statusEl.textContent = result.status;
  statusEl.className = `status ${result.css}`;
  contextCheck.textContent = result.context;
  contractCheck.textContent = result.contract;
  traceCheck.textContent = result.trace.length ? 'VISIBLE' : 'MISSING';
  inferenceCheck.textContent = result.unsupported;
  actsEl.textContent = result.acts.join(' → ');
  traceEl.innerHTML = '';
  result.trace.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    traceEl.appendChild(li);
  });
}

async function validate() {
  validateBtn.disabled = true;
  validateBtn.textContent = API_URL ? 'VALIDATING…' : 'ANALYZING…';
  try {
    if (!API_URL) {
      render(localAnalyze(promptEl.value));
      return;
    }
    const response = await fetch(`${API_URL}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: promptEl.value, read_pdf: false }),
    });
    if (!response.ok) throw new Error(`API ${response.status}`);
    render(apiResult(await response.json()));
  } catch (error) {
    render({ acts: ['ERROR'], status: 'API UNAVAILABLE', css: 'bad', score: 0, context: 'UNKNOWN', contract: 'INTERRUPTED', unsupported: '—', trace: [String(error), 'La demo locale resta disponibile rimuovendo KYVERNEX_API_URL da config.js.'] });
  } finally {
    validateBtn.disabled = false;
    validateBtn.textContent = 'VALIDATE';
  }
}

modeNote.textContent = API_URL
  ? `API reale collegata: ${API_URL}. Nessun modello esterno viene interrogato.`
  : 'Modalità demo locale. L’API reale si attiva impostando KYVERNEX_API_URL in config.js.';

validateBtn.addEventListener('click', validate);
document.querySelectorAll('.example').forEach(button => button.addEventListener('click', () => {
  promptEl.value = button.dataset.text;
  validate();
}));
document.querySelector('#copyCommand').addEventListener('click', async event => {
  const command = 'git clone https://github.com/benleva/ARGUS.git\ncd ARGUS/engine-reference\npython -m pip install -e " .[test]"\nuvicorn argus_engine.api:app --host 0.0.0.0 --port 8000'.replace('" .[test]"', '".[test]"');
  try {
    await navigator.clipboard.writeText(command);
    event.currentTarget.textContent = 'COPIATO';
    setTimeout(() => event.currentTarget.textContent = 'COPIA', 1600);
  } catch {
    event.currentTarget.textContent = 'SELEZIONA';
  }
});

validate();