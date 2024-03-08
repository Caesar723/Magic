function set_from_button(){
    document.getElementById('itemForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // 获取表单数据
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    console.log(JSON.stringify(data));
    if (data.password==data.password_repest){
        const response=await post_request(data);
        const responseData = await response.json();
        if (responseData.message=="Sign up successful"){
            window.location.href = '/login';
            }
        else{
            error_raise("Unsuccessful, repeat username")
        }
    }
    else{
        error_raise("Password Confirm error")
    }
    


    

    // // 处理响应数据
    // const responseData = await response.json();
    // if (responseData.message=="Login successful"){
    //     window.location.replace('/');
    // }
    // console.log('Received:', responseData);
    // 可以在此处更新页面内容
});
}
async function post_request(data){
    const response = await fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response

}
function error_raise(content){
    document.getElementById('login__password').value = '';
    document.getElementById('login__password_repeat').value = ''; 
    var message = document.getElementById('message_confirm');
    message.style.display = 'block';
    message.textContent=content;
    setTimeout(function() {
        message.style.display = 'none';
        
    }, 3000); // 3秒后执行
}
set_from_button()