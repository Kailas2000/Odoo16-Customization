# -*- coding: utf-8 -*-
from odoo import api,  fields, models


class ConfSetting(models.TransientModel):
   _inherit = "res.config.settings"

   discount_limit = fields.Boolean(
      string="Discount Limit",
      config_parameter='discount_limit.discount_limit',
      help="If the field is enabled then the amount mention below will be the"
           "maximum discount amount for this month")
   discount_money = fields.Float(
      string="Max Limit",
      config_parameter='discount_limit.discount_money',
      help="Mention the maximum amount discount for a month")
   discount_period = fields.Selection(
      string="Discount Period",
      selection=[('month', 'Month'), ('week', 'Week'), ('day', 'Day')],
      config_parameter='discount_limit.discount_period',
      required=True,
      help="Mention the maximum amount discount for a period")

   @api.onchange('discount_money')
   def discount_amount(self):
      """Function discount_amount is used to find the amount in the settings"""
      if not self.discount_limit:
         self.discount_money = 0.00
         print(self.discount_limit)

