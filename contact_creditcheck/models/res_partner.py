import requests
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

class Partner(models.Model):
    _inherit = 'res.partner'
    
    credit_check_file = fields.Binary("Credit Check File", store=True, attachment=True) 
    credit_status = fields.Boolean("Credit Status", compute="compute_credit_status")
    latest_paid_invoice = fields.Many2one(string="Latest Paid Invoice", comodel_name="account.move")

    def compute_credit_status(self):
        credit_check_file = True if self.credit_check_file else False
        invoices_paid = True
        result = False
        latest_invoice = False
        latest_invoice_date = False
        inmediate_payment = True if self.property_payment_term_id.name == "Immediate Payment" else False
        
        for invoice in self.invoice_ids:
            if invoice.invoice_date:
                if(invoice.payment_state != 'paid'):
                    invoices_paid = False
                    break
                else:
                    if not latest_invoice_date:
                        latest_invoice_date = invoice.invoice_date
                        latest_invoice = invoice
                    else:
                        latest_invoice_date = invoice.invoice_date if(latest_invoice_date < invoice.invoice_date) else latest_invoice_date
                        latest_invoice = invoice if(latest_invoice_date <= invoice.invoice_date) else latest_invoice
        if(inmediate_payment and invoices_paid and latest_invoice):
            self.latest_paid_invoice = latest_invoice
            result = True
        else:
            if(credit_check_file and invoices_paid):
                self.latest_paid_invoice = latest_invoice
                result = True
        self.credit_status = result