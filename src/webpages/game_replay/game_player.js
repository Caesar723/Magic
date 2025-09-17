





class Game_Player{
    constructor(message_processor,room){
        this.datas=[]
        this.check_point_datas=[]
        this.data_index=-1
        this.wait_flag=false
        this.pause_flag=false
        this.length=0
        this.message_processor=message_processor
        this.room=room
        this.current_timeout=null
        this.init_listen()
    }

    init_listen(){
        const dropZone=document.getElementById("read_mode")
        const playBtn = document.getElementById("play_button");
        const playIcon = document.getElementById("play_icon");
        const progressBar = document.getElementById("progress_bar");
        const progressValue = document.getElementById("progress_value");
        const playZone=document.getElementById("play_mode")
        dropZone.style.display="block"
        playZone.style.display="none"
        
        

        // 播放/暂停切换
        playBtn.addEventListener("click", async() => {
            if (!this.pause_flag) {
                this.pause_flag = true;
                playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>'; // pause 图标
                
            } else {
                this.pause_flag = false;
                
                playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>'; // play 图标
            }
        });

        // 拖动进度条
        progressBar.addEventListener("input", async () => {
            progressValue.textContent = progressBar.value;
            this.change_data_index(parseInt(progressBar.value));
        });

        dropZone.addEventListener("dragover", (e) => {
            
            e.preventDefault();
            dropZone.classList.add("dragover");
        });
        dropZone.addEventListener("dragover", (e) => {
            
            e.preventDefault();
            dropZone.classList.add("dragover");
        });
        
        dropZone.addEventListener("dragleave", () => {
            
            dropZone.classList.remove("dragover");
        });
        
        // 放下文件
        dropZone.addEventListener("drop", (e) => {
            
            e.preventDefault();
            dropZone.classList.remove("dragover");
            if (e.dataTransfer.files.length) {
                this.handleFile(e.dataTransfer.files[0]);
                const dropZone=document.getElementById("read_mode")
                const playZone=document.getElementById("play_mode")
                dropZone.style.display="none"
                playZone.style.display="block"
            }
        });
        document.getElementById("fileInput").addEventListener("change", async (event) => {
            this.handleFile(event.target.files[0]);
        });
    }

    async handleFile(file){
        //const file = event.target.files[0];
        if (!file) return;
    
        // 1. 读取文件为 ArrayBuffer
        const arrayBuffer = await file.arrayBuffer();
    
        // 2. 转换为 Uint8Array
        const uint8Array = new Uint8Array(arrayBuffer);
    
        // 3. 解压 (zlib inflate)
        let decompressed;
        try {
            decompressed = pako.inflate(uint8Array);
        } catch (err) {
            console.error("解压失败:", err);
            return;
        }
    
        // 4. Uint8Array 转字符串
        const decoder = new TextDecoder("utf-8");
        const jsonString = decoder.decode(decompressed);
    
        // 5. 解析 JSON
        const data = JSON.parse(jsonString);
        console.log(data)
    
        this.load_datas(data)
    }

    async load_datas(datas){
        
        this.room.self_player.name=datas.basic_info.self_name
        this.room.oppo_player.name=datas.basic_info.opponent_name
        this.datas=datas.game_records
        this.check_point_datas=datas.check_point_datas
        this.data_index=0
        this.wait_flag=false
        this.pause_flag=false
        this.length=datas.game_records.length
        const progressBar = document.getElementById("progress_bar");
        progressBar.max=this.length
        progressBar.value=0
        const progressValue = document.getElementById("progress_value");
        progressValue.textContent = this.data_index;
    }

    update(){
        if (this.length==0 || this.data_index==-1){
            return
        }
        if (this.data_index>=this.length){
            return
        }
        if (this.pause_flag){
            return
        }
        if (this.wait_flag){
            return
        }
        
        let time=0;
        if (this.data_index>=this.length-2){
            //time=1;
            this.wait_flag=false
        }
        else{
            time=this.datas[this.data_index+1].game_times
        }

        time=Math.max(time,1)
        console.log(this.datas[this.data_index])
        this.message_processor.extractParts(this.datas[this.data_index].game_records)
        this.wait_flag=true
        this.current_timeout=setTimeout(() => {
            this.wait_flag=false
            this.data_index++
            const progressValue = document.getElementById("progress_value");
            progressValue.textContent = this.data_index;
            const progressBar = document.getElementById("progress_bar");
            progressBar.value=this.data_index;
        }, time*1000)

    }

    async play(){
        this.pause_flag=false
    }
    async pause(){
        this.pause_flag=true
    }
    
    async change_data_index(index){
        
        if (index>=this.length){
            return
        }
        if (this.current_timeout){
            clearTimeout(this.current_timeout)
            this.current_timeout=null
            
        }
        this.wait_flag=true
        const self_player=this.room.self_player
        const oppo_player=this.room.oppo_player
        self_player.cards=[]
        
        oppo_player.cards=[]
        this.room.table.self_battlefield=[]
        this.room.table.opponent_battlefield=[]
        this.room.table.self_landfield=[]
        this.room.table.opponent_landfield=[]
        this.room.table.actions=[]

        let restore_index=0;
        for (let i=0;i<this.check_point_datas.length;i++){
            
            const check_index=this.check_point_datas[i].index
            if (check_index<=index){
                restore_index=i
            }
        }

       
        this.data_index=this.check_point_datas[restore_index+1].index
        console.log(this.check_point_datas[restore_index].game_ini_records)
        console.log(this.data_index)
        this.message_processor.extractParts(this.check_point_datas[restore_index].game_ini_records)
        
        this.current_timeout=setTimeout(() => {
            this.wait_flag=false
            //this.data_index++
            const progressValue = document.getElementById("progress_value");
            progressValue.textContent = this.data_index;
            const progressBar = document.getElementById("progress_bar");
            progressBar.value=this.data_index;
        }, 1000)
    }
    
}