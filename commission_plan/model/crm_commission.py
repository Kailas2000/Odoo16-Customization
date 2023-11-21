# -*- coding: utf-8 -*-
from odoo import fields, models


class CrmCommission(models.Model):
    _name = "crm.commission"
    _inherit = 'mail.thread'
    _description = "Commission Plan"

    name = fields.Char(string="Name", help="Name of the plan")
    active = fields.Boolean(string="Active", help="Plan active or not")
    from_date = fields.Date(string="From Date", help="Plan starting date")
    to_date = fields.Date(string="To Date", help="Plan ending date")
    type_selection = fields.Selection(
        string='Type',
        selection=[('product_wise', 'Product Wise'),
                   ('revenue_wise', 'Revenue Wise')],
        default='product_wise',
        required=True,
        help="Type of the plan"
    )
    revenue_wise_type = fields.Selection(
        string="Revenue Wise",
        selection=[('straight', 'Straight'),
                   ('graduated', 'Graduated')],
        help="Select the type of revenue"
    )
    product_type_ids = fields.One2many(
        comodel_name="product.wise",
        inverse_name="type_id",
        help="")
    revenue_type_ids = fields.One2many(
        comodel_name="revenue.wise",
        inverse_name="type_id")

