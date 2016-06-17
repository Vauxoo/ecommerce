# coding: utf-8
from openerp import http
from openerp.http import request
from operator import itemgetter
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website_sale.controllers.main import QueryURL


class WebsiteSale(website_sale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',  # noqa
        '/shop/brands'], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """This method was inherited wit the purpose of filtering attributes
        instead of showing all that exist on the instance, it will allow
        to show attribute filters based on the selected category.
        """
        cr, uid, context, pool = (request.cr,
                                  request.uid,
                                  request.context,
                                  request.registry)
        res = super(WebsiteSale, self).shop(page=page,
                                            category=category,
                                            search=search, ppg=ppg,
                                            **post)

        ranges_obj = pool['product.price.ranges']
        category_obj = pool['product.public.category']
        ranges_list = request.httprequest.args.getlist('range')
        brand_list = request.httprequest.args.getlist('brand')
        unknown_list = request.httprequest.args.getlist('unknown')
        unknown_values = [map(int, a.split("-")) for a in unknown_list if a]
        brand_selected_ids = [int(b) for b in brand_list if b]
        ranges_selected_ids = [int(v) for v in ranges_list if v]
        unknown_set = set([x[0] for x in unknown_values])
        ranges_ids = ranges_obj.search(cr, uid, [], context=context)
        ranges = ranges_obj.browse(cr, uid, ranges_ids, context=context)
        attrs_unknown = {}
        categ_id = (isinstance(category, int) or
                    isinstance(category, (str, unicode))) and \
            int(category) or category and category.id or 0
        attributes_ids, att_unkn_ids = category_obj.\
            _get_attributes_related(cr, uid,
                                    categ_id, context)
        attrs_unknown.fromkeys(att_unkn_ids, True)
        brands = category_obj.\
            _get_brands_related(cr, uid,
                                categ_id, context)
        attributes = pool['product.attribute'].browse(cr, uid, attributes_ids)
        res.qcontext['attributes'] = attributes
        res.qcontext['attrs_unknown'] = attrs_unknown
        filtered_products = res.qcontext['products']
        args = res.qcontext['keep'].args
        if category and category.child_id and not search:
            ordered_products = []
            res.qcontext['pager']['page_count'] = 0
            popular = category_obj._get_product_sorted(cr, uid,
                                                       int(category.id or 0),
                                                       'rating DESC', 3)
            newest = category_obj._get_product_sorted(cr, uid,
                                                      int(category.id or 0),
                                                      'create_date DESC', 3)
            res.qcontext['populars'] = popular
            res.qcontext['newest'] = newest
            res.qcontext['products'] = ordered_products
        elif not category and not search and not brand_list:
            res.qcontext['products'] = []
            res.qcontext['pager']['page_count'] = 0
        else:
            values = ('name', 'pasc-lst_price', 'pdesc-lst_price',
                      'hottest-create_date', 'rating', 'popularity-views')
            keys = {}
            for val in values:
                fields, rever = val.split('-'), 'pdesc' in val
                keys[fields[0]] = filtered_products.\
                    sorted(key=itemgetter(fields[-1]), reverse=rever)
            keys['0'] = filtered_products

            if post.get('product_sorter', '0') != '0':
                sortby = post['product_sorter']
                res.qcontext['sortby'] = sortby
                ordered_products = keys.get(sortby)
            elif request.httprequest.cookies.get('default_sort', 'False') != 'False':  # noqa
                sortby = request.httprequest.cookies.get('default_sort')
                ordered_products = keys.get(sortby)
            elif request.httprequest.cookies.get('default_sort') == 'False':
                sortby = request.website.default_sort
                ordered_products = keys.get(sortby)
            else:
                ordered_products = filtered_products
            res.qcontext['products'] = ordered_products

        attribute_ids = attributes.ids
        for arg in args.get('attrib', []):
            attr_id = arg.split('-')
            if int(attr_id[0]) not in attribute_ids:
                res.qcontext['keep'] = QueryURL(
                    '/shop',
                    category=category and int(category),
                    search=search)

        parent_category_ids = []
        if category:
            categs = category
        else:
            domain = [('parent_id', '=', False)]
            categ_ids = category_obj.search(cr, uid, domain, context=context)
            categs = category_obj.browse(cr, uid, categ_ids, context=context)

        res.qcontext['parent_category_ids'] = parent_category_ids
        res.qcontext['brands'] = brands
        res.qcontext['categories'] = categs
        res.qcontext['price_ranges'] = ranges
        res.qcontext['brand_set'] = brand_selected_ids
        res.qcontext['ranges_set'] = ranges_selected_ids
        res.qcontext['unknown_set'] = unknown_set
        return res

    @http.route(['/shop/product/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        cr, uid, context, pool =\
            request.cr, request.uid, request.context, request.registry
        template_obj = pool['product.template']
        if not category and len(product.public_categ_ids) >= 1:
            category = product.public_categ_ids[0]
        viewed = product.views + 1
        template_obj.write(cr, uid, [product.id],
                           {'views': viewed}, context=context)
        res = super(WebsiteSale, self).product(product=product,
                                               category=category,
                                               search=search, **kwargs)
        return res
