jQuery(document).ready(function($) {

        var slide_images = ['static/img/0a2d3016f375.jpg', 'static/img/6f03eb85463c.jpg', 
                            'static/img/d6bf0c928b5a.jpg', 'static/img/f0c687aa6ec2.jpg']

        var i = 1;
        function myLoop() { 
          setTimeout(function() {
            $('#image').attr('src', slide_images[i])
            i++;
            if (i < 4) {
              myLoop();
            }
            else if (i == 4){
              i = 0;
              myLoop();
            }
          }, 2000)
        }
        
        myLoop();
});