const size_rat = 7 / 10;
var SIZE = 1000 * size_rat;
var POSITION = [2000, -700, 3000];
var TIME_INTERVAL = 2;

let lastTime = 0;

function main(time, client) {
  const deltaTime = (time - lastTime) / 1000;
  lastTime = time;
  TIME_INTERVAL = (2 / 0.0167) * deltaTime;

  client.ctx_table.clearRect(0, 0, client.canvas_table.width, client.canvas_table.height);
  client.update();
  client.draw();
  requestAnimationFrame((t) => main(t, client));
}

function resizeCanvas() {
  const canvas = document.getElementById("myCanvas");
  if (!canvas) return;

  const body = document.body;
  const windowWidth = body.clientWidth;
  const windowHeight = body.clientHeight;
  const canvasAspectRatio = 10 / 6;
  const windowRatio = windowWidth / windowHeight;

  let scale;
  if (windowRatio > canvasAspectRatio) {
    scale = windowHeight / 742;
  } else {
    scale = windowWidth / ((10 * 742) / 6);
  }
  canvas.style.transform = `scaleX(0.841) scaleY(1) scale(${scale})`;
  canvas.style.transformOrigin = "top left";
  canvas.style.right = "0px";
  canvas.style.top = "0px";
}

window.addEventListener("resize", resizeCanvas);

async function createTestingRoom() {
  const response = await fetch("/matching_testing_area", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  window.dataFromBackend = await response.json();
}

window.addEventListener("beforeunload", async function () {
  await fetch("/delete_testing_room", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
});

async function initTestingArea() {
  await createTestingRoom();
  const client = new Game_Client();
  await client.init();
  resizeCanvas();
  new TestingLabPanel(client);
  main(0, client);
}

initTestingArea();
