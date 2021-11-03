$(function() {

    window.addEventListener('click', function(e) {
        // e.preventDefault();
        let profButtonPicture = document.getElementsByClassName('profile-button__picture')[0]
        let profDrop = document.getElementById('profile-drop')
        let mentionDrop = document.getElementsByClassName('mention_drop')[0]
        let mentionButton = document.getElementById('mention_button')
        let newPostButton = document.getElementById('new-post')
        let newPostWindow = document.getElementById('post-image-body')
        let newPostModal = document.getElementsByClassName('post-inner-body')[0]
        let click_target = e.target

        if(profDrop.style.display == 'block'){
            if(!profDrop.contains(click_target)){
                profDrop.style.display = 'none'
            }
        }
        else if (mentionDrop.style.display == 'block'){
            if (!mentionDrop.contains(click_target)){
                mentionDrop.style.display = 'none'
            }
        }
        else if(newPostWindow.style.display == 'block'){
            if(!newPostModal.contains(click_target)){
                newPostWindow.style.display = 'none'
            }
        }
        else if (newPostButton.contains(click_target)){
            newPostWindow.style.display = 'block'
        }
        else if (mentionButton.contains(click_target)){
            mentionDrop.style.display = 'block'
        }
        else if (profButtonPicture.contains(click_target)){
            profDrop.style.display = 'block'
        }
    });
});