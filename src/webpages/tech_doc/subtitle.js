var links = document.querySelectorAll('.link');

// 为每个链接添加点击事件
links.forEach(function(link) {
    link.addEventListener('click', function() {
        // 移除其他所有链接的 active 类
        links.forEach(function(el) {
            el.classList.remove('active');
            const children = el.parentElement.getElementsByTagName('div')[0];
            //console.log(el,children)
            children.classList.remove('show_sublinks');


            
            children.style.height="0px";
            children.classList.add('show_sublinks');



        });
        // 为当前点击的链接添加 active 类
        link.classList.add('active');
        const children = link.parentElement.getElementsByTagName('div')[0];



        var childrens_a = children.children;
        var totalHeight = 0;

        for (var i = 0; i < childrens_a.length; i++) {
            totalHeight += childrens_a[i].offsetHeight;
        }
        children.style.height=totalHeight + "px";
        children.classList.add('show_sublinks');
    });

    link.addEventListener('click', function(event) {
        links.forEach(function(el) {
            const children = el.parentElement.getElementsByTagName('div')[0];
            //console.log(el,children)
            //children.classList.remove('show_sublinks');


            
            children.style.height="0px";
            //children.classList.add('show_sublinks');



        });
        // 为当前点击的链接添加 active 类
        const children = link.parentElement.getElementsByTagName('div')[0];



        var childrens_a = children.children;
        var totalHeight = 0;

        for (var i = 0; i < childrens_a.length; i++) {
            totalHeight += childrens_a[i].offsetHeight;
        }
        children.style.height=totalHeight + "px";
        children.classList.add('show_sublinks');
    });

    const div = link.parentElement.getElementsByTagName('div')[0];
    div.querySelectorAll('.sublink').forEach(function(sublink) {
        sublink.addEventListener('click', function() {
            links.forEach(function(el) {
                el.classList.remove('active');
            })
            link.classList.add('active');
        })
    })


});
var sublinks = document.querySelectorAll('.sublink');
sublinks.forEach(function(link) {
    link.addEventListener('click', function() {
        // 移除其他所有链接的 active 类
        sublinks.forEach(function(el) {
            el.classList.remove('active');
            const children_a = Array.from(el.parentElement.querySelectorAll('a.sublink'));
            console.log(children_a)
            const index = children_a.indexOf(el);
            console.log(index)
            const children = el.parentElement.getElementsByTagName('div')[index];
            //console.log(el,children)
            children.classList.remove('show_sublinks');


            
            children.style.height="0px";
            children.classList.add('show_sublinks');



        });
        // 为当前点击的链接添加 active 类
        link.classList.add('active');

        const children_a = Array.from(link.parentElement.querySelectorAll('a.sublink'));
        console.log(children_a)
        const index = children_a.indexOf(link);
        console.log(index)
        const children = link.parentElement.getElementsByTagName('div')[index];



        var childrens_a = children.children;
        var totalHeight = 0;

        for (var i = 0; i < childrens_a.length; i++) {
            totalHeight += childrens_a[i].offsetHeight;
        }
        children.style.height=totalHeight + "px";
        children.classList.add('show_sublinks');
    });

    link.addEventListener('click', function(event) {
        sublinks.forEach(function(el) {


            //const targetLink = link.parentElement.querySelector('a.sublink');
            console.log(el)
            const children_a = Array.from(el.parentElement.querySelectorAll('a.sublink'));
            console.log(children_a)
            const index = children_a.indexOf(el);
            console.log(index)
            const children = el.parentElement.getElementsByTagName('div')[index];
            //console.log(el,children)
            //children.classList.remove('show_sublinks');


            
            children.style.height="0px";
            //children.classList.add('show_sublinks');



        });
        // 为当前点击的链接添加 active 类
        const children_a = Array.from(link.parentElement.querySelectorAll('a.sublink'));
        console.log(children_a)
        const index = children_a.indexOf(link);
        console.log(index)
        const children = link.parentElement.getElementsByTagName('div')[index];



        var childrens_a = children.children;
        var totalHeight = 0;

        for (var i = 0; i < childrens_a.length; i++) {
            totalHeight += childrens_a[i].offsetHeight;
        }
        children.style.height=totalHeight + "px";
        console.log(children.offsetHeight)
        children.classList.add('show_sublinks');


        const parent =link.parentElement.parentElement.getElementsByTagName('div')[0];
        console.log(parent)
        var childrens_a = parent.querySelectorAll('a.sublink');
        var totalHeight = totalHeight;

        for (var i = 0; i < childrens_a.length; i++) {
            totalHeight += childrens_a[i].offsetHeight;
            //console.log(childrens_a[i],childrens_a[i].offsetHeight,childrens_a[i].style.height)
        }
        parent.style.height=totalHeight + "px";
        //console.log(totalHeight + "px")
        parent.classList.add('show_sublinks');
    });

    //const div = link.parentElement.getElementsByTagName('div')[0];
    // div.querySelectorAll('.sublink').forEach(function(sublink) {
    //     sublink.addEventListener('click', function() {
    //         links.forEach(function(el) {
    //             el.classList.remove('active');
    //         })
    //         link.classList.add('active');
    //     })
    // })


});

window.addEventListener('load', function() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    console.log(scrollPosition)
    if (scrollPosition) {
        window.scrollTo({
            top: parseInt(scrollPosition),  // 目标元素的垂直位置
            behavior: 'smooth'      // 平滑滚动
            }
            
        );
    }
});
function scrollToTarget(e) {
    
    const root = document.documentElement;
    root.style.setProperty('--top-position', "0px");
    const a=e.target
    e.preventDefault();  // 阻止默认的锚点跳转行为
    var target = document.getElementById(a.getAttribute('href').slice(1));
    
    var rect=target.getBoundingClientRect()
    var container = document.getElementById('main_body');
    var top_cap=container.querySelector('.top').getBoundingClientRect();
    
    const target_top=-top_cap.top+rect.top//- container.offsetTop;
    localStorage.setItem('scrollPosition', e.currentTarget.getBoundingClientRect().top-top_cap.top);
    container.scrollTop+=target_top
    
    window.scrollTo({
    top: target_top,  // 目标元素的垂直位置
    behavior: 'smooth'      // 平滑滚动
    })
    console.log(e.currentTarget.offsetTop)
    

    
    // console.log(rect.top - container.offsetTop)
    // container.scrollTop = rect.top - container.offsetTop;
    // console.log(container.scrollTop)
}

