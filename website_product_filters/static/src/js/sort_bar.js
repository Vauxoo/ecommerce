(function (){
    'use strict';
    openerp.website.if_dom_contains('.sort_bar', function(){
        $('.removable-badge').click(function(ev) {
            ev.preventDefault();
            var $element = $(this),
                value_id = $element.data('attrvalue'),
                unknown_id = $element.data('attr-unknown'),
                brand_id = $element.data('brandvalue'),
                search_tag = $element.data('searchtag'),
                range_id = $element.data('rangevalue');
            $element.parents("h4").remove();
            if (value_id) {
                $('.att-value#'+value_id).trigger('click');
            }
            if (unknown_id) {
                $(".att-unknown[data-id='"+unknown_id+"']").trigger('click');
            }
            if (brand_id) {
                $(".att-brand[data-id='"+brand_id+"']").trigger('click');
            }
            if (range_id) {
                $(".att-range[data-id='"+range_id+"']").trigger('click');
            }
            if (search_tag) {
                $("input[name='search']").val('');
                $("input[name='search']")[0].closest('form').submit();
            }
        });
    });
    openerp.website.if_dom_contains('#search_oncategs_input', function (selector) {
        $(selector).find('span.input-group-btn').on('click', function() {
            $(this).closest('form').submit();
        });
        var listCategories = $(".search-box-category-list") || [];
        $.each(listCategories, function (index, element) {
            $(element).on('click', function () {
                var val = $(this).data('filter-box-categid');
                if (val === 0) {
                    $('#search_oncategs_input input[name="category"]').val("");
                    $(this).closest('form').submit(function () {
                       $(this).children('input[name="category"]').remove();
                    });
                } else {
                    $('#search_oncategs_input input[name="category"]').val(val);
                }
                $('#search_oncategs_input button.dropdown-toggle').html($(this).text() + " <span class='caret'/>");

            });
        });
    });
}());
