# -*- coding: utf-8 -*-
import calendar
from datetime import timedelta, date
from odoo import models, fields


class MonthDiscount(models.Model):
    _inherit = "sale.order"

    total_discounts = fields.Float(
        help="To calculate total discount of a month")
    max_discount = fields.Float(
        help="Maximum discount set in the sales settings")
    warning = fields.Boolean(compute="_compute_warning")
    discount_value = fields.Boolean(
        help="The discount field value in sales settings")

    def _compute_warning(self):
        self.discount_value = self.env['ir.config_parameter'].sudo().get_param(
            'discount_limit.discount_limit')
        self.max_discount = self.env['ir.config_parameter'].sudo().get_param(
            'discount_limit.discount_money')
        self.warning = True if self.discount_value == True and self.total_discounts > self.max_discount else False

    def action_confirm(self):
        """While confirming the sale order then particular function will be
      working based on the Quotation Date month, The amount set in the settings
      will be taken as the maximum discount amount."""
        self.total_discounts = 0
        if self.env['ir.config_parameter'].sudo().get_param('discount_limit.discount_period') == 'month':
            print('month')
            start_date = self.date_order.replace(day=1)
            _, last_day = calendar.monthrange(self.date_order.year,
                                              self.date_order.month)
            end_date = self.date_order.replace(day=last_day)
            orders = self.search([
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date)
            ])
        elif self.env['ir.config_parameter'].sudo().get_param('discount_limit.discount_period') == 'week':
            print('week')
            start_date = self.date_order - timedelta(days=self.date_order.weekday())
            week_start_date = start_date.date()
            # Find the end date of the current week (assuming Sunday as the end of the week)
            week_end_date = (start_date + timedelta(days=6)).date()
            orders = self.search([
               ('date_order', '>=', week_start_date),
               ('date_order', '<=', week_end_date)
            ])
        elif self.env['ir.config_parameter'].sudo().get_param('discount_limit.discount_period') == 'day':
            print('day')
            current_date = date.today()
            orders = self.search([
                ('date_order', '>=', current_date)
            ])

        for records in orders:
            for order_lines in records.order_line:
                discount = (order_lines.product_uom_qty * order_lines.price_unit) * (order_lines.discount / 100)
                self.total_discounts += discount
                print(self.total_discounts, "total+")
            self.warning = True if self.discount_value == True and self.total_discounts > self.max_discount else False
        super().action_confirm()


