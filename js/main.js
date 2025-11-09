const darkModeButton = document.getElementById('toggle-dark-mode');
 const bodyElement = document.body;
 // 2. 监听按钮的点击事件
 darkModeButton.addEventListener('click', function() {
     // 3. 执行切换操作：检查body是否有一个叫'dark-mode'的class
     //    如果有，就移除它；如果没有，就添加它。
     bodyElement.classList.toggle('dark-mode');
 });
 const addProjectBtn = document.getElementById('add-project-btn');
 const newProjectInput = document.getElementById('new-project-input');
 const projectList = document.getElementById('history'); // 获取紧跟在.title后的.list-group
 // 2. 监听按钮点击
 addProjectBtn.addEventListener('click', function() {
     // 3. 获取输入框的值
     const newProjectText = newProjectInput.value;
 
     // 4. 检查输入是否为空
     if (newProjectText.trim() === '') {
         alert('请输入项目名称！');
         return; // 结束函数执行
     }
 
     // 5. 创建一个新的列表项 <li>
     const newListItem = document.createElement('li');
     newListItem.className = 'list-group-item'; // 添加Bootstrap的class
     newListItem.textContent = newProjectText; // 设置文本内容
 
     // 6. 将新的列表项添加到列表中
     projectList.appendChild(newListItem);
 
     // 7. 清空输入框
     newProjectInput.value = '';
 });
 
 $(document).ready(function () {
     var qs=false,ws=false;
     const man = new Audio("static\\sound\\man.wav")
     const bo = new Audio("static\\sound\\bo.wav")
     $("#qq").click(function () {
         $("#qqcode").slideToggle('fast');
         if(qs){
             $("#qq").html("→QQ：<b>30738009</b>(单击出码)");
             qs=false;
         }else{
             $("#qq").html("↓&nbsp&nbspQQ：<b>30738009</b>(单击收码)");
             qs=true;
         }
         // $("#qq").html("→QQ：<b>30738009</b>(单击收码)");
     });
     $("#wechat").click(function () {
         $("#wechatcode").slideToggle('fast');
         if(ws){
             $("#wechat").html("→微信：<b>y30738009</b>(单击出码)");
             ws=false;
         }else{
             $("#wechat").html("↓&nbsp&nbsp微信：<b>y30738009</b>(单击收码)");
             ws=true;
         }
     });
     $("#manbo").mousedown(function () { 
         man.play();
         man.loop = false;
     });
     $("#manbo").mouseup(function () {
         bo.play();
         bo.loop = false;
     });
     $('#skills li').on('click', function() {
         // 'this' 在这里指的是被点击的那个li元素
         // 使用 .fadeOut() 方法实现淡出效果
         $(this).fadeOut();
     });
     // 1. 选择紧跟在“个人简介”标题后的 #bio-content 的父级h2
     const bioTitle = $('#bio-content').prev('.section-title');
     // 2. 修改鼠标样式，提示用户这里可以点击
     bioTitle.css('cursor', 'pointer');
     // 3. 绑定点击事件
     bioTitle.on('click', function() {
     // 使用 .slideToggle() 方法实现平滑的滑动展开/收起效果
         $('#bio-content').slideToggle();
     });
 });