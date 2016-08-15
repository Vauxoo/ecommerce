(function(){
    'use strict';
    openerp.Tour.register({
        id: 'test_special_cases',
        name: 'Test Special Cases',
        path: '/shop',
        mode: 'test',
        steps: [
            {
                title: 'Wait for JSON',
                content: 'Step made to test a special case when a category without products is called to get products per attribute.',
                element: 'body',
                onload: function() {
                    $.get( "/get_prods?category=23", function( data ) {
                        if (data !== "[]") {
                            return false;
                        }
                    });
                }
            },
            {
                title: 'Wait for JSON Ranges',
                content: 'Step made to test a special case when a category without products is called to get products per price range.',
                element: 'body',
                onload: function() {
                    $.get( "/get_ranges?category=23", function( data ) {
                        if (data !== "[]") {
                            return false;
                        }
                    });
                }
            },
            {
                title: 'Test Cookie Unset',
                content: 'test a special case when a being at the database selector cookie must be unset.',
                element: 'body',
                onload: function() {
                    $.get( "/web/database/manager#action=database_manager", function( data ) {
                            return data;
                    });
                }
            },
        ],
    });
}());

