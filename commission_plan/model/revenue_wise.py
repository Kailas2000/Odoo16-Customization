# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RevenueWise(models.Model):
    _name = "revenue.wise"
    _description = "Revenue Wise"

    sequences = fields.Char()
    from_amount = fields.Integer(string="From Amount")
    to_amount = fields.Integer(string="To Amount")
    rate = fields.Integer(string="Rate in %")

    type_id = fields.Many2one(comodel_name="crm.commission")