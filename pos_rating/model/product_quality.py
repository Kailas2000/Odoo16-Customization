# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductQuality(models.Model):
    _inherit = 'product.product'

    product_quality = fields.Selection(
        string="Product Quality",
        selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        help="Rate the product based on the quality.")
