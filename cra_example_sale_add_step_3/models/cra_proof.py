# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

# New model for the proof wizard.


class CRAProof(models.Model):
    _name = 'cra.proof'
    _description = "CRA custom model to store proofs for sale orders and MOs."

    # proof_image = fields.Image("Proof Image",
    #                            max_width=1920,
    #                            max_height=1920,
    #                            store=True)
    pdf_link = fields.Char("Proof Link", compute='get_proof_url')
    proof_pdf = fields.Binary("Proof PDF", store=True, attachment=True)
    product_id = fields.Many2one('product.product', "Product", store=True)

    sale_order_line = fields.Many2one('sale.order.line', 'SOL', store=True)

    def get_proof_url(self):
        self.pdf_link = "http://localhost:8069/web/content/cra.proof/%s/proof_pdf/" % self.id

    def proof_wizard(self):
        view = self.env.ref('cra_example_sale_add_step_3.view_proof_wizard')
        # Calls create method on cra.proof, and passes the sale_order_line as well as the proof image if there is any.
        wiz = self.env['cra.proof.wizard'].create({
            'cra_proof':
            self.id,
            'proof_pdf':
            self.proof_pdf
        })
        # Creates action to display the wizard
        return {
            'name': _('Proof for %s', self.product_id.display_name),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cra.proof.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }

    @api.depends('proof_pdf')
    def check_order_lines(self):
        self.sale_order_line.proof_ready = True
        if(self.sale_order_line.order_id.needs_proof):
            self.sale_order_line.order_id.check_if_proofs_ready()
