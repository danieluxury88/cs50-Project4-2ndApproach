document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('edit_btn').addEventListener('click', () => test_function());
    document.getElementById('delete_btn').addEventListener('click', () => test_function());
    console.log("hi");
});

function test_function(){
    console.log("hi");
}