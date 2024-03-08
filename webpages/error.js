function showBox(content){
    const box = document.getElementById('box');
    var message = document.getElementById('text_box')
    message.textContent=content
    box.style.visibility = 'visible';
    box.style.opacity = 1;
    box.style.borderRadius = '10%'; // 变为无圆角
    box.style.transform = 'translate(-50%, -50%) scale(1)'; // 变为原始大小
    setTimeout(() => {
        box.style.opacity = 0;
        box.style.borderRadius = '50%'; // 再次变为圆形
        box.style.transform = 'translate(-50%, -50%) scale(0)'; // 缩小回0
        // 确保visibility的改变延迟执行，以便opacity渐变完成
        setTimeout(() => {
          box.style.visibility = 'hidden';
        }, 500); // 这里的延迟应与CSS中transition的持续时间相匹配
      }, 3000); // 3秒后开始淡出
    
}
