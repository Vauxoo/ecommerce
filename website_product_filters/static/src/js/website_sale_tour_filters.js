(function (){
    'use strict';
    openerp.Tour.register({
        id: 'shop_test_filters',
        name: 'Test Shop With filters',
        path: '/browse',
        mode: 'test',
        steps: [
            {
                title: 'Click on category Computers',
                element: 'a[href="/browse/computers-2"]',
            },
            {
                title: 'Click on category Devices',
                content: "Here we check if the products on the tree are the right ones to render on popular products",
                waitFor: '.subcategories:contains("Laptops"), .subcategories:contains("Computers"), .subcategories:contains("Devices")',
                element: 'li[data-categid="11"] a',
            },
            {
                title: 'Click on category Keyboard / Mouse',
                content: "This step will wait to see if it finds the subcagtegories on the main div of subcategories",
                waitFor: '.subcategories:contains("Keyboard / Mouse"), .subcategories:contains("Screen"), .subcategories:contains("Speakers")',
                element: 'li[data-categid="15"] a:contains("Keyboard / Mouse")',
            },
            {
                title: 'Select 16 GB filter on memory section',
                waitNot: '*[data-name="iPad Mini"],[data-name="iPad Retina Display"]',
                waitFor: '.js_attributes label:contains(16 GB), .js_attributes label:contains(32 GB)',
                element: 'label:contains(16 GB) input:not(:checked)',
            },
            {
                title: 'Select price range of 0 to 100 USD',
                waitFor: '.sort_bar h4:contains(16 GB)',
                element: '.js_attributes input[name=range]input[value=1]:visible',
            },
            {
                title: 'Click on category Computers',
                waitFor: 'a:contains(Computers)',
                element: 'ul.breadcrumb li:contains(Computers) a:visible',
            },
            {
                title: 'Click on subcategory Computers',
                waitFor: 'a:contains(Computers)',
                element: '.nav-pills ul a:contains(Computers)',
            },
            {
                title: 'Click on category Computer all-in-one',
                waitFor: 'a:contains("Computer all-in-one")',
                element: 'li[data-categid="22"] a:contains("Computer all-in-one")',
            },
            {
                title: 'Filter by 16GB iPad',
                waitFor: '.js_attributes label:contains(16 GB), .js_attributes label:contains(32 GB)',
                element: 'label:contains(16 GB) input:not(:checked)',
            },
            {
                title: 'Filter by White value on iPad',
                waitFor: '.sort_bar h4:contains(16 GB)',
                element: '.js_attributes label.css_attribute_color input[value="2-3"]:visible',
            },
            {
                title: 'Click on Filter 32GB on iPad',
                waitFor: '.sort_bar h4:contains(White)',
                element: 'label:contains(32 GB) input:not(:checked)',
            },
            {
                title: 'Delete 32GB from checkbox list',
                element: '.sort_bar h4:contains(32 GB) a.removable-badge',
            },
            {
                title: 'Uncheck checkbox White Filter',
                element: '.js_attributes label.css_attribute_color input[value="2-3"]:visible',
                waitNot: '.sort_bar h4:contains(32 GB)',
            },
            {
                title: 'Click on Filter 500 - 1000 price range',
                waitNot: '.sort_bar h4:contains(White) a.removable-badge',
                element: 'label:contains(1000) input[value="4"]:not(:checked)',
            },
            {
                title: 'Uncheck checkbox 500 - 1000 price range',
                waitFor: '.sort_bar h4:contains(1000)',
                element: 'label:contains(1000) input[value="4"]:checked',
            },
            {
                title: 'Uncheck checkbox filter by 16GB',
                waitNot: '.sort_bar h4:contains(1000)',
                element: 'label:contains(16 GB) input:checked',
            },
            {
                title: 'Click on Filter Brand Apple',
                waitNot: '.sort_bar h4:contains(16 GB)',
                element: 'label:contains(Apple):visible input:not(:checked)',
            },
            {
                title: 'Uncheck checkbox Brand Apple',
                waitFor: '.sort_bar h4:contains(Apple)',
                element: 'label:contains(Apple):visible input:checked',
            },
            {
                title: 'Click on category Computers',
                waitNot: '.sort_bar h4:contains(Apple)',
                element: 'ul.breadcrumb li:contains(Computers) a:visible',
            },
            {
                title: 'Click on subcategory Computers',
                waitFor: 'a:contains(Computers)',
                element: '.nav-pills ul a:contains(Computers)',
            },
            {
                title: 'Click on category Computer all-in-one',
                waitFor: 'a:contains("Computer all-in-one")',
                element: 'li[data-categid="22"] a:contains("Computer all-in-one")',
            },
            {
                title: 'Click on Filter Unknown Memory',
                waitFor: 'a:contains(Computers)',
                element:   'form.js_attributes label:contains(Unknown) input:not(:checked)',

            },
            {
                title: 'Wait for products to appear and tag to dissapear',
                waitNot: 'h5:contains(iPad Retina Display), h5:contains(iPhone 6s Plus)',
            },
            {
                title: 'Filter by 16GB iPad',
                element: 'form.js_attributes label:contains(16 GB) input:not(:checked)',
                waitFor: '.sort_bar h4:contains(Unknown)',
            },
            {
                title: 'Uncheck the Unknown Memory filter',
                element: 'form.js_attributes label:contains(Unknown) input:checked',
                waitFor: '.sort_bar h4:contains(16 GB)',
            },
            {
                title: 'Click on Filter 500 - 1000 price ranges',
                waitNot: '.sort_bar h4:contains(Unknown) a.removable-badge',
                element: 'label:contains(1000) input[value="4"]:not(:checked)',
            },

            {
                title: 'Filter by White value on iPad',
                waitFor: '.sort_bar h4:contains(1000)',
                element: '.js_attributes label.css_attribute_color input[value="2-3"]:visible',
            },
            {
                title: 'Click on Filter 200 - 500 price range',
                waitFor: '.sort_bar h4:contains(White) a.removable-badge',
                element: 'label:contains(200) input:not(:checked)',
            },
            {
                title: 'Click on Filter 32 GB on iPad',
                waitFor: '.sort_bar h4:contains(200)',
                element: 'label:contains(32 GB) input:not(:checked)',
            },
            {
                title: 'Filter by Black value on iPad',
                waitFor: '.sort_bar h4:contains(32 GB)',
                element: '.js_attributes label.css_attribute_color input[value="2-4"]:visible',
            },
            {
                title: 'Remove 500 - 1000 price range filter',
                waitFor: '.sort_bar h4:contains(Black)',
                element: 'label:contains(1000) input:checked'
            },
            {
                title: 'Finish Tour',
                waitNot: '.sort_bar h4:contains(1000)',
            },
        ],
    });

}());
