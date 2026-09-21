const size_rat = 7 / 10;
var SIZE = 1000 * size_rat;
var POSITION = [2000, -700, 3000];
var TIME_INTERVAL = 2;

class ReplayClock {
  constructor() {
    this.time = 0;
    this.speed = 1;
    this.tasks = [];
  }

  setSpeed(speed) {
    this.speed = [1, 2, 4, 8].includes(speed) ? speed : 1;
  }

  reset() {
    this.time = 0;
    this.tasks = [];
  }

  wait(delay, callback) {
    this.tasks.push({ at: this.time + delay, callback });
  }

  advance(elapsed) {
    this.time += elapsed * 1000 * this.speed;
    const due = this.tasks.filter((task) => task.at <= this.time);
    this.tasks = this.tasks.filter((task) => task.at > this.time);
    due.forEach((task) => task.callback());
  }
}

window.replayClock = new ReplayClock();
const client = new Game_Client();

let lastTime = performance.now();
let animationFrame = null;

function renderFrame(elapsed) {
  TIME_INTERVAL = (2 / 0.0167) * elapsed * window.replayClock.speed;
  client.ctx_table.clearRect(0, 0, client.canvas_table.width, client.canvas_table.height);
  client.update();
  client.draw();
}

function main(time) {
  animationFrame = null;
  const deltaTime = Math.min((time - lastTime) / 1000, 0.1);
  lastTime = time;

  if (client.game_player.pause_flag || client.game_player.isFinished()) {
    return;
  }

  // One update and draw per screen frame keeps every visible animation frame
  // in order.  Only the replay clock and animation time are scaled.
  window.replayClock.advance(deltaTime);
  renderFrame(deltaTime);
  animationFrame = requestAnimationFrame(main);
}

window.startReplayRender = () => {
  if (animationFrame === null) {
    lastTime = performance.now();
    animationFrame = requestAnimationFrame(main);
  }
};

window.stopReplayRender = () => {
  if (animationFrame !== null) {
    cancelAnimationFrame(animationFrame);
    animationFrame = null;
  }
};

const canvas = document.getElementById("myCanvas");

function resizeCanvas() {
  const canvasAspectRatio = 10 / 6;
  const windowWidth = document.body.clientWidth;
  const windowHeight = document.body.clientHeight;
  const scale = windowWidth / windowHeight > canvasAspectRatio
    ? windowHeight / 742
    : windowWidth / (10 * 742 / 6);

  canvas.style.transform = `scaleX(0.841) scaleY(1) scale(${scale})`;
  canvas.style.transformOrigin = "top left";
  canvas.style.left = `${(windowWidth - (10 * 742 / 6) * scale) / 2}px`;
  canvas.style.top = `${windowHeight - 742 * scale}px`;
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
