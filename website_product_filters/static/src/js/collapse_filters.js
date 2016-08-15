(function(){
  'use strict';
    openerp.website.if_dom_contains('.js_attributes', function () {

      /* this method hides and shows all lists of attributes that are longer
         than 4 lines. */
      $(".show-more").click(function(){
        var $element = $(this),
            parent = $element.parent(),
            button = $element,
            hidden_elements = parent.find(".hidden");
        if (button.hasClass("clicked")){
          var shown_elements = parent.find(".un-hidden");
          shown_elements.addClass("hidden");
          shown_elements.removeClass("un-hidden");
          button.html('<a class="show-more"><span class="fa fa-plus-square"></span> Show More</a>');
          button.removeClass("clicked");
        }
        else {
          hidden_elements.removeClass("hidden");
          hidden_elements.addClass("un-hidden");
          button.html('<a class="show-more"><span class="fa fa-minus-square"></span> Show Less</a>');
          button.addClass("clicked");
        }
        });
  });

})();
