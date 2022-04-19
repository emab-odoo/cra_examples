# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

#New model for the proof wizard.
class Proof(models.TransientModel):
    _name = 'cra.proof'

    sale_order_line = fields.Many2one('sale.order.line', "SOL", required=True)
    proof_image = fields.Image("Proof Image", max_width=1920, max_height=1920, default = "avatar_128")
    
    def save_proof(self):
        if(self.proof_image != self.sale_order_line.proof_image):
            self.sale_order_line.proof_image = self.proof_image

