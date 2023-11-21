odoo.define('pos_remove_orderline.remove_orderline', function (require) {
"use strict";


    var Orderline = require('point_of_sale.Orderline');
    var Registries = require('point_of_sale.Registries');

/*  Extends Orderline and created the remove_orderlines()
    function to remove the order line */
   const RemoveOrderline = (Orderline) => class RemoveOrderline extends Orderline {
       remove_orderlines(eve) {
            var c_id = eve.target.dataset.id;
            var select_orderline = this.env.pos.selectedOrder.orderlines;
            for(let id=0; id<select_orderline.length; id++){
                if(select_orderline[id].cid == c_id) {
                    this.env.pos.selectedOrder.remove_orderline( select_orderline[id] )
                    break;
                }
            }
       }
   }
       Registries.Component.extend(Orderline, RemoveOrderline);
   });

