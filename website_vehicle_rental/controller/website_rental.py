from odoo.http import Controller, request, route


class VehicleRental(Controller):
    @route('/vehicle_rental', auth='public', website=True)
    def rental_url(self):
        """While clicking the button from website datas will be loaded and pass to the template"""
        customer_ids = request.env['res.partner'].search([])
        vehicle_ids = request.env['rental.vehicle'].search([('state', '=', 'available')])

        return request.render('website_vehicle_rental.website_rental_template',
                              {'customer_ids': customer_ids,
                                'vehicle_ids': vehicle_ids})

    @route('/get_period_type', type='json', auth='public', website=True)
    def get_period_type(self, vehicle_id=None):
        """To get the period type based on the vehicle"""
        # Perform a database query to fetch data based on the vehicle_id
        data = request.env['rental.vehicle'].search([('id', '=', vehicle_id or False)])
        records = []
        for rec in data.rent_charge_id:
            records.append({
                'id': rec.id,
                'period_type': rec.time,
                'amount': rec.amount,
                'rent': data.rent,
            })
        return records

    @route('/get_amount', type='json', auth='public', website=True)
    def get_amount(self, rec=None, vehicle_id=None):
        """To get the rent amount based on the period type"""
        data = request.env['rent.charge'].search([('id', '=', rec or False)])
        if not data:
            datas = request.env['rental.vehicle'].browse(int(vehicle_id)).rent
            record = {
                'rent': datas
            }
        else:
            record = {
                'rent': data.time_id.rent,
                'period_type': data.time,
                'amount': data.amount
            }
        return record

    @route('/create/rent_request', auth='public', website=True)
    def create_rent_request(self, **kw):
        """Create the new rent request in DB"""
        rent_request = request.env['rent.request'].sudo().create({
            'customer_id': kw.get('customer'),
            'request_date': kw.get('request_date'),
            'vehicle_id': kw.get('vehicle'),
            'from_date': kw.get('from_date'),
            'to_date': kw.get('to_date'),
            'period': kw.get('period'),
            'rent': kw.get('rent'),
            'period_type_id': kw.get('period_type'),
        })
        return request.render(
            'website_vehicle_rental.website_rental_success_template',
            {'rent_request': rent_request})

    @route('/customer', auth='public', website=True)
    def partner(self):
        """To view the countries in the partner form"""
        country_ids = request.env['res.country'].search([])
        return request.render('website_vehicle_rental.website_customer_template',
                              {'country_ids': country_ids})

    @route('/create/customer', auth='public', website=True)
    def create_partner(self, name, email, **kw):
        """Create the partner in DB"""
        partner_id = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': kw.get('phone'),
            'street': kw.get('street'),
            'country_id': kw.get('country'),
        })
        return request.render(
            'website_vehicle_rental.website_customer_template',
            {'partner_id': partner_id})

    @route(route='/rent_requests', auth='public', website=True)
    def rent_requests(self):
        """To list the rent request"""
        rent_requests = request.env['rent.request'].search([])
        return request.render('website_vehicle_rental.rent_request_list_template',
                              {'rent_req': rent_requests})

    @route(['''/view/rent_request/<model("rent.request"):rec>'''], auth='user',
           website=True)
    def view_rent_request(self, rec):
        """To view the specific rent request based on the button click"""
        return request.render('website_vehicle_rental.rent_request_view_template',
                              {'rent_details': rec})

