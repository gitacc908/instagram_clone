$(function(){


  class SlideStories {
    constructor(id) {
      this.slide = document.querySelector(`[data-slide="${id}"]`);
      this.active = 0;
      this.init();
    }
  
    activeSlide(index) {
      this.active = index;
      this.items.forEach((item) => item.classList.remove('active'));
      this.items[index].classList.add('active');
      this.thumbItems.forEach((item) => item.classList.remove('active'));
      this.thumbItems[index].classList.add('active');
      this.autoSlide();
    }
  
    prev() {
      if (this.active > 0) {
        this.activeSlide(this.active - 1);
      } else {
        this.activeSlide(this.items.length - 1);
      }
    }
  
    next() {
      if (this.active < this.items.length - 1) {
        this.activeSlide(this.active + 1);
      } else {
        this.activeSlide(0);
      }
    }
  
    addNavigation() {
      const nextBtn = this.slide.querySelector('.slide-next');
      const prevBtn = this.slide.querySelector('.slide-prev');
      nextBtn.addEventListener('click', this.next);
      prevBtn.addEventListener('click', this.prev);
    }
  
    addThumbItems() {
      this.items.forEach(() => (this.thumb.innerHTML += `<span></span>`));
      this.thumbItems = Array.from(this.thumb.children);
    }

    autoSlide() {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(this.next, 5000);
    }

    init() {
      this.next = this.next.bind(this);
      this.prev = this.prev.bind(this);
      this.items = this.slide.querySelectorAll('.slide-items > *');
      this.thumb = this.slide.querySelector('.slide-thumb');
      this.addThumbItems();
      this.activeSlide(0);
      this.addNavigation();
    }
  }


  var userStoryButtons = document.querySelectorAll('.user_story_button');
  for (let i=0; userStoryButtons.length > i; i++){
      userStoryButtons[i].onclick = function(){
        var userId = userStoryButtons[i].dataset.username
        var userStoryContainer = document.querySelector(`#${userId}`)
        var slide = $(`#${userId}`).find('.slide')
        if (userStoryContainer.style.visibility != 'visible'){
            userStoryContainer.style.visibility = 'visible';
            userStoryContainer.style.transform = 'scale(1.0)';
            userStoryContainer.style.opacity = '1';
            new SlideStories(slide.attr('data-slide'));
        }
      }
  }
  var userStoryCloseButtons = document.querySelectorAll('.close_story');
  for (let i=0; userStoryCloseButtons.length > i; i++){
    userStoryCloseButtons[i].onclick = function(){
      var storyModal = userStoryCloseButtons[i].closest('.story_modal');
      if (storyModal.style.visibility == 'visible'){
          storyModal.style.visibility = ''
          storyModal.style.transform = ''
          storyModal.style.opacity = ''
          storyModal.querySelector('.slide-thumb').innerHTML = ''
      }
    }
  }

});
