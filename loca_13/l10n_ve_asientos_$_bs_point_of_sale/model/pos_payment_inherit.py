# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosPayment(models.Model):
    _inherit = 'pos.payment'

    amount_total_signed_aux_bs=fields.Float(digits=(12, 2),compute="_compute_monto_conversion")
    payment_date_aux = fields.Datetime(string='Date',compute='_compute_fecha')

    def _compute_fecha(self):
        for selff in self:
            selff.payment_date_aux=selff.pos_order_id.date_order
            selff.payment_date=selff.pos_order_id.date_order

    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rates'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.payment_date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount*det.rate
            selff.amount_total_signed_aux_bs=valor