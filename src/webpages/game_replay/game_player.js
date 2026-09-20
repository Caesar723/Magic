





class Game_Player{
    constructor(message_processor,room){
        this.datas=[]
        this.check_point_datas=[]
        this.reward_datas=[]
        this.data_index=-1
        this.wait_flag=false
        this.pause_flag=false
        this.length=0
        this.message_processor=message_processor
        this.room=room
        this.current_timeout=null
        this.set_replay_records()
        this.init_listen()
    }
    parseFilename(file) {
        const base = file.replace(/\.mgf$/, "");
        const parts = base.split("_");
        const self_name = parts[0];
        const opponent_name = parts[1];
        const datetime = parts.slice(2).join("_");
        return { self_name, opponent_name, datetime };
    }

    async set_replay_records(){
        try{
        const response=await fetch(
            `/get_replay_records`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            }
        );
        const data=await response.json();
        console.log(data)
        const replayButton=document.getElementById("expand_button")
        replayButton.addEventListener("click", () => {
            const myCanvas=document.getElementById("myCanvas")
            const replayZone=document.getElementById("replay_list")
            const overlay=document.getElementById("overlay")
            myCanvas.classList.toggle('active');
            replayZone.classList.toggle('active');
            overlay.classList.toggle('active');
        })
        for ( const file_name of data.files){
            const { self_name, opponent_name, datetime } = this.parseFilename(file_name);
            const record_card=document.createElement("div")
            record_card.classList.add("record_card")
            record_card.innerHTML=`
<div class="record_info">
      <h2 id="player">${self_name}</h2>
      <h2 id="opponent">${opponent_name}</h2>
      <div class="record_time" id="time">${datetime}</div>
</div>
<div class="record_buttons">
      <button class="record_load" >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zm7-18l-7 7h4v6h6v-6h4l-7-7z"/></svg>
      </button>
      <a href="/download/game_records/${file_name}" download class="record_download">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5 20h14v-2H5v2zm7-18v12l5-5h-3V4h-4v5H7l5 5z"/></svg>
      </a>
</div>
            `
            record_card.querySelector(".record_load").addEventListener("click", async () => {
                console.log(file_name)
                const response = await fetch(`/download/game_records/${file_name}`);
                const blob = await response.blob();

                // 转成 File 对象，补齐 name / lastModified
                const file = new File([blob], file_name, { type: blob.type });
                if (await this.handleFile(file)) this.setReplayMode(true);
            })
            
            const replayZone=document.getElementById("replay_list")
            replayZone.appendChild(record_card)
        }
        
        }
        catch(error){
            console.error("获取回放记录失败:", error);
            this.replay_records=[];
        }
    }

    init_listen(){
        const dropZone=document.getElementById("read_mode")
        const playBtn = document.getElementById("play_button");
        const playIcon = document.getElementById("play_icon");
        const progressBar = document.getElementById("progress_bar");
        const progressValue = document.getElementById("progress_value");
        const playZone=document.getElementById("play_mode")
        const overlay = document.getElementById("overlay");
        this.setReplayMode = (loaded) => {
            dropZone.style.display = loaded ? "none" : "flex";
            playZone.style.display = loaded ? "flex" : "none";
            overlay.classList.toggle("replay-loading", !loaded);
            if (loaded) {
                overlay.classList.remove("active");
                document.getElementById("myCanvas").classList.remove("active");
                document.getElementById("replay_list").classList.remove("active");
            }
        };
        this.setReplayMode(false);

        // 播放/暂停切换
        playBtn.addEventListener("click", async() => {
            if (!this.pause_flag) {
                this.pause_flag = true;
                playIcon.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>'; // pause 图标
                
            } else {
                this.pause_flag = false;
                window.startReplayRender();
                playIcon.innerHTML = '<path d="M8 5v14l11-7z"/>'; // play 图标
            }
        });

        const fileInput = document.getElementById("fileInput");
        const loadReplay = async (file) => {
            if (await this.handleFile(file)) {
                this.setReplayMode(true);
            }
        };

        // 拖动进度条
        progressBar.addEventListener("input", async () => {
            progressValue.textContent = progressBar.value;
            this.change_data_index(parseInt(progressBar.value));
        });

        dropZone.addEventListener("dragover", (e) => {
            
            e.preventDefault();
            dropZone.classList.add("dragover");
        });
        dropZone.addEventListener("dragleave", () => {
            
            dropZone.classList.remove("dragover");
        });
        
        dropZone.addEventListener("drop", (e) => {
            
            e.preventDefault();
            dropZone.classList.remove("dragover");
            loadReplay(e.dataTransfer.files[0]);
        });
        fileInput.addEventListener("change", (event) => {
            loadReplay(event.target.files[0]);
        });
    }

    async handleFile(file){
        try {
            if (!file || !file.name.endsWith(".mgf")) {
                throw new Error("Please choose a .mgf replay file.");
            }
            const data = JSON.parse(new TextDecoder().decode(pako.inflate(new Uint8Array(await file.arrayBuffer()))));
            await this.load_datas(data);
            return true;
        } catch (error) {
            console.error("Could not load replay:", error);
            alert(error.message || "Could not read this replay file.");
            return false;
        }
    }

    async fetchFile(filename) {
        
        try{
            const response= await fetch(`/download/game_records/${filename}`);
            const blob = await response.blob();
      
            // 转成 File 对象，补齐 name / lastModified
            const file = new File([blob], filename, { type: blob.type });
            return file;
        }
        catch(error){
            console.error("下载失败:", error);
            return;
        }
        
    }

    async load_datas(datas){
        
        this.room.self_player.name=datas.basic_info.self_name
        this.room.oppo_player.name=datas.basic_info.opponent_name
        this.datas=datas.game_records
        this.check_point_datas=datas.check_point_datas
        this.reward_datas=datas.reward_datas
        this.data_index=0
        this.wait_flag=false
        this.pause_flag=false
        this.length=datas.game_records.length
        window.startReplayRender();
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
        this.show_game_reward(this.data_index)
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

    isFinished(){
        return this.length === 0 || this.data_index >= this.length;
    }


    show_game_reward(index){
        let reward_info=null;
        for (let i=0;i<this.reward_datas.length;i++){
            if (this.reward_datas[i].index<=index){
                reward_info=this.reward_datas[i]
                
            }
        }
        
        if (reward_info==null){
            return
        }
        const game_info=document.getElementById("game_info_reward")
        let creatures_self_old = reward_info.old_value.score_battle_self_creatures.map(num => num.toFixed(4)); 
        let creatures_self_new = reward_info.new_value.score_battle_self_creatures.map(num => num.toFixed(4)); 
        let creatures_oppo_old = reward_info.old_value.score_battle_oppo_creatures.map(num => num.toFixed(4)); 
        let creatures_oppo_new = reward_info.new_value.score_battle_oppo_creatures.map(num => num.toFixed(4)); 
        game_info.innerHTML=`
        <div class="game_info_reward">reward:${reward_info.reward.toFixed(4)}</div>
        <div class="game_info_reward">score_life_self:${reward_info.old_value.score_life_self.toFixed(4)}->${reward_info.new_value.score_life_self.toFixed(4)}</div>
        <div class="game_info_reward">score_oppo_self:${reward_info.old_value.score_oppo_self.toFixed(4)}->${reward_info.new_value.score_oppo_self.toFixed(4)}</div>
        <div class="game_info_reward">score_mana:${reward_info.old_value.score_mana.toFixed(4)}->${reward_info.new_value.score_mana.toFixed(4)}</div>
        <div class="game_info_reward">score_hand:${reward_info.old_value.score_hand.toFixed(4)}->${reward_info.new_value.score_hand.toFixed(4)}</div>
        <div class="game_info_reward">score_battle_self:${reward_info.old_value.score_battle_self.toFixed(4)}->${reward_info.new_value.score_battle_self.toFixed(4)}</div>
        <div class="game_info_reward">score_battle_oppo:${reward_info.old_value.score_battle_oppo.toFixed(4)}->${reward_info.new_value.score_battle_oppo.toFixed(4)}</div>
        <div class="game_info_reward">score_battle_self_creatures:${creatures_self_old.join(",")}->${creatures_self_new.join(",")}</div>
        <div class="game_info_reward">score_battle_oppo_creatures:${creatures_oppo_old.join(",")}->${creatures_oppo_new.join(",")}</div>
        
        `
        const game_act_message=document.getElementById("game_info_action")
        game_act_message.innerHTML=`
        ${reward_info.action}
        `

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
        window.startReplayRender();
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
        this.show_game_reward(this.data_index)
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
