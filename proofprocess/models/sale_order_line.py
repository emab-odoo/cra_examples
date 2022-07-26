# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    # addons/sale/models/sale_order_line.py

    proof_pdf = fields.Binary("Proof PDF", related='cra_proof.proof_pdf')

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
    order_line_qty = fields.Integer(string='Ordered Qty', required=True, store=True, default=1)
    dimensions = fields.Char(string='Dimensions', help='Dimensions of order_line', copy=False, store=True)
    width_in = fields.Integer(string='Width', store=True, default=0)
    height_in = fields.Integer(string='Height', store=True, default=0)
    per_unit_val = fields.Float(compute="_compute_unit_val", string="Price Per Unit", store=True, readonly=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)

    # TODO: Create an overwrite method that calculates square feet and updates the Quantity value
    # Pseudo Code:
    # overwrite the _compute_amount method for SOL
    # for line in self:
    #   line.product_uom_qty = ((line.width_col_in * line.height_col_in)%144)*line.order_line_qty
    #   line.per_unit_val = (line.product_uom_qty%line.order_line_qty)*line.price_unit
    # Notes:
    # use @api.onchange
    # width, height
    # check if both fields
    # perform calculation
    # provide calculated value on product_uom_qty
    # api.onchange('height')
    # def on_change_height(self):

    @api.onchange('width_in', 'height_in', 'order_line_qty')
    def on_change_width_in_height_in(self):
        if self.width_in and self.height_in:
            self.product_uom_qty = ((self.width_in * self.height_in)/144)*self.order_line_qty
            self.per_unit_val = (self.product_uom_qty/self.order_line_qty)*self.price_unit

    @api.depends("per_unit_val")
    def _compute_unit_val(self):
        for line in self:
            line.per_unit_val = (line.product_uom_qty%line.order_line_qty)*line.price_unit

    def proof_wizard(self):
        if not self.cra_proof:
            if (self.needs_proof):
                vals_list = {
                    'product_id': self.product_id.id,
                    'sale_order_line': self.id
                }
                self.cra_proof = self.env['cra.proof'].create(vals_list)
        return self.cra_proof.proof_wizard()

    @api.ondelete(at_uninstall=False)
    def _unlink_except_confirmed(self):
        if(self.cra_proof):
            self.cra_proof.unlink()
        if not self.order_id.check_if_so_needs_proof():
            self.order_id.write({
                'state': 'sent'
            })
        if self._check_line_unlink():
            print(self.state)
            raise UserError(
                _('You can not remove an order line once the sales order is confirmed.\nYou should rather set the quantity to 0.'
                  ))
