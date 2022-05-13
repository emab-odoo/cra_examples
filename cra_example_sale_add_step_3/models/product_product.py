# -*- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, fields, _

# New model for the proof wizard.


class ProductProduct(models.Model):
    _inherit = 'product.product'

    needs_proof = fields.Boolean(related='product_tmpl_id.needs_proof', string='Needs Proof',
                                 store=False)
