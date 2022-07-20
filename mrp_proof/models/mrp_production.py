# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    #Reference to the sale order line, its id and cra_proof pdf
    sale_order_id = fields.Many2one(comodel_name = 'sale.order', string='Sale Order', store = True)
    sale_order_line_id = fields.Many2one(comodel_name = 'sale.order.line', string='Sale Order Line', store = True, domain="[('order_id', '=', sale_order_id)]")
    cra_proof = fields.Binary(related ='sale_order_line_id.cra_proof.proof_pdf') 
    alt_proof = fields.Binary("Alt Proof PDF", store=True, attachment=True)

    #Override create method to find the sale order line from which it comes from and set the cra proof pdf reference.
    def create(self, values):
        #mrp.production create method returns a record of itself.
        productions = super(MrpProduction, self).create(values)
        #Origin is the name of the object from which the manufacturing order comes from in our case, from a sale order.
        origins = []
        origin_to_so_map = {}

        for value in values:
            origin = value.get('origin', False)
            if(origin):
                if(origin not in origins):
                    origins.append(origin)
        sale_orders = self.env['sale.order'].search([('name', 'in', origins)])

        for sale in sale_orders:
            if(sale.name not in origin_to_so_map):
                origin_to_so_map[sale.name] = sale

        for production in productions:
            sale_order = None
            if(production.origin in origin_to_so_map):
                sale_order = origin_to_so_map[production.origin]
            if(sale_order):
                production.sale_order_id = sale_order.id
                for line in sale_order.order_line:
                    if (not line.is_on_manufacturing_order and line.needs_proof and production.product_id == line.product_id):
                        # If the product on the line is the same as on the MO, assign the sale order line on production. The proof pdf is using this relation
                        production.sale_order_line_id = line.id
                        line.is_on_manufacturing_order = True
                        break
        return production
