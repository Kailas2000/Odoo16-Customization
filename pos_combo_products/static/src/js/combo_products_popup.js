odoo.define('pos_combo_products.ComboProductPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useState, onWillStart } = owl;

    class ComboProductPopup extends AbstractAwaitablePopup {
        setup(){
            super.setup();
            this.state = useState({
                id: [],
                select_product_name: [],
                count: 0,
                value: [],
            });
        }
    //  confirm button in the combo product popup
        async confirm(body) {
            const order = this.env.pos.get_order();
            order.add_product(body.product);
            body.product.required = body.required_pro;
            body.product.selected = this.state.select_product_name;
            order.selected_orderline.customerNote = 'Combo Products';
            super.confirm();
        }

    /* Select the optional product from the popup, showing the selected ribbon
        and checking the condition */
        async select_product(product, count) {
            if (!this.state.id.includes(product.id)) {
                this.state.id.push(product.id);
                this.state.select_product_name.push(product.display_name);
                this.state.count ++;
                if (this.state.value.length == 0) {
                    this.state.value.push({
                        'category': product.pos_categ_id[1],
                        'count': this.state.count
                    })
                }
                else {
                    let categoryExists = false;
                    for (let rec in this.state.value) {
                        if (this.state.value[rec].category === product.pos_categ_id[1]) {
                            // If the category exists, update the count
                            this.state.value[rec].count = this.state.count;
                            categoryExists = true;
                            break;
                        }
                    }
                    // If the category doesn't exist, add a new entry
                    if (!categoryExists) {
                        this.state.value.push({
                            'category': product.pos_categ_id[1],
                            'count': 1
                        });
                    }
                }
            }
            else{
                const index = this.state.id.indexOf(product.id);
                this.state.id.splice(index, 1);
                this.state.select_product_name.splice(index, 1);
                this.state.count --;
                for (var rec in this.state.value) {
                    if (this.state.value[rec].category == product.pos_categ_id[1]) {
                        this.state.value[rec].count = this.state.count;
                    }
                }
            }
            for (let record of count) {
                if (product.pos_categ_id[1] == record.category) {
                    if (this.state.count > record.count) {
                        this.showPopup('ErrorPopup', {
                            title: this.env._t(' Error'),
                            body:  this.env._t('Your maximum product selection reached !!'),
                        });
                        this.state.id.pop(product.id);
                        this.state.select_product_name.pop(product.display_name);
                        this.state.count --;
                    }
                }
            }
        }
    //  Cancel button in the popup
        async cancel() {
            super.cancel();
        }
    }
    ComboProductPopup.template = 'ComboProductsPopup';
    ComboProductPopup.defaultProps = {
        confirmText: 'Confirm',
        title: '',
        body: '',
    };
    Registries.Component.add(ComboProductPopup);
    return ComboProductsPopup;
});