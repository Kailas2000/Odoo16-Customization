from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteShop(WebsiteSale):

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, access_token=None, revive='', **post):
        """Inherit the shop/cart from website to add the custom BOM products as
                description in the cart."""
        bom_cart_field = request.env['ir.config_parameter'].sudo().get_param(
            'bom_cart.bom_cart')
        res = super(WebsiteShop, self).cart(access_token=access_token,
                                            revive=revive, **post)
        if bom_cart_field == 'True':
            config_products = request.env['ir.config_parameter'].sudo().get_param(
                'bom_cart.bom_products_ids').split(',')
            setting_products = []
            if len(config_products) == 1:
                setting_products.append(int(config_products[0][1:-1]))
            else:
                try:
                    for rec in range(len(config_products)):
                        if rec == 0:
                            first_split = config_products[rec].split('[')
                            setting_products.append(int(first_split[1]))
                        elif rec == len(config_products) - 1:
                            second_split = config_products[rec].split(']')
                            setting_products.append(int(second_split[0]))
                        else:
                            setting_products.append(int(config_products[rec]))
                except:
                    pass
            cart_products = request.website.sale_get_order().order_line.product_template_id
            bom_products_id = []
            for data in cart_products:
                if data.id in setting_products:
                    if data.bom_ids:
                        for records in data.bom_ids:
                            bom_products_id.append(records.product_tmpl_id.id)
            res.qcontext['product_id'] = bom_products_id
        return res

