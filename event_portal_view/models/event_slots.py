# -*- coding: utf-8 -*-
from odoo import models, fields


class EventSlots(models.Model):
    _name = "event.slots"
    _description = "event.slots"

    from_time = fields.Float(string="From", help="Add the event start time")
    to_time = fields.Float(string="To", help="Add the event end time")
    content = fields.Char('Content', help="Mention the event content")
    state = fields.Char(string='State', help="TO add the state of the event slot")
    slot_id = fields.Many2one("events", string="Event Slots",
                              help="To connect with the model events")

