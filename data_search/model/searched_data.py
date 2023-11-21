# -*- coding: utf-8 -*-
from odoo import fields, models


class SearchedData(models.Model):
    _name = "searched.data"
    _description = "Searched Data"

    line_id = fields.Integer(string="Line ID", help="To store the record id")
    data = fields.Char(string="Searched Data",
                       help="To view the matched data with input data")
    model = fields.Char(string="Model",
                        help="To specify the model of that particular data model")
    type_id = fields.Many2one(comodel_name="data.search")

    def action_view_form(self):
        """Function is created for view the form of particular listed data"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': self.model,
            'view_mode': 'form',
            'res_id': self.line_id,
            'target': 'current',
        }