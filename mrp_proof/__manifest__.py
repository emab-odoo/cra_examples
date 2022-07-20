# -*- coding: utf-8 -*-
{
    'name': 'CRA Proof to Mrp',

    'summary': """Adding proof pdf mrp production order""",
    'description': """
        capturing the proof_pdf from the sales module and presenting it in the mrp module
    """,
    'author': 'Christopher K Rad (cracustom), Emiliano Abascal (odoo)',
    'website': 'https://www.cracustom.com',
    'category': 'CRA Custom Development | MRP App',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['mrp', 'proofprocess'],

    'data': [
        'views/mrp_production_views.xml'
    ],

    'demo': [

    ],
}
