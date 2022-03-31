document.addEventListener("DOMContentLoaded", function () {
    console.log('JavaScript is working.')
    edit_buttons = document.querySelectorAll("#edit_button");
    edit_buttons.forEach(btn => {
        btn.addEventListener("click", edit_button_clicked)
    });
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

    div = post.parentNode
    input = document.createElement('input')
    input.setAttribute('type', 'submit')
    input.value = 'Save'

    form.append(textarea)
    form.append(input)

    form.addEventListener('submit', (e) => {
        console.log('inside the submit listener function')
        post_id = this.dataset.buttonid
        e.preventDefault();
        the_text = document.getElementById(`area${post_id}`)
        console.log(this.dataset.buttonid)
        console.log(the_text.value)

        fetch('edit', {
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