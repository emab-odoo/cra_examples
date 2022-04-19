# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    #Re declaration, for selection fields the field should be extended using selection_add as used below, but Odoo displays the states in the order in which they are declared, there is a way to define the order, but I'm researching how this is done.
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('proof', 'Proof'),
        ('proof_sent', 'Proof Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    #Best practice but the above issue is present, if you want, uncomment it and try it for ur self.

    # state = fields.Selection(selection_add = [
    #     ('proof', 'Proof'),
    #     ('proof_sent', 'Proof Sent')
    #     ])