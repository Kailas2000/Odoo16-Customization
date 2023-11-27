{
    'name': "Employee Contract Expiry Email",
    'version': '16.0.5.2.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Employee Contract Expiry Email',
    'description': """
    Sending email to the manager when the contract date expiry.
    """,
    'depends' : [
        'base',
        'mail',
        'hr',
    ],
    'data': [
        'report/ir_report_templates.xml',
        'report/ir_actions_report.xml',
        'data/ir_cron_email_sending.xml',
        'data/contract_expiry_email.xml',
        'views/conf_settings.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
