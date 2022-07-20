# -*- coding: utf-8 -*-
{
    'name': 'CRA Calendar',

    'summary': """Model that auto creates calendar events based on SO completion value""",
    'description': """
    This module will create calendar events under the condition that the completion method value for an SO is:
    --> Delivery
    --> Install
    """,
    'author': 'Christopher K Rad (cracustom)',
    'website': 'https://www.cracustom.com',
    'category': 'CRA Custom Development | Calendar App',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['calendar', 'proofprocess', 'mrp_proof'],

    'data': [
        'views/calendar_views.xml'
    ],

    'demo': [

    ],
}

