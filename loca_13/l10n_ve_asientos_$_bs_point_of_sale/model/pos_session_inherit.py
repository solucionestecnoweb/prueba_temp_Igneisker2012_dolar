# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
    

class PosSession(models.Model):
    _inherit = 'pos.session'

    tasa_dia = fields.Float(compute="_compute_tasa")

    def _compute_tasa(self):
        tasa=0
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.start_at)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    tasa=det.rate
            selff.tasa_dia=tasa

    def conv_div_bs(self,valor):
        resultado=0
        resultado=valor
        return resultado