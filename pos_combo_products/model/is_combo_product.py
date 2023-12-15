# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ComboProducts(models.Model):
    _inherit = 'product.template'

    is_combo = fields.Boolean('Is Combo',
                              help="If the product is a combo product")
    combo_ids = fields.One2many(comodel_name="combo.products.details",
                                inverse_name="product_details_id",
                                help="Combo Products")

    @api.model
    def combo_product_details(self, combo):
        required_product = {}
        optional_product = {}
        count = {}
        for product in combo:
            combo_product = self.env['combo.products.details'].browse(product)
            for products in combo_product.combo_product_ids:
                if combo_product.is_required:
                    if products.pos_categ_id.name in required_product:
                        required_product[products.pos_categ_id.name].append(
                            products.id)
                        continue
                    required_product[products.pos_categ_id.name] = [products.id]
                else:
                    if products.pos_categ_id.name in optional_product:
                        optional_product[products.pos_categ_id.name].append(
                            products.id)
                        continue
                    else:
                        optional_product[products.pos_categ_id.name] = [products.id]
                        count[products.pos_categ_id.name] = combo_product.item_count
        return {
            'required_product': required_product,
            'optional_product': optional_product,
            'optional_count': count
        }
