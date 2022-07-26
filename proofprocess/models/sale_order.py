# -*- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Re declaration, for selection fields the field should be extended using selection_add as used below, but Odoo displays the states in the order in which they are declared, there is a way to define the order, but I'm researching how this is done.
    # TODO: create a 'Project Name' field that captures the project name and present in mrp and calendar views
    state = fields.Selection(selection_add=[('proof', 'Upload Proof'), ('proof_sent', 'Proof Sent'), ('sale', )], )
    project_name = fields.Char(string='Project Name', store=True)
    proof_validated = fields.Boolean('Is the Proof Validated', copy=False, default=False, store=True)
    needs_proof = fields.Boolean('Needs proof', compute='check_if_so_needs_proof')
    # related = 'root related value. field you're relating 
    completion_method = fields.Selection(selection=[('deliver', 'Delivery'), ('ship', 'Shipping'), ('pick', 'Pick Up'), ('install', 'Installation')], string='Completion Method')
    customer_exp_date = fields.Datetime(string='Customer Expected Date', store=True, help='Date the customer expects the products to be recieved [delivered, installed, picked up, etc]')
    completion_date = fields.Date(string='Due Date', store=True, help='Date the manufactured products should be ready and on the shelf for last mile logistics')
    completion_notes = fields.Text(string='Notes', store=True)
    
    # TODO: Adding sale order -> create calendar event for later
    # self.env['calendar.event'].create(vals_list)
    # {'completion_method':self.completion_method}


    @api.onchange('order_line')
    def check_if_so_needs_proof(self):
        res = False
        for line in self.order_line:

            if (line.needs_proof):
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
        return proof_ready_to_send

    def proof_ready_for_approval(self):
        for line in self.order_line:
            if line.product_id.needs_proof:
                if not line.proof_pdf:
                    return False
        return True

    def proof_has_to_be_validated(self, include_draft=False):
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
  
    # moves state into proof status
    def action_approve_quotation(self):
        self.check_if_so_needs_proof()
        if (self.needs_proof):
            self.write({'state': 'proof'})
        else:
            self.action_confirm()

    def action_send_proof(self):
        res = ""
        error = False
        for line in self.order_line:
            if (line.needs_proof):
                if not line.proof_pdf:
                    error = True
                    res += line.display_name + "\n"

        if (error):
            raise UserError("Proof missing for lines:\n%s" % res)

        self.write({'state': 'proof_sent'})
        return self.action_quotation_send()


    def has_to_be_signed(self, include_draft=False):
        allowed_states = ['proof_sent', 'proof']
        if not self.needs_proof:
            allowed_states = ['sent']
        return (self.state in allowed_states or (self.state == 'draft' and include_draft)) and not self.is_expired and self.require_signature and not self.signature

    def has_to_be_paid(self, include_draft=False):
        allowed_states = ['proof_sent', 'proof']
        if not self.needs_proof:
            allowed_states = ['sent']
        transaction = self.get_portal_last_transaction()
        print(transaction)
        return (
            self.state in allowed_states or (self.state == 'draft' and include_draft)
        ) and not self.is_expired and self.require_payment and transaction.state != 'done' and self.amount_total

