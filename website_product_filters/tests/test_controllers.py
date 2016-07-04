# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import openerp.tests


@openerp.tests.common.at_install(False)
@openerp.tests.common.post_install(True)
class TestUi(openerp.tests.HttpCase):
    def test_01_empty_category(self):
        self.phantom_js(
            "/",
            "openerp.Tour.run('test_special_cases', 'test')",
            "openerp.Tour.tours.test_special_cases",
            login="admin")
