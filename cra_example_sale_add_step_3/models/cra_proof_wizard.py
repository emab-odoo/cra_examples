# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

# New model for the proof wizard.


class CRAProofWizard(models.TransientModel):
    _name = 'cra.proof.wizard'
    _description = "Wizard to upload a proof and add it to the cra.proof model."

    cra_proof = fields.Many2one('cra.proof', "CRA Proof", required=True)
    proof_pdf = fields.Binary("Proof pdf", attachment=False)
    file_name = fields.Char("File Name")
    # proof_image = fields.Image("Proof Image",
    #                            max_width=1920,
    #                            max_height=1920,
    #                            default="avatar_128")

    def save_proof(self):
        if(self.proof_pdf != self.cra_proof.proof_pdf):
            self.cra_proof.proof_pdf = self.proof_pdf
        self.cra_proof.check_order_lines()
        # if (self.proof_image != self.cra_proof.proof_image    http://localhost:8069/web/content/cra.proof/15/datas?download=true http://localhost:8069/web/content/cra.proof/15/proof_pdf/
        #         and self.proof_image != "avatar_128"):

        #     self.cra_proof.proof_image = self.proof_image
        #     self.cra_proof.check_order_lines()
