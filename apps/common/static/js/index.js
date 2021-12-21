$(document).ready(function(){

    $('.posts').on('click', '.like_button', function(){
        let pathEl = this.getElementsByTagName('path')[0];
        let likesTag = this.parentNode.parentNode.getElementsByClassName('likes-count')[0];
        let totalLikes = parseInt(likesTag.text);
        let postId = this.parentNode.parentNode.getAttribute('data-post-id');
        $.ajax({
            url : $('#posts-id').attr('data-like-url'),
            type : "POST", 
            data : {'post_id': postId}, 
            success : function(data) {
                if (data.status == 'liked'){
                    pathEl.style.fill = 'rgb(237, 73, 86)';
                    pathEl.style.stroke = 'rgb(237, 73, 86)';
                    likesTag.text = totalLikes += 1;
                }
                else if (data.status == 'unliked'){
                    pathEl.style.fill = '#fdfdfd';
                    pathEl.style.stroke = '#000000';
                    likesTag.text = totalLikes -= 1;
                }
            },
            error : function(data) {
                console.log('not success')
            }
        });

    });
    $('.posts').on('click', '.save-button', function(){
        let pathEl = this.getElementsByTagName('path')[0];
        let postId = this.parentNode.parentNode.getAttribute('data-post-id');
        $.ajax({
            url : $('#posts-id').attr('data-save-url'),
            type : "POST", 
            data : {'post_id': postId}, 
            success : function(data) {
                if (data.status == 'saved'){
                    pathEl.style.fill = '#262626'
                }
                else if (data.status == 'removed'){
                    pathEl.style.fill = '#ffffff'
                }
            },
            error : function(data) {
                console.log('not success')
            }
        });
    });

    window.addEventListener('click', function(e) {
        var sharePostCloseButton = document.getElementsByClassName('x-button')[0]
        var sharePostWindow = document.getElementsByClassName('share-post')[0]
        var sharePostModal = document.getElementsByClassName('inner-share-block')[0]
        var shareButton = e.target.parentNode.parentNode.parentNode.getElementsByClassName('share-button')[0]
        let click_target = e.target
    
    
        // hide modals
        if(sharePostWindow.style.display == 'block'){
            if(!sharePostModal.contains(click_target)){
                sharePostWindow.style.display = 'none'
            }
            else if(sharePostCloseButton.contains(click_target)){
                sharePostWindow.style.display = 'none'
            }
        }

        // show modals
        else if (shareButton.contains(click_target)){
            sharePostWindow.style.display = 'block'
        }
    
    
    
    });

});