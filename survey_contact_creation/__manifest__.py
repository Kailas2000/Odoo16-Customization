# -*- coding: utf-8 -*-
{
    'name': "survey_contact_creation",
    'summary': """
    Contact creation from survey""",
    'description': """
        Creating an contact from survey
    """,
    'author': "Kailas",
    'category': 'Category',
    'version': '16.0.1.0.0',
    'depends': ['survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_contact_creation_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
