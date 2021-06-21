$(function() {
    var message = document.body.querySelector(".dj-message");
    if(message) {
        for (let x of message.children) {
            x.style.listStyle = "none";
        }
        setTimeout(() => message.remove(), 3000);
    };
    var delete_btn = document.body.querySelector(".delete_obj");
    var main_delete = document.body.querySelector(".delete_modal")
    main_delete.addEventListener("click", (event) => {
        var main_delete = document.body.querySelector(".main_delete_btn");
        // alert(typeof event.target);
    })
});