{
    'name': "Float to Integer field widget",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Float to Integer field widget',
    'description': """
     float field widget that will convert the 
     floating value to the nearest integer.
    """,
    'depends' : ['web'],
    'assets': {
        "web.assets_backend": [
            "/float_to_int_widget/static/src/js/float_to_int.js",
            "/float_to_int_widget/static/src/xml/float_to_int.xml"
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}