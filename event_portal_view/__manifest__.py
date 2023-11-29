{
    'name': 'Upcoming Event Portal View',
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Upcoming events portal view',
    'description': """
    Upcoming events portal view
    """,
    'depends': [
        'base',
        'mail',
        'portal'
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/event_view.xml',
        'views/portal_view.xml',
        'views/event_menu.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
