{
    'name': "Commission plan",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Commission plan',
    'description': """
    Commission plan.
    """,
    'depends' : [
        'base',
        'sale',
        'purchase',
        'mail'
    ],
    'data': [
        'view/crm_commission_action.xml',
        'security/ir.model.access.csv',
        'view/crm_commission.xml',
        'view/sales_person.xml',
        'view/sale_team.xml',
        'view/sales_order.xml',
    ]
}