# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)2010-  OpenERP SA (<http://openerp.com>). All Rights Reserved
#    App Author: Vauxoo
#
#    Developed by Oscar Alcala
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class ProductPriceRanges(models.Model):
    _name = "product.price.ranges"

    lower = fields.Integer("Lower")
    upper = fields.Integer("Upper")

    @api.model
    def _get_all_ranges(self, domain=None):
        """Get price ranges given a domain, if the domain is not sent all
        ranges will be returned

        @param domain: Basic domain used in search method, to search ranges
        with specific values
        @param: list

        @return: Records found by the search method
        @rtype: RecordSet
        """
        domain = domain or []
        records = self.search(domain)
        return records


class ProductCategory(models.Model):
    _inherit = 'product.public.category'

    _parent_store = True
    _order = 'parent_left'

    parent_left = fields.Integer('Left Parent', select=1)
    parent_right = fields.Integer('Right Parent', select=1)
    parent_id = fields.Many2one(ondelete='restrict')

    product_ids = fields.Many2many(
        "product.template", "product_public_category_product_template_rel",
        "product_public_category_id",
        "product_template_id", readonly=True)
    total_tree_products = fields.Integer("Total Subcategory Prods",
                                         compute="_compute_product_count",
                                         store=True)
    has_products_ok = fields.Boolean(compute="_compute_product_count",
                                     store=True, readonly=True)

    @api.model
    def _get_async_ranges(self, category):
        """Get quantity of products per price range based on a given category.

        @param category: The category id on which the quantities will be
        searched for.
        @param: int

        @return: List of dictionaries where the key is the id of the range
        and the value is the quantity of products found in that price range.
        @rtype: dict

        """
        prod_obj = self.env['product.template']
        ranges_obj = self.env['product.price.ranges'].search([])
        count_dict = {}
        prod_ids = prod_obj.search(
            [('public_categ_ids', 'child_of', category),
             ('website_published', '=', True)])
        for prod in prod_ids:
            for ran in ranges_obj:
                count_dict.setdefault(ran.id, 0)
                if ran.upper > prod.list_price > ran.lower:
                    count_dict[ran.id] += 1
        to_jsonfy = [{'id': k, 'qty': count_dict[k]} for k in count_dict]
        return to_jsonfy

    @api.model
    def _get_async_values(self, category):
        """Get quantity of products per attribute value based on a given
        category.

        @param category: The category id on which the quantities will be
        searched for.
        @param: int

        @return: List of dictionaries where the key is the id of the range
        and the value is the quantity of products found in that price range.
        @rtype: dict

        """
        prod_obj = self.env['product.template']
        count_dict = {}
        prod_ids = prod_obj.search(
            [('public_categ_ids', 'child_of', category),
             ('website_published', '=', True)])
        for prod in prod_ids:
            for line in prod.attribute_line_ids:
                for value in line.value_ids:
                    count_dict.setdefault(value.id, 0)
                    count_dict[value.id] += 1
        to_jsonfy = [{'id': k, 'qty': count_dict[k]} for k in count_dict]
        return to_jsonfy

    @api.depends("product_ids", "product_ids.website_published")
    def _compute_product_count(self):
        """Gets the total of website_published products on the category tree
        (all childs) and writes a boolean wether it has or not products.
        """
        prod_obj = self.env["product.template"]
        for rec in self:
            prod_ids = prod_obj.search(
                [('public_categ_ids', 'child_of', rec.id),
                 ('website_published', '=', True)], count=True)
            rec.total_tree_products = prod_ids
            rec.has_products_ok = prod_ids > 0

    @api.multi
    def _get_attributes_related(self):
        """Find the attributes related among the products with any public category

        @return: Attributes ids related to the category
        @rtype: list, list

        """
        attr_ids = []
        attr_ids2 = []
        self._cr.execute('''
                SELECT
                    l.attribute_id,
                    array_agg(v.val_id)
                FROM
                    product_attribute_line AS l
                LEFT OUTER JOIN
                    product_attribute_line_product_attribute_value_rel AS v ON
                    v.line_id=l.id
                WHERE
                    product_tmpl_id IN %s
                GROUP BY
                    l.attribute_id
                         ''', (tuple(self.product_ids.ids or (0,)),))
        for i in self._cr.fetchall():
            attr_ids.append(i[0])
# pylint: disable=expression-not-assigned
            None in i[1] and attr_ids2.append(i[0])
        return attr_ids, attr_ids2

    @api.multi
    def _get_brands_related(self):
        """Find the brands related among the products with the public category

        @return: Ids of the branch related to the category
        @rtype: list
        """
        brand_ids = self.product_ids.mapped('product_brand_id')
        return brand_ids

    @api.multi
    def _get_product_sorted(self, sort, limit=3):
        """Get the products related with the category returned in an specific order

        @param sort: Field which you want order the recordset returned
        @type sort: str or unicode

        @param limit: Limit of the recorset returned
        @type limit: int or long

        @return: All product found related with the current category recordset
        considering the domain used in the search function
        @rtype: recordset
        """
        domain = [('website_published', '=', True),
                  ('public_categ_ids', 'child_of', self.id)]

        domain += 'rating' in sort and [('rating', '>', 0)] or []
        product_ids = self.env['product.template'].\
            search(domain, limit=limit, order=sort)
        return product_ids

    @api.model
    def _get_all_categories(self, domain=None):
        """Get categories given a domain, if the domain is not sent all
        ranges will be returned

        @param domain: Basic domain used in search method, to search ranges
        with specific values
        @param: list

        @return: Records found by the search method
        @rtype: RecordSet
        """
        domain = domain or []
        records = self.search(domain)
        return records


class ProductBrand(models.Model):
    _inherit = 'product.brand'

    @api.multi
    def _get_categories_related(self):
        """Get the public categories related
        with the products that contain these brands

        @return: All public categories related with the brands
        @rtype: RecordSet
        """

        pcategory = self.env['product.public.category']
        products = self.env['product.product'].\
            search([('product_brand_id', 'in', self.ids),
                    ('public_categ_ids', '!=', False)])
        for product in products:
            pcategory = pcategory | product.public_categ_ids
        return pcategory
