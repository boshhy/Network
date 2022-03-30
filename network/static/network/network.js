document.addEventListener("DOMContentLoaded", function () {
    console.log('JavaScript is working.')
    edit_buttons = document.querySelectorAll("#edit_button");
    edit_buttons.forEach(btn => {
        btn.addEventListener("click", edit_button_clicked)
    });
})

function edit_button_clicked() {
    btn = this
    btn.innerHTML = 'save'
    btn.setAttribute('id', 'save_button')

    post = document.querySelector(`[data-postid="${btn.dataset.buttonid}"]`);
    btn.removeEventListener("click", edit_button_clicked)
    //btn.addEventListener('click', test)
    btn.setAttribute('type', 'submit')
    form = document.createElement('form')
    form.onsubmit = test()
    textarea = document.createElement('textarea')
    textarea.innerHTML = post.innerHTML
    post.innerHTML = ""
    div = document.getElementById('edit_div')
    div.append(btn)
    form.append(textarea)
    post.append(form)
}

function test() {
    // btn = this
    // btn.innerHTML = 'Edit'
    //btn.setAttribute('id', 'edit_button')

    //post = document.querySelector(`[data-postid="${btn.dataset.buttonid}"]`);
    console.log(this)
    console.log("you are now calling the save function")
    //console.log(post.innerHTML)
}