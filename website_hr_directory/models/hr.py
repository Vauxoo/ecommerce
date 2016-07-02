# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    website_published = fields.Boolean(
        'Available in the website', copy=False, default=False)
    public_info = fields.Html('Public Info')

    @api.model
    def _get_departments(self):
        """Retrieves all published departments.
        """
        dept_obj = self.env['hr.department']
        depts = dept_obj.sudo().search([('website_published', '=', True)])
        return depts


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    website_published = fields.Boolean('Available in the website', copy=False,
                                       default=False)
    public_info = fields.Text('Public Info')
    work_location_id = fields.Many2one('hr.work.location')

    @api.model
    def _publish_department(self):
        """Publishes a department on the website, it will publish it if it
        has employees marked as `website_published = True` and will unpublish
        if a product is marked as `website_published = False` and the
        department does not contain more published employees.
        """
        if self.website_published and self.department_id:
            self.department_id.sudo().write({'website_published': True})
        if not self.website_published and self.department_id and not \
                self.department_id.member_ids.filtered('website_published'):
            self.department_id.sudo().write({'website_published': False})


class HrWorkLocation(models.Model):
    _name = 'hr.work.location'

    name = fields.Char('Name')
