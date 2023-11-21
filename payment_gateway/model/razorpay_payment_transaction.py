# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import razorpay
from werkzeug.urls import url_encode
from odoo import _, models
from odoo.exceptions import ValidationError

client = razorpay.Client(auth=("rzp_test_o36UiDz9mXH4ls", "iKGlIK4BqUyorTzWE6W2qsIQ"))
_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Rendering the details from processing values,
        the values in the order details, amount and all
        passing as a dict file."""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'razorpayment':
            return res
        DATA = {
            "amount": float(processing_values.get('amount')) * 100,
            "currency": "INR",
            "receipt": processing_values['reference']
        }
        order = client.order.create(data=DATA)
        base_url = self.provider_id.get_base_url()
        return_url_params = {'reference': self.reference}

        rendering_values = {
            'key_id': 'rzp_test_o36UiDz9mXH4ls',
            'name': self.company_id.name,
            'description': self.reference,
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'partner_name': self.partner_name,
            'partner_email': self.partner_email,
            'return_url': f"{base_url}razor/payment-success?{url_encode(return_url_params)}",
        }
        return rendering_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Accessing the function from odoo addons"""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'razorpayment' or len(tx) == 1:
            return tx
        reference = notification_data.get('error[description]')
        tx = self.search([('reference', '=', notification_data['reference']), ('provider_code', '=', 'razorpayment')])
        if not tx:
            raise ValidationError(
                "RAZORPAY: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def verify_signature(self, data):
        """ verify_signature() function is for payment signature verification:
        If the signature you generate on your server matches the razorpay_signature """
        verify = client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        })
        return verify

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'razorpayment':
            return
        if notification_data.get('error[description]'):
            self._set_error(notification_data.get('error[description]'))
        elif notification_data.get('razorpay_payment_id'):
            self._set_done()