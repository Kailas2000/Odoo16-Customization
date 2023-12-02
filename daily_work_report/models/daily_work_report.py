# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.fields import Date


class DailyWorkReport(models.Model):
    _name = "daily.work.report"
    _description = "Daily Work Report"

    name = fields.Char(string="Report", help="Name of the report")
    employee = fields.Char(string="Employee", help="Name of the employee")
    date = fields.Date(string="Date", help="Report date")
    work_report = fields.Html(string="Work Report",
                              help="To show the work report")

    @api.model
    def get_work_report(self, input):
        """Function to get the daily reports count based on the date and return
        the date and count to js"""
        report_date = []
        report_count = []
        report_employee = []
        # Data based on date
        if input == 'date':
            for day in range(8):
                date_to_check = Date.subtract(Date.today(), days=day)
                count = self.search_count([('date', '=', date_to_check)])
                if count != 0:
                    report_date.append(str(date_to_check))
                    report_count.append(count)
            result = {'value': report_date, 'count': report_count}
        # Data based on employee
        if input == 'employee':
            records = self.search([]).mapped('employee')
            for employee in set(records):
                count = self.search_count([('employee', '=', employee)])
                report_employee.append(employee)
                report_count.append(count)
            result = {'value': report_employee, 'count': report_count}
        return result
