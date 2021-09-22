# -*- coding: utf-8 -*-
{
    'name': "Traer forma automatica cuentas contables para proveedores y clientes",

    'summary': """Traer forma automatica cuentas contables para proveedores y clientes""",

    'description': """
       Traer forma automatica cuentas contables para proveedores y clientes
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Traer forma automatica cuentas contables para proveedores y clientes',

    # any module necessary for this one to work correctly
    'depends': ['product','base', 'account','sale','purchase','l10n_ve_igtf'],

    # always loaded
    'data': [
        'vista/res_partner_inherit.xml',
        'vista/res_company_inherit.xml',
        #'security/ir.model.access.csv',
    ],
    'application': True,
}
