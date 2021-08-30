# -*- coding: utf-8 -*-
{
    'name': "Adaptacion contable de moneda local dolares a Bs inventario fabricacion",

    'summary': """Adaptacion contable de moneda local dolares a Bs inventario fabricacion""",

    'description': """
       Adaptacion contable de moneda local dolares a Bs inventario fabricacion
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Adaptacion contable de moneda local dolares a Bs inventario fabricacion',

    # any module necessary for this one to work correctly
    'depends': ['product',
    'base', 
    'account',
    'l10n_ve_asientos_$_bs_account',
    'stock_account',
    ],

    # always loaded
    'data': [
        'vista/stock_valuation_layer.xml',
        'vista/stock_quant.xml',
    ],
    'application': True,
}
