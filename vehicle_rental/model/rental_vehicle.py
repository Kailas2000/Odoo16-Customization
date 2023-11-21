# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RentalVehicle(models.Model):
    """Class represents the vehicle rental module"""
    _name = "rental.vehicle"
    _inherit = 'mail.thread'
    _description = "Rental Vehicle"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle',
                                 domain="[('state_id', 'in', 'Registered')]")
    name = fields.Char('Vehicle Name', compute='_compute_name', required=True)
    brand = fields.Char('Brand', related='vehicle_id.brand_id.name', store=True)
    model = fields.Char('Model Year', compute='_compute_model_year', store=True)
    rent = fields.Float('Rent')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id,
                                  required=True)
    state = fields.Selection(
        string='State',
        selection=[('available', 'Available'),
                   ('not available', 'Not Available'), ('sold', 'Sold')],
        default='available'
    )
    rent_request = fields.Integer(compute='compute_count')
    confirmed_id = fields.One2many("rent.request", inverse_name="vehicle_id",
                                   string="Confirmed",
                                   domain=[('state', '=', 'confirm')])
    rent_charge_id = fields.One2many("rent.charge", inverse_name="time_id",
                                     string="charge")

    @api.depends('vehicle_id')
    def _compute_name(self):
        """Setting the vehicle name"""
        for record in self:
            if record.vehicle_id:
                record.name = (
                        str(record.vehicle_id.brand_id.name) + '/' + record.vehicle_id.model_id.name +
                        '/' + record.model)
            else:
                record.name = ""

    @api.depends('vehicle_id')
    def _compute_model_year(self):
        """selecting the model year from the date"""
        for record in self:
            record.model = str(
                record.vehicle_id.registration_date.year) if record.vehicle_id.registration_date else ""

    def get_request(self):
        """Smart button inside rental vehicle"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent Request',
            'view_mode': 'tree,form',
            'res_model': 'rent.request',
            'domain': [('vehicle_id', '=', self.id)],
            'context': "{'create': False}"
        }

    @api.depends('vehicle_id')
    def compute_count(self):
        """counting the number of request inside smart button"""
        for record in self:
            record.rent_request = self.env['rent.request'].search_count(
                [('vehicle_id', '=', record.id)])