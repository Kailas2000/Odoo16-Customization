# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ProductMultipleReference(models.Model):
    _name = "product.multiple.reference"
    _rec_name = "multiple_product"
    _description = "Product Multiple Reference"

    multiple_product = fields.Char(string="Multiple Product",
                                   required=True,
                                   help="")
    product_id = fields.Many2one(comodel_name="product.product",
                                 string="Product",
                                 required=True,
                                 help="")

    def action_set_default(self):
        """Action to set the new input reference code as product default code"""
        self.product_id.write({'default_code': self.multiple_product})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _(self.multiple_product+' Default code'),
                'message': 'You set the default code for product '
                           +self.product_id.name,
                'sticky': False,
            }
        }
