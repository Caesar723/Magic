class Music{
    constructor(player_self,player_opponent){
        this.player_self=player_self
        this.player_opponent=player_opponent
        this.player_self.music=this
        this.player_opponent.music=this
        this.hit_path=[
            "webpages/audio/music_sorce/hit/hit1.mp3",
            "webpages/audio/music_sorce/hit/hit2.mp3",
            "webpages/audio/music_sorce/hit/hit3.mp3"
        ]
        this.missile_path=[
            "webpages/audio/music_sorce/missile/missile1.mp3",
            "webpages/audio/music_sorce/missile/missile2.mp3",
            "webpages/audio/music_sorce/missile/missile3.mp3"
        ]
        this.gamming_path=[
            "webpages/audio/music_sorce/gamming/gaming1.mp3",
            "webpages/audio/music_sorce/gamming/gaming2.mp3",
            "webpages/audio/music_sorce/gamming/gaming3.mp3"
        ]
        this.gamming_end_path=["webpages/audio/music_sorce/gamming/gaming_end1.mp3"]
        this.card_pic_path=["webpages/audio/music_sorce/card/pic.mp3"]
        this.card_send_path=["webpages/audio/music_sorce/card/send.mp3"]

        this.set_music()

        this.gamming_bgm=this.get_music("gamming")
        this.gamming_bgm.addEventListener('ended', this.changeBackgroundMusic.bind(this));
        this.start_flag=true
        console.log(this.gamming_bgm)
        
    }

    set_music(){
        this.hit=this.initinal_list(this.hit_path)
        this.missile=this.initinal_list(this.missile_path)
        this.gamming=this.initinal_list(this.gamming_path)
        this.gamming_end=this.initinal_list(this.gamming_end_path)
        this.card_pic=this.initinal_list(this.card_pic_path)
        this.card_send=this.initinal_list(this.card_send_path)

        this.dict_effect={
            "hit":this.hit,
            "missile":this.missile,
            "card_pic":this.card_pic,
            "card_send":this.card_send,
            "gamming":this.gamming,
            "gamming_end":this.gamming_end,
        }
    }
    initinal_list(list){
        const result=[]
        for (let path of list){
            const audio=new Audio(path);
            audio.volume = 0.3;
            result.push(audio);
        }
        return result;
    }

    get_music(name){
        if (name in this.dict_effect){
            console.log(this.dict_effect[name])
            const music =this.dict_effect[name][Math.floor(Math.random() * this.dict_effect[name].length)];
            console.log(music)
            return music
        }
        
    }
    play_music_effect(name){
        const music=this.get_music(name)
        music.currentTime = 0;
        music.play()
    }
    

    fadeVolumeIn(audioElement, duration) {
        audioElement.volume = 0;
        let volume = 0;
        const step = 0.1;
        const interval = duration / (1 / step);

        const fadeIn = setInterval(() => {
            volume += step;
            if (volume >= 1) {
                volume = 1;
                clearInterval(fadeIn);
            }
            audioElement.volume = volume;
        }, interval);
    }
    changeBackgroundMusic(){
        if (this.player_self.player_life_ring.life<=5 || this.player_opponent.player_life_ring.life<=5){
            this.gamming_bgm=this.get_music("gamming_end")
        }
        else{
            this.gamming_bgm=this.get_music("gamming")
        }
        
        this.gamming_bgm.addEventListener('ended', this.changeBackgroundMusic.bind(this));
        setTimeout(this.play_bgm.bind(this),4000)
    }
    play_bgm(){
        // console.log(this.gamming_bgm)
        // this.gamming_bgm.currentTime = 0;
        // this.gamming_bgm.play();
        // this.fadeVolumeIn(this.gamming_bgm, 7000);
    }
    
}