odoo.define('vehicle_rental.dynamic', function (require) {``

var PublicWidget = require('web.public.widget');
var rpc = require('web.rpc');
var core = require('web.core');
var qweb = core.qweb;

    var Dynamic = PublicWidget.Widget.extend({
        selector: '.rental_snippet',

        start: function() {
            var self = this;
            rpc.query({
                route: '/top_rental',
            }).then((datas) => {
                var chunks = _.chunk(datas, 4)
                chunks[0].is_active = true
                this.$el.find('#courosel').html(
                    qweb.render('vehicle_rental.vehicle_view_template',
                    {
                        chunks,
                        'carousel_id': Math.floor(Math.random()*1000+1)
                    })
                )
            });
        },
    });
   PublicWidget.registry.rental_snippet = Dynamic;
   return Dynamic;
});

