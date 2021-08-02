# -*- coding: utf-8 -*-
{
    'name': "POS multi uom price",
    'summary': 'POS Price per unit of measure',
    'category': 'Point of Sale',
    'version': '13.0.1.0.1',
    'license': "AGPL-3",
    'description': """
        With this module you can sell your products with different units of measure in POS.
    """,

    'author': "ehuerta at ixer.mx",
    'depends': ['point_of_sale','l10n_ve_res_currency'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/pos_multi_uom_price_templates.xml',
        'views/pos_order_views.xml'
    ],
    'qweb': [
        'static/src/xml/pos_multi_uom_price_templates.xml',
    ],
    'images': [
        'static/description/POS_multi_uom_price.png',
    ],
    'installable': True,
    'auto_install': False,
}
