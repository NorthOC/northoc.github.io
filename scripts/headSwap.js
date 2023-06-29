const head_pics = ['<img class="heads" draggable="false" src="/static/images/heads/face_2.png">',
'<img class="heads" draggable="false" src="/static/images/heads/face_1.png">',
'<img class="heads" draggable="false" src="/static/images/heads/face_4.png">',
'<img class="heads" draggable="false" src="/static/images/heads/face_3.png">',
'<img class="heads" draggable="false" src="/static/images/heads/face_5.png">'];

function headSwap(idx){
    if (window.innerWidth < 840){
        return
    }
    elem = document.getElementById("head-box");
    elem.innerHTML = head_pics[idx];
    
}