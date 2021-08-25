# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
    
class libro_ventas(models.TransientModel):
    _inherit = "pos.wizard.libro.ventas"


    def conv_div_bs(self,valor,det):
        tasa=det.session_id.tasa_dia
        resultado=valor*tasa
        return resultado