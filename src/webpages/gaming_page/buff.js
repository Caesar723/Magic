class Buff{
    constructor(buff_name,image_url,content,id){
        this.image_url=image_url
        this.content=content
        this.id=id
        this.name=buff_name
        this.img = new Image();
        this.img.src =this.image_url;
        this.canvas=document.createElement('canvas');
        this.img.onload=() =>{
            this.initinal_canvas()
        }
    }
    initinal_canvas(){
        this.canvas.width=200
        this.canvas.height=50

        const ctx=this.canvas.getContext('2d');
        

        // 绘制一个白色的边框矩形
        // 参数：x, y, width, height
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.drawImage(this.img, 0, 0, this.canvas.height, this.canvas.height);

        const max_width=this.canvas.width-this.canvas.height
        // 设置字体
        ctx.font = '24px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'rgba(0, 0, 0, 1)';

        const name_text=this.drawTextWithEllipsis(ctx,this.name,max_width)
        const x = ((this.canvas.width-this.canvas.height) / 2)+this.canvas.height;
        const y_n = this.canvas.height / 4;
        ctx.fillText(name_text, x, y_n);
        

        ctx.font = '16px Arial';
        const y_c = 3*this.canvas.height / 4;
        const content_text=this.drawTextWithEllipsis(ctx,this.content,max_width)
        ctx.fillText(content_text, x, y_c);

    }
    drawTextWithEllipsis(ctx, text, maxWidth) {
        const ellipsis = '...';
        // 初始文本
        let displayText = text;
    
        // 测量完整文本的宽度
        let textWidth = ctx.measureText(displayText).width;
    
        // 如果文本宽度超过了最大宽度
        if (textWidth > maxWidth) {
            // 添加省略号的宽度
            const ellipsisWidth = ctx.measureText(ellipsis).width;
            
            // 循环裁剪文本，直到文本宽度小于最大宽度
            while (textWidth + ellipsisWidth > maxWidth && displayText.length > 0) {
                displayText = displayText.slice(0, -1);
                textWidth = ctx.measureText(displayText).width;
            }
    
            // 添加省略号
            displayText += ellipsis;
        }
    
        return displayText
    }
    draw(position,ctx,canvas){
        console.log(position)
        ctx.drawImage(this.canvas, ...position, this.canvas.width, this.canvas.height);

    }
}