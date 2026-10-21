if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('webpages/service-worker.js').then(function(registration) {
      console.log('Service Worker registered with scope:', registration.scope);
  });
}
const size_rat=7/10;
var SIZE=1000*size_rat;
var POSITION=[2000,-700,3000];
var TIME_INTERVAL=2
const client = new Game_Client();

let lastTime = 0;
let animationFrame = 0;
function main(time){
  animationFrame = 0;
  if (document.hidden || !document.hasFocus()) { lastTime = 0; return; }
  const deltaTime = lastTime ? Math.min((time - lastTime) / 1000, .05) : 1 / 60;
  
  lastTime = time;

  TIME_INTERVAL=(2/0.0167)*deltaTime
  
  //await client.init();
  //while (true){
  client.ctx_table.clearRect(0, 0, client.canvas_table.width, client.canvas_table.height);
  //client.main_ctx.clearRect(0, 0, client.main_canvas.width, client.main_canvas.height);
  //console.time('update');
  client.update()
  //console.timeEnd('update');
  //console.time('game');
  client.draw()
  client.table.renderer?.render();
  //console.timeEnd('game');
  
  
  
  animationFrame = requestAnimationFrame(main);
}

function updatePlayback() {
  cancelAnimationFrame(animationFrame);
  animationFrame = 0;
  lastTime = 0;
  if (!document.hidden && document.hasFocus()) animationFrame = requestAnimationFrame(main);
}
window.addEventListener('blur', updatePlayback);
window.addEventListener('focus', updatePlayback);
document.addEventListener('visibilitychange', updatePlayback);
window.addEventListener('pagehide', () => cancelAnimationFrame(animationFrame));

const canvas = document.getElementById('myCanvas');


function resizeCanvas() {
  client.table.resizeViewport(canvas.parentElement);
}

new ResizeObserver(resizeCanvas).observe(canvas.parentElement);
window.visualViewport?.addEventListener('resize', resizeCanvas);

// 监听窗口大小变化事件
window.addEventListener('resize', resizeCanvas);

// 初始化canvas大小
resizeCanvas();

updatePlayback();
