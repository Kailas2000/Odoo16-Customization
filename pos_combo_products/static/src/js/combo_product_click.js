odoo.define('pos_combo_products.ComboProduct', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    var rpc = require('web.rpc');

    const ComboProduct = (ProductScreen) => class ComboProduct extends ProductScreen {
//    On clicking the product from product screen
        async _clickProduct(event) {
            if (event.detail.is_combo){
                var products = await this.rpc({
                    model: 'product.template',
                    method: 'combo_product_details',
                    args: [event.detail.combo_ids],
                });
                var combo_products = {'product': event.detail, 'required_pro': [], 'optional_pro': [], 'count': []}
                for (var key in products) {
                    if (key == 'required_product'){
                        for (var category in products[key]) {
                            combo_products.required_pro.push({
                                category,
                                products: products[key][category].map((item)=>{
                                    return this.env.pos.db.get_product_by_id(item)
                                })
                            });
                        }
                    }
                    if (key == 'optional_product'){
                        for (var category in products[key]) {
                            combo_products.optional_pro.push({
                                category,
                                products: products[key][category].map((item)=>{
                                    return this.env.pos.db.get_product_by_id(item)
                                })
                            });
                            combo_products.count.push({
                                category,
                                count: products.optional_count[category]
                            });
                        }
                    }
                }
                this.showPopup('ComboProductPopup',{
                    title: event.detail.display_name,
                    body: combo_products,
                    required: combo_products.required_pro,
                    optional: combo_products.optional_pro,
                });
            }
            else {
                if (!this.currentOrder) {
                    this.env.pos.add_new_order();
                }
                const product = event.detail;
                const options = await this._getAddProductOptions(product);
                if (!options) return;
                await this._addProduct(product, options);
                NumberBuffer.reset();
            }
        }
    }
Registries.Component.extend(ProductScreen, ComboProduct);
return ComboProduct;
});
