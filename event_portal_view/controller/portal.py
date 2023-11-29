# -*- coding: utf-8 -*-
from datetime import datetime, time, date
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal


class EventPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'events_count' in counters:
            events_count = request.env['events'].search_count([])
            values['events_count'] = events_count
        return values

    @http.route(['/my/events'], type='http', auth="user", website=True)
    def portal_my_events(self, **kwargs):
        event = request.env['events'].sudo().search([])
        return request.render("event_portal_view.portal_my_events",
                              {'events': event, 'page_name': 'events'})

    @http.route(['''/view/events/<model("events"):event>'''],
                type='http', auth="public", website=True)
    def portal_event_page(self, event):
        current_time = datetime.now().time()
        for slot in event.event_slot_ids:
            from_time_hours, from_time_minutes = divmod(int(slot.from_time * 60),
                                                        60)
            to_time_hours, to_time_minutes = divmod(int(slot.to_time * 60), 60)
            start_time = time(from_time_hours, from_time_minutes)
            end_time = time(to_time_hours, to_time_minutes)
            if (start_time <= current_time <= end_time
                    and event.start_date == date.today()):
                slot.state = 'Ongoing'
            elif start_time > current_time and event.start_date == date.today():
                slot.state = 'Upcoming'
            else:
                slot.state = 'Finished'
            if event.state == 'draft':
                slot.state = 'Upcoming'
        return request.render('event_portal_view.events_portal_template',
                              {'event_details': event, 'page_name': 'event'})

