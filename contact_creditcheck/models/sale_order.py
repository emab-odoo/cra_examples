# -- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    state = fields.Selection(selection_add=[('cred_check', 'Check Credit'), ('proof', )], )
    credit_check_file = fields.Binary("Credit Check File", store=True, attachment=True, related='partner_id.credit_check_file')
    credit_status = fields.Boolean("Credit Status", related='partner_id.credit_status')
    property_payment_term_id = fields.Many2one(string="Customer Payment Terms", related='partner_id.property_payment_term_id')

    # moves state into proof status
    def action_approve_quotation(self):
        self.check_if_so_needs_proof()
        if (self.needs_proof):
            self.write({'state': "proof" if self.credit_status else "cred_check"})
        else:
            self.action_confirm()

    # moves state into proof status
    def action_approve_credit_check(self):
        if (self.state == "cred_check" and self.credit_status):
            self.write({'state': "proof"})
        else:
            raise UserError("The proof process can't start if the credit check is not approved.")


