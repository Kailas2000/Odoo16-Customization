# -*- coding: utf-8 -*-
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import json

from odoo.tools.safe_eval import datetime

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Wizard form for report'

    from_date = fields.Date(string="From Date",
                           help="Report data will be visible from From Date")
    to_date = fields.Date(string="ToDate",
                         help="Data will be visible upto this date, if mention")
    name_id = fields.Many2one(comodel_name='fleet.vehicle',
                          string="Vehicle Name",
                          help="To access the vehicles")
    customer_id = fields.Many2one("res.partner", string="Customer")

    @api.onchange('to_date', 'from_date')
    def _date_check(self):
        """created for date validation"""
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("To date must be after From date")

    def button_action_pdf(self):
        """While clicking the button from the form
        it return to the report.xml action."""
        return self.env.ref('vehicle_rental.action_report_vehicle_rental'
                            ).report_action(self, data=self.read()[0])

    def button_action_xlsx(self):
        """While clicking the button from the form
        it return the values"""
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'name_id': self.name_id.id,
            'customer_id': self.customer_id.id
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'report.wizard',
                    'options': json.dumps(data,
                                          default=date_utils.json_default),
                    'output_format': 'xlsx',
                    'report_name': 'Excel Report',
                    },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print(data)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        vehicle_name = self.env['fleet.vehicle'].browse(data.get('name_id')).name
        print(vehicle_name)
        customer_name = self.env['res.partner'].browse(data.get('customer_id')) .name
        query = """select pr.name as name, fv.name as model, 
                    rr.period, rr.from_date, rr.to_date, rr.state from rent_request as rr
                    inner join res_partner as pr on pr.id = rr.customer_id
                    inner join fleet_vehicle as fv on fv.id = rr.vehicle_id """
        term = 'where '
        if data['from_date']:
            query += """ where rr.from_date >= '%s' """ % data.get('from_date')
            term = 'AND '
        if data['to_date']:
            query += term + """ rr.to_date <= '%s' """ % data.get('to_date')
            term = 'AND '
        if data['name_id']:
            query += term + """ rr.vehicle_id = %s """ % data.get('name_id')
            term = 'AND '
        if data['customer_id']:
            query += term + """ rr.customer_id = '%s' """ % data.get('customer_id')
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px', 'border': 1})
        table_head = workbook.add_format(
            {'font_size': '12px', 'bold': True})
        date_style = workbook.add_format(
            {'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'align': 'center'})
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
        sheet.set_column(1, 8, 28)

        if customer_name != False:
            sheet.write('B5', 'Customer Name :', table_head)
            sheet.write('C5', customer_name, txt)
        if vehicle_name != False:
            sheet.write('B6', 'Vehicle Name :', table_head)
            sheet.write('C6', vehicle_name, txt)
        sheet.write('B7', 'Printed Date :', table_head)
        sheet.write('C7', datetime.datetime.now().strftime('%Y-%m-%d'), txt)
        if data['from_date'] != False:
            sheet.write('E5', 'From Date :', table_head)
            sheet.write('F5', data['from_date'], txt)
        if data['to_date'] != False:
            sheet.write('E6', 'To Date :', table_head)
            sheet.write('F6', data['to_date'], txt)
        sheet.write('E7', 'Company Details :', table_head)
        sheet.write('F7', self.env.company.name, txt)
        sheet.write('F8', self.env.company.city, txt)
        sheet.write('F9', self.env.company.mobile, txt)

        row = 12
        sl_no = 1
        if customer_name:
            sheet.merge_range('A2:F3', 'VEHICLE RENTAL REPORT', head)
            sheet.write('A11', 'SL.No', cell_format)
            sheet.write('B11', 'Model', cell_format)
            sheet.write('C11', 'No: of Days', cell_format)
            sheet.write('D11', 'Start Date', cell_format)
            sheet.write('E11', 'End Date', cell_format)
            sheet.write('F11', 'State', cell_format)
            for line in report:
                sheet.write(row, 0, sl_no, txt)
                sheet.write(row, 1, line.get('model'))
                sheet.write(row, 2, line.get('period'), txt)
                sheet.write(row, 3, line.get('from_date'), date_style)
                sheet.write(row, 4, line.get('to_date'), date_style)
                sheet.write(row, 5, line.get('state'), txt)
                row += 1
                sl_no += 1
        else:
            sheet.merge_range('A2:G3', 'VEHICLE RENTAL REPORT', head)
            sheet.write('A11', 'SL.No', cell_format)
            sheet.write('B11', 'Customer Name', cell_format)
            sheet.write('C11', 'Model', cell_format)
            sheet.write('D11', 'No: of Days', cell_format)
            sheet.write('E11', 'Start Date', cell_format)
            sheet.write('F11', 'End Date', cell_format)
            sheet.write('G11', 'State', cell_format)
            for line in report:
                sheet.write(row, 0, sl_no, txt)
                sheet.write(row, 1, line.get('name'))
                sheet.write(row, 2, line.get('model'))
                sheet.write(row, 3, line.get('period'), txt)
                sheet.write(row, 4, line.get('from_date'), date_style)
                sheet.write(row, 5, line.get('to_date'), date_style)
                sheet.write(row, 6, line.get('state'), txt)
                row += 1
                sl_no += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

