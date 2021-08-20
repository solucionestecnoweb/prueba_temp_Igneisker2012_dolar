# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosOrder(models.Model):
    _inherit = 'pos.order'

    amount_total_signed_aux_bs=fields.Float(compute="_compute_monto_conversion")
    tasa_dia = fields.Float(compute="_compute_tasa")

    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount_total*det.rate
            selff.amount_total_signed_aux_bs=valor

    def _compute_tasa(self):
        tasa=0
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    tasa=det.rate
            selff.tasa_dia=tasa