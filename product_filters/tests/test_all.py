# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.tests.common import TransactionCase


class TestFilterMethods(TransactionCase):

    def setUp(self):
        super(TestFilterMethods, self).setUp()
        self.attr_products = \
            self.env.ref('product.product_product_4_product_template') + \
            self.env.ref('product.product_product_3_product_template') + \
            self.env.ref('product.product_product_25_product_template')
        self.ranges_obj = self.env['product.price.ranges']
        self.ranges_ids = [self.env.ref('product_filters.price_range_1').id,
                           self.env.ref('product_filters.price_range_2').id,
                           self.env.ref('product_filters.price_range_3').id,
                           self.env.ref('product_filters.price_range_4').id,
                           self.env.ref('product_filters.price_range_5').id, ]
        self.category_obj = self.env['product.public.category']
        self.category_speakers = self.env.ref('product.Speakers')
        self.ranges = [
            {'id': self.env.ref('product_filters.price_range_1').id, 'qty': 0},
            {'id': self.env.ref('product_filters.price_range_2').id, 'qty': 0},
            {'id': self.env.ref('product_filters.price_range_3').id, 'qty': 2},
            {'id': self.env.ref('product_filters.price_range_4').id, 'qty': 0},
            {'id': self.env.ref('product_filters.price_range_5').id, 'qty': 0},
        ]
        self.category_aio = self.env.ref('product.Computer_all_in_one')
        self.products_per_attr = [
            {'id': self.env.ref('product.product_attribute_value_1').id,
             'qty': 1},
            {'id': self.env.ref('product.product_attribute_value_2').id,
             'qty': 2},
            {'id': self.env.ref('product.product_attribute_value_3').id,
             'qty': 1},
            {'id': self.env.ref('product.product_attribute_value_4').id,
             'qty': 1},
            {'id': self.env.ref('product.product_attribute_value_5').id,
             'qty': 1},
        ]
        self.category_aio = self.env.ref('product.Computer_all_in_one')
        self.known = [
            self.env.ref('product.product_attribute_1').id,
            self.env.ref('product.product_attribute_2').id,
            self.env.ref('product.product_attribute_3').id,
        ]
        self.unknown = [
            self.env.ref('product.product_attribute_1').id,
        ]
        self.brands = [
            self.env.ref('product_filters.brand_apple').id,
            self.env.ref('product_filters.brand_google').id,
        ]
        self.highest_rated = [
            self.env.ref('product.product_product_5b_product_template').id,
            self.env.ref('product.product_product_9_product_template').id,
            self.env.ref('product.product_product_7_product_template').id,
        ]
        self.selected_ranges = [
            self.env.ref('product_filters.price_range_3').id,
            self.env.ref('product_filters.price_range_4').id,
            self.env.ref('product_filters.price_range_5').id,
        ]

    def test_01_ranges(self):
        """Tests if all the price ranges are retrieved
        """
        result_ranges = self.ranges_obj._get_all_ranges()
        self.assertEqual(set(self.ranges_ids), set(result_ranges._ids))

    def test_02_async_ranges(self):
        """Tests if the quantity of products per range returned is correct.
        """
        res = self.category_obj._get_async_ranges(
            int(self.category_speakers.id))
        self.assertEqual(res, self.ranges)

    def test_03_async_values(self):
        """Tests if the quantity of products per attribute value is correct.
        """
        res = self.category_obj._get_async_values(int(self.category_aio.id))
        self.assertEqual(res, self.products_per_attr)

    def test_04_compute_product_count(self):
        """Tests if the category has products and if the quantity of products
        per public category is correct.
        """
        self.category_aio._compute_product_count()
        self.assertTrue(self.category_aio.has_products_ok)
        self.assertEqual(4, self.category_aio.total_tree_products)

    def test_05_attributes_related(self):
        """Tests if the attributes retrieved are the ones of the category and
        tests if the attribute has unknown values for certain products.
        """
        known, unknown = self.category_aio._get_attributes_related(
            self.attr_products)
        self.assertEqual(known, self.known)
        self.assertEqual(unknown, self.unknown)

    def test_06_brands_related(self):
        """Test the brands related to the category All-in-One
        """
        res = self.category_aio._get_brands_related(self.attr_products)
        self.assertEqual(set(res._ids), set(self.brands))

    def test_07_test_all_categories(self):
        """Tests if all retrieved categories are the ones related to the
        All-in-One category.
        """
        res = self.category_aio._get_all_categories()
        self.assertEqual(res, self.category_aio.search([]))

    def test_08_test_product_sorted(self):
        """Test if the products are sorted as expected by highest rating.
        """
        res = self.category_obj._get_product_sorted('rating DESC')
        self.assertEqual(set(res._ids), set(self.highest_rated))

    def test_09_test_related_ranges(self):
        """ Tests case: bring ipad, galaxy and nexus price ranges.
        """
        res = self.ranges_obj._get_related_ranges(self.attr_products)
        self.assertEqual(set(res._ids), set(self.selected_ranges))


class TestBrand(TransactionCase):

    def setUp(self):
        super(TestBrand, self).setUp()
        self.brand_apple = self.env.ref('product_filters.brand_apple')
        self.category_ids = [
            self.env.ref('product.Computer_all_in_one').id,
            self.env.ref('product.Keyboard_Mouse').id,
            self.env.ref('product.Screen').id,
        ]

    def test_01_test_categories_related(self):
        """Tests if the categories retrieved are the ones related to the brand
        Apple.
        """
        res = self.brand_apple._get_categories_related()
        self.assertEqual(set(res._ids), set(self.category_ids))
