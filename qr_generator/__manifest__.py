{
    "name": "QR-Code Generator",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'summary' : 'QR Code Generating',
    'description': """
    QR Code generating based on the user input and the user can download the QR
    """,
    "depends": [ 'web' ],
    "version": "16.0.1.0.0",

    "assets": {
        "web.assets_backend": [
            '/qr_generator/static/src/js/qr_generate.js',
            '/qr_generator/static/src/xml/systray_qr_icon.xml'
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}