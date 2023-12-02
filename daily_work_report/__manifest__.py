{
    'name': "Daily Work Report Tracker",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Daily Work Report Tracker',
    'description': """
    Employee Daily Work Report Tracker.
    """,
    'depends' : [
        'base',
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/daily_work_report.xml',
        'views/daily_work_report_menu.xml',
        'data/action.xml'
    ],
    'assets': {
       'web.assets_backend': [
           'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
           'daily_work_report/static/src/xml/daily_work_report.xml',
           'daily_work_report/static/src/js/daily_work_report.js',
       ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}