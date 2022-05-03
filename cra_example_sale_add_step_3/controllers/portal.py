# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager


class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/validate_proof'],
                type='http',
                auth="public",
                website=True)
    def portal_quote_validate_proof(self,
                                    order_id,
                                    access_token=None,
                                    approve=None,
                                    reasons=None):
        print(access_token, request.env.user.email)

        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get(
            'access_token')
        try:
            order_sudo = self._document_check_access('sale.order',
                                                     order_id,
                                                     access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo.proof_has_to_be_validated():
            return {
                'error': _('The order does not need to be approved for proof.')
            }
        if (approve):
            try:
                order_sudo.write({
                    'proof_validated_by': request.env.user.email,
                    'proof_validated_on': fields.Datetime.now(),
                    'proof_validated': True
                })
                request.env.cr.commit()
            except (TypeError, binascii.Error) as e:
                return {'error': _('Invalid signature data.')}

            pdf = request.env.ref('sale.action_report_saleorder').with_user(
                SUPERUSER_ID)._render_qweb_pdf([order_sudo.id])[0]
            attachments = [('%s.pdf' % order_sudo.name, pdf)]
            attachments = None
            chatter_message = _('Proof validated by %s(%s)') % (
                order_sudo.partner_id.display_name, request.env.user.email)
            allow_payment = '#allow_payment=yes'
        else:
            chatter_message = reasons
            attachments = None
            allow_payment = '#allow_payment=no'

        _message_post_helper('sale.order',
                             order_sudo.id,
                             chatter_message,
                             attachments=attachments,
                             **({
                                 'token': access_token
                             } if access_token else {}))

        query_string = '&message=proof_ok'
        if order_sudo.has_to_be_paid(True):
            query_string += allow_payment
        return request.redirect(
            order_sudo.get_portal_url(query_string=query_string))