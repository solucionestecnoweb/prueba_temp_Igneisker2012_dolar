# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class PosOrder(models.Model):
    _inherit = 'pos.order'

    amount_total_signed_aux_bs=fields.Float(digits=(12, 2),compute="_compute_monto_conversion")
    

    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount_total*det.rate
            selff.amount_total_signed_aux_bs=valor

    """def _compute_monto_conversion(self):
        valor=0
        cont=1
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_line = selff.env['pos.order.line'].search([('order_id', '=', selff.id)],order='id ASC')
            if lista_line:
                for det in lista_line:
                    valor=valor+det.sub_total_aux
                    cont=cont+1
            selff.amount_total_signed_aux_bs=valor"""

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    price_unit_aux=fields.Float(digits=(12, 2),compute="_compute_valor1")
    sub_neto_aux=fields.Float(digits=(12, 2),compute="_compute_valor2")
    sub_total_aux=fields.Float(digits=(12, 2),compute="_compute_valor3")

    def _compute_valor1(self):
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.order_id.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.price_unit*det.rate
            selff.price_unit_aux=valor

    def _compute_valor2(self):
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.order_id.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.price_subtotal*det.rate
            selff.sub_neto_aux=valor

    def _compute_valor3(self):
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.order_id.date_order)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.price_subtotal_incl*det.rate
            selff.sub_total_aux=valor
