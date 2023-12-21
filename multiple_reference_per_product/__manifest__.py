{
    'name': 'Product Multiple Reference',
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Product Multiple Reference',
    'description': """
    Product Multiple Reference
    """,
    'depends': [
        'base',
        'sale_management'
    ],
    'data':[
        'security/ir.model.access.csv',
        'view/product_add_more.xml',
        'view/multiple_reference_per_product_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}