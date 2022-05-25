# -- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # manufacturing_order = fields.One2many(comodel_name='mrp.production',
    #                             inverse_name='sale_order_id')