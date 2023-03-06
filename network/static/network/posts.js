document.addEventListener('DOMContentLoaded', function () {
//    document.getElementById('edit_btn').addEventListener('click', () => test_function());
//    document.getElementById('delete_btn').addEventListener('click', () => test_function());
    console.log("hi");
});


function showModalWindow(post_content, post_id ){
    const postNum = document.getElementById("post-num");
    postNum.value = post_id;
    const modalContent = document.getElementById("modal-content");
    modalContent.innerHTML = post_content;
    const myModal = new bootstrap.Modal('#modal_window', {
        keyboard: false
      }).show()
}

function updatePostContent(){
    const modalContent = document.getElementById("modal-content");
    let postNum = document.getElementById("post-num").value;
    console.log("update:", postNum);
    console.log("update", modalContent.value);
}