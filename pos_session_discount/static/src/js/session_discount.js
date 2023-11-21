odoo.define('pos_session_discount.session', function (require) {
"use strict";

    var ProductScreen = require('point_of_sale.ProductScreen');
    var Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');

    const CustomOrder = (ProductScreen) => class CustomOrder extends ProductScreen {
        async _onClickPay() {
        var value = true
        var session_id = this.env.pos.pos_session.id
        var orders = this.env.pos.orders
        var discount_limit = this.env.pos.config.discount_limit
        var discount_amount = this.env.pos.config.discount_amount
        var self = this;

        await rpc.query({
            model: 'pos.config',
            method: 'get_order_id',
            args: [session_id],
        }).then(function (total_discount_amount) {
            let order_dis_amount = 0
            if(discount_limit == true){
                if(total_discount_amount > discount_amount) {
                    value = false
                    self.showPopup('ConfirmPopup', {
                        title: self.env._t('Discount Limit Exceed'),
                        body: self.env._t('Your Session maximum discount amount is reached.'),
                    });
                }
                else{
                    for(let order = 0; order < orders.length; order++) {
                        var orderline = orders[order].orderlines
                        for(let line = 0; line < orderline.length; line++) {
                            let dis_per = orderline[line].discount
                            let pro_price = orderline[line].price
                            let pro_qty = orderline[line].quantity
                            order_dis_amount = order_dis_amount + (pro_price * pro_qty) * (dis_per / 100)
                        }
                    }
                    total_discount_amount = total_discount_amount + order_dis_amount
                    if(total_discount_amount > discount_amount) {
                        value = false
                        self.showPopup('ConfirmPopup', {
                            title: self.env._t('Discount Limit Exceed'),
                            body: self.env._t('Your Session maximum discount amount is reached.'),
                        });
                    }
                }
            }
        });
        if(value == true) {
            var result = super._onClickPay(...arguments)
        }
        return result;
        }
    }
       Registries.Component.extend(ProductScreen, CustomOrder);
    });