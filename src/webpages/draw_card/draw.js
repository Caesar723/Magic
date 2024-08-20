// 获取Canvas元素并设置其宽度和高度

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('webpages/service-worker.js').then(function(registration) {
        console.log('Service Worker registered with scope:', registration.scope);
    });
}

function set_Listener(){
    const draw = document.getElementById('exit');
    draw.addEventListener('click',  function () {
            window.location.href = '/';
    });
}

set_Listener();

var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
canvas.width = 1470;
canvas.height = 742;
// 设置正方形的位置和大小
console.log(window.height)
console.log(window.innerWidth)

// 在此处添加你的Canvas绘制代码
function draw_pack_store_space(){
    var size = Math.min(canvas.width, canvas.height); // 正方形的边长
    var x = (canvas.width - size) / 2; // 正方形左上角的x坐标
    var y = (canvas.height - size) / 2; // 正方形左上角的y坐标
    var rectWidth = canvas.width * 0.2; 

    // 绘制半透明白色矩形
    ctx.fillStyle = "rgba(255, 255, 255, 0.5)"; // 半透明的白色
    ctx.fillRect(canvas.width-rectWidth, 0, rectWidth, canvas.height);
}
// 定义退出函数


function exitCanvas() {
    // 在此处添加退出逻辑，可以是隐藏Canvas或其他操作
}

const size_rat=7/10;
var SIZE=1000*size_rat;
var POSITION=[2000,-700,3000];

const camera=new Camera([0,0,-50])

const frame_generator=new Card_frame()
const paras=[
    ["blue","Caesar","Creature","Uncommon","nothing nothing","cards/creature/Spectral Harbinger/image.jpg"],
    ["red","Caesar","Creature","Mythic_Rare","nothing nothing","cards/creature/Eternal Phoenix/image.jpg"],
    ["black","Caesar","Creature","Common","nothing nothing","cards/creature/Nyxborn Serpent/image.jpg"],
    ["gold","Caesar","Creature","Rare","nothing nothing","cards/creature/Luminous Guardian/image.jpg"],
    ["green","Caesar","Creature","Mythic_Rare","nothing nothing","cards/creature/Verdant Wyrm/image.jpg"]
]
// const card_1=new Creature(4,5.62,[0,0,40],3,frame_generator.generate_card(...paras[0]),"2UU",10,3)
// const card_2=new Creature(4,5.62,[-60,0,40],3,frame_generator.generate_card(...paras[1]),"20RRRRRRRR",2,10)
// const card_3=new Card(4,5.62,[-35,0,40],3,frame_generator.generate_card(...paras[2]),"BBBB")
// const card_4=new Card(4,5.62,[-10,0,40],3,frame_generator.generate_card(...paras[3]),"WWWWWWW")
// const card_5=new Card(4,5.62,[30,0,40],3,frame_generator.generate_card(...paras[4]),"G")
// card_1.angle_x=0
const draw_card_system= new Draw_card(camera,ctx);
draw_card_system.set_listener(canvas);
//##functions##//

function draw_picture(){
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'white';
    
    // card_1.update()
    // card_2.update()
    // card_3.update()
    // card_4.update()
    // card_5.update()
    draw_card_system.update()
    var startTime = performance.now();
    draw_pack_store_space()
    
    // card_2.draw(camera)
    // card_3.draw(camera)
    // card_4.draw(camera)
    // card_5.draw(camera)
    

   
    // card_1.draw(camera)
    draw_card_system.draw()
    var endTime = performance.now();
    var elapsedTime = endTime - startTime;

    //console.log("代码执行耗时：" + elapsedTime + " 毫秒");     
    //block.angle_z=block.angle_z+0.01;
    //block.angle_y=block.angle_y+0.01;
    //card_1.angle_y=card_1.angle_y+0.02
    //card_1.size=card_1.size+0.001
    //block.angle_x=block.angle_x+0.01;
    
    // b.angle_x=b.angle_x+0.01
    
    requestAnimationFrame(draw_picture);
    
}
draw_picture();