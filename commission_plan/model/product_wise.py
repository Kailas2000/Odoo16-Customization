# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductWise(models.Model):
    _name = "product.wise"
    _description = "Product Wise"

    product_cate_id = fields.Many2one(
        comodel_name='product.category',
        string="Product Category",
        help="Product category can be selected here")
    products_id = fields.Many2one(
        comodel_name='product.template',
        string="Products",
        help="Product can be specify")
    rate_percentage = fields.Float(string="Rate in %")
    max_commission_amount = fields.Float(
        string="Max Commission Amount",
        help="The amount in the maximum commission will be the max commission amount")
    type_id = fields.Many2one(comodel_name="crm.commission")

    @api.onchange('product_cate_id')
    def _onchange_product_cate(self):
        """While creating a plan in product wise and choose a particular
        product_category then products corresponds to that category only be
        shown"""
        if self.product_cate_id:
            return {'domain': {'products_id': [('categ_id', '=', self.product_cate_id.id)]}}
