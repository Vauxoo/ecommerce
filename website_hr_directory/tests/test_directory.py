# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.tests.common import TransactionCase


class TestPublishBrands(TransactionCase):

    def setUp(self):
        super(TestPublishBrands, self).setUp()
        self.hr_employee = self.env['hr.employee']
        self.published_employee = self.env.ref('hr.employee_vad')
        self.unpublished_employee = self.env.ref('hr.employee_al')

    def test_pulbish_dept(self):
        """Test case: a deparment is published if a employee is published.
        """
        self.unpublished_employee.write({'website_published': True})
        self.assertTrue(
            self.unpublished_employee.department_id.website_published)

    def test_unpublish_dept(self):
        """Test case: a deparment is unpublished if a employee is unpublished.
        """
        self.published_employee.write({'website_published': False})
        self.assertFalse(
            self.published_employee.department_id.website_published)
