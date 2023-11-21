# -*- coding: utf-8 -*-
from odoo import fields, models


class SalesTeam(models.Model):
    _inherit = 'crm.team'
    _description = "Sales Team"

    commission_plan_id = fields.Many2one(
        string="Commission Plan",
        comodel_name="crm.commission",
        help="Select the specific plan for the sales team and the commission is calculated based on the plan")
