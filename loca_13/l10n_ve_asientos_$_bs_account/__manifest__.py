# -*- coding: utf-8 -*-
{
    'name': "Adaptacion contable de moneda local dolares a Bs modulo contabilidad",

    'summary': """Adaptacion contable de moneda local dolares a Bs modulo contabilidad""",

    'description': """
       Adaptacion contable de moneda local dolares a Bs modulo contabilidad
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Adaptacion contable de moneda local dolares a Bs modulo contabilidad',

    # any module necessary for this one to work correctly
    'depends': ['product',
    'base', 
    'account',
    'libro_ventas',
    'libro_compras',
    'libros_filtros',
    'vat_retention',
    'municipality_tax',
    'isrl_retention',
    'l10n_ve_txt_iva',],

    # always loaded
    'data': [
        'vista/res_company_inherit.xml',
        'vista/account_move_inherit.xml',  
        'vista/compro_ret_inherit.xml',
        #'vista/pos_order_inherit.xml',
        #'vista/pos_payment_inherit.xml',
    ],
    'application': True,
}
