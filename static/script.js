/* ================= JAVASCRIPT (script.js) ================= */

let seconds = 0;
let minutes = 0;
let hours = 0;
let interval;

function updateTimer() {
  seconds++;

  if(seconds == 60) {
    seconds = 0;
    minutes++;
  }

  if(minutes == 60) {
    minutes = 0;
    hours++;
  }

  document.getElementById('timer').innerText =
    `${String(hours).padStart(2,'0')}:${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}`;
}

function startTimer() {
  clearInterval(interval);
  interval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  clearInterval(interval);
}

function resetTimer() {
  clearInterval(interval);
  seconds = 0;
  minutes = 0;
  hours = 0;

  document.getElementById('timer').innerText = '00:00:00';
}

const themeToggle = document.getElementById('themeToggle');

if(themeToggle){
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
    });
}