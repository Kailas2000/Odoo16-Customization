{
    'name': "BOM Cart",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'BOM Cart',
    'description': """
    Show the bill of materials(BOM) of the products 
    after the product description in shop or cart.
    """,
    'depends' : [
        'website',
        'website_sale',
        'mrp',
    ],
    'data': [
        'view/conf_settings.xml',
        'view/bom_products_list.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}