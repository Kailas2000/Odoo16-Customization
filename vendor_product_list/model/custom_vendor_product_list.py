# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VendorProductList(models.Model):
    _inherit = 'purchase.order'

    is_vendor_products = fields.Boolean(string="Is Vendor Products")


class VendorPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_list_id = fields.Many2many(comodel_name="product.product")

    @api.onchange('product_id')
    def vendor_product(self):
        # Collecting the vendor specific products into the variable records
        records = self.env['product.supplierinfo'].search(
            [('partner_id', '=', self.order_id.partner_id.id)]).mapped(
            'product_tmpl_id.id')
        # Convert product_tmpl into product_product
        self.product_list_id = self.env['product.product'].search(
            [('product_tmpl_id', 'in', records)]).ids

        if self.order_id.is_vendor_products == True:
            return {'domain': {'product_id': [
                ('id', '=', self.product_list_id.ids)]}}

