{
    'name': 'Website Vehicle Rental',
    'version': '16.0.1.0.0',
    'depends': ['website'],
    'data':[
        'data/website_rental_menu.xml',
        'views/website_rental_template.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            "/website_vehicle_rental/static/src/js/vehicle_rental.js"
        ]
    }
}