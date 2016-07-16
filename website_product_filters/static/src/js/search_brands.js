(function() {
    'use strict';
    openerp.website.if_dom_contains('#input-search-brands', function(){
      $("#input-search-brands").keyup(function () {
          var filter = $(this).val();
          $("ul#filter-brands li").each(function () {
              if ($(this).text().search(new RegExp(filter, "i")) < 0) {
                  $(this).hide();
              } else {
                  $(this).show();
              }
          });
      });

    });
}());
