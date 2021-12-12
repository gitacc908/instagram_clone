$(document).ready(function(){
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

});