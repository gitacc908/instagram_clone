$(function() {
    // profile page modals
    window.addEventListener('click', function(e) {
        let click_target = e.target;
        
        var postWindow;
        var postModalContent;
        var postCloseButton;
        var postModalButton;

        var commentsDrop;
        var commentsButton;

        var postSettingWindow;
        var postSettingCloseButton;
        var postSettingModal;

        let confWindow = document.getElementById("myModal");
        let confModalContent = document.getElementsByClassName("modal-content")[0];
        let confButton = document.getElementById("myBtn");
        let confCloseButton = document.getElementsByClassName("close")[0];
        

        // show post modals on profile
        try {
            postWindow = click_target.closest('.publication-link').closest('.publication').getElementsByClassName('post-window')[0];
            postModalButton = click_target.closest('.publication-link');
            if (postModalButton.contains(click_target)){
                postWindow.style.display = 'block'
            }
              
        }
        // work with opened post modal
        catch (TypeError) {
            $( ".post-window" ).each(function( index ) {
                // get opened modal 
                if (this.style.display == 'block'){
                        // current post modal
                        postWindow = this;
                        postModalContent = this.getElementsByClassName('post-modal-content')[0];
                        postCloseButton = this.getElementsByClassName('postclose')[0];

                        // current post setting modal
                        postSettingWindow = this.querySelector('.post-setting-container');
                        postSettingModal = this.querySelector('.post-setting-inner');
                        postSettingCloseButton = this.querySelector('.close');
                        postSettingButton = this.getElementsByClassName('post__more-options');
                        
                        // current comment dropup
                        commentsDrop = postWindow.nextElementSibling;
                        commentsButton = postWindow.getElementsByClassName('comments_button')[0];

                        if (commentsDrop.style.bottom == '0px'){
                            if (!commentsDrop.contains(click_target)){
                                commentsDrop.style.bottom = '-60%'
                            }
                        }
                        else if(postSettingWindow.style.display == 'flex'){
                            if(!postSettingModal.contains(click_target)){
                                postSettingWindow.style.display = ''
                            }
                            else if(postSettingCloseButton.contains(click_target)){
                                postSettingWindow.style.display = ''
                            }
                        }
                        else if(!postModalContent.contains(click_target)){
                            postWindow.style.display = 'none'
                        }
                        else if(postCloseButton.contains(click_target)){
                            postWindow.style.display = 'none'
                        }
                        else if (commentsButton.contains(click_target)){
                            commentsDrop.style.bottom = '0'
                        }
                        else{
                            for(let postSettingButtonClass = 0; postSettingButtonClass < postSettingButton.length; postSettingButtonClass++){
                                if (postSettingButton[postSettingButtonClass].contains(click_target)){
                                    postSettingWindow.style.display = 'flex'
                                }
                            }
                        }
                       
                }
            });
        }

        // hiding modals
        if(confWindow.style.display == 'block'){
            if(!confModalContent.contains(click_target)){
                confWindow.style.display = 'none'
            }
            else if (confCloseButton.contains(click_target)){
                confWindow.style.display = 'none'
            }
        }

        // showing modals
        else if (confButton.contains(click_target)){
            confWindow.style.display = 'block'
        }

    });


});
