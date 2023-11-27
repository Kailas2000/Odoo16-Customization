# -*- coding: utf-8 -*-
from odoo import fields, models


class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"

    is_expiry_email = fields.Boolean(
        string="Expiry Email",
        config_parameter='employee_contract_expiry_email.is_expiry_email')
    expiry_email = fields.Integer(
        string="Expiry email sending",
        config_parameter='employee_contract_expiry_email.expiry_email',
        help="Mention the number to send the expiry email before the contract expires")
