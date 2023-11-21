# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import UserError, ValidationError


class VehicleRentalReport(models.AbstractModel):
    _name = 'report.vehicle_rental.report_vehicle_rent'
    _description = 'Get vehicle rental report PDF.'

    @api.model
    def _get_report_values(self, docids, data=None):
        """The model will be called from the action, the
         datas will be in the parameter data and the query
         will be processed based on the user 'input'"""

        query = """select pr.name as name, fv.name as model, 
                rr.period, rr.from_date, rr.to_date, rr.state from rent_request as rr
                inner join res_partner as pr on pr.id = rr.customer_id
                inner join fleet_vehicle as fv on fv.id = rr.vehicle_id"""

        term = ' where'
        if data['from_date']:
            query += """ where rr.from_date >= '%s' """ % data.get('from_date')
            term = 'AND'
        if data['to_date']:
            query += term + """ rr.to_date <= '%s' """ % data.get('to_date')
            term = 'AND '
        if data['name_id']:
            query += term + """ rr.vehicle_id = '%s' """ % data.get('name_id')[0]
            term = ' AND '
        if data['customer_id']:
            query += term + """ rr.customer_id = '%s' """ % data.get('customer_id')[0]

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        if report == []:
            raise UserError('There is no records to print.')
        return {
            'report': report,
            'data': data
        }

