odoo.define('pos_remove_orderline.clear_cart', function (require) {
"use strict";

    var ProductScreen = require('point_of_sale.ProductScreen');
    var Registries = require('point_of_sale.Registries');

/*  Extends ProductsScreen and created the clear_orderlines()
    function to clear all order lines in a single click */
    const ClearOrder = (ProductScreen) => class ClearOrder extends ProductScreen {
    clear_orderlines(eve) {
        var select_order_id = this.env.pos.selectedOrder.orderlines.slice()
        for(let id=0; id < select_order_id.length; id++){
            this.env.pos.selectedOrder.remove_orderline( select_order_id[id] )
        }
    }
    }
        Registries.Component.extend(ProductScreen, ClearOrder);
    });