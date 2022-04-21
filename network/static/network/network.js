// After the page has finished loading add event listeners to
// the like icons and the edit buttons
document.addEventListener("DOMContentLoaded", function () {
    edit_buttons = document.querySelectorAll("#edit_button");
    like_icons = document.querySelectorAll("#like_icon")

    // When an edit button is clicked run the 'edit_button_clicked' function
    edit_buttons.forEach(btn => {
        btn.addEventListener("click", edit_button_clicked)
    });

    // When a like icon is clicked run the 'like_icon_clicked' function
    like_icons.forEach(icon => {
        icon.addEventListener("click", like_icon_clicked)
    })

})

// This function lets a user edit a post and at the same time updates
// the data base tables by using a fetch call, all without reloading
// the entire contents of the page
function edit_button_clicked() {
    // Get the id of button that was clicked and set display to none
    btn = this
    post_id = btn.dataset.buttonid
    btn.style.display = 'none'

    // Hide the contents of the post text
    post = document.querySelector(`[data-postid="${post_id}"]`);
    post.style.display = 'none'

    // Create a form
    form = document.createElement('form')
    form.setAttribute('id', `post_form${post_id}`)

    // Create a text area populated by the old post text
    textarea = document.createElement('textarea')
    textarea.setAttribute('id', `area${post_id}`)
    textarea.innerHTML = post.innerHTML
    textarea.setAttribute('style', 'min-height: 64px; width: 520px; resize:none; border-radius: 10px; padding:5px;')

    // Get the div of the current post and create a button to submit form
    div = post.parentNode
    btn = document.createElement('button')
    btn.setAttribute('type', 'submit')
    btn.setAttribute('id', 'save_button')
    btn.innerHTML = '<i class="fa-solid fa-floppy-disk"></i>'

    // Create a div to append the button 
    btn_div = document.createElement('div')
    btn_div.setAttribute('style', 'width: 520px;')
    btn_div.append(btn)

    // add text area and button to the form
    form.append(textarea)
    form.append(btn_div)

    // When form is submitted get the contents of the text 
    // from the newly added text area
    form.addEventListener('submit', (e) => {
        post_id = this.dataset.buttonid
        e.preventDefault();
        the_text = document.getElementById(`area${post_id}`)

        // Use the id and text to call backend to update the post
        // with matching id with the new text
        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
                'post': the_text.value,
                'id': post_id,
            })
        })
            .then(result => result.json())
            .then(data => {
                // If post was successfully updated then display post with newly 
                // updated text and display the edit button again
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

// This function will let the user like or unlike a post
// and update the count accordingly 
function like_icon_clicked() {
    // Get the id of the post for which the clicked like icon belongs to
    post_id = this.dataset.iconid
    count = document.getElementById(`postcount${post_id}`)

    // Call the like function in the backend to deal with the click
    // either add or removes the user from the posts likes table
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            'id': post_id,
        })
    })
        .then(result => result.json())
        .then(data => {
            // When added to the table change to red heart icon
            // and increase the count by 1
            if (data['outcome'] == 'Added') {
                count.innerHTML = parseInt(count.innerHTML) + 1
                this.className = "fa-solid fa-heart liked"
            }
            // When removed from the table change to hollow heart icon
            // and decrease the count by 1
            else {
                count.innerHTML = parseInt(count.innerHTML) - 1
                this.className = "fa-regular fa-heart"
            }
        })
}