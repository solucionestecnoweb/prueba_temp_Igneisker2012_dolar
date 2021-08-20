# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosPayment(models.Model):
    _inherit = 'pos.payment'

    amount_total_signed_aux_bs=fields.Float(compute="_compute_monto_conversion")

    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.payment_date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount*det.rate
            selff.amount_total_signed_aux_bs=valor