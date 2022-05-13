# -*- coding: utf-8 -*-

from email.policy import default
from tracemalloc import stop
from odoo import models, fields, _

# New model for the proof wizard.


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    needs_proof = fields.Boolean(string='Needs Proof',
                                 store=True)
