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

        let confWindow = document.getElementById("myModal");
        let confModalContent = document.getElementsByClassName("modal-content")[0];
        let confButton = document.getElementById("myBtn");
        let confCloseButton = document.getElementsByClassName("close")[0];
        
        try {
            postWindow = click_target.closest('.publication-link').closest('.publication').getElementsByClassName('post-window')[0];
            postModalButton = click_target.closest('.publication-link');
            if (postModalButton.contains(click_target)){
                postWindow.style.display = 'block'
            }
              
        }
        catch (TypeError) {
            $( ".post-window" ).each(function( index ) {
                // get opened modal 
                if (this.style.display == 'block'){
                        postWindow = this;
                        postModalContent = this.getElementsByClassName('post-modal-content')[0];
                        postCloseButton = this.getElementsByClassName('postclose')[0];
                        
                        commentsDrop = postWindow.nextElementSibling;
                        commentsButton = postWindow.getElementsByClassName('comments_button')[0];

                        if (commentsDrop.style.bottom == '0px'){
                            if (!commentsDrop.contains(click_target)){
                                commentsDrop.style.bottom = '-60%'
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


// function openNav() {document.getElementById("comments").style.bottom = "0";}
// function closeNav() {document.getElementById("comments").style.bottom = "-60%";}
