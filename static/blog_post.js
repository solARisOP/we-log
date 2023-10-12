var likeBtn = document.getElementById('like-btn');
var dislikeBtn = document.getElementById('dislike-btn');
var likeCnt = document.getElementById('like-cnt');
var dislikeCnt = document.getElementById('dislike-cnt');

var Like = (btn)=>{
    btn.disabled = true;
    let message = btn.classList.contains('fa-thumbs-o-up') ? 1 : 2;
    var post = btn.dataset.post;
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
                btn.classList.remove('fa-thumbs-o-up');
                btn.classList.add('fa-thumbs-up');
                if(dislikeBtn.classList.contains('fa-thumbs-down')){
                    dislikeBtn.classList.remove('fa-thumbs-down');
                    dislikeBtn.classList.add('fa-thumbs-o-down');
                    let num = dislikeCnt.innerText;
                    dislikeCnt.innerText = Number(num)-1;
                }
                let num = likeCnt.innerText;
                likeCnt.innerText = Number(num)+1;
            } 
            else if(data['message'] == 2){
                btn.classList.remove('fa-thumbs-up');
                btn.classList.add('fa-thumbs-o-up');
                let num = likeCnt.innerText;
                likeCnt.innerText = Number(num)-1;
            }
            btn.disabled = false;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

var Dislike = (btn)=>{
    btn.disabled = true;
    let message = btn.classList.contains('fa-thumbs-o-down') ? 3 : 4;
    var post = btn.dataset.post;
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
                btn.classList.remove('fa-thumbs-o-down');
                btn.classList.add('fa-thumbs-down');
                if(likeBtn.classList.contains('fa-thumbs-up')){
                    likeBtn.classList.remove('fa-thumbs-up');
                    likeBtn.classList.add('fa-thumbs-o-up');
                    let num = likeCnt.innerText;
                    likeCnt.innerText = Number(num)-1;
                }
                let num = dislikeCnt.innerText;
                dislikeCnt.innerText = Number(num)+1;
            } 
            else if(data['message'] == 4){
                btn.classList.remove('fa-thumbs-down');
                btn.classList.add('fa-thumbs-o-down');
                let num = dislikeCnt.innerText;
                dislikeCnt.innerText = Number(num)-1;
            }
            btn.disabled = false;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}