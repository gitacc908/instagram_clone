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
});