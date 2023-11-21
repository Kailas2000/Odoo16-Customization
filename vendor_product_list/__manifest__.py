{
    'name': "Vendor Product List",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Customize the Purchase order module',
    'description': """
    Customize the purchase module.
    """,
    'depends' : [
        'base',
        'purchase',
    ],
    'data': [
        'views/custom_vendor_product_list.xml',
    ]
}