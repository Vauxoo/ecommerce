# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)2010-  OpenERP SA (<http://openerp.com>). All Rights Reserved
#    App Author: Vauxoo
#
#    Coded by Oscar Alcala
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
from openerp.http import request


class Website(models.Model):
    _inherit = 'website'

    default_sort = fields.Selection(
        [('name', 'Name'),
         ('pasc', 'Price Lowest'),
         ('pdesc', 'Price Highest'),
         ('hottest', 'Hottest'),
         ('rating', 'Customer Rating'),
         ('popularity', 'Popularity')], defult="popularity")
    maximum_attributes = fields.Integer(
        'No. Attribute Panels to Show',
        help=""""Determines the maximum quantity of attribute panels displayed
        uncollapsed in the filters columns, if the quantity of attributes to
        display is greater than the value set here, the remainning panels will
        be collapsed.
        """)

    @api.model
    def sale_product_domain(self):
        domain = super(Website, self).sale_product_domain()
        rg_domain = []
        brand_domain = []
        if request.params.get('brand', False):
            brand_arg = request.httprequest.args.getlist('brand')
            brand_list = [int(v) for v in brand_arg if v]
            brand_domain.append(('product_brand_id', 'in', brand_list))
        if request.params.get('range', False):
            ranges_obj = self.env['product.price.ranges']
            ranges_list = request.httprequest.args.getlist('range')
            ranges_selected_ids = [int(v) for v in ranges_list if v]
            ranges_selected = ranges_obj.browse(ranges_selected_ids)
            for idx, rang in enumerate(ranges_selected):
                rg_domain += ['|'] if len(ranges_selected) != idx + 1 else []
                rg_domain += ['&', ('lst_price', '>=', rang.lower),
                              ('lst_price', '<=', rang.upper)]
        return rg_domain + brand_domain + domain
