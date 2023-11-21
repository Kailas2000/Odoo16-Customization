# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class DataSearch(models.Model):
    _name = "data.search"
    _description = "Data Search"

    data = fields.Char(string="Data", required=True,
                       help="Input the data that you want to search from any model")
    model_ids = fields.Many2many('ir.model', string='Models',
                                 help="Specify the models that you want to search the data")
    fields_id = fields.Many2one('ir.model.fields', string='Field',
                                domain="[('model_id', '=',  model_ids)]")
    record_ids = fields.One2many(comodel_name="searched.data",
                                 inverse_name="type_id")

    def action_search(self):
        """Action for searching the inputed data in the model.
        If the model is more than 1 and field is specified,then only that
        particular field model will be checked."""
        self.record_ids = [fields.Command.clear()]
        for single_model in self.model_ids:
            model_name = single_model.model
            if self.env[model_name].sudo()._abstract:
                if len(self.model_ids) == 1:
                    raise ValidationError("Abstract models are not allowed")
                continue
            model_records = self.env[model_name].sudo().search_read([])
            for record in model_records:
                for key, value in record.items():
                    if self.fields_id and single_model.model == self.fields_id.model:
                        # If field input is selected and checking the field model.
                        if key == self.fields_id.name and self.data.lower() in str(value).lower():
                            self.record_ids = [fields.Command.create({
                                'line_id': record['id'],
                                'data': f"{value}",
                                'model': model_name
                            })]
                    elif not self.fields_id:
                        # If more than 1 model is selected.
                        if self.data.lower() in str(value).lower():
                            self.record_ids = [fields.Command.create({
                                'line_id': record['id'],
                                'data': f"{value}",
                                'model': model_name
                            })]

