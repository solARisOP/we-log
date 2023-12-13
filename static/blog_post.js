var likeBtn = document.getElementById('like-btn');
var dislikeBtn = document.getElementById('dislike-btn');
var likeCnt = document.getElementById('like-cnt');
var dislikeCnt = document.getElementById('dislike-cnt');
var likeIcn = document.getElementById('like-icn');
var dislikeIcn = document.getElementById('dislike-icn');

likeBtn.addEventListener('click', ()=>{
    likeBtn.style.pointerEvents="none";
    likeBtn.style.cursor="default";
    let message = likeIcn.classList.contains('fa-thumbs-o-up') ? 1 : 2;
    var post = likeIcn.dataset.post;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch(`/blog/stat/${post}`, {
        method: 'POST',
        body: JSON.stringify({ message: message }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if(data['message'] == 1){
                likeIcn.classList.remove('fa-thumbs-o-up');
                likeIcn.classList.add('fa-thumbs-up');
                if(dislikeIcn.classList.contains('fa-thumbs-down')){
                    dislikeIcn.classList.remove('fa-thumbs-down');
                    dislikeIcn.classList.add('fa-thumbs-o-down');
                    let num = dislikeCnt.innerText;
                    dislikeCnt.innerText = Number(num)-1;
                }
                let num = likeCnt.innerText;
                likeCnt.innerText = Number(num)+1;
            } 
            else if(data['message'] == 2){
                likeIcn.classList.remove('fa-thumbs-up');
                likeIcn.classList.add('fa-thumbs-o-up');
                let num = likeCnt.innerText;
                likeCnt.innerText = Number(num)-1;
            }
            likeBtn.style.pointerEvents="auto";
            likeBtn.style.cursor="pointer";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

dislikeBtn.addEventListener('click', ()=>{
    dislikeBtn.style.pointerEvents="none";
    dislikeBtn.style.cursor="default";
    let message = dislikeIcn.classList.contains('fa-thumbs-o-down') ? 3 : 4;
    var post = dislikeIcn.dataset.post;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch(`/blog/stat/${post}`, {
        method: 'POST',
        body: JSON.stringify({ message: message }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if(data['message'] == 3){
                dislikeIcn.classList.remove('fa-thumbs-o-down');
                dislikeIcn.classList.add('fa-thumbs-down');
                if(likeIcn.classList.contains('fa-thumbs-up')){
                    likeIcn.classList.remove('fa-thumbs-up');
                    likeIcn.classList.add('fa-thumbs-o-up');
                    let num = likeCnt.innerText;
                    likeCnt.innerText = Number(num)-1;
                }
                let num = dislikeCnt.innerText;
                dislikeCnt.innerText = Number(num)+1;
            } 
            else if(data['message'] == 4){
                dislikeIcn.classList.remove('fa-thumbs-down');
                dislikeIcn.classList.add('fa-thumbs-o-down');
                let num = dislikeCnt.innerText;
                dislikeCnt.innerText = Number(num)-1;
            }
            dislikeBtn.style.pointerEvents="auto";
            dislikeBtn.style.cursor="pointer";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});