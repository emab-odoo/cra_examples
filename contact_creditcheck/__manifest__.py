# -*- coding: utf-8 -*-
{
    'name': 'CRA Contact Credit Check',

    'summary': """Adding contact credit check status to contact""",
    'description': """
        Goals for this development:
        Create a credit check form value to store credit check pdf
        Create a step in the proofprocess quotation stage for credit approval to be applied by a subset of users
        Create automated invoices based on the payment terms value:
            i.e. if quote accepted && payment terms = 50/50 --> create an invoice for 50% of the total amount
            - functional process: quote-creditcheck-proof-SO-MO(with invoice status)
    """,
    'author': 'Christopher K Rad (cracustom), Emiliano Abascal (odoo)',
    'website': 'https://www.cracustom.com',
    'category': 'CRA Custom Development | MRP App',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['base', 'proofprocess'],

    'data': [
        'views/res_partner_views.xml',
        'views/sale_views.xml'
    ],

    'demo': [

    ],
}
