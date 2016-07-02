# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import http
from openerp.http import request


class WebsiteHr(http.Controller):
    @http.route(['/directory'], type='http', auth="public", website=True)
    def departments(self, department=None, **post):
        depts = request.env['hr.department']._get_departments()
        values = {
            'departments': depts,
        }
        return request.website.render('website_hr_directory.directory', values)
