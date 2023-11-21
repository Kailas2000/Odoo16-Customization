from datetime import timedelta
from odoo import models, fields, api


class real_estate(models.Model):
    _name = "real.estate"
    _description = "New module"

    name = fields.Char("Estate Name", required=True, copy=False)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', required=True)
    date_availability = fields.Date('Available Date', required=True, copy=False,
                                    default=fields.Datetime.now() + timedelta(days=3 * 30))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedroom', required=True, default="2")
    living_area = fields.Integer('Living Area', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage', required=True)
    garden = fields.Boolean('Garden', required=True)
    garden_area = fields.Integer('Garden Area(sqm)')
    garden_orientation 	= fields.Selection(
        string='Garden Orientation',
        selection=[('east', 'East'), ('west', 'West'), ('north', 'North'), ('south', 'South')],
        help="Type is used to separate Leads and Opportunities"
    )
    Status = fields.Selection(
        string='status',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancel', 'Cancel')], default='new', copy=False
    )
    Active = fields.Boolean('Active', default=True)
    property_type = fields.Many2one("property.type", 'Property Type', required=True)
    salesman = fields.Many2one("res.partner", string="Salesman")
    buyer = fields.Many2one("res.users", string="Buyer", index=True, tracking=True, default=lambda self: self.env.user)
    property_tag = fields.Many2many("property.tag")
    offers_id = fields.One2many("estate.property.offer", inverse_name="property_id", string="Offer Lines")
    total_area = fields.Float(compute="_compute_total", string="Total Area")
    best_price = fields.Float(compute='_update_best_price', string="Best Price")

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offers_id.price')
    def _update_best_price(self):
        for record in self:
            if record.offers_id:
                record.best_price = max(record.offers_id.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_sold(self):
        self.ensure_one()
        self.write({'Status': 'sold'})

    def action_cancel(self):
        self.ensure_one()
        self.write({'Status': 'cancel'})

class property_type(models.Model):
    _name = "property.type"
    _description = "property type"

    name = fields.Char("Name", required=True)

class PropertyTag(models.Model):
    _name = "property.tag"

    name = fields.Char("Name", required=True)

class Property_Offer(models.Model):
    _name = "estate.property.offer"

    price = fields.Float()
    status2 = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
    partner_id = fields.Many2one("res.partner", 'Partner', required=True)
    property_id = fields.Many2one("real.estate", string="Property")
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline',
                                store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

