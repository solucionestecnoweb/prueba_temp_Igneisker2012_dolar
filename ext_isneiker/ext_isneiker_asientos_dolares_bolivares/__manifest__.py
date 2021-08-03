# -*- coding: utf-8 -*-
{
    'name': "Adaptacion contable de moneda local dolares a Bs",

    'summary': """Adaptacion contable de moneda local dolares a Bs""",

    'description': """
       Adaptacion contable de moneda local dolares a Bs
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Adaptacion contable de moneda local dolares a Bs ',

    # any module necessary for this one to work correctly
    'depends': ['product',
    'base', 
    'account',
    'point_of_sale',
    'libro_ventas',
    'libro_compras',
    'libros_filtros',
    'vat_retention',
    'municipality_tax',
    'isrl_retention',
    'l10n_ve_txt_iva',],

    # always loaded
    'data': [
        'vista/account_move_inherit.xml',
        'vista/res_company_inherit.xml',
        'vista/pos_payment_inherit.xml',
        'vista/pos_order_inherit.xml',
        'vista/compro_ret_inherit.xml',
        #'view_add.xml',
        #'vista_pos_paymet_inheret.xml',
        #'vista_pos_order_inherit.xml',
        #'pos_config_inherit.xml',
        #'security/ir.model.access.csv',
        #'reports/report_libro_pos.xml',
        #'wizards/wizard_libro_ventas_pos.xml',
    ],
    'application': True,
}
