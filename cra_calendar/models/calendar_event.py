# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

class Meeting(models.Model):
    _inherit = 'calendar.event'

    sale_order_id = fields.Many2one(comodel_name = 'sale.order', string='Sale Order', store=True)
    sale_order_line_id = fields.Many2one(comodel_name = 'sale.order.line', string='Sale Order Line', store=True, domain="[('order_id', '=', sale_order_id)]")
    completion_method = fields.Selection(string='Completion Method', related='sale_order_id.completion_method', store=True)
    # customer_exp_date = fields.Datetime(related='sale_order_line_id.customer_exp_date', string='Customer Expected Date', store=True)
    completion_notes = fields.Text(related='sale_order_id.completion_notes', string='Notes', store=True)
    partner_id = fields.Many2one(related='sale_order_id.partner_id', string='Customer', store=True, readonly=True)