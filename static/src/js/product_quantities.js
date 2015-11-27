(function() {
    'use strict';

    openerp.website.if_dom_contains('.js_attributes', function(){
        console.log("loaded shit ===");
        $.ajax({
          url: "/get_prods",
          method: "POST",
          data: { category: $("#products_grid_before li.active").data("categid")},
          beforeSend: function( xhr ) {
            $('*[data-oe-model="product.attribute.value"]').after(' <i class="fa fa-spinner fa-spin"></i>');
          }
        }).done(function( data ) {
            if ( console && console.log ) {
              console.log( "Sample of data:", data);
              $.each(JSON.parse(data), function(i, obj) {
                console.log(obj.id);
                console.log(obj.qty);
              $('*[data-oe-model="product.attribute.value"][data-oe-id="'+obj.id+'"]').next().replaceWith('<span class="badge">'+obj.qty+'</span>');
              });
            }
          });
    });

}());