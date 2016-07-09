# coding: utf-8
{
    "name": "Product Filters",
    "version": "8.0.0.1.0",
    "author": "Vauxoo",
    "category": "Website",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": [
        "product_brand",
        "website_rate_product",
        "website_sale_options",
    ],
    "demo": [
        'demo/filters_demo_data.xml',
    ],
    "data": [
        'data/price_ranges_data.xml',
        'security/price_ranges_security.xml',
        'security/ir.model.access.csv',
        'views/product_price_ranges_view.xml',
    ],
    "test": [],
    "qweb": [
    ],
    "installable": True,
    "auto_install": False,
}
