from odoo import http
from odoo.http import request, route


class RentSnippet(http.Controller):
    @http.route('/top_rental', type="json", auth="public")
    def top_rental(self):
        top_rent = request.env['rental.vehicle'].search_read([], ['name', 'brand', 'rent', 'rent_request', 'vehicle_id'])
        descending_order = sorted(top_rent, key=lambda l: l['rent_request'], reverse=True)
        records = []
        for rec in descending_order:
            values = {
                'name': rec['name'],
                'brand': rec['brand'],
                'rent': rec['rent'],
                'vehicle_id': rec['id']
            }
            records.append(values)
        return records

    @route(route='/vehicle_details/<vehicle_id>', auth='public', website=True)
    def vehicle_details(self, vehicle_id):
        vehicle_details = request.env['rental.vehicle'].browse(int(vehicle_id))
        return request.render(
            'vehicle_rental.vehicle_details_view_template',
            {'vehicle_details': vehicle_details})

