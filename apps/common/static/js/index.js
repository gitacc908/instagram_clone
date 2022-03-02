$(document).ready(function(){

    $('.posts').on('click', '.like_button', function(){
        let pathEl = this.getElementsByTagName('path')[0];
        let previousAction = this.querySelector('path').getAttribute('data-action');
        let likesTag = this.parentNode.parentNode.getElementsByClassName('likes-count')[0];
        let totalLikes = parseInt(likesTag.text);
        let postId = this.parentNode.parentNode.getAttribute('data-post-id');
        if (previousAction == 'like'){
            pathEl.style.fill = 'rgb(237, 73, 86)';
            pathEl.style.stroke = 'rgb(237, 73, 86)';
            likesTag.text = totalLikes += 1;

            this.querySelector('path').setAttribute('data-action', 'unlike');
        }
        else{
            pathEl.style.fill = '#fdfdfd';
            pathEl.style.stroke = '#000000';
            likesTag.text = totalLikes -= 1;
            this.querySelector('path').setAttribute('data-action', 'like');

        }

        $.ajax({
            url : $('#posts-id').attr('data-like-url'),
            type : "POST", 
            data : {'post_id': postId}, 
            success : function(data) {
                console.log(' success')
                // if (data.status == 'liked'){
                //     pathEl.style.fill = 'rgb(237, 73, 86)';
                //     pathEl.style.stroke = 'rgb(237, 73, 86)';
                //     likesTag.text = totalLikes += 1;
                // }
                // else if (data.status == 'unliked'){
                //     pathEl.style.fill = '#fdfdfd';
                //     pathEl.style.stroke = '#000000';
                //     likesTag.text = totalLikes -= 1;
                // }
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
        let click_target = e.target

        // hide share post modal
        $( ".share-post" ).each(function( index ) {
            if(this.style.display == 'block'){
                let sharePostWindow = this;
                let sharePostCloseButton = this.querySelector('.x-button')
                let sharePostModal = this.querySelector('.inner-share-block')
                if(!sharePostModal.contains(click_target)){
                    sharePostWindow.style.display = ''
                }
                else if(sharePostCloseButton.contains(click_target)){
                    sharePostWindow.style.display = ''
                }
            }
        });
        // show share post modal
        $( ".share-button" ).each(function( index ) {
            if (this.contains(click_target)){
                let sharePostWindow = this.closest(".post").nextElementSibling
                sharePostWindow.style.display = 'block'
            }
        });

        // hide post setting modal
        $( ".post-setting-container" ).each(function( index ) {
            // get opened modal 
            if (this.style.display == 'flex'){
                let postSettingWindow = this;
                let postSettingCloseButton = this.querySelector('.close')
                let postSettingModal = this.querySelector('.post-setting-inner')
                if(!postSettingModal.contains(click_target)){
                    postSettingWindow.style.display = ''
                }
                else if(postSettingCloseButton.contains(click_target)){
                    postSettingWindow.style.display = ''
                }
            }
        });
        // show post setting modal
        $( ".post__more-options" ).each(function( index ) {
            // get opened modal 
            if (this.contains(click_target)){
                let postSettingWindow = this.closest(".post").previousElementSibling
                postSettingWindow.style.display = 'flex'
            }
        });

        $('.posts').on('click', '.copy-link', function(){
            var dummy = document.createElement('input')
            var postLink = this.closest('.post-setting-container').querySelector('.post-link')
            var text = postLink.getAttribute('href')
            var domain = postLink.getAttribute('data-domain')
            var link = `${domain}${text}`
            document.body.appendChild(dummy);
            dummy.value = link;
            dummy.select();
            console.log(link)
            document.execCommand('copy');
            document.body.removeChild(dummy);
            $('.notification-text').html('Link has been copied!');
            $('#notify').fadeIn('slow');
            $('#notify').delay(3000).fadeOut();
            
            // close current modal
            $( ".post-setting-container" ).each(function( index ) {
                if (this.style.display == 'flex'){
                    this.style.display = ''
                }
            });
        });
    });

    $('#create-story').click(function(){
        $('#story-input').trigger('click'); 
    });

    $('#story-input').on('change',function(){
        let file = this.files[0];
        var storyCont = $('#public_open_story');
        if(file){
            let reader = new FileReader();
            reader.onload = function(event){
                $($.parseHTML('<img>'))
                .attr('src', event.target.result).appendTo(storyCont.find('.story_content_media'));
            }
            reader.readAsDataURL(file);
            storyCont.css({'visibility': 'visible', 'opacity': '1', 'transform': 'scale(1.0)'})
        }
    });

    $('#close-story-create-container').click(function(){
        var storyCont =  $('#public_open_story');
        storyCont.css({'visibility': '', 'opacity': '', 'transform': ''})
        $('#story-input').val(''); 
        storyCont.find('.story_content_media').empty();
    });

    $('#add-story').click(function(){
        var input = $('#story-input')
        var data = new FormData(input.closest('form').get(0));
        $.ajax({
            type : "POST",
            url : input.closest('form').attr('action'),
            processData: false,
            contentType: false,
            data : data,
            success : function(data) {
                var storyCont =  $('#public_open_story');
                storyCont.css({'visibility': '', 'opacity': '', 'transform': ''})
                input.val('');
                storyCont.find('.story_content_media').empty();
                $('.notification-text').html("Your story was updated!");
                $('#notify').fadeIn('slow')
                $('#notify').delay(5000).fadeOut('slow');
            },
            error : function(data) {
                console.log('something went wrong!')
            }
        });

    });

});
