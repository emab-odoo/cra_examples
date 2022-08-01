# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        #Calls OG action_confirm
        res = super().action_confirm()
        #List of dictionaries with values desired for creation
        vals_list = []
        #Since we need info from sale order lines, we iterate over them, also, I believe the idea is to create an event for each of the products that need proof.\
        if self.completion_method == 'deliver' or self.completion_method == 'install':
            if not self.customer_exp_date:
                raise UserError('For a calendar event to be created, customer expected date must be set.')
            vals_list.append({
                    'sale_order_id': self.id,
                    'name':self.partner_id.name + " ",
                    'start': self.customer_exp_date,
                    'stop': self.customer_exp_date + relativedelta(hours=1)
                })
            print(vals_list, self.customer_exp_date)
            #Call the create method of the calendar.event, passing the list of dictionaries, each dictionary = new record.
            self.env['calendar.event'].create(vals_list)
        return res
