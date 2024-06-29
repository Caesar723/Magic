window.addEventListener("message", function(event) {
    if (event.data === "saveAudioTime") {
        const iframe = document.getElementById("audio-frame");
        iframe.contentWindow.postMessage("getAudioTime", "*");
    }
});
const iframe = document.getElementById('audio-frame');
iframe.onload = () => {
    // 获取 iframe 的内容窗口和文档
    const iframeContentWindow = iframe.contentWindow;
    const iframeDocument = iframeContentWindow.document;

    const audio = iframeDocument.getElementById('background-music');
    const audioSource = iframeDocument.getElementById('audio-source');
    const audioFiles = ['music_sorce/hall/hall1.mp3', 'music_sorce/hall/hall3.mp3'];

    // 恢复音频播放状态
    // audio.addEventListener('canplay', () => {
    //     audio.currentTime = localStorage.getItem('audioTime');
        
    // });
    
    // if (localStorage.getItem('audioTime')!=0) {
    //     console.log(localStorage.getItem('audioTime'))
        
    //     audio.currentTime = localStorage.getItem('audioTime');
    //     //audio.play()
    //     console.log("play")
        
    // }
    
    document.body.addEventListener('click',click_event );
    
    // 定时保存音频播放状态
    setInterval(() => {
        localStorage.setItem('audioTime', audio.currentTime);
    }, 1000);

    // 音量渐变函数
    function fadeVolumeIn(audioElement, duration) {
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

    // 切换背景音乐
    function changeBackgroundMusic() {
        const nextAudio = audioFiles[Math.floor(Math.random() * audioFiles.length)];

        audioSource.src = nextAudio;
        audio.load();
        setTimeout(play_audio,4000)
    }

    // 当音频播放结束时切换背景音乐
    audio.addEventListener('ended', changeBackgroundMusic);

    function play_audio(){
        console.log("play")
        audio.play();
        fadeVolumeIn(audio, 7000);
    }
    
    // 在 iframe 内部添加鼠标移动事件监听器
    function click_event(){
        setTimeout(play_audio,3000)
        document.body.removeEventListener('click',click_event)
    }
    
    
};