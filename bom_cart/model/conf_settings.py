# -*- coding: utf-8 -*-
from ast import literal_eval
from odoo import fields, models, api


class ConfSetting(models.TransientModel):
   _inherit = "res.config.settings"

   bom_cart = fields.Boolean(
      string="BOM Cart",
      config_parameter='bom_cart.bom_cart',
      help="")
   bom_products_ids = fields.Many2many(
      'product.template',
      'bom_products_rel',
      string="BOM Products",
      help="")

   def set_values(self):
      res = super(ConfSetting, self).set_values()
      self.env['ir.config_parameter'].sudo().set_param(
         'bom_cart.bom_products_ids', self.bom_products_ids.ids)
      return res

   @api.model
   def get_values(self):
      res = super(ConfSetting, self).get_values()
      product_list = self.env['ir.config_parameter'].sudo().get_param('bom_cart.bom_products_ids')
      res.update(bom_products_ids=[(6, 0, literal_eval(product_list))
                                   ] if product_list else False, )
      return res

