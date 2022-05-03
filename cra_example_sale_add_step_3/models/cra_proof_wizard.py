# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

# New model for the proof wizard.


class CRAProofWizard(models.TransientModel):
    _name = 'cra.proof.wizard'

    cra_proof = fields.Many2one('cra.proof', "CRA Proof", required=True)
    proof_image = fields.Image("Proof Image",
                               max_width=1920,
                               max_height=1920,
                               default="avatar_128")

    def save_proof(self):
        if (self.proof_image != self.cra_proof.proof_image
                and self.proof_image != "avatar_128"):
            print("save")
            self.cra_proof.proof_image = self.proof_image
            self.cra_proof.check_order_lines()
