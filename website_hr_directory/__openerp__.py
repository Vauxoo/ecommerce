# coding: utf-8
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Directory Page",
    'summary': """
        Show all employee directory
        """,
    'author': "Vauxoo",
    'website': "http://vauxoo.com",
    'category': 'Website',
    'version': '8.0.0.1.0',
    'license': 'AGPL-3',
    'depends': [
        'base_action_rule',
        'hr',
        'website',
    ],
    'demo': [
        'demo/hr_work_location.xml',
        'demo/hr_department.xml',
        'demo/hr_job.xml',
        'demo/hr_employee.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_hr_directory.xml',
        'data/server_actions.xml',
        'data/action_rules.xml',
        'views/assets.xml',
        'views/hr_view.xml',
        'views/templates.xml',
    ],
}
