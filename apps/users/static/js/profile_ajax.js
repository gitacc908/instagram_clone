$(document).ready(function(){
	// like comments
    $('.post-actions-comments, .post-actions-comments-mobile').on('click', 'button.like-comment', function(){
		let heartIcon = this.querySelector('._8-yf5');
		let commentLikesTag = this.previousElementSibling.querySelector('.comment-like-counter');
		let totalLikes = parseInt(commentLikesTag.text);
		let comment_id = this.getAttribute('data-comment-id');
		let url = this.parentNode.parentNode.getAttribute('data-comment-like-url');

		$.ajax({
			url : url,
			type : 'POST',
			data : {'comment_id' : comment_id},
			success : function(data) {
                if (data.status == 'liked'){
					heartIcon.style.fill = 'rgb(237, 73, 86)';
					heartIcon.style.stroke = 'rgb(237, 73, 86)';
                    commentLikesTag.text = totalLikes += 1;
                }
                else if (data.status == 'unliked'){
                    heartIcon.style.fill = '#fdfdfd';
                    heartIcon.style.stroke = '#000000';
                    commentLikesTag.text = totalLikes -= 1;
                }
            },
            error : function(data) {
                console.log('not success')
            }
		})

	});
	// prepare for reply on comment
	$('.post-actions-comments, .post-actions-comments-mobile').on('click', '.reply-button', function(){
		let commentId = $(this).attr('data-comment-id');
		let username = this.closest('.user-comment').querySelector('.user-name').innerHTML; //get author of comment
		try{
			var commentInput = this.closest('.post-actions').querySelector('.comment-input');
		}
		catch(TypeError){
			var commentInput = this.closest('.comments').querySelector('.comment-input');
		}

		commentInput.value = `@${username} `//fill in input with username
		dct = {
			'commentId':commentId,
			'username': username,
		}
		localStorage.setItem('data', JSON.stringify(dct))
	});
	$('.show-replies').click(function(){
		let replies = this.closest('.reply-counter').nextElementSibling;
		if (replies.style.display=='block'){
			replies.style.display = ''
		}
		else{
			replies.style.display = 'block'
		}
	
	});
	$('#upload_image').click(function(){
		document.getElementById("upload_image_input").click();
	});


    // Like or unlike post
    $('.like_button').click(function(){
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

    // Save or remove post
    $('.save-button').click(function(){
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

    // copy link of post
    $('.copy-link').click(function(){
        var dummy = document.createElement('input')
        var postLink = this.closest('.post-setting-container').querySelector('.post-link')
        var text = postLink.getAttribute('href')
        var domain = postLink.getAttribute('data-domain')
        var link = `${domain}${text}`
        document.body.appendChild(dummy);
        dummy.value = link;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        $('.notification-text').html('Link has been copied!');
        $('#notify').fadeIn('slow');
        $('#notify').delay(3000).fadeOut();
        
    });
    
    var send_dm_button = document.querySelector('.send-message')
    if (send_dm_button){
        send_dm_button.onclick = function(){
            dm_username = document.querySelector('.header-profile-username')
            localStorage.setItem('dm_username', dm_username.textContent)
        }
    }

});