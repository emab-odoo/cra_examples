# -*- coding: utf-8 -*-
{
    'name':
    'Example CRA Module with widgets to add images.',
    'summary':
    """""",
    'description':
    """
        - Quadrigram: emab.
        """,
    'author':
    'Odoo, Inc.',
    'website':
    'https://www.odoo.com',
    'category':
    'Custom Development',
    'version':
    '0.1',
    'depends': ['sale_management', 'portal', 'web'],
    'data': [
        'views/sale_views.xml', 'wizards/cra_proof.xml',
        'security/ir.model.access.csv', 'views/sale_portal_templates.xml',
        'views/product_views.xml'
    ],
    'license':
    'OPL-1',
}
