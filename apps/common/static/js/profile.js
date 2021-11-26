    $(function() {

        window.addEventListener('click', function(e) {

            // profile page modals
            let click_target = e.target
            var confWindow = document.getElementById("myModal");
            var confModalContent = document.getElementsByClassName("modal-content")[0];
            var confButton = document.getElementById("myBtn");
            var confCloseButton = document.getElementsByClassName("close")[0];


        // post page modals
        var confWindowPost = document.getElementById("postModal");
        var confModalContentPost = document.getElementsByClassName("post-modal-content")[0];
        var confButtonPost = document.getElementById("postBtn");
        var confCloseButtonPost = document.getElementsByClassName("postclose")[0];

        


        if(confWindow.style.display == 'block'){
            if(!confModalContent.contains(click_target)){
                confWindow.style.display = 'none'

            }
            else if (confButton.contains(click_target)){
                confWindow.style.display = 'block'
            }
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


