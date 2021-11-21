$(document).ready(function(){

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

    // Unable or disable comment button
    $('.comment-input').on('input', function() {
        if (this.value == "") {
            this.nextElementSibling.setAttribute('disabled', '');
        }
        else{
            this.nextElementSibling.removeAttribute('disabled');
        }
    });

    // Insert comments below post
    $('.send-comment').click(function(){
        let parentItem = this.parentNode.parentNode.parentNode.parentNode;
        let commentSection = parentItem.getElementsByClassName('my-comments')[0];
        let commentCounter = parentItem.getElementsByClassName('comment-counter')[0];
        let totalComments = parseInt(commentCounter.textContent);
        let postId = this.getAttribute('data-post-id');
        let commentButton = this;
        let commentInput = this.previousElementSibling;
        let comment = commentInput.value;
        let username = document.getElementById('myusername').textContent;
        $.ajax({
            url : $('#posts-id').attr('data-comment-url'),
            type : "POST", 
            data : {'post_id': postId, 'comment': comment}, 
            success : function(data) {
                if (data.status == 'created'){
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
            },
            error : function(data) {
                console.log('not success')
            }
        });
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

});