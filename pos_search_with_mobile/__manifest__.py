{
    'name': "POS Search with Mobile",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'POS Search with Mobile',
    'description': """
     Search Orders from POS based on Customer Mobile.
    """,
    'depends' : [
        'base',
        'point_of_sale'
    ],
    'assets': {
       'point_of_sale.assets': [
           'pos_search_with_mobile/static/src/js/add_mobile_searchbar.js',
           'pos_search_with_mobile/static/src/xml/add_mobile_list.xml'
       ],
    },
}