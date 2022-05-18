# -*- codig: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

# New model for the proof wizard.


class CRAProofWizard(models.TransientModel):
    _name = 'cra.proof.wizard'
    _description = 'Wizard to upload the proof and add it to the cra.proof model'

    cra_proof = fields.Many2one('cra.proof', "CRA Proof", required=True)
    proof_pdf = fields.Binary("Proof PDF", attachment=False)
    file_name = fields.Char("File Name")

    def save_proof(self):
        if(self.proof_pdf != self.cra_proof.proof_pdf):
            self.cra_proof.proof_pdf = self.proof_pdf
        self.cra_proof.check_order_lines()

