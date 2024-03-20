class Table{
    constructor(){
        this.canvas = document.getElementById("myCanvas");
        this.ctx = this.canvas.getContext("2d");
        this.canvas.width = 1470;
        this.canvas.height = 742;
        this.time_interval=0.02//每隔0.02秒进行一次刷新
        this.table_graph=new Table_graph(2,1,1,[0,0,0],10,"webpages/image_source/game/background.jpg");
        
        this.camera=new Camera([0,-30,-7*0.7])
        this.camera.angle_y=1.34
        this.camera.angle_x=0
    }
    update(){
        this.table_graph.update(this.camera)
        
        
    }
    draw(){
        this.table_graph.draw(this.camera,this.canvas,this.ctx)
    }

    draw_table(){

    }
}