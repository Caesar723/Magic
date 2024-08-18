const root = document.documentElement;

document.body.addEventListener('wheel', (event) => {
    const bar=document.getElementById("Top_Bar")
    if (event.deltaY<0){
        root.style.setProperty('--top-position', "0px");

    }
    // else{
    //     root.style.setProperty('--top-position', "-"+bar.offsetHeight+"px");
    // }
    
})
document.getElementById('company_name').addEventListener('click', function(){
    window.location.href= 'home.html';
})

window.addEventListener('resize', function(event) {

    checkDistance()
    
});

function checkDistance() {
    const element=document.getElementById('nagvigation_bar')
    const width=window.innerWidth
    const parentPosition = element.getBoundingClientRect();
    console.log(parentPosition.x+parentPosition.width,width)
    if ((parentPosition.x+parentPosition.width)>(width)){
        
        const childElements = element.querySelectorAll('.bar');
        const childElements_more = document.getElementById('more').querySelectorAll('a');;
        console.log(childElements_more)
        const more=document.getElementById('dropdown-content')
        more.style.visibility = 'visible';
        const more_pos=more.getBoundingClientRect();


        for (let i = 0; i < childElements.length; i++){
            const child=childElements[i]
            const child_pos = child.getBoundingClientRect();
            if (child_pos.x+child_pos.width>more_pos.x){
                child.style.visibility = 'hidden'; // 输出每个匹配的子元素
                
                childElements_more[i].style.display = 'flex';
            }
            else{
                child.style.visibility = 'visible';
                
                childElements_more[i].style.display = 'none';
            }
        }
        
    }
    // else{
    //     const more=document.getElementById('dropdown-content')
    //     more.style.visibility = 'hidden';
    //     const childElements = element.querySelectorAll('.bar');
    //     childElements.forEach(child => {
    //         child.style.visibility = 'visible'; // 输出每个匹配的子元素
    //       });
    //       console.log(1)
    // }
   
    
}

checkDistance()