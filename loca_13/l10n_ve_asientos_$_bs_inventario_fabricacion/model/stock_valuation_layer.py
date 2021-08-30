# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class ValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    amount_total_signed_aux_bs=fields.Float(compute="_compute_monto_conversion")
    

    def _compute_monto_conversion(self):
        valor=0
        #self.amount_total_signed_aux_bs=valor
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.create_date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.value*det.rate
            selff.amount_total_signed_aux_bs=valor
            
