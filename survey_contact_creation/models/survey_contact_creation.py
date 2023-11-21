# -*- coding: utf-8 -*-
from odoo import models, fields


class SurveyInherit(models.Model):
    _inherit = 'survey.survey'

    contact_relation_ids = fields.One2many(comodel_name='survey.contact',
                                           inverse_name="surveys_id")


class SurveyContactCreation(models.Model):
    _name = 'survey.contact'
    _description = 'Survey Contact Relation'

    question_id = fields.Many2one('survey.question',
                                  string='Question',
                                  domain="[('survey_id', '=', surveys_id)]",
                                  help="Select the question from the survey")
    contact_fields_id = fields.Many2one('ir.model.fields',
                                        string='Contact Fields',
                                        domain="[('model_id', '=',  85)]",
                                        help="Select the suitable field matching for the question.")
    surveys_id = fields.Many2one(comodel_name='survey.survey')

