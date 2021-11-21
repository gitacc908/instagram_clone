$(function() {

    window.addEventListener('click', function(e) {
        // e.preventDefault();
        let click_target = e.target
        let profButtonPicture = document.getElementsByClassName('profile-button__picture')[0]
        let profDrop = document.getElementById('profile-drop')
        let mentionDrop = document.getElementsByClassName('mention_drop')[0]
        let mentionButton = document.getElementById('mention_button')
        let newPostButton = document.getElementById('new-post')
        let newPostWindow = document.getElementById('post-image-body')
        let newPostModal = document.getElementsByClassName('post-inner-body')[0]
        let sharePostCloseButton = document.getElementsByClassName('x-button')[0]
        let sharePostWindow = document.getElementsByClassName('share-post')[0]
        let sharePostModal = document.getElementsByClassName('inner-share-block')[0]
        let shareButton = e.target.parentNode.parentNode.parentNode.getElementsByClassName('share-button')[0]

        
        // Closing Modal Blocks
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
        else if(sharePostWindow.style.display == 'block'){
            if(!sharePostModal.contains(click_target)){
                sharePostWindow.style.display = 'none'
            }
            else if(sharePostCloseButton.contains(click_target)){
                sharePostWindow.style.display = 'none'
            }
        }

        // Opening Modal Blocks
        else if(shareButton){
            if (shareButton.contains(click_target)){
                sharePostWindow.style.display = 'block'
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
