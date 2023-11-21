{
    'name': 'Data Search',
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'summary' : 'Data Searching',
    'description': """
    Data searching from all models
    """,
    'depends': [
        'base'
    ],
    'data':[
        'security/ir.model.access.csv',

        'view/data_search_view.xml',
        'view/data_search_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}