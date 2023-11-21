# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import api, models


class SalesDashboard(models.Model):
    _name = 'sales.dashboard'
    _description = 'SalesDashboard'

    @api.model
    def get_sale_details(self, limit=None):
        """get_sale_details function is for accessing the records in between
        the dates.
        data_access() function is calling from this function.
        """
        date_count = int(limit)
        end_date = date.today()
        if date_count == 30:
            start_date = end_date - timedelta(days=30)
            result = self.data_access(start_date, end_date)
        elif date_count == 90:
            start_date = end_date - timedelta(days=90)
            result = self.data_access(start_date, end_date)
        return result

    def data_access(self, start_date, end_date):
        """Access all data required for the sales dashboard from this function."""
        sale_orders = self.env['sale.order'].search(
            [('date_order', '>', start_date), ('date_order', '<', end_date)])
        # For list of quotations and count
        quotations = []
        for quotation in sale_orders.filtered(lambda qtns: qtns.state == 'draft'):
            quotations.append(quotation.id)
        # For list of orders and count
        orders = []
        for order in sale_orders.filtered(lambda order: order.state == 'sale'):
            orders.append(order.id)
        revenue = round(sum(sale_orders.mapped('amount_total')), 2)
        avg_orders = round(revenue / len(sale_orders), 2)

        # For accessing the Sales Team
        sales_team = sale_orders.mapped('team_id')
        teams = []
        teams_values = []
        for team_id in sales_team:
            teams.append(
                team_id.name
            )
            sales_count = len(sale_orders.filtered(lambda sale: sale.team_id.id == team_id.id))
            teams_values.append(
                sales_count
            )

        # For accessing the sales Person
        sales_person = sale_orders.mapped('user_id')
        persons = []
        persons_values = []
        for person_id in sales_person:
            persons.append(
                person_id.name
            )
            person_count = len(sale_orders.filtered(lambda sale_person: sale_person.user_id.id == person_id.id))
            persons_values.append(
                person_count
            )

        # For top 10 customers
        customers = sale_orders.mapped('partner_id')
        customer_value = []
        for partner_id in customers:
            customer_sales = len(sale_orders.filtered(lambda cs: cs.partner_id.id == partner_id.id))
            customer_value.append({
                'name': partner_id.name,
                'count': customer_sales
            })
        top_customer = sorted(customer_value, key=lambda i: i['count'], reverse=True)
        customer_name = [i.get('name') for i in top_customer]
        customer_value = [i.get('count') for i in top_customer]

        # For lowest and highest selling products
        sale_order_lines = sale_orders.order_line
        products = []
        for pro in sale_order_lines:
            products.append(
                pro.product_template_id.id
            )
        product_details = []
        for product_id in set(products):
            product_sales = len(sale_orders.order_line.filtered(
                lambda tp: tp.product_template_id.id == product_id))
            product_details.append({
                'name': self.env['product.template'].browse(product_id).name,
                'count': product_sales
            })
        top_products = sorted(product_details, key=lambda count_desc: count_desc['count'], reverse=True)
        top_products_name = [name.get('name') for name in top_products[:7]]
        top_products_count = [count.get('count') for count in top_products[:7]]

        low_products = sorted(product_details, key=lambda count_asc: count_asc['count'])
        low_products_name = [name.get('name') for name in low_products[:7]]
        low_products_count = [count.get('count') for count in low_products[:7]]

        # sale order based on order state
        order_status = sale_orders.mapped('state')
        state_name = []
        state_value = []
        for state in set(order_status):
            state_name.append(
                state
            )
            order_state = len(sale_orders.filtered(
                lambda ordr_state: ordr_state.state == state))
            state_value.append(
                order_state
            )

        # sale order based on order state
        invoice_status = sale_orders.mapped('invoice_status')
        invoice_state = []
        invoice_value = []
        for state in set(invoice_status):
            invoice_state.append(
                state
            )
            order_state = len(sale_orders.filtered(
                lambda ordr_state: ordr_state.invoice_status == state))
            invoice_value.append(
                order_state
            )

        # Return the dict of datas to sales_dashboard.js
        records = {
            'quotation_count': len(quotations), 'quotations': quotations,
            'order_count': len(orders), 'orders': orders,
            'revenue': revenue, 'avg_order': avg_orders,
            'teams': teams, 'team_value': teams_values,
            'persons': persons, 'persons_values': persons_values,
            'customer_names': customer_name, 'customer_values': customer_value,
            'low_products_name': low_products_name, 'low_products_count': low_products_count,
            'top_products_name': top_products_name, 'top_products_count': top_products_count,
            'state': state_name, 'state_count': state_value,
            'invoice_state': invoice_state, 'invoice_value': invoice_value,
        }
        return records
