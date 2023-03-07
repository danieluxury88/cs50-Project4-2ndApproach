document.addEventListener('DOMContentLoaded', function () {
//    document.getElementById('edit_btn').addEventListener('click', () => test_function());
//    document.getElementById('delete_btn').addEventListener('click', () => test_function());
//    console.log("hi");
});


function showModalWindow(post_contentVal, post_id ){

    const modalContent = document.getElementById("modal_content_text_area_id");
    modalContent.value = post_contentVal;

    // Hidden type to save post_id when updating
    const postNum = document.getElementById("post-num");
    postNum.value = post_id;

    const myModal = new bootstrap.Modal('#modal_window', {
        keyboard: false
      }).show()
}

function updatePostContent(){
    let modalContent = document.getElementById("modal_content_text_area_id");
    let postNum = document.getElementById("post-num").value;

    fetch(`/edit/${postNum}`, {
      method: 'POST',
      body: JSON.stringify({
          id: postNum,
          content: modalContent.value,
      })
    })
    .then(response => response.json())
    .then(result => {
        const postContent = document.getElementById(`post_content_${postNum}`);
        postContent.innerHTML = modalContent.value;
        console.log(result);
    });
}

function reactToPost (post_id, value) {
    let like_btn = document.getElementById(`like_btn_${post_id}`);
    let dislike_btn = document.getElementById(`dislike_btn_${post_id}`);
    let likes_counter = document.getElementById(`likes_counter_${post_id}`);

    if ( value == "add" ) {
        like_btn.style.display = 'block';
        dislike_btn.style.display = 'none';
    }
    else {
        like_btn.style.display = 'none';
        dislike_btn.style.display = 'block';
    }

    fetch(`/like/${post_id}`, {
      method: 'POST',
      body: JSON.stringify({
          id: post_id,
          action:value,
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        likes_counter.innerHTML= result.likers+ " Likes";
    });
}