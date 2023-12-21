# -*- coding: utf-8 -*-
{
    'name': "Fetch Sale orders",
    'summary': """
    Fetch Sale orders from odoo version 15""",
    'description': """
        Fetch Sale orders from odoo version 15
    """,
    'author': "Kailas",
    'category': 'Category',
    'version': '16.0.1.0.0',
    'depends': ['sale_management'],
    'data': [
        'Security/ir.model.access.csv',
        'data/fetch_wizard_view.xml',
        'data/action.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
