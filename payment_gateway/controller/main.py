# -*- coding: utf-8 -*-
import logging
import pprint
from werkzeug.exceptions import Forbidden
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RazorPayController(http.Controller):
    @http.route(
        '/razor/payment-success', type='http', methods=['GET', 'POST'],
        auth='public', save_session=False, csrf=False)

    def razorpay_return_from_checkout(self, **data):
        """Process the notification data sent by RAZORPAY after redirection"""
        _logger.info("Handling redirection from razorpay with data:\n%s",
                     pprint.pformat(data))

        # Check the integrity of the notification.
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'razorpayment', data
        )
        if data.get('razorpay_order_id'):
            self._verify_notification_signature(data, tx_sudo)
        # Handle the notification data.
        tx_sudo._handle_notification_data('razorpayment', data)
        return request.redirect('/payment/status')

    @staticmethod
    def _verify_notification_signature(notification_data, tx_sudo):
        """Compare the received signature with the expected signature"""
        verified = tx_sudo.verify_signature(notification_data)
        if not verified:
            _logger.warning("received notification with invalid signature")
            raise Forbidden()
