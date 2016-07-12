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

    @http.route(
        ['/department/<int:department_id>'],
        type='http',
        auth='public',
        website=True)
    def employees(self, department_id, **post):
        employees = request.env['hr.employee'].search(
            [('department_id', '=', department_id),
             ('website_published', '=', True)],
            order='work_location_id DESC')
        values = {
            'employees': employees,
        }
        return request.website.render('website_hr_directory.employees', values)
