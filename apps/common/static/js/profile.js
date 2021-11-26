    $(function() {

        window.addEventListener('click', function(e) {

            // profile page modals
            let click_target = e.target
            var confWindow = document.getElementById("myModal");
            var confModalContent = document.getElementsByClassName("modal-content")[0];
            var confButton = document.getElementById("myBtn");
            var confCloseButton = document.getElementsByClassName("close")[0];


<<<<<<< HEAD
        // post page modals
        var confWindowPost = document.getElementById("postModal");
        var confModalContentPost = document.getElementsByClassName("post-modal-content")[0];
        var confButtonPost = document.getElementById("postBtn");
        var confCloseButtonPost = document.getElementsByClassName("postclose")[0];

        


        if(confWindow.style.display == 'block'){
            if(!confModalContent.contains(click_target)){
                confWindow.style.display = 'none'
=======
            if(confWindow.style.display == 'block'){
                if(!confModalContent.contains(click_target)){
                    confWindow.style.display = 'none'
                }
                else if(confCloseButton.contains(click_target)){
                    confWindow.style.display = 'none'
                }
>>>>>>> b9c55f850f0e435072c832b433f913918e6ca5d7
            }
            else if (confButton.contains(click_target)){
                confWindow.style.display = 'block'
            }
<<<<<<< HEAD
        }
        else if (confButton.contains(click_target)){
            confWindow.style.display = 'block'
        }




        if(confWindowPost.style.display == 'block'){
            if(!confModalContentPost.contains(click_target)){
                confWindowPost.style.display = 'none'
            }
            else if(confCloseButtonPost.contains(click_target)){
                confWindowPost.style.display = 'none'
            }
        }
        else if (confButtonPost.contains(click_target)){
            confWindowPost.style.display = 'block'
        }

             
    });


});



function openNav() {document.getElementById("comments").style.bottom = "0";}
function closeNav() {document.getElementById("comments").style.bottom = "-60%";}

=======
                
        });


    });
>>>>>>> b9c55f850f0e435072c832b433f913918e6ca5d7
