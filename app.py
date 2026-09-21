import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ML Shooter Quiz",
    page_icon="🎯",
    layout="centered"
)

QUESTIONS = [
    {
        "question": "¿Qué significa Machine Learning?",
        "options": [
            "Una técnica para diseñar páginas web",
            "Una rama de la IA que aprende patrones a partir de datos",
            "Un lenguaje de programación",
            "Un sistema operativo"
        ],
        "answer": "Una rama de la IA que aprende patrones a partir de datos",
        "explanation": "Machine Learning permite aprender patrones a partir de datos."
    },
    {
        "question": "¿Cuál es un tipo principal de Machine Learning?",
        "options": [
            "Aprendizaje supervisado",
            "Aprendizaje manual",
            "Aprendizaje estático",
            "Aprendizaje visual únicamente"
        ],
        "answer": "Aprendizaje supervisado",
        "explanation": "Los tipos principales incluyen supervisado, no supervisado y por refuerzo."
    },
    {
        "question": "¿Qué caracteriza al aprendizaje supervisado?",
        "options": [
            "Trabaja con datos etiquetados",
            "Nunca necesita datos",
            "Solo utiliza imágenes",
            "No permite predicciones"
        ],
        "answer": "Trabaja con datos etiquetados",
        "explanation": "El modelo aprende con ejemplos que contienen una respuesta conocida."
    },
    {
        "question": "¿Cuál es un ejemplo de clasificación?",
        "options": [
            "Predecir el precio de una vivienda",
            "Agrupar clientes por similitud",
            "Determinar si un correo es spam o no spam",
            "Reducir la cantidad de columnas"
        ],
        "answer": "Determinar si un correo es spam o no spam",
        "explanation": "La clasificación predice categorías o clases."
    },
    {
        "question": "¿Cuál es un ejemplo de regresión?",
        "options": [
            "Predecir el precio de una vivienda",
            "Clasificar imágenes como gato o perro",
            "Agrupar documentos",
            "Detectar comunidades"
        ],
        "answer": "Predecir el precio de una vivienda",
        "explanation": "La regresión predice valores numéricos."
    },
    {
        "question": "¿Qué busca el aprendizaje no supervisado?",
        "options": [
            "Aprender exclusivamente con etiquetas",
            "Encontrar patrones en datos sin etiquetas",
            "Eliminar todos los datos",
            "Reemplazar la base de datos"
        ],
        "answer": "Encontrar patrones en datos sin etiquetas",
        "explanation": "Busca estructuras o grupos sin una respuesta etiquetada."
    },
    {
        "question": "¿Cuál de estos algoritmos se usa para clustering?",
        "options": [
            "K-Means",
            "Linear Regression",
            "Logistic Regression",
            "Naive Bayes"
        ],
        "answer": "K-Means",
        "explanation": "K-Means agrupa datos según su similitud."
    },
    {
        "question": "¿Qué es el overfitting?",
        "options": [
            "Cuando el modelo no aprende nada",
            "Cuando memoriza demasiado el entrenamiento y generaliza mal",
            "Cuando faltan columnas",
            "Cuando siempre obtiene 50% de precisión"
        ],
        "answer": "Cuando memoriza demasiado el entrenamiento y generaliza mal",
        "explanation": "El overfitting aparece cuando el modelo se adapta demasiado a los datos de entrenamiento."
    },
    {
        "question": "¿Para qué se divide un dataset en entrenamiento y prueba?",
        "options": [
            "Para evaluar el modelo con datos no usados en el entrenamiento",
            "Para duplicar los datos",
            "Para eliminar la variable objetivo",
            "Para evitar usar algoritmos"
        ],
        "answer": "Para evaluar el modelo con datos no usados en el entrenamiento",
        "explanation": "El conjunto de prueba permite evaluar la generalización."
    },
    {
        "question": "¿Qué es una feature?",
        "options": [
            "La predicción final",
            "Una variable de entrada utilizada por el modelo",
            "El nombre del archivo Python",
            "Un error de programación"
        ],
        "answer": "Una variable de entrada utilizada por el modelo",
        "explanation": "Una feature es una variable de entrada, como edad, precio o cantidad."
    }
]

# Puntos necesarios para ganar
WIN_SCORE = 5

