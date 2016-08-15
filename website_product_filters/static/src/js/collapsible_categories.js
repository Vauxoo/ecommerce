(function(){
  'use strict';
    openerp.website.if_dom_contains("#o_shop_collapse_category", function(){
        if(!$('#o_shop_collapse_category, .oe_website_sale').length) {
          return $.Deferred().reject("DOM doesn't contain '#o_shop_collapse_category, .oe_website_sale'");
        }
        $('#o_shop_collapse_category').on('click', '.fa-chevron-right',function(){
          $(this).parent().siblings().find('.fa-chevron-down:first').click();
          $(this).parents('li').find('ul:first').show('normal');
          $(this).toggleClass('fa-chevron-down fa-chevron-right');
        });
        $('#o_shop_collapse_category').on('click', '.fa-chevron-down',function(){
          $(this).parent().find('ul:first').hide('normal');
          $(this).toggleClass('fa-chevron-down fa-chevron-right');
        });
    });
    // Collapses the attr filter panels otuside the range set on the website
    // backend settings in the variable maximum_attributes
    openerp.website.if_dom_contains("#products_grid_before", function(){
      var MaxUncollapsed = $('#max-panel-uncollapsed').data('max-uncollapsed'),
          PanelCount = $(".panel-collapse.collapse.in") || [];
          if (PanelCount.length > MaxUncollapsed) {
            var diff = PanelCount.length - MaxUncollapsed,
                toCollapse = PanelCount.slice(PanelCount.length - diff);
            $.each(toCollapse, function(index, value) {
              $(value).removeClass('in');
            });
          }
    });
})();
