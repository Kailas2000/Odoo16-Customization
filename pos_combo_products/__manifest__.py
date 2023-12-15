{
    'name': "POS Combo Products",
    'version': '16.0.5.2.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'POS Combo Products',
    'description': """
    POS Combo Products
    """,
    'depends' : [
        'base',
        'point_of_sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/is_combo_products_view.xml',
    ],
    'assets': {
       'point_of_sale.assets': [
           'pos_combo_products/static/src/xml/combo_tag.xml',
           'pos_combo_products/static/src/xml/combo_products_popup.xml',
           'pos_combo_products/static/src/js/combo_products_popup.js',
           'pos_combo_products/static/src/js/combo_product_click.js',
           'pos_combo_products/static/src/js/receipt_combo_products.js',
           'pos_combo_products/static/src/xml/orderline_combo_product_details.xml',
           'pos_combo_products/static/src/xml/combo_product_receipt.xml'
       ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}