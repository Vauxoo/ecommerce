# coding: utf-8
from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website_sale.controllers.main import QueryURL


class WebsiteSale(website_sale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',  # noqa
        '/shop/brands'], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', brand='', ppg=False,
             **post):
        cr, uid, pool = (request.cr,
                         request.uid,
                         request.registry)
        res = super(WebsiteSale, self).shop(page=page,
                                            category=category,
                                            search=search, brand=brand,
                                            ppg=ppg,
                                            **post)
        category_obj = pool['product.public.category']
        brand_list = request.httprequest.args.getlist('brand')
        brand_selected_ids = [int(b) for b in brand_list if b]
        column_data = self.build_filter_column(res, post)
        res.qcontext.update(column_data)
        # Update the URL with processed data
        products = res.qcontext['products']
        attributes_ids = category_obj.\
            _get_attributes_related(cr, uid, products)[0]
        attributes = pool['product.attribute'].browse(cr, uid, attributes_ids)
        args = res.qcontext['keep'].args
        attribute_ids = attributes.ids
        attribs = [i.split('-')[0] for i in args.get('attrib', [])]
        keep = (list(set(attribs) - set(attribute_ids)) or
                brand_selected_ids) and \
            {
            'keep': QueryURL(
                '/shop',
                category=category and int(category),
                search=search,
                brand=brand_selected_ids and
                brand_selected_ids[0] or brand)} or {}
        res.qcontext.update(keep)
        return res

    def build_filter_column(self, res, post):
        """Builds the filter column, taking in account the data recieved it
        will be returning the values of all the filters with more specific
        values, alowing to filter only by values that are available.

        :param res: The response to return to the client.
        :type res: http.response

        :param post: Values sent via the form embedded in the column filters.
        :type post: dict

        :return: Dictionary with the objects to render in the column filters,
        the products sorted on the given sort and the clicked elements on
        the form column filters.
        :rtype: dict
        """
        cr, uid, pool = (request.cr, request.uid, request.registry)
        category_obj = pool['product.public.category']
        ranges_obj = pool['product.price.ranges']
        ranges_list = request.httprequest.args.getlist('range')
        brand_list = request.httprequest.args.getlist('brand')
        unknown_list = request.httprequest.args.getlist('unknown')
        default_cookie = request.httprequest.cookies.get('default_sort',
                                                         'False')
        brand_selected_ids = [int(b) for b in brand_list if b]
        ranges_selected_ids = [int(v) for v in ranges_list if v]
        unknown_values = [map(int, a.split("-")) for a in unknown_list if a]
        unknown_set = set([x[0] for x in unknown_values])
        all_prods = res.qcontext['products']
        all_attr, all_unknown = category_obj._get_attributes_related(
            cr, uid, all_prods)
        all_categories = res.qcontext.get(
            'products', False) and res.qcontext['products'].mapped(
            'public_categ_ids') or []
        all_attributes = pool['product.attribute'].browse(
            cr, uid, all_attr)
        all_ranges = ranges_obj._get_related_ranges(cr, uid, all_prods)
        all_brands = category_obj._get_brands_related(cr, uid, all_prods)
        ordered_products, sortby = self.website_sort_products(
            all_prods, default_cookie, post)
        column_data = {
            'related_categories': all_categories,
            'attributes': all_attributes,
            'attrs_unknown': all_unknown,
            'price_ranges': all_ranges,
            'brands': all_brands,
            'brand_set': brand_selected_ids,
            'ranges_set': ranges_selected_ids,
            'unknown_set': unknown_set,
            'products': ordered_products,
        }
        # pylint: disable=expression-not-assigned
        post.get('product_sorter', '0') != '0' and column_data.update({'sortby': sortby})  # noqa
        return column_data

    def website_sort_products(self, products, default_cookie, post):
        """Sorts the porduct recordset and returns it sorted by the
        given criteria, wether it comes from the user post or the cookie
        stored.

        :param products: Recordset of products to sort.
        :type products: recordset

        :param default_cookie: Criteria to sort by comming from the cookie.
        :type default_cookie: string

        :param post: Values sent via the form embedded in the sort bar.
        :type post: dict

        :return: The recordset of ordered products and the criteria updated.
        :rtype: recordset, string

        """
        sortby = (post.get('product_sorter', '0') != '0') and \
            post['product_sorter'] or \
            (default_cookie != 'False') and \
            default_cookie or \
            (default_cookie == 'False') and \
            request.website.default_sort or 'None'
        values = {
            'name': 'name',
            'pasc': 'lst_price',
            'pdesc': 'lst_price',
            'hottest': 'create_date',
            'rating': 'rating',
            'popularity': 'views'}

        ordered = values.get(sortby, False) and \
            products.\
            sorted(key=lambda a: sortby == 'name' and
                   getattr(a, values[sortby]).upper() or
                   getattr(a, values[sortby]),
                   reverse=sortby == 'pdesc') or \
            products
        return ordered, sortby

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

    @http.route(
        ['/browse',
         '/browse/<model("product.public.category"):category>'],
        type="http", auth="public", website=True)
    def browse(self, category=None, **kwargs):
        """Builds the data to render the category tiles when browsing by
        category, returns all when no category recieved, returns subcategories
        if category is supplied.

        :param category: The category to get subcategories of.
        :type category: object

        :return: Template with the data to render categories.
        :rtype: render
        """
        cr, uid, pool = (request.cr,
                         request.uid,
                         request.registry)
        keep = QueryURL('/browse', category=category)
        category_obj = pool['product.public.category']
        populars = category_obj._get_product_sorted(
            cr, uid, int(category or 0), 'rating DESC', 3)
        newest = category_obj._get_product_sorted(
            cr, uid, int(category or 0), 'create_date DESC', 3)
        categories = not category and \
            category_obj._get_all_categories(
                cr, uid, [('parent_id', '=', False),
                          ('has_products_ok', '=', True)]) or category
        values = {
            'category': category,
            'categories': categories,
            'populars': populars,
            'newest': newest,
            'keep': keep,
        }
        return request.website.render(
            "website_product_filters.browse_by_category", values)
