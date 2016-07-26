$(document).ready(function () {
$('.oe_website_sale').each(function () {
    $('form.js_attributes_sorter').on('change', function () {
        var $form =$(this).closest("form");
        var search_query = $('.search-query').val();
        var input = $("<input>")
                     .attr("type", "hidden")
                     .attr("name", "search").val(search_query);
        $form.append($(input));
        var selected_val = $("input[name='product_sorter']:checked", $form).val();
        if (selected_val) {
            $("#product_sorter").val(selected_val);
        }
        $("form.js_attributes input, form.js_attributes select").closest('form#main-js-attributes').submit();
        $form.submit(function(ev) {
            ev.preventDefault();
            $("#main-js-attributes").submit();
        });
    });

});
});
