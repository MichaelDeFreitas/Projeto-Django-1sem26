/* ================= JAVASCRIPT (script.js) ================= */

let totalSeconds = Number(localStorage.getItem('studyflow_timer_seconds') || 0);
let interval = null;

function getCookie(name) {
  let cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;

  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function setMessage(text) {
  const message = document.getElementById('timer-message');

  if (message) {
    message.innerText = text;
  }
}

function renderTimer() {
  const timer = document.getElementById('timer');

  if (timer) {
    timer.innerText = formatTime(totalSeconds);
  }
}

function updateTimer() {
  totalSeconds++;
  localStorage.setItem('studyflow_timer_seconds', totalSeconds);
  renderTimer();
}

function startTimer() {
  clearInterval(interval);
  interval = setInterval(updateTimer, 1000);
  setMessage('Temporizador em andamento...');
}

function stopTimer() {
  clearInterval(interval);

  if (totalSeconds > 0) {
    setMessage('Temporizador pausado. Você pode continuar ou salvar a sessão.');
  }
}

function resetTimer() {
  clearInterval(interval);
  totalSeconds = 0;
  localStorage.removeItem('studyflow_timer_seconds');
  renderTimer();
  setMessage('');
}

function saveSession() {
  if (totalSeconds < 60) {
    setMessage('Estude pelo menos 1 minuto antes de salvar.');
    return;
  }

  stopTimer();

  const formData = new FormData();
  formData.append('segundos', totalSeconds);

  fetch('/salvar-sessao/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: formData
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        throw new Error(data.erro || 'Erro ao salvar sessão.');
      }

      setMessage(`${data.mensagem} Tempo registrado: ${data.tempo_formatado}.`);
      totalSeconds = 0;
      localStorage.removeItem('studyflow_timer_seconds');
      renderTimer();

      setTimeout(() => {
        window.location.reload();
      }, 900);
    })
    .catch(error => {
      setMessage(error.message);
    });
}

renderTimer();

const themeToggle = document.getElementById('themeToggle');

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
  });
}
