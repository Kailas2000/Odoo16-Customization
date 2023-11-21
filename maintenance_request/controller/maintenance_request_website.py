from odoo.http import Controller, request, route


class MaintenanceRequest(Controller):
    @route('/maintenance_request', auth='public', website=True)
    def maintenance_request(self):
        """Data loading in the selection field request form"""
        equipment_id = request.env['maintenance.equipment'].search([])
        maintenance_team_id = request.env['maintenance.team'].search([])
        responsible_id = request.env['res.users'].search([])

        return request.render('maintenance_request.website_maintenance_template',
                              {'equipment_id': equipment_id,
                               'maintenance_team_id': maintenance_team_id,
                               'responsible_id': responsible_id})

    @route('/create/maintenance_request', auth='public', website=True)
    def create_maintenance_request(self, **kw):
        """Creating the request for the maintenance request through website."""
        maintenance_request = request.env['maintenance.request'].sudo().create({
            'name': kw.get('request'),
            'equipment_id': int(kw.get('equipment')),
            'request_date': kw.get('request_date'),
            'maintenance_type': kw.get('maintenance_type'),
            'maintenance_team_id': kw.get('team'),
            'user_id': int(kw.get('responsible')),
            'schedule_date': kw.get('schedule_date'),
        })
        mail_template = request.env.ref('maintenance_request.request_email_template')
        email_values = {
                'email_from': maintenance_request.company_id.email,
                'email_to': maintenance_request.user_id.email,
            }
        mail_template.send_mail(maintenance_request.id,
                                force_send=True,
                                email_values=email_values)
        return request.render(
            'maintenance_request.website_maintenance_request_success_template',
            {'maintenance_request': maintenance_request})

