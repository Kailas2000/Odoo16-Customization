# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RentRequest(models.Model):
    """Class represents the Rent Request"""
    _name = "rent.request"
    _inherit = 'mail.thread'
    _description = "Rent Request"
    _rec_name = "sequence_no"

    sequence_no = fields.Char(string='Sequence No', required=True,
                              readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one("res.partner", string="Customer")
    request_date = fields.Date('Request Date', required=True,
                               default=fields.Datetime.now())
    vehicle_id = fields.Many2one('rental.vehicle', string="Vehicle",
                                 domain="[('state', '=', 'available')]")
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    period = fields.Integer(string="Period", compute='_compute_period',
                            store=True)
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('confirm', 'Confirm'),
                   ('invoiced', 'Invoiced'), ('returned', 'Returned')],
        tracking=True,
        default='draft'
    )
    rent = fields.Float(string="Rent", compute='_compute_rent', tracking=True)
    period_type_id = fields.Many2one('rent.charge',
                                     string="Period Type",
                                     domain="[('time_id', '=', vehicle_id)]")
    period_rent = fields.Float(related='period_type_id.amount')
    warning = fields.Boolean(readonly=True)
    late = fields.Boolean(readonly=True)
    invoice_data_id = fields.Many2one(comodel_name="account.move")
    invoice_count = fields.Boolean()
    payment_states = fields.Boolean(compute='_compute_payment_state')
    company_id = fields.Many2one(
        'res.company', required=True,
        default=lambda self: self.env.company, readonly=True
    )

    @api.model
    def create(self, vals):
        """function declared for creating sequence Number"""
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code(
                'rent.request') or _('New')
        res = super(RentRequest, self).create(vals)

        # While saving the page checking the warning and late field
        if res.to_date < fields.Date.today():
            res.late = True
        elif ((res.to_date == fields.Date.today() + timedelta(days=2) or
               res.to_date == fields.Date.today() + timedelta(days=1)) or
              res.to_date == fields.Date.today()):
            res.warning = True
        return res

    @api.constrains('to_date', 'from_date')
    def _date_validation(self):
        """created for date validation"""
        if self.from_date >= self.to_date:
            raise ValidationError("To date must be after From date")

    @api.depends('to_date', 'from_date')
    def _compute_period(self):
        """To compute the number of days between from date and to date"""
        for record in self.filtered(lambda r: r.to_date and r.from_date):
            record.period = (record.to_date - record.from_date).days

    def action_confirm(self):
        """To change the state of model while clicking confirm button"""
        self.state = 'confirm'
        self.vehicle_id.state = 'not available'

    def action_return(self):
        """To change the state of model while clicking return button"""
        self.state = 'returned'
        # sudo is used as superuser, user has no write access in the rental_vehicle model so for that sudo is used.
        self.vehicle_id.sudo().state = 'available'

    @api.depends('period_type_id')
    def _compute_rent(self):
        """To compute the rent based on period type"""
        for record in self:
            if record.period_type_id.time == 'hour':
                record.rent = ((record.period * 24) * record.period_rent)
            elif record.period_type_id.time == 'day':
                record.rent = record.period * record.period_rent
            elif record.period_type_id.time == 'weak':
                record.rent = (record.period_rent / 7) * record.period
            elif record.period_type_id.time == 'month':
                record.rent = (record.period_rent / 30) * record.period
            else:
                record.rent = record.vehicle_id.rent * record.period

    def _date_check(self):
        """To set the warning true or false"""
        one_day_ago = fields.Date.today() - timedelta(days=1)

        records = self.search([
            ('state', '=', 'confirm')
        ])

        # 'Warning' condition
        warning = records.filtered(
            lambda r: r.to_date == fields.Date.today() + timedelta(days=2) or
                      r.to_date == fields.Date.today() + timedelta(days=1) or
                      r.to_date == fields.Date.today())

        # 'Late' condition
        late = records.filtered(lambda r: r.to_date <= one_day_ago)

        warning.write({'warning': True, 'late': False})
        late.write({'warning': False, 'late': True})

    def create_invoice(self):
        """Create an invoice and associate it with the request."""
        self.ensure_one()
        self.invoice_count = True

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.id,
            'invoice_line_ids': [
                fields.Command.create({
                    'name': self.vehicle_id.name,
                    'quantity': 1,
                    'price_unit': self.rent,
                })
            ]
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_data_id = invoice.id
        invoice.action_post()
        self.state = 'invoiced'

        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_data_id.id,
        }

    def action_view_invoice(self):
        """Invoice view"""
        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_data_id.id,
        }

    def _compute_payment_state(self):
        """Checking payment status to show the ribbon"""
        self.payment_states = True if self.invoice_data_id.payment_state == 'paid' else False

