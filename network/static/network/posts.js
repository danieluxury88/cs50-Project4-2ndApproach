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