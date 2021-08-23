# -*- coding: utf-8 -*-
{
    'name': "storage_contract",

    'description': """
       a module for storage contract
    """,

    'author': "shaiju",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/sale_inher.xml',
        'views/templates.xml',
        'views/storage_contracts_view.xml',
        'wizard/storage_contract_wizard_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
