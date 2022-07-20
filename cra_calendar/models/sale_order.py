# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        #Calls OG action_confirm
        res = super().action_confirm()
        #List of dictionaries with values desired for creation
        vals_list = []
        #Since we need info from sale order lines, we iterate over them, also, I believe the idea is to create an event for each of the products that need proof.
        for line in self.order_line:
            if line.needs_proof:
                #KEY = field_name, #Value = field_value, only name (description) is required, but here you could pass other fields, such as the date and time of the event, etc...
                vals_list.append({
                    'sale_order_id': self.id,
                    'sale_order_line_id': line.id,
                    'name':self.partner_id.name + " " + line.name
                })
        #Call the create method of the calendar.event, passing the list of dictionaries, each dictionary = new record.
        self.env['calendar.event'].create(vals_list)
        return res
