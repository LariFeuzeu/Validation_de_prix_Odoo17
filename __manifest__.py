# -*- coding: utf-8 -*-
{
    'name': "its_price_validation",

    'summary': "Validation du prix dans le systeme",

    'description': """
     Il permet la validation du prix entrer par l'utilisateur dans le systeme 
                              """,

    'author': "ITS, LARI FEUZEU",
    'website': "its-nh.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/SaleOrder.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
