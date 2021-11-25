    $(function() {

        window.addEventListener('click', function(e) {

            // profile page modals
            let click_target = e.target
            var confWindow = document.getElementById("myModal");
            var confModalContent = document.getElementsByClassName("modal-content")[0];
            var confButton = document.getElementById("myBtn");
            var confCloseButton = document.getElementsByClassName("close")[0];


            if(confWindow.style.display == 'block'){
                if(!confModalContent.contains(click_target)){
                    confWindow.style.display = 'none'
                }
                else if(confCloseButton.contains(click_target)){
                    confWindow.style.display = 'none'
                }
            }
            else if (confButton.contains(click_target)){
                confWindow.style.display = 'block'
            }
                
        });


    });
