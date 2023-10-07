// var delConfirm = (blogp) => {
//     let response = confirm("Are you sure you want to delete this Post, This action is irreversible");
//     if (response) {
//         var link = blogp.dataset.slug;
//         document.location = `/blog/delete/${link}`;
//     }
// }

// var unfollowButton = document.getElementById('unfollow-Button');
// var followButton = document.getElementById('follow-Button');

// document.addEventListener('DOMContentLoaded', ()=>{
//     unfollowButton.hide();
//     followButton.hide();

//     if ({{user.is_authenticated}})
//     {
//         if({{user.following}} == {{user_}})
//         {
//             unfollowButton.show();
//         }
//         else
//         {
//             followButton.show();
//         }
//     }
// });

// var unFollow = () =>{
//     unfollowButton.disabled = true;

//     fetch('/you/unfollow', {
//         method: 'POST',
//         body: JSON.stringify({ username: {{user_.username}} }),
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken,
//         },
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             unfollowButton.disabled = false;
//             unfollowButton.hide();
//             followButton.show();
//             return true;
//         }
//         .catch((error) => {
//             console.error('Error:', error);
//             return false;
//         });
// }

// var Follow = () =>{
//     followButton.disabled = true;

//     fetch('/you/follow', {
//         method: 'POST',
//         body: JSON.stringify({ username: {{user_.username}} }),
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken,
//         },
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             followButton.disabled = false;
//             followButton.hide();
//             unfollowButton.show();
//             return true;
//         }
//         .catch((error) => {
//             console.error('Error:', error);
//             return false;
//         });
// }