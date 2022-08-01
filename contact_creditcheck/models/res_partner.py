from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    
    credit_check_file = fields.Binary("Credit Check File", store=True, attachment=True)
    parent_credit_check_file = fields.Binary("Credit Check File", related='parent_id.credit_check_file', attachment=True)
    credit_status = fields.Boolean("Credit Status", compute="compute_credit_status")
    latest_paid_invoice = fields.Many2one(string="Latest Paid Invoice", comodel_name="account.move")

    def compute_credit_status(self):
        credit_check_file = True if (self.credit_check_file or self.parent_credit_check_file) else False
        invoices_paid = True
        result = False
        latest_invoice = False
        latest_invoice_date = False
        inmediate_payment = True if self.property_payment_term_id.name == "Immediate Payment" else False
        for invoice in self.invoice_ids:
            if invoice.invoice_date:
                # print(fields.Date.context_today(self), invoice.invoice_date_due)
                if(invoice.payment_state != 'paid' and invoice.invoice_date_due >= fields.Date.context_today(self)):
                    invoices_paid = False
                    break
                else:
                    if not latest_invoice_date:
                        latest_invoice_date = invoice.invoice_date
                        latest_invoice = invoice
                    else:
                        latest_invoice_date = invoice.invoice_date if(latest_invoice_date < invoice.invoice_date) else latest_invoice_date
                        latest_invoice = invoice if(latest_invoice_date <= invoice.invoice_date) else latest_invoice
        if inmediate_payment and invoices_paid and latest_invoice:
            self.latest_paid_invoice = latest_invoice
            result = True
        else:
            if credit_check_file and invoices_paid:
                self.latest_paid_invoice = latest_invoice
                result = True

        for child in self.child_ids:
            if not child.credit_status:
                result = False
                break

        self.credit_status = result