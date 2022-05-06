# -*- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Re declaration, for selection fields the field should be extended using selection_add as used below, but Odoo displays the states in the order in which they are declared, there is a way to define the order, but I'm researching how this is done.
    state = fields.Selection([('draft', 'Quotation'), ('sent', 'Quotation Sent'), ('proof', 'Upload Proof'), ('proof_sent', 'Proof Sent'),
                              ('sale', 'Sales Order'), ('done', 'Locked'),
                              ('cancel', 'Cancelled')],
                             string='Status',
                             readonly=True,
                             copy=False,
                             index=True,
                             tracking=3,
                             default='draft')

    proof_validated = fields.Boolean('Is the Proof Validated',
                                     copy=False,
                                     default=False, store=True)
    needs_proof = fields.Boolean(
        'Needs proof', compute='check_if_so_needs_proof')

    @api.onchange('order_line')
    def check_if_so_needs_proof(self):
        res = False
        for line in self.order_line:
            if(line.needs_proof):
                res = True
                break
        self.needs_proof = res

    def check_if_proofs_ready(self):
        proof_ready_to_send = True
        for line in self.order_line:
            if line.needs_proof:
                if not line.proof_ready:
                    proof_ready_to_send = False
                    break
        if (proof_ready_to_send):
            self.state = 'proof_sent'
        return proof_ready_to_send

    def proof_ready_for_approval(self):
        for line in self.order_line:
            if line.product_id.needs_proof:
                if not line.proof_image:
                    return False
        return True

    def proof_has_to_be_validated(self, include_draft=False):
        print(self.proof_validated)
        if (self.proof_validated):
            return False
        for line in self.order_line:
            if line.product_id.needs_proof:
                return True
        return False

    def check_if_all_items_have_been_validated(self):
        sale_order_proof_validated = True
        for line in self.order_line:
            if line.needs_proof:
                if not line.proof_validated:
                    sale_order_proof_validated = False
        self.proof_validated = sale_order_proof_validated
        return sale_order_proof_validated

    def action_approve_quotation(self):
        self.write({
            'state': 'proof'
        })

    def action_send_proof(self):
        self.write({
            'state': 'proof_sent'
        })

    def has_to_be_signed(self, include_draft=False):
        return (self.state == 'proof_sent' or (self.state == 'draft' and include_draft)) and not self.is_expired and self.require_signature and not self.signature

    # Best practice but the above issue is present, if you want, uncomment it and try it for ur self.

    # state = fields.Selection(selection_add = [
    #     ('proof', 'Proof'),
    #     ('proof_sent', 'Proof Sent')
    #     ])
