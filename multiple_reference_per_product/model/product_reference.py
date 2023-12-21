# -*- coding: utf-8 -*-
from odoo import models


class ProductReference(models.Model):
    _inherit = "product.product"

    def action_add_more(self):
        """Add More Button action to redirect to another model
        'product.multiple.reference'"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Multiple Reference',
            'res_model': 'product.multiple.reference',
            'view_mode': 'tree,form',
            'context': {'default_product_id': self.id},
            'domain': [('product_id', '=', self.id)],
            'target': 'current',
        }
