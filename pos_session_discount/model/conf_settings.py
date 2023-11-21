# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    discount_limit = fields.Boolean()
    discount_amount = fields.Float()

    @api.model
    def get_order_id(self, s_id=None):
        """Function created for getting the data from pos order
        lines based on session_id"""
        data = self.env['pos.order'].search([('session_id', '=', s_id)]).lines
        total_discount_amount = 0
        for rec in data:
            total_discount_amount = total_discount_amount + ((rec.price_unit * rec.qty) - rec.price_subtotal)
        return total_discount_amount


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    discount_limit = fields.Boolean(
        string="Discount Limit",
        related='pos_config_id.discount_limit',
        readonly=False,
        help="If the boolean field is enabled then the amount will be the "
             "maximum session discount amount.")
    discount_amount = fields.Float(
        string="Max Limit",
        related='pos_config_id.discount_amount',
        readonly=False,
        help="The maximum discount amount for the session.")

