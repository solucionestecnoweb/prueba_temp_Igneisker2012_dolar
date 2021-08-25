# -*- coding: utf-8 -*-
{
    'name': "Adaptacion contable de moneda local dolares a Bs modulo punto de venta",

    'summary': """Adaptacion contable de moneda local dolares a Bs punto de venta""",

    'description': """
       Adaptacion contable de moneda local dolares a Bs modulo punto de venta
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Adaptacion contable de moneda local dolares a Bs punto de venta',

    # any module necessary for this one to work correctly
    'depends': ['product',
    'base', 
    'account',
    'libro_ventas',
    'libro_compras',
    'l10n_ve_asientos_$_bs_account',
    'ext_extension_tpdv',
    ],

    # always loaded
    'data': [
        'vista/pos_order_inherit.xml',
        'vista/pos_payment_inherit.xml',
    ],
    'application': True,
}
