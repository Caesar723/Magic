


async function get_image_five(){
    
    const response = await fetch('/login/cards_show', {
                method: 'POST',
            });
    const responseData = await response.json();
    return responseData
}
function set_from_button(){
    document.getElementById('itemForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // 获取表单数据
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    console.log(JSON.stringify(data));
    // 发送 POST 请求到服务器
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // 处理响应数据
    const responseData = await response.json();
    console.log(responseData);
    if (responseData.message=="Login successful"){

        window.location.href = '/';
    }
    console.log('Received:', responseData);
    // 可以在此处更新页面内容
});
}


async function set_image_slider(){
    const lis = document.querySelectorAll('.image_card_div');
    const images=await get_image_five();
    
    for (var li=0;li<5;li++){
        
        const div = document.createElement('div');
        
        const img = document.createElement('img');
        
        img.src = '/get-images/'+images.image_url[li]; // 设置图片源
        img.className = 'image_card'; // 设置替代文本

        // 创建段落元素
        const p = document.createElement('p');
        p.textContent = images.image_story[li]; // 设置段落文本
        p.className="text--center";

        div.appendChild(img);
        div.appendChild(p);
        lis[li].appendChild(div);
    }
}

function main(){
    
    set_image_slider();
    set_from_button();
    
}


main();