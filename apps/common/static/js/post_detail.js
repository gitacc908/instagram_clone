$(function(){

    window.addEventListener('click', function(e) {
        let commentsButton = document.querySelector('.comments_button')
        let commentsBody = document.querySelector('.comments') 
        let commentsCloseButton = document.querySelector('.closebtn')

        let postSettingWindow = document.querySelector('.post-setting-container');
        let postSettingModal = document.querySelector('.post-setting-inner');
        let postSettingCloseButton = document.querySelector('.close');
        let postSettingButton = document.getElementsByClassName('post__more-options');

        // hide modals
        if(commentsBody.style.bottom == '0px'){
            if(!commentsBody.contains(e.target)){
                commentsBody.style.bottom = '-60%'
            }
            else if(commentsCloseButton.contains(e.target)){
                commentsBody.style.bottom = '-60%'
            }
        }
        else if(postSettingWindow.style.display == 'flex'){
            if(!postSettingModal.contains(e.target)){
                postSettingWindow.style.display = ''
            }
            else if(postSettingCloseButton.contains(e.target)){
                postSettingWindow.style.display = ''
            }
        }
        // show modals
        else if(commentsButton.contains(e.target)){
            commentsBody.style.bottom = '0px'
        }
        else {
            for(let postSettingButtonClass = 0; postSettingButtonClass < postSettingButton.length; postSettingButtonClass++){
                if (postSettingButton[postSettingButtonClass].contains(e.target)){
                    postSettingWindow.style.display = 'flex'
                }
            }
        }
    });


});