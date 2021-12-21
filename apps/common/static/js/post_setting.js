$(function() {

    window.addEventListener('click', function(e) {
        var click_target = e.target
        var postSettingWindow = document.querySelector('.post-setting-container')
        var postSettingCloseButton = document.querySelector('.close')
        var postSettingModal = document.querySelector('.post-setting-inner')
        // var postSettingButton = document.querySelector('.post__more-options')

        // postSettingWindow.style.display = 'block'
        if(postSettingWindow.style.display == 'block'){
            if(!postSettingModal.contains(click_target)){
                postSettingWindow.style.display = ''
            }
            else if(postSettingCloseButton.contains(click_target)){
                postSettingWindow.style.display = ''
            }
        }
        else{
            $( ".post__more-options" ).each(function( index ) {
                if(this.contains(click_target)){
                    postSettingWindow.style.display = 'block'
                }
            });
        }

   

        // else if (postSettingButton.contains(click_target)){
        //     console.log('button')
        //     postSettingWindow.style.display = 'block'
        // }
    
    });

});
