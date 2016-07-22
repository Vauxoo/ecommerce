(function () {
    'use strict';
    openerp.website.if_dom_contains('.obfuscated-email', function(selector) {
        var elements = $(selector) || [];
        $.each(elements, function(index, item) {
            var $item = $(item)
            var name = $item.find('a').data('name-email'),
                doma = $item.find('a').data('domain-email');
            $item.find('a').attr('href', 'mailto:'+name+String.fromCharCode(64)+doma);
            $item.find('span').text(name+String.fromCharCode(64)+doma);
        });
    });
})();
