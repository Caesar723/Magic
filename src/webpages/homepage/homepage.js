if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/webpages/service-worker.js').catch(()=>{});
}
async function get_currency() {
    try {
        const response=await fetch('/get_currency',{method:'POST',signal:AbortSignal.timeout(15000)});
        if(!response.ok)throw new Error();
        const data=await response.json();
        document.querySelector('#currency .button-text').textContent=data.currency;
    } catch (_) { document.getElementById('currency').title='Unable to load coins'; }
}
const decks=new Decks_Container();
const home=new Home(decks);
const lobbyData = get_currency();
window.PageTransition?.wait(Promise.all([lobbyData, decks.ready]));

// Reuse the existing audio iframe and music assets; settings affect the real player.
const preferences={
    get(key,fallback){try{return localStorage.getItem(key)??fallback;}catch(_){return fallback;}},
    set(key,value){try{localStorage.setItem(key,value);}catch(_){}}
};
const musicControl=document.getElementById('music-enabled');
const motionControl=document.getElementById('reduce-motion');
musicControl.checked=preferences.get('lobby-music','true')==='true';
motionControl.checked=preferences.get('lobby-reduced-motion','false')==='true';
function applyMotion(){document.body.classList.toggle('motion-reduced',motionControl.checked);document.dispatchEvent(new Event('lobby:motion-change'));}
applyMotion();motionControl.addEventListener('change',()=>{preferences.set('lobby-reduced-motion',String(motionControl.checked));applyMotion();});
// The same atlas crops serve the CSS fallback and the Three.js enhancement.
document.querySelectorAll('.object-button:not(#studio) .object-art').forEach(art=>{
    const active=art.cloneNode(true);
    active.classList.add('object-active');
    const image=active.querySelector('image');
    image.setAttribute('href',image.getAttribute('href').replace('props.png','props-active.png'));
    art.after(active);
});
function pauseEffects(){document.body.classList.toggle('motion-paused',document.hidden||!document.hasFocus());}
window.addEventListener('blur',()=>document.body.classList.add('motion-paused'));
window.addEventListener('focus',pauseEffects);
document.addEventListener('visibilitychange',pauseEffects);
pauseEffects();
let music, interacted=false, resumeOnFocus=false;
function playMusic(){if(music&&musicControl.checked&&interacted&&!document.hidden&&document.hasFocus())music.play().catch(()=>{});}
function setupMusic(){
    const frame=document.getElementById('audio-frame');
    music=frame.contentDocument?.getElementById('background-music');
    if(!music||music.dataset.lobbyReady)return;
    music.dataset.lobbyReady='true';music.volume=.3;
    music.addEventListener('loadedmetadata',()=>{const saved=Number(preferences.get('audioTime','0'));if(saved>0&&saved<music.duration)music.currentTime=saved;},{once:true});
    music.addEventListener('ended',()=>{music.src=`/webpages/audio/music_sorce/hall/hall${Math.random()<.5?1:3}.mp3`;playMusic();});
    playMusic();
}
document.getElementById('audio-frame').addEventListener('load',setupMusic);setupMusic();
document.addEventListener('click',()=>{interacted=true;playMusic();},{once:true});
musicControl.addEventListener('change',()=>{preferences.set('lobby-music',String(musicControl.checked));if(musicControl.checked){interacted=true;playMusic();}else music?.pause();});
function pauseMusic(){if(music){resumeOnFocus=resumeOnFocus||!music.paused;preferences.set('audioTime',String(music.currentTime));music.pause();}}
window.addEventListener('blur',pauseMusic);
window.addEventListener('focus',()=>{if(resumeOnFocus)playMusic();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseMusic();else if(resumeOnFocus)playMusic();});
window.addEventListener('pagehide',pauseMusic);
