# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, api, fields, _

# New model for the proof wizard.


class CRAProof(models.Model):
    _name = 'cra.proof'

    proof_image = fields.Image("Proof Image",
                               max_width=1920,
                               max_height=1920,
                               store=True)
    product_id = fields.Many2one('product.product', "Product", store=True)

    sale_order_line = fields.Many2one('sale.order.line', 'SOL', store=True)

    def proof_wizard(self):
        view = self.env.ref('cra_example_sale_add_step_3.view_proof_wizard')
        # Calls create method on cra.proof, and passes the sale_order_line as well as the proof image if there is any.
        wiz = self.env['cra.proof.wizard'].create({
            'cra_proof':
            self.id,
            'proof_image':
            self.proof_image
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

    @api.depends('proof_image')
    def check_order_lines(self):
        self.sale_order_line.order_id.check_if_proofs_ready()
