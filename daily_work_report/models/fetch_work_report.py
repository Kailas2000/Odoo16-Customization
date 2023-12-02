# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.tools.safe_eval import datetime


class FetchWorkReport(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_parse(self, message, save_original=False):
        """Super the message_parse function to create the daily work report list
        while fetching the email."""
        res = super().message_parse(message, save_original)
        data = res['from'].split('<')[1]
        email = data.split('>')[0]
        employee = self.env['hr.employee'].search([
                                        ('work_email', '=', email)]).name
        date_details = res['subject'].split('_')[1].split()
        month_num = datetime.datetime.strptime(date_details[1], '%b').month
        date = datetime.date(int(date_details[2]), month_num, int(date_details[0]))
        self.env['daily.work.report'].sudo().create({
            'name': res['subject'],
            'employee': employee,
            'date': date,
            'work_report': res['body']
        })
