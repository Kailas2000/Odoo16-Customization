# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SalesPerson(models.Model):
    _inherit = 'sale.order'
    _description = "Sales Order"

    commission_amount = fields.Float(readonly=True)

    @api.onchange('order_line')
    def commission_plan(self):
        """While Changing the order line in the sale order the function
        will work based on the Type"""
        self.commission_amount = 0
        max_reached = False

        # User Graduated Comparison
        if self.user_id.commission_plan_id.revenue_wise_type == 'graduated':
            # print('user graduate')
            for rec in self.order_line:
                for record in self.user_id.commission_plan_id.revenue_type_ids:
                    if rec.price_subtotal >= record.from_amount and rec.price_subtotal <= record.to_amount:
                        amount = rec.price_subtotal * (record.rate / 100)
                        self.commission_amount += amount

        # Team Graduated Comparison
        if self.team_id.commission_plan_id.revenue_wise_type == 'graduated' and not self.user_id.commission_plan_id:
            # print('team graduate')
            for rec in self.order_line:
                for record in self.team_id.commission_plan_id.revenue_type_ids:
                    if rec.price_subtotal >= record.from_amount and rec.price_subtotal <= record.to_amount:
                        amount = rec.price_subtotal * (record.rate / 100)
                        self.commission_amount += amount

        for rec in self.order_line:
            # User Straight Comparison
            for plans in self.user_id.commission_plan_id.revenue_type_ids:
                # print('user straight')
                if self.user_id.commission_plan_id.revenue_wise_type == 'straight':
                    if self.amount_total >= plans.from_amount and self.amount_total <= plans.to_amount:
                        self.commission_amount = self.amount_total * (
                                    plans.rate / 100)

            # User Product Wise Comparison
            for plan in self.user_id.commission_plan_id.product_type_ids:
                # print('user product')
                if rec.product_id.product_tmpl_id.categ_id == plan.product_cate_id and max_reached == False:
                    amount = rec.price_subtotal * (plan.rate_percentage / 100)
                    if amount > plan.max_commission_amount and plan.max_commission_amount != 0:
                        self.commission_amount = plan.max_commission_amount
                        max_reached = True
                    else:
                        self.commission_amount += amount
                if rec.product_id.product_tmpl_id == plan.products_id:
                    amount = rec.price_subtotal * (plan.rate_percentage / 100)
                    if amount > plan.max_commission_amount and plan.max_commission_amount != 0:
                        self.commission_amount = plan.max_commission_amount
                        max_reached = True
                    else:
                        self.commission_amount += amount

            # Team Comparison straight and product wise
            if not self.user_id.commission_plan_id:
                # Team straight Comparison
                for plans in self.team_id.commission_plan_id.revenue_type_ids:
                    # print('team straight')
                    if self.team_id.commission_plan_id.revenue_wise_type == 'straight':
                        if self.amount_total >= plans.from_amount and self.amount_total <= plans.to_amount:
                            self.commission_amount = self.amount_total * (plans.rate/100)

                # Team Product Wise Comparison
                for plan in self.team_id.commission_plan_id.product_type_ids:
                    # print('team product')
                    if rec.product_id.product_tmpl_id.categ_id == plan.product_cate_id and max_reached == False:
                        amount = rec.price_subtotal * (plan.rate_percentage/100)
                        if amount > plan.max_commission_amount:
                            self.commission_amount = plan.max_commission_amount
                            max_reached = True
                        else:
                            self.commission_amount += amount
                    if rec.product_id.product_tmpl_id == plan.products_id:
                        amount = rec.price_subtotal * (plan.rate_percentage/100)
                        self.commission_amount += amount
