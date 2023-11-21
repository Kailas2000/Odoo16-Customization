# -*- coding: utf-8 -*-
{
    'name': "sales_dashboard",
    'summary': """
    Sales Dashboard""",
    'description': """
        Customize the sales dashboard
    """,
    'author': "Kailas",
    'category': 'Category',
    'version': '16.0.1.0.0',
    'depends': ['sale_management'],
    'data': [
        'data/action.xml'
    ],
    'assets': {
       'web.assets_backend': [
           'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
           '/sales_dashboard/static/src/xml/sales_dashboard_view.xml',
           '/sales_dashboard/static/src/js/sales_dashboard.js',
       ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
