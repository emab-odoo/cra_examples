# -*- coding: utf-8 -*-
{
    'name': 'CRA Proof Process Sales Extension',

    'summary': """Adding proof process to drafted sales order""",
    'description': """
        Proof Process overview
            Quote -
            Quote Sent -
            Proof -
            Proof Sent -
            Sales Order
    """,
    'author': 'Christopher K Rad (cracustom), Emiliano Abascal (odoo)',
    'website': 'https://www.cracustom.com',
    'category': 'CRA Custom Development | Sales App',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['sale_management', 'portal', 'web'],

    'data': [
        'views/sale_views.xml',
        'views/sale_portal_templates.xml',
        'views/product_views.xml',
        'wizards/cra_proof.xml',
        'security/ir.model.access.csv'
    ],

    'demo': [

    ],
}
