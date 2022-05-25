# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    #Don't know yet if this is necessary
    sale_order_id = fields.Many2one(comodel_name = 'sale.order', string='Sale Order', store = True)
    #Reference to the sale order line.
    sale_order_line_id = fields.Many2one(comodel_name = 'sale.order.line', string='Sale Order Line', store = True)
    #Reference to the cra_proof pdf.
    cra_proof = fields.Binary(related = 'sale_order_line_id.cra_proof.proof_pdf')
    #Override create method to find the sale order line from which it comes from and set the cra proof pdf reference.
    def create(self, values):
        #mrp.production create method returns a record of itself.
        production = super(MrpProduction, self).create(values)
        #Origin is the name of the object from which the manufacturing order comes from in our case, from a sale order.
        origin = production.origin
        if(origin):
            #FInd the sale order.
            sale_order = self.env['sale.order'].search([('name', '=', origin)])
            #TODO: If two equal products are on the sale order it will find one and create the reference to it, which is wrong, it should check if other MO have been created from the same origin and use the sale order line that has not been used yet.
            manufacturing_orders_with_same_product = self.env['sale.order'].search([('origin', '=', origin), ('')])
            #If sale order exists, then assign the references to it on mrp.production
            if(sale_order):
                self.sale_order_id = sale_order.id
                for line in sale_order.order_line:
                    if(line.needs_proof):
                        #If the product on the line is the same as on the MO, assign the sale order line on production. The proof pdf is using this relation.
                        if(production.product_id == line.product_id):
                            production.sale_order_line_id = line.id
        return production