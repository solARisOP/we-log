var delConfirm = (blogp) => {
    let response = confirm("Are you sure you want to delete this Post, This action is irreversible");
    if (response) {
        var link = blogp.dataset.slug;
        document.location = `/blog/delete/${link}`;
    }
}
var imgSize = ()=>{
    var img = document.getElementById('avatar');
    if (img.files.length > 0) {
        var fileSize = img.files[0].size; // Get the file size in bytes
        var maxSize = 5 * 1024 * 1024; 

        if(fileSize > maxSize)
        {
            alert("image file size exceeds the maximum allowed size (5 MB).");
            return false;
        }
        return true;
    }
}

var relationToggle =(btn)=>{

    btn.disabled = true;
    let txt = btn.innerText;

    let link = ``;
    if(txt == "Follow") link = `/you/follow/${btn.dataset.username}`;
    else link = `/you/unfollow/${btn.dataset.username}`;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch(link, {
        method: 'POST',
        body: JSON.stringify({ message: '' }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            btn.disabled = false;
            if(txt == "Follow")
            {
                btn.innerText = "Unfollow";
                btn.classList.remove('btn-dark');
                btn.classList.add('btn-outline-dark');
                var followerCnt = document.getElementById('followers-cnt');
                followerCnt.innerText = Number(followerCnt.innerText) + 1;
            } 
            else
            {
                btn.innerText = "Follow";
                btn.classList.remove('btn-outline-dark');
                btn.classList.add('btn-dark');
                document.getElementById('followers-cnt').innerText -= 1;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
