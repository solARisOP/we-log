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