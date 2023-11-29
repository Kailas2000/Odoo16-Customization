# -*- coding: utf-8 -*-
from datetime import date
from odoo import fields, models, api


class Events(models.Model):
    _name = "events"
    _inherit = ['mail.thread']
    _description = "Event"
    _rec_name = "university_name"

    university_name = fields.Char(string="Name", required=True,
                                  help="Mention the university name")
    university_code = fields.Integer(string="Code", required=True,
                                     help="Mention university code")
    university_type = fields.Selection(
        string='University Type',
        selection=[('central_university', 'Central university'),
                   ('state_university.', 'State University.'),
                   ('private_university', ' Private University'),
                   ('land_grant_university', 'Land-grant university')],
        required=True,
        help="Mention the university type"
    )
    university_event = fields.Char(string="University Event",
                                   help="Name the event to be held")
    university_event_type = fields.Char(string="University Event Type",
                                        help="Event type")
    start_date = fields.Date(string="Start Date", help="Start date of the event")
    end_date = fields.Date(string="End Date", help="End date of the event")
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'), ('ongoing', 'Ongoing'),
                   ('expired', 'Expired')],
        tracking=True,
        help="state of the event")
    event_slot_ids = fields.One2many("event.slots", inverse_name="slot_id",
                                     string="Event Slot",
                                     help="To access the event slot")

    @api.model
    def create(self, vals):
        """Set the state of the event based on the date
         while creating the event"""
        res = super(Events, self).create(vals)
        today = date.today()
        if today == res.start_date:
            res.state = 'ongoing'
        elif today < res.start_date:
            res.state = 'draft'
        elif today > res.end_date:
            res.state = 'expired'
        return res

