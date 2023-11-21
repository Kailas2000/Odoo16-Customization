{
    'name': "POS Rating",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'POS Rating',
    'description': """
     Rating for the product and visible in the POS.
    """,
    'depends' : [
        'base',
        'point_of_sale'
    ],
    'data': [
        'view/product_quality_rating.xml',
    ],
    'assets': {
       'point_of_sale.assets': [
           'pos_rating/static/src/js/product_quality.js',
           'pos_rating/static/src/xml/pos_screen.xml',
           'pos_rating/static/src/xml/pos_receipt.xml'
       ],
    },
}