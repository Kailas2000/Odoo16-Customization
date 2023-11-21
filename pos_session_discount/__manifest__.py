{
    'name': "POS Session Discount",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'POS Session Discount',
    'description': """
     Discount for the session in POS.
    """,
    'depends' : [
        'base',
        'point_of_sale'
    ],
    'data': [
        'view/conf_settings.xml',
    ],
    'assets': {
       'point_of_sale.assets': [
           'pos_session_discount/static/src/js/session_discount.js'
       ],
    },
}