# ---------------------------------------------------------------------------
# Juego: todo corre en el navegador (HTML + canvas + JS) para poder disparar
# con el mouse. Streamlit solo lo muestra con components.html.
# ---------------------------------------------------------------------------
GAME_HTML = """
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: system-ui, -apple-system, Segoe UI, sans-serif; color: #fff; background: transparent; }
  #wrap { max-width: 760px; margin: 0 auto; }
  #hud { display: flex; justify-content: space-between; align-items: center; gap: 10px;
         background: #141b36; padding: 10px 14px; border-radius: 10px 10px 0 0; font-size: 15px; flex-wrap: wrap; }
  #bar { flex: 1; min-width: 120px; height: 10px; background: #2b3563; border-radius: 6px; overflow: hidden; }
  #barfill { height: 100%; width: 0%; background: linear-gradient(90deg, #ff9f43, #ff4d4d); transition: width .3s; }
  .btn { background: #2b3563; color: #fff; border: 0; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
  .btn:hover { background: #3a4680; }
  #question { background: #26305a; padding: 12px 14px; font-size: 18px; font-weight: 600; }
  #hint { background: #26305a; padding: 0 14px 10px; font-size: 13px; color: #b9c3ee; }
  canvas { display: block; width: 100%; background: linear-gradient(#0f1630, #1c2b5a); cursor: none; touch-action: none; border-radius: 0 0 10px 10px; }
  #feedback { min-height: 46px; margin-top: 8px; padding: 10px 14px; border-radius: 8px; font-size: 15px; display: none; }
  .ok { background: #1e7a46; display: block !important; }
  .bad { background: #a12b2b; display: block !important; }
  .info { background: #3a4680; display: block !important; }
</style>

<div id="wrap">
  <div id="hud">
    <span>🎯 <b id="score">0</b>/__WIN__</span>
    <div id="bar"><div id="barfill"></div></div>
    <span>Disparos: <b id="shots">0</b></span>
    <button class="btn" id="mute">🔊</button>
    <button class="btn" id="restart">🔄 Reiniciar</button>
  </div>
  <div id="question"></div>
  <div id="hint">Apunta con el mouse y haz clic sobre la alternativa correcta.</div>
  <canvas id="c" width="760" height="400"></canvas>
  <div id="feedback"></div>
</div>

<script>
const QUESTIONS = __QUESTIONS__;
const WIN = __WIN__;
const W = 760, H = 400;

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const elScore = document.getElementById('score');
const elShots = document.getElementById('shots');
const elFill = document.getElementById('barfill');
const elQuestion = document.getElementById('question');
const elFeedback = document.getElementById('feedback');

let deck = [], lastQ = null, q = null, targets = [];
let score = 0, shots = 0, locked = false, finished = false, muted = false;
let mouse = { x: W / 2, y: H / 2, inside: false };
let particles = [], holes = [], timer = null;

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function pickQuestion() {
  if (!deck.length) {
    deck = shuffle(QUESTIONS.slice());
    if (deck[deck.length - 1] === lastQ) deck.unshift(deck.pop());
  }
  lastQ = deck.pop();
  return lastQ;
}

function setupQuestion() {
  q = pickQuestion();
  elQuestion.textContent = '🎯 Objetivo: ' + q.question;
  const opts = shuffle(q.options.slice());
  const laneH = H / opts.length;
  targets = opts.map((text, i) => {
    const w = 250, h = Math.min(74, laneH - 12);
    const dir = Math.random() < 0.5 ? -1 : 1;
    return {
      text, w, h,
      x: Math.random() * (W - w),
      y: i * laneH + (laneH - h) / 2,
      vx: dir * (1.3 + Math.random() * 1.4),
      correct: text === q.answer,
      state: 'idle'
    };
  });
  holes = [];
  locked = false;
}

function updateHud() {
  elScore.textContent = score;
  elShots.textContent = shots;
  elFill.style.width = (score / WIN * 100) + '%';
}

function showFeedback(kind, msg) {
  elFeedback.className = kind;
  elFeedback.textContent = msg;
}

function resetGame() {
  clearTimeout(timer);
  score = 0; shots = 0; finished = false; particles = [];
  elFeedback.className = ''; elFeedback.textContent = '';
  setupQuestion();
  updateHud();
}

// ---------- sonido ----------
let audio = null;
function beep(freq, dur, type, vol) {
  if (muted) return;
  try {
    audio = audio || new (window.AudioContext || window.webkitAudioContext)();
    const o = audio.createOscillator(), g = audio.createGain();
    o.type = type || 'square'; o.frequency.value = freq; g.gain.value = vol || 0.05;
    o.connect(g); g.connect(audio.destination);
    g.gain.exponentialRampToValueAtTime(0.0001, audio.currentTime + dur);
    o.start(); o.stop(audio.currentTime + dur);
  } catch (e) {}
}

// ---------- efectos ----------
function burst(x, y, colors, n) {
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2, s = 2 + Math.random() * 5;
    particles.push({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 1, g: 0.15,
      life: 30 + Math.random() * 30, color: colors[Math.floor(Math.random() * colors.length)]
    });
  }
}

function confetti() {
  for (let i = 0; i < 6; i++) {
    particles.push({
      x: Math.random() * W, y: -10, vx: (Math.random() - 0.5) * 2, vy: 2 + Math.random() * 2, g: 0.02,
      life: 200, color: ['#ff4d4d', '#ffd166', '#06d6a0', '#4dabf7', '#f783ac'][Math.floor(Math.random() * 5)]
    });
  }
}

// ---------- input ----------
function getPos(e) {
  const r = canvas.getBoundingClientRect();
  return { x: (e.clientX - r.left) * (W / r.width), y: (e.clientY - r.top) * (H / r.height) };
}

canvas.addEventListener('pointermove', e => { const p = getPos(e); mouse.x = p.x; mouse.y = p.y; mouse.inside = true; });
canvas.addEventListener('pointerleave', () => { mouse.inside = false; });
canvas.addEventListener('pointerdown', e => {
  const p = getPos(e);
  mouse.x = p.x; mouse.y = p.y; mouse.inside = true;
  shoot(p.x, p.y);
});

function shoot(x, y) {
  if (locked || finished) return;
  shots++;
  beep(180, 0.12, 'sawtooth', 0.06);

  const t = targets.find(t => x >= t.x && x <= t.x + t.w && y >= t.y && y <= t.y + t.h);
  if (!t) {
    holes.push({ x, y });
    burst(x, y, ['#aab4e8'], 6);
    showFeedback('info', '💨 Disparo al aire. Apunta a una de las alternativas.');
    updateHud();
    return;
  }

  locked = true;
  if (t.correct) {
    score++;
    t.state = 'correct';
    burst(x, y, ['#ffd166', '#ff9f43', '#ff4d4d'], 40);
    beep(660, 0.25, 'triangle', 0.08);
    showFeedback('ok', '💥 ¡Impacto! Respuesta correcta. ' + q.explanation);
  } else {
    t.state = 'wrong';
    const right = targets.find(o => o.correct);
    right.state = 'correct';
    burst(x, y, ['#ff4d4d', '#888'], 20);
    beep(110, 0.35, 'sawtooth', 0.08);
    showFeedback('bad', '❌ Fallaste el objetivo. Respuesta correcta: ' + q.answer + '.');
  }
  updateHud();

  if (score >= WIN) {
    finished = true;
    showFeedback('ok', '🏆 ¡Victoria! Has conseguido ' + WIN + ' respuestas correctas. ¡Excelente puntería, agente de Machine Learning!');
    beep(880, 0.4, 'triangle', 0.08);
  } else {
    timer = setTimeout(() => {
      elFeedback.className = ''; elFeedback.textContent = '';
      setupQuestion();
    }, t.correct ? 1600 : 2600);
  }
}

document.getElementById('restart').addEventListener('click', resetGame);
document.getElementById('mute').addEventListener('click', e => {
  muted = !muted; e.target.textContent = muted ? '🔇' : '🔊';
});

// ---------- dibujo ----------
function wrapText(text, maxW) {
  const words = text.split(' '), lines = [];
  let line = '';
  for (const w of words) {
    const test = line ? line + ' ' + w : w;
    if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = w; }
    else line = test;
  }
  lines.push(line);
  return lines;
}

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

function drawTarget(t) {
  let fill = '#fff8e1', border = '#ff5252';
  if (t.state === 'correct') { fill = '#c8f7d4'; border = '#1e9e52'; }
  if (t.state === 'wrong')   { fill = '#ffd0d0'; border = '#c62828'; }

  ctx.fillStyle = fill; ctx.strokeStyle = border; ctx.lineWidth = 3;
  roundRect(t.x, t.y, t.w, t.h, 12); ctx.fill(); ctx.stroke();

  // diana a la izquierda
  const cx = t.x + 26, cy = t.y + t.h / 2;
  [16, 11, 6].forEach((r, i) => {
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = i % 2 === 0 ? '#ff5252' : '#ffffff'; ctx.fill();
  });

  // texto
  ctx.fillStyle = '#1b1b1b';
  ctx.font = '14px system-ui, sans-serif';
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  const lines = wrapText(t.text, t.w - 64);
  const lh = 17, startY = t.y + t.h / 2 - (lines.length - 1) * lh / 2;
  lines.forEach((l, i) => ctx.fillText(l, t.x + 50, startY + i * lh));
}

function drawCrosshair() {
  if (!mouse.inside) return;
  const { x, y } = mouse;
  ctx.strokeStyle = locked ? '#888' : '#ff4d4d'; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.arc(x, y, 14, 0, Math.PI * 2); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x - 22, y); ctx.lineTo(x - 6, y);
  ctx.moveTo(x + 6, y);  ctx.lineTo(x + 22, y);
  ctx.moveTo(x, y - 22); ctx.lineTo(x, y - 6);
  ctx.moveTo(x, y + 6);  ctx.lineTo(x, y + 22);
  ctx.stroke();
  ctx.fillStyle = '#ff4d4d';
  ctx.beginPath(); ctx.arc(x, y, 2, 0, Math.PI * 2); ctx.fill();
}

function update() {
  if (!locked && !finished) {
    const speed = 1 + score * 0.15; // se pone más difícil
    targets.forEach(t => {
      t.x += t.vx * speed;
      if (t.x < 0) { t.x = 0; t.vx *= -1; }
      if (t.x + t.w > W) { t.x = W - t.w; t.vx *= -1; }
    });
  }
  if (finished) confetti();
  particles.forEach(p => { p.x += p.vx; p.y += p.vy; p.vy += p.g; p.life--; });
  particles = particles.filter(p => p.life > 0);
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  // líneas de fondo
  ctx.strokeStyle = 'rgba(255,255,255,0.05)'; ctx.lineWidth = 1;
  for (let i = 1; i < 4; i++) {
    ctx.beginPath(); ctx.moveTo(0, i * H / 4); ctx.lineTo(W, i * H / 4); ctx.stroke();
  }

  targets.forEach(drawTarget);

  // agujeros de bala
  holes.forEach(h => {
    ctx.fillStyle = 'rgba(0,0,0,0.6)';
    ctx.beginPath(); ctx.arc(h.x, h.y, 4, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(h.x, h.y, 6, 0, Math.PI * 2); ctx.stroke();
  });

  particles.forEach(p => {
    ctx.globalAlpha = Math.min(1, p.life / 20);
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, 5, 5);
  });
  ctx.globalAlpha = 1;

  if (finished) {
    ctx.fillStyle = 'rgba(0,0,0,0.45)'; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = '#ffd166'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = 'bold 44px system-ui, sans-serif';
    ctx.fillText('🏆 ¡Victoria!', W / 2, H / 2 - 10);
    ctx.fillStyle = '#fff'; ctx.font = '18px system-ui, sans-serif';
    ctx.fillText('Dale a "Reiniciar" para jugar otra vez', W / 2, H / 2 + 35);
  }

  drawCrosshair();
}

function loop() { update(); draw(); requestAnimationFrame(loop); }

resetGame();
loop();
</script>
"""

game_html = (
    GAME_HTML
    .replace("__QUESTIONS__", json.dumps(QUESTIONS, ensure_ascii=False))
    .replace("__WIN__", str(WIN_SCORE))
)

st.title("🎯 ML Shooter Quiz")
st.write("Apunta con el mouse y haz clic sobre la alternativa correcta para dispararle.")

components.html(game_html, height=650, scrolling=False)

st.divider()
st.caption("El juego corre en el navegador (canvas + JavaScript) embebido dentro de Streamlit.")
