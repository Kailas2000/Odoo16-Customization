# -*- coding: utf-8 -*-

import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class RazorpayProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('razorpayment', "Razorpayment")],
        ondelete={'razorpayment': 'set default'}
    )
    razorpay_api_key = fields.Char(
        string="Api Key",
        help="The key solely used to identify the account with Razorpay money")
    razorpay_secret_key = fields.Char(
        string="Secret Key")
