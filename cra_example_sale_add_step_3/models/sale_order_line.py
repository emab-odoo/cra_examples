# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    proof_image = fields.Image("Proof Image",
                               max_width=1920,
                               max_height=1920,
                               related='cra_proof.proof_image')
    needs_proof = fields.Boolean('product.product',
                                 related='product_id.needs_proof')
    cra_proof = fields.One2many(comodel_name='cra.proof',
                                inverse_name='sale_order_line')
    proof_validated_by = fields.Char(
        'Proof Signed By',
        help='Name of the person that signed the SO.',
        copy=False, store='True')
    proof_validated_on = fields.Datetime('Proof Validated On',
                                         help='Date of the signature.',
                                         copy=False, store=True)
    proof_validated = fields.Boolean('Is the Proof Validated',
                                     copy=False,
                                     default=False, store=True)

    proof_ready = fields.Boolean('Ready for approval',
                                 copy=False,
                                 default=False, store=True)

    def proof_wizard(self):
        if not self.cra_proof:
            if (self.needs_proof):
                vals_list = {
                    'product_id': self.product_id.id,
                    'sale_order_line': self.id
                }
                self.cra_proof = self.env['cra.proof'].create(vals_list)
        return self.cra_proof.proof_wizard()
