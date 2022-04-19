# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    proof_image = fields.Image("Proof Image", max_width=1920, max_height=1920, store = True)
    
    def proof_wizard(self):
        view = self.env.ref('cra_example_sale_add_step_2.view_proof_wizard')
        #Calls create method on cra.proof, and passes the sale_order_line as well as the proof image if there is any.
        wiz = self.env['cra.proof'].create({'sale_order_line': self.id, 'proof_image':self.proof_image})
        #Creates action to display the wizard
        return {
            'name': _('Proof for %s', self.product_id.display_name),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cra.proof',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }
    
