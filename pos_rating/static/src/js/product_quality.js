odoo.define('pos_rating.receipt', function (require) {
"use strict";

   var { Orderline } = require('point_of_sale.models');
   var Registries = require('point_of_sale.Registries');

   const CustomOrder = (Orderline) => class CustomOrder extends Orderline {
       export_for_printing() {
       var result = super.export_for_printing(...arguments);
       var product_rating = this.get_product().product_quality
       result.product_quality = product_rating
       return result;
   }
   }
       Registries.Model.extend(Orderline, CustomOrder);
   });