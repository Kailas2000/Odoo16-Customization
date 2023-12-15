odoo.define('pos_combo_products.receipt', function (require) {
"use strict";

    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrder = (Orderline) => class CustomOrder extends Orderline {
//    Inherit the export for printing and pass the value to be shown in the receipt
        export_for_printing() {
           var result = super.export_for_printing(...arguments);
           result.combo_required = this.get_product().required;
           result.combo_selected = this.get_product().selected;
           return result;
        }
    }
        Registries.Model.extend(Orderline, CustomOrder);
    });