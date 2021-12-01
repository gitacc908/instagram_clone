$(function() {

    window.addEventListener('click', function(e) {
        // e.preventDefault();
        let click_target = e.target
        let profButtonPicture = document.getElementsByClassName('profile-button__picture')[0]
        let profDrop = document.getElementById('profile-drop')
        let mentionDrop = document.getElementsByClassName('mention_drop')[0]
        let mentionButton = document.getElementById('mention_button')
        let newPostButton = document.getElementsByClassName('new-post')

        let newPostWindow = document.getElementById('post-image-body')
        let newPostModal = document.getElementsByClassName('post-inner-body')[0]
        
        
        try{
            var sharePostCloseButton = document.getElementsByClassName('x-button')[0]
            var sharePostWindow = document.getElementsByClassName('share-post')[0]
            var sharePostModal = document.getElementsByClassName('inner-share-block')[0]
            var shareButton = e.target.parentNode.parentNode.parentNode.getElementsByClassName('share-button')[0]

            if(sharePostWindow.style.display == 'block'){
                if(!sharePostModal.contains(click_target)){
                    sharePostWindow.style.display = 'none'
                }
                else if(sharePostCloseButton.contains(click_target)){
                    sharePostWindow.style.display = 'none'
                }
            }
            else if(shareButton){
                if (shareButton.contains(click_target)){
                    sharePostWindow.style.display = 'block'
                }
            }
        }
        catch(TypeError){
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
            // Opening Modal Blocks
            else if (mentionButton.contains(click_target)){
                mentionDrop.style.display = 'block'
            }
            else if (profButtonPicture.contains(click_target)){
                profDrop.style.display = 'block'
            }

            for(let newPostClass = 0; newPostClass < newPostButton.length; newPostClass++){
                if (newPostButton[newPostClass].contains(click_target)){
                    newPostWindow.style.display = 'block'
                }
            }
        }
      
        finally{
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
            // Opening Modal Blocks
            else if (mentionButton.contains(click_target)){
                mentionDrop.style.display = 'block'
            }
            else if (profButtonPicture.contains(click_target)){
                profDrop.style.display = 'block'
            }

            for(let newPostClass = 0; newPostClass < newPostButton.length; newPostClass++){
                if (newPostButton[newPostClass].contains(click_target)){
                    newPostWindow.style.display = 'block'
                }
            }
        }
    });

});
