



class Shelf{
  constructor(){
    this.all_items=[];
    this.send_request();
    

    

  }

  async send_request(){
    const request=new Request("/shop/items",{
      method:"POST",
    });
    const response=await fetch(request);
    const data=await response.json();
    console.log(data);
    this.create_list(data);
  }

  create_list(data){
    const element=document.getElementById("shop_list");
    for(let i=0; i<data.length; i+=2){
      const line=document.createElement("div");
      line.classList.add("shop_line");

      const shop_item_container=document.createElement("div");
      shop_item_container.classList.add("shop_item_container");
      for(let j=i; j<i+2 && j<data.length; j++){
        const item=new Item(data[j].name, data[j].price, data[j].pack_url, data[j].id);
        this.all_items.push(item);
        shop_item_container.appendChild(item.element);
      }
      line.appendChild(shop_item_container);

      const shop_bottom1=document.createElement("div");
      shop_bottom1.classList.add("shop_bottom1");
      const shop_bottom2=document.createElement("div");
      shop_bottom2.classList.add("shop_bottom2");
      line.appendChild(shop_bottom1);
      line.appendChild(shop_bottom2);
      element.appendChild(line);
    }
    this.initinal_pack_position();
    console.log(this.all_items);
  }
  update(){
    for(let i=0; i<this.all_items.length; i++){
      this.all_items[i].update();
    }
  }
  draw(camera){
    for(let i=0; i<this.all_items.length; i++){
      this.all_items[i].draw(camera);
    }
  }
  initinal_pack_position(){
    const POSITION_X=-0;
    const POSITION_Y=-0;
    const POSITION_Z=4400;
    const rate=1
    for(let i in this.all_items){
        this.all_items[i].pack.position=[POSITION_X,POSITION_Y,POSITION_Z];
        this.all_items[i].pack.angle_x=0;
        this.all_items[i].pack.angle_y=0;
    }
}
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("exit").addEventListener("click",()=>{
    window.location.href="/";
  });
});
  

const size_rat=7/10;
var SIZE=1000*size_rat;
var POSITION=[2500,-700,3000];
const shelf=new Shelf();
const camera=new Camera([0,0,-50])
function draw_picture(){
  shelf.update();
  shelf.draw(camera);
  requestAnimationFrame(draw_picture);
}
draw_picture();