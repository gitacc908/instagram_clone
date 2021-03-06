$(document).ready(function(){

    // open page with saved posts tab
    $('#saved_url').click(function(){
        localStorage.setItem("saved", 'saved'); 
    });

    // Unable or disable comment button
    $('#posts-id').on("input", "input.comment-input", function() {
        if (this.value == "") {
            this.nextElementSibling.setAttribute('disabled', '');
        }
        else{
            this.nextElementSibling.removeAttribute('disabled');
        }
    });
    $('.comment-input').on('input', function(){
        if (this.value == "") {
            localStorage.removeItem('data');
            this.nextElementSibling.setAttribute('disabled', '');
        }
        else{
            this.nextElementSibling.removeAttribute('disabled');
        }
    });

    // Insert comments below post
    $('.send-comment').click(function(){
        let parentItem = this.parentNode.parentNode.parentNode.parentNode;
        var mobileCommentSection = parentItem.getElementsByClassName('post-actions-comments-mobile')[0];
            try{
                // check if its main page
                var commentSection = parentItem.getElementsByClassName('my-comments')[0];
                var commentCounter = parentItem.getElementsByClassName('comment-counter')[0];
                var totalComments = parseInt(commentCounter.textContent);
            }
            catch(TypeError){
                // profile page 
                var commentList = parentItem.previousElementSibling;
            }
        var profImage = document.getElementById('prof-image');
        let postId = this.getAttribute('data-post-id');
        let commentButton = this;
        let commentInput = this.previousElementSibling;
        let comment = commentInput.value;

        // add reply
        let data = JSON.parse(localStorage.getItem('data'))
        commentText = comment.split(" ")

        try{
            if (commentText[0] == `@${data.username}`){
                var replyUrl = $('#posts-id').attr('data-reply-url');
                $.ajax({
                    type: 'POST',
                    url : replyUrl,
                    data: {'commentId': data.commentId, 'replyText': comment},
                    success: function(data){
                        commentInput.value = "";
                        commentButton.setAttribute('disabled', '');
                        $('.notification-text').html('Reply has been added');
                        $('#notify').fadeIn('slow');
                        $('#notify').delay(3000).fadeOut();
                        localStorage.removeItem('data');
                        // return;
                    },
                    error: function(data){
                        $('.notification-text').html("Couldn't update reply");
                        $('#notify').fadeIn('slow');
                        $('#notify').delay(3000).fadeOut();
                        // return;
                    }
                })
            }
        }
        catch(TypeError){
            // add comment 
            let username = this.getAttribute('data-author-of-comment');
            $.ajax({
                url : $('#posts-id').attr('data-comment-url'),
                type : "POST", 
                data : {'post_id': postId, 'comment': comment}, 
                success : function(data) {
                    // check which page is this
                    if (totalComments){
                        $(`<div class="post__description addedcomment">
                                        <span>
                                            <a class="post__name--underline" href="#" target="_blank">${username}</a>
                                            ${comment}
                                        </span>
                        </div>`).appendTo(commentSection);
                        commentCounter.textContent = totalComments += 1;
                        commentInput.value = ""; // clear input after comment insert
                        commentButton.setAttribute('disabled', '');
                    }
                    else if(mobileCommentSection){
                        $(`<div class="user-post-action-comment">
                        <div class="user-profile-comment">
                        <a href="#">
                        <img src="${profImage.src}" alt="">
                        </a>
                        </div>
                        <div class="user-comment">
                        <span class="user-name">${username}</span>
                        <p>${comment}</p>
                        <div class="action-buttons">
                        <a href="#" class="action-button data-comment">????????????</a><button class="action-button">????????????????: <a href="#" class="comment-like-counter">0</a></button><button class="action-button reply-button" data-comment-id=${data.comment_id}>????????????????</button><button class="action-button complaint">??????</button>
                        </div>
                        </div>
                        <button class="like-comment" data-comment-id=${data.comment_id}>
                            <svg fill="white" stroke="black" aria-label="???? ????????????????" class="_8-yf5 " color="#ed4956" height="12" role="img" viewBox="0 0 48 48" width="12"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>
                        </button>
                    </div>`).appendTo(mobileCommentSection);
                    commentInput.value = "";
                    commentButton.setAttribute('disabled', '');
                    mobileCommentSection.scrollTop = mobileCommentSection.scrollHeight;
                    }
                    else{
                        $(`<div class="user-post-action-comment">
                                <div class="user-profile-comment">
                                    <a href="#">
                                    <img src="${profImage.src}" alt="">
                                    </a>
                                </div>
                                <div class="user-comment">
                                    <span class="user-name">${username}</span>
                                    <p>${comment}</p>
                                    <div class="action-buttons">
                                    <a href="#" class="action-button data-comment">????????????</a><button class="action-button">????????????????: <a href="#" class="comment-like-counter">0</a></button><button class="action-button reply-button" data-comment-id=${data.comment_id}>????????????????</button><button class="action-button complaint">??????</button>
                                    </div>
                                </div>
                                <button class="like-comment" data-comment-id=${data.comment_id}>
                                <svg fill="white" stroke="black" aria-label="???? ????????????????" class="_8-yf5 " color="#ed4956" height="12" role="img" viewBox="0 0 48 48" width="12"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>
                                </button>
                        </div>`).appendTo(commentList)
                        commentInput.value = "";
                        commentButton.setAttribute('disabled', '');
                        if(commentList){
                            commentList.scrollTop = commentList.scrollHeight;
                        }
                    }
                },
                error : function(data) {
                    console.log('not success')
                }
            });
        }
    });

    $('.post-button').click(function(){
        $('#image-loader').click();
    });
    $('#image-loader').change(function(){
        let files = this.files;
        let postBody = $('.post-body');
        let postPreview = $('.post-preview');

        if(files){ // if user chose some images
            postBody.css('display', 'none');
            postPreview.css('display', 'block');
            for(let i = 0; i<files.length; i++){
                if(i == 0){
                    let reader = new FileReader();
                    reader.onload = function(event){
                        $($.parseHTML('<img class="item main">'))
                        .attr('src', event.target.result).appendTo(postPreview.find('.carousel'));
                    }
                    reader.readAsDataURL(files[i]);
                }
                else{
                    let reader = new FileReader();
                    reader.onload = function(event){
                        $($.parseHTML('<img class="item">'))
                        .attr('src', event.target.result).appendTo(postPreview.find('.carousel'));
                    }
                    reader.readAsDataURL(files[i]);
                }
        
            }
        }
        if (files.length > 1){
            postPreview.find('.navigation').css('display', 'block');
            const images = document.querySelector('.carousel').children;
            const prev = document.querySelector('.prev');
            const next = document.querySelector('.next');
            let index = 0;


            prev.addEventListener('click', () => {
            nextImage('next');
            })

            next.addEventListener('click', () => {
            nextImage('prev');
            })

            function nextImage(direction) {
                if(direction == 'next') {
                    index++;
                    if(index == files.length) {
                        index = 0;
                    }
                } else {
                    if(index == 0) {
                        index = files.length - 1;
                    } else {
                        index--;
                    }
                }
                for(let i = 0; i < files.length; i++) {
                    images[i].classList.remove('main');
                }
                images[index].classList.add('main');
            }
        }
    });


    // publish new post
    $('#share-post').click(function(){

        let postPreview = $('.post-preview');
        let postBody = $('.post-body');
        let input = $('#image-loader');
        let shareUrl = input.attr('data-share-url');
        let files = input.prop('files');

        // collect form data with multiple images
        let body = $('#share-body');
        var formData = new FormData();
        formData.append('body', body.val());
        formData.append('comments_off', $('#f21c8f774f0e2a4').is(':checked'));
        for (var index = 0; index < files.length; index++) {
            formData.append("images", files[index]);
        }
         $.ajax({
            type : "POST", 
            url : shareUrl,
            cache: false,
            processData: false,
            contentType: false,
            enctype: 'multipart/form-data',
            data : formData, 
            success : function(data) {
                // clear out data
                body.val('');
                input.val('');
                // setting modals to its default css values
                postPreview.css('display', '');
                postBody.css('display', '');
                postBody.css('visibility', 'hidden');
                postPreview.find('.carousel').empty();
                postPreview.find('.navigation').css('display', '');
                console.log('success')
                $('.success-alert').css('visibility', 'visible');
                $('#success-gif').attr('src', '/static/img/10a8cbeb94ba.gif')
                setTimeout(function() {
                    $('.success-alert').css('visibility', '');
                    postBody.css('visibility', '');
                }, 2000); 
            },
            error : function(data) {
                console.log('not success')
            }
        });

    });

    $('.follow').click(function(){
        let followButton = $(this);
        $.ajax({
            type : "POST",
            url : $(this).attr('data-follow-url'),
            data : {follow_user_id:$(this).attr('data-user-id')},
            success: function(data){
                if(data.status == 'followed'){
                    followButton.text('Unfollow')
                }
                else if (data.status == 'unfollowed'){
                    followButton.text('Follow')
                }
            },
            error: function(data){
                console.log('error')
            }
        });
    });

});