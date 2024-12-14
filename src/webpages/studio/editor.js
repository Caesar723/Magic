var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
  lineNumbers: true,
  mode: "python",
  theme: "dracula",
  indentUnit: 4,
  tabSize: 4,
  autoCloseBrackets: true,
  matchBrackets: true,
  showCursorWhenSelecting: true
});
document.getElementById('card-image').addEventListener('change', function(e) {
  var file = e.target.files[0];
  var reader = new FileReader();
  reader.onload = function(event) {
      var img = document.getElementById('image-preview');
      img.src = event.target.result;
      img.style.display = 'block';
  }
  reader.readAsDataURL(file);
});

document.getElementById('card-form').addEventListener('submit', function(e) {
  e.preventDefault();
  // 这里可以添加发送表单数据的逻辑
  console.log('表单提交');
});
function handleDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  
  const files = e.dataTransfer.files;
  if(files.length) {
      handleFiles(files[0]);
  }
  
  e.target.classList.remove('drag-over');
}

function handleDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  e.target.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.preventDefault();
  e.stopPropagation(); 
  e.target.classList.remove('drag-over');
}

function handleFileSelect(e) {
  const files = e.target.files;
  if(files.length) {
      handleFiles(files[0]);
  }
}

function handleFiles(file) {
  if(!file.type.startsWith('image/')) {
      alert('请上传图片文件!');
      return;
  }

  const reader = new FileReader();
  reader.onload = function(e) {
      const preview = document.getElementById('preview-image');
      preview.src = e.target.result;
      preview.style.display = 'block';
      
      document.querySelector('.drop-zone-content').style.display = 'none';
  }
  reader.readAsDataURL(file);
}