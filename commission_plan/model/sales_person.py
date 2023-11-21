# -*- coding: utf-8 -*-
from odoo import fields, models


class SalesPerson(models.Model):
    _inherit = 'res.users'
    _description = "Sales Person"

    commission_plan_id = fields.Many2one(
        string="Commission Plan",
        comodel_name="crm.commission",
        help="Select the specific plan for the sales person and the commission is calculated based on the plan")
