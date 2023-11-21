{
    'name': "POS Remove OrderLine",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'POS Remove OrderLine',
    'description': """
     Remove orderline from the selected order in the POS.
    """,
    'depends' : [
        'base',
        'point_of_sale'
    ],
    'assets': {
       'point_of_sale.assets': [
           'pos_remove_orderline/static/src/js/remove_orderlines.js',
           'pos_remove_orderline/static/src/js/clear_cart.js',
           'pos_remove_orderline/static/src/xml/remove_orderlines.xml'
       ],
    },
}