# -*- coding: utf-8 -*-
{
    'name': "Razorpay Payment",
    'version': '16.0.1.0.0',
    'author': "Kailas",
    'category': 'Category',
    'summary' : 'Razorpay Payment Provider',
    'description': """
     Razorpay Payment Provider.
    """,
    'depends' : [
        'payment',
        'website',
    ],
    'data': [
        'views/razorpay_provider_view.xml',
        'views/razorpay_payment_templates.xml',
        'data/razorpay_payment_data.xml',
        'data/automatic_invoice_enable.xml',
    ],
}