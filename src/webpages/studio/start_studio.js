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
function main(time){

  const deltaTime = (time - lastTime) / 1000;
  
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
  //console.timeEnd('game');
  
  
  
  requestAnimationFrame(main);
}

const canvas = document.getElementById('myCanvas');


function resizeCanvas() {
  const body = document.body;
  
  const canvasAspectRatio = 10/6;
  const windowWidth = body.clientWidth;
  const windowHeight = body.clientHeight;
  const windowRatio = windowWidth / windowHeight;
  //console.log(windowWidth,windowHeight,canvas.width,canvas.height)

  let scale;

  if (windowRatio > canvasAspectRatio) {
      // 如果窗口比较宽，基于高度来设置缩放
      scale = windowHeight / 742;
  } else {
      // 如果窗口比较窄，基于宽度来设置缩放
      scale = windowWidth / (10*742/6);
  }
  scale/=2
  canvas.style.transform = `scaleX(0.841) scaleY(1) scale(${scale})`;
  canvas.style.transformOrigin = 'top left';
  canvas.style.left = `${0}px`;
  canvas.style.top = `${0}px`;

  const adding_card=document.getElementById("adding_card")
  
  adding_card.style.height=`${windowHeight-scale*canvas.height}px`
  adding_card.style.top = `${scale*canvas.height}px`;
}

// 监听窗口大小变化事件
window.addEventListener('resize', resizeCanvas);

// 初始化canvas大小
resizeCanvas();

main()