const audio = document.getElementById('background-music');
const audioSource = document.getElementById('audio-source');
const audioFiles = ['music_sorce/hall/hall1.mp3', 'music_sorce/hall/hall2.mp3', 'music_sorce/hall/hall3.mp3'];

// 恢复音频播放状态
if (localStorage.getItem('audioTime')) {
    audio.currentTime = localStorage.getItem('audioTime');
}

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
    audio.play();
    fadeVolumeIn(audio, 3000); // 音量从小到大，渐变时间为3秒
}

// 当音频播放结束时切换背景音乐
audio.addEventListener('ended', changeBackgroundMusic);



// audio.load();
// audio.play();
// 初始化时音量渐变


console.log("play")