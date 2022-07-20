# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super().action_confirm()
        vals_list = []
        for line in self.order_line:
            if line.needs_proof:
                vals_list.append({
                    'sale_order_id': self.id,
                    'sale_order_line_id': line.id,
                    'name':self.partner_id.name + " " + line.name
                })
        self.env['calendar.event'].create(vals_list)
        return res
