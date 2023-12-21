# -*- coding: utf-8 -*-
from odoo import fields, models
import xmlrpc.client


class DbDetailsWizard(models.TransientModel):
    _name = 'db.details.wizard'
    _description = 'Wizard form for migrate the sale orders'

    db_15 = fields.Char(string="DB 15 Name", help="odoo 15 database name")
    username_db_15 = fields.Char(string="DB 15 Username",
                                 required=True,
                                 help="odoo 15 database username")
    password_db_15 = fields.Char(string="DB 15 Password",
                                 required=True,
                                 help="odoo 15 database password")
    url_db15 = fields.Char(string="DB 15 Port Number",
                           required=True,
                           default="http://localhost:",
                           help="odoo 15 port number")
    password_db_16 = fields.Char(string="DB 16 Password",
                                 required=True,
                                 help="odoo 16 database password")
    url_db16 = fields.Char(string="DB 16 URL",
                           required=True,
                           default=lambda self: self.env.company.get_base_url(),
                           help="url of odoo 16")

    def action_fetch_so(self):
        """While clicking the button in the wizard the data will be migrate from
        the database to current database."""
        try:
            db_16 = self.env.cr.dbname
            username_db_16 = self.env.user.login
            common_15 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url_db15))
            models_15 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url_db15))
            common_16 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url_db16))
            models_16 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url_db16))
            uid_db15 = common_15.authenticate(self.db_15, self.username_db_15,
                                              self.password_db_15, {})
            uid_db16 = common_16.authenticate(db_16, username_db_16,
                                              self.password_db_16, {})
        except:
            raise models.ValidationError("Database Connection Failed!! Enter valid datas")
        try:
            # ************************** Customers *****************************
            db_15_partners = models_15.execute_kw(self.db_15, uid_db15,
                                                  self.password_db_15,
                                                  'res.partner', 'search_read',
                                                  [], {'fields': ['id', 'name',
                                                                  'email',
                                                                  'user_ids',
                                                                  'image_1920']})
            db_16_partners = self.env['res.partner'].search([])
            customer_id = []
            for rec in db_15_partners:
                customer = db_16_partners.search(
                    [('name', '=', rec['name']), ('email', '=', rec['email'])])
                if not customer:
                    if rec['user_ids']:
                        db_15_users = models_15.execute_kw(self.db_15,
                                                          uid_db15,
                                                          self.password_db_15,
                                                          'res.users',
                                                          'search_read',
                                                           [[['id', '=', rec['user_ids'][0]]]],
                                                           {'fields': [
                                                               'name',
                                                               'login',
                                                               'email'
                                                           ]})
                        data = models_16.execute_kw(db_16, uid_db16,
                                                    self.password_db_16,
                                                    'res.users', 'create',
                                                    [db_15_users])
                        customer_id.append({rec['user_ids'][0]: data[0]})
                    else:
                        data = models_16.execute_kw(db_16, uid_db16,
                                                    self.password_db_16,
                                                    'res.partner', 'create',
                                                    [{'name': rec['name'],
                                                      'email': rec['email'],
                                                      'image_1920': rec['image_1920']
                                                      }])
                        customer_id.append({rec['id']: data})

            # *************************** Products *****************************
            db_15_products = models_15.execute_kw(self.db_15, uid_db15,
                                                  self.password_db_15,
                                                  'product.product', 'search_read',
                                                  [],
                                                  {'fields': ['id',
                                                              'default_code',
                                                              'name',
                                                              'detailed_type',
                                                              'image_1920',
                                                              'list_price']})
            db_16_products = self.env['product.product'].search([])
            product_id = []
            for rec in db_15_products:
                product = db_16_products.search([
                    ('name', '=', rec['name']),
                    ('default_code', '=', rec['default_code'])
                ])
                if not product:
                    value = models_16.execute_kw(db_16, uid_db16,
                                                 self.password_db_16,
                                                 'product.product', 'create',
                                                 [{'name': rec['name'],
                                                   'default_code': rec['default_code'],
                                                   'detailed_type': rec['detailed_type'],
                                                   'image_1920': rec['image_1920'],
                                                   'list_price': rec['list_price']
                                                 }])
                    product_id.append({rec['id']: value})

            # ************************** Sale Orders ***************************
            db_15_sale_orders = models_15.execute_kw(self.db_15, uid_db15,
                                                     self.password_db_15,
                                                     'sale.order', 'search_read',
                                                     [],
                                                     {'fields':
                                                          ['name', 'id',
                                                           'date_order',
                                                           'partner_id',
                                                           'user_id', 'state']})
            orders_id = []
            db_16_sale_orders = self.env['sale.order'].search([])
            for rec in db_15_sale_orders:
                sale_order = db_16_sale_orders.search([('name', '=', rec['name'])])
                if not sale_order:
                    for val in customer_id:
                        for key, value in val.items():
                            if key == rec['partner_id'][0]:
                                for user in customer_id:
                                    for user_key, user_value in user.items():
                                        if user_key == rec['user_id'][0]:
                                            order = models_16.execute_kw(db_16, uid_db16, self.password_db_16,
                                                                'sale.order', 'create',
                                                                [{'name': rec['name'],
                                                                  'date_order': rec['date_order'],
                                                                  'partner_id': value,
                                                                  'user_id': user_value,
                                                                  'state': rec['state']
                                                                }])
                                            orders_id.append({rec['id']: [order, rec['name']]})

            # ************************ Sale order line *************************
            db_15_sale_order_line = models_15.execute_kw(self.db_15, uid_db15,
                                                         self.password_db_15,
                                                         'sale.order.line',
                                                         'search_read', [],
                                                         {'fields': [
                                                             'order_id',
                                                             'product_id',
                                                             'name',
                                                             'product_uom_qty',
                                                             'customer_lead',
                                                             'price_unit', ]})
            for rec in db_15_sale_order_line:
                for val in orders_id:
                    for key, value in val.items():
                        if rec['order_id'][0] == key:
                            for product_val in product_id:
                                for product_key, product_value in product_val.items():
                                    if rec['product_id'][0] == product_key:
                                        models_16.execute_kw(
                                            db_16, uid_db16, self.password_db_16,
                                            'sale.order.line',
                                            'create', [{
                                                'order_id': value[0],
                                                'product_id': product_value,
                                                'product_uom_qty': rec['product_uom_qty'],
                                                'customer_lead': rec['customer_lead'],
                                                'price_unit': rec['price_unit']
                                            }])
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Data Transfer successfully completed',
                    'type': 'rainbow_man',
                }
            }
        except:
            raise models.ValidationError("Error !!")
