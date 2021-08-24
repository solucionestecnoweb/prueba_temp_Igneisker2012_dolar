# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosConfig(models.Model):
    _inherit = 'pos.order'

    nb_caja_comp=fields.Char(string="Registro de Máquina Fiscal",compute='_compute_nb_caja')
    nb_caja=fields.Char(string="Registro de nombre de la caja")
    status_impresora = fields.Char(default="no")
    tipo = fields.Char(default="venta")


    def _compute_nb_caja(self):
        self.nb_caja_comp=self.session_id.config_id.nb_identificador_caja
        self.nb_caja=self.nb_caja_comp

    """def refund(self):
        super().refund()
        self.nro_fact_seniat=0"""

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    status_impresora=fields.Char(related='order_id.status_impresora')
    tipo = fields.Char(related='order_id.tipo')
