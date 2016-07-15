(function () {
    'use strict';
    var _t = openerp._t;
    var steps = openerp.Tour.tours.shop_customize.steps;
    for (var k=0; k<steps.length; k++) {
        if (steps[k].title === "open customize menu bis") {
            steps.splice(k, 1);
        }
        if (steps[k].title === "click on 'Product Attribute's Filters'") {
            steps.splice(k, 1);
        }
        if (steps[k].title === "remove 'Product Attribute's Filters'") {
            steps.splice(k, 1);
        }
        if (steps[k].title === "finish") {
            steps.splice(k, 1, {
                title: 'Finished tour',
            });
        }
    }
}());
