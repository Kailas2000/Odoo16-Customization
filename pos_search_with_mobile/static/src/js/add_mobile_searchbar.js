odoo.define('pos_search_with_mobile.AddMobile', function (require) {
    'use strict';

    const { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const TicketScreen = require('point_of_sale.TicketScreen');

    // Extend the already exist class TicketScreen and added the mobile
    const AddMobile = (TicketScreen) =>class AddMobile extends TicketScreen {
        _getSearchFields() {
            const result = super._getSearchFields();
            result.MOBILE = {
                repr: (order) => order.get_partner_name(),
                displayName: this.env._t('Mobile'),
                modelField: 'partner_id.mobile',
            }
            return result;
        }

        getMobileNumber(order){
            var mobile = "";
            if  (order.partner){
                if (order.partner.mobile){
                    var mobile = order.partner.mobile
                }
            }
            return mobile;
        }
    }
    Registries.Component.extend(TicketScreen, AddMobile);
    return AddMobile;
});