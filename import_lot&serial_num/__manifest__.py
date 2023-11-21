{
    'name': "Import Lot & Serial Number",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Import Lot & Serial Number',
    'description': """
    Import Lot & Serial Number.
    """,
    'depends' : [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'view/import_menu.xml'
    ]
}