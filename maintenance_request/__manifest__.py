{
    'name': 'Maintenance Request',
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'summary' : 'Maintenance Request',
    'description': """
    Requesting for maintenance through website
    """,
    'depends': [
        'website',
        'maintenance',
        'mail'
    ],
    'data':[
        'data/website_maintenance_menu.xml',
        'data/request_details_email.xml',
        'view/maintenance_request_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}