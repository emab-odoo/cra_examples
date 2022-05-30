# -- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from xmlrpc.client import Boolean
from odoo import models, api, fields, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_on_manufacturing_order = fields.Boolean(string="Is on MO", store=True)