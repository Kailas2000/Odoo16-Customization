# -*- coding: utf-8 -*-
from odoo import models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date(string="Registration Date",
                                    default=fields.Date.today,
                                    help="Registration date of the vehicle")
