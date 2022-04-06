document.addEventListener("DOMContentLoaded", function () {
    console.log('JavaScript is working.')
    edit_buttons = document.querySelectorAll("#edit_button");
    like_icons = document.querySelectorAll("#like_icon")
    edit_buttons.forEach(btn => {
        btn.addEventListener("click", edit_button_clicked)
    });
    like_icons.forEach(icon => {
        icon.addEventListener("click", like_icon_clicked)
    })

})

function edit_button_clicked() {
    btn = this
    post_id = btn.dataset.buttonid
    btn.style.display = 'none'

    post = document.querySelector(`[data-postid="${post_id}"]`);
    post.style.display = 'none'

    form = document.createElement('form')
    form.setAttribute('id', `post_form${post_id}`)

    textarea = document.createElement('textarea')
    textarea.setAttribute('id', `area${post_id}`)
    textarea.innerHTML = post.innerHTML
    textarea.setAttribute('style', 'min-height: 64px; width: 520px; resize:none; border-radius: 10px; padding:5px;')

    div = post.parentNode
    btn = document.createElement('button')
    btn.setAttribute('type', 'submit')
    btn.setAttribute('id', 'save_button')
    btn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>'

    btn_div = document.createElement('div')
    btn_div.setAttribute('style', 'width: 520px;')
    btn_div.append(btn)

    form.append(textarea)
    form.append(btn_div)

    form.addEventListener('submit', (e) => {
        console.log('inside the submit listener function')
        post_id = this.dataset.buttonid
        e.preventDefault();
        the_text = document.getElementById(`area${post_id}`)
        console.log(this.dataset.buttonid)
        console.log(the_text.value)

        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
                'post': the_text.value,
                'id': post_id,
            })
        })
            .then(result => result.json())
            .then(data => {
                if (data['outcome'] == 'Success') {
                    the_text.parentNode.style.display = 'none'
                    post = document.querySelector(`[data-postid="${post_id}"]`);
                    post.innerHTML = the_text.value
                    post.style.display = ''
                    btn = document.querySelector(`[data-buttonid="${post_id}"]`)
                    btn.style.display = ''
                }
                else {
                    console.log('failure')
                }
            })
    })
    div.prepend(form)
}


function like_icon_clicked() {
    post_id = this.dataset.iconid
    //this.className = "fa-solid fa-heart"
    //console.log(post_id)
    count = document.getElementById(`postcount${post_id}`)
    //console.log(count)
    //count.innerHTML = parseInt(count.innerHTML) + 1


    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            'id': post_id,
        })
    })
        .then(result => result.json())
        .then(data => {
            if (data['outcome'] == 'Added') {
                count.innerHTML = parseInt(count.innerHTML) + 1
                this.className = "fa-solid fa-heart liked"
            }
            else {
                count.innerHTML = parseInt(count.innerHTML) - 1
                this.className = "fa-regular fa-heart"
            }
        })
}