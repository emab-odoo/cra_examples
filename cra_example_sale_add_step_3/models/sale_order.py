# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Re declaration, for selection fields the field should be extended using selection_add as used below, but Odoo displays the states in the order in which they are declared, there is a way to define the order, but I'm researching how this is done.
    state = fields.Selection([('draft', 'Quotation'), ('proof', 'Proof Ready'),
                              ('sent', 'Proof/Quotation Sent'),
                              ('sale', 'Sales Order'), ('done', 'Locked'),
                              ('cancel', 'Cancelled')],
                             string='Status',
                             readonly=True,
                             copy=False,
                             index=True,
                             tracking=3,
                             default='draft')
    proof_ready = fields.Boolean('Ready for approval',
                                 copy=False,
                                 default=False)

    proof_validated_by = fields.Char(
        'Proof Signed By',
        help='Name of the person that signed the SO.',
        copy=False)
    proof_validated_on = fields.Datetime('Proof Validated On',
                                         help='Date of the signature.',
                                         copy=False)
    proof_validated = fields.Boolean('Is the Proof Validated',
                                     copy=False,
                                     default=False)

    def check_if_proofs_ready(self):
        proof_ready_to_send = True
        for line in self.order_line:
            if line.needs_proof:
                if not line.cra_proof:
                    proof_ready_to_send = False
                    break
        if (proof_ready_to_send):
            self.state = 'proof'
        else:
            self.state = 'draft'

    def proof_ready_for_approval(self):
        for line in self.order_line:
            if line.product_id.needs_proof:
                if not line.proof_image:
                    return False
        return True

    def proof_has_to_be_validated(self, include_draft=False):
        # transaction = self.get_portal_last_transaction()
        if (self.proof_validated):
            return False
        for line in self.order_line:
            if line.product_id.needs_proof:
                return True
        return False

    #Best practice but the above issue is present, if you want, uncomment it and try it for ur self.

    # state = fields.Selection(selection_add = [
    #     ('proof', 'Proof'),
    #     ('proof_sent', 'Proof Sent')
    #     ])