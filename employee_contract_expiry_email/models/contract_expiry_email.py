# -*- coding: utf-8 -*-
import base64
from odoo import models
from odoo.fields import Date


class ContractExpiryEmail(models.Model):
    _name = "contract.expiry.email"
    _description = "Contract Expiry Email"

    def _contract_date_check(self):
        """Function is call from the schedule action based on the interval
        number and check the expiring date with the added date in settings."""
        expiry_value = self.env['ir.config_parameter'].sudo().get_param(
            'employee_contract_expiry_email.is_expiry_email')
        date_count = self.env['ir.config_parameter'].sudo().get_param(
            'employee_contract_expiry_email.expiry_email')
        employee_contract_date_end = self.env['hr.contract'].search(
                                                    [('state', '=', 'open')])
        date_to_check = Date.add(Date.today(), days=int(date_count))
        admin_email = self.env.ref('base.group_erp_manager').users

        email_to_send = []
        managers = {'nomanager': []}
        for admin in employee_contract_date_end:
            if admin.date_end == date_to_check:
                email_to_send.append(admin.employee_id)

        for record in email_to_send:
            if record.parent_id:
                if record.parent_id in managers:
                    managers[record.parent_id].append(record)
                    continue
                managers[record.parent_id] = [record]
            else:
                managers['nomanager'].append(record)

        mail_template = self.env.ref(
            'employee_contract_expiry_email.contract_expiry_email_template')
        if expiry_value:
            for manager, employees in managers.items():
                if manager == 'nomanager':
                    data = {'report': employees}
                    email_values = {
                        'email_to': admin_email.email,
                    }
                    self.create_pdf(data, email_values, mail_template)
                else:
                    data = {'report': employees}
                    email_values = {
                        'email_to': manager.work_email,
                    }
                    self.create_pdf(data, email_values, mail_template)

    def create_pdf(self, data, email_values, mail_template):
        """Function is to create the pdf and convert the pdf into binary format
           and attach with the email."""
        report_template_id = self.env.ref(
            'employee_contract_expiry_email.action_report_contract_expire')
        data_record = base64.b64encode(
            self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                report_template_id, data=data)[0])
        ir_values = {
            'name': "Contract Details Report",
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        mail_template.attachment_ids = data_id.ids
        mail_template.send_mail(self.id,
                                force_send=True,
                                email_values=email_values)
