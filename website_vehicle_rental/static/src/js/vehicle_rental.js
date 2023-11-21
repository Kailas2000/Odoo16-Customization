odoo.define('website_vehicle_rental.website_rental_template', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

    publicWidget.registry.RentRequest = publicWidget.Widget.extend({
        selector: '#rental_form',
        events: {
            'change #vehicle_ids': '_onVehicleChange',
            'change #from_date': '_onDateChange',
            'change #to_date': '_onDateChange',
            'change #period_types': '_onPeriodTypeChange',
        },

// Function to get the vehicle rent period
        _onVehicleChange: function () {
            var vehicle_id = this.$('#vehicle_ids').val();
            // Make an AJAX request to fetch data based on the selected vehicle_id
            if (!vehicle_id) {
                self.$('#period_types').empty();
            }
            this._rpc({
                route: '/get_period_type',
                params: {
                    vehicle_id: vehicle_id,
                },
            }).then(function (records) {
                console.log(records)
                self.$('#period_types').empty();
                self.$('#period_types').prepend('<option value="">Select Period Type</option>');
                records.forEach(function (record) {
                    self.$('#period_types').append(
                        `<option value="${record.id}">${record.period_type}</option>`
                    );
                });
            });
        },

// Function to calculate the period based on to date and from date
        _onDateChange: function () {
            var fromDate = new Date(this.$('#from_date').val());
            var toDate = new Date(this.$('#to_date').val());
            var daysDifference = 0;
            if (toDate < fromDate) {
                document.getElementById("date_check").style.visibility="visible";
                this.$('#period').val(daysDifference);
            }
            if (!isNaN(fromDate) && !isNaN(toDate) && toDate >= fromDate) {
                daysDifference = (toDate.getTime() - fromDate.getTime()) / (1000 * 3600 * 24);
                document.getElementById("date_check").style.visibility="hidden";
                this.$('#period').val(daysDifference);
                if (this.$('#period_types').val() !== '' && this.$('#vehicle_ids').val() !== '') {
                    this._onPeriodTypeChange();
                }
            }
        },

// Based on the rent period the rent should be changed
        _onPeriodTypeChange: function () {
            if (!isNaN(new Date(this.$('#from_date').val())) && !isNaN(new Date(this.$('#to_date').val()))) {
                this._rpc({
                    route: '/get_amount',
                    params: {
                        rec: this.$('#period_types').val(),
                        vehicle_id: this.$('#vehicle_ids').val(),
                    },
                }).then(function (record) {
                    console.log(record)
                    var period = self.$('#period').val()
                    if (record.period_type == 'hour') {
                        var rent_amount = ((period * 24) * record.amount)
                        }
                    else if (record.period_type == 'day') {
                        var rent_amount = period * record.amount
                        }
                    else if (record.period_type == 'weak') {
                        var rent_amount = (record.amount / 7) * period
                        }
                    else if (record.period_type == 'month') {
                        var rent_amount = (record.amount / 30) * period
                        }
                    else {
                        var rent_amount = record.rent
                        }
                    self.$('#rent').val(rent_amount);
                });
            }
        }
    })
})

