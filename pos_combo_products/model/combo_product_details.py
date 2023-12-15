# -*- coding: utf-8 -*-
from odoo import fields, models

class ComboProductsDetails(models.Model):
    _name = 'combo.products.details'
    _description = 'Combo Products Details'

    combo_category_id = fields.Many2one(comodel_name='pos.category',
                                     string="Category",
                                     help="Product Category")
    combo_product_ids = fields.Many2many(comodel_name='product.product',
                                     domain="[('pos_categ_id', '=', combo_category_id)]",
                                     string="Products")
    is_required = fields.Boolean('Is Required',
                                 help="Combo Products is required or not")
    item_count = fields.Integer('Items Count',
                                help="Items Count")
    product_details_id = fields.Many2one('product.template')
