# -*- coding: utf-8 -*-
from odoo import fields, models


class QuizIdleTimer(models.Model):
    _inherit = "survey.survey"

    is_question_time = fields.Boolean(
        help="If the boolean active then only it will effect")
    question_time = fields.Integer(
        help="time limit for the question")
