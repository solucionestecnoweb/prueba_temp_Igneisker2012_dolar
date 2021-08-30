# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_total_signed_bs=fields.Float()
    amount_total_signed_aux_bs=fields.Float(compute="_compute_monto_conversion")
    amount_untaxed_signed_bs=fields.Float(compute="_compute_monto_conversion_untaxed")
    amount_residual_signed_bs=fields.Float(compute="_compute_monto_conversion_residual")

    def _compute_monto_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount_total_signed*det.rate
            selff.amount_total_signed_aux_bs=valor
            selff.amount_total_signed_bs=valor

    def _compute_monto_conversion_untaxed(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount_untaxed_signed*det.rate
            selff.amount_untaxed_signed_bs=valor

    def _compute_monto_conversion_residual(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=selff.amount_residual_signed*det.rate
            selff.amount_residual_signed_bs=valor

#******************* RUTINA PARA LAS RETENCIONES ISLR ***************
    def create_retention(self):
        if self.type in ('in_invoice','out_invoice','in_refund','out_refund','in_receipt','out_receipt'):#darrell
            if self.isrl_ret_id.id:
                pass
            else: 
                if self.partner_id.people_type :
                    self.isrl_ret_id = self.env['isrl.retention'].create({
                        'invoice_id': self.id,
                        'partner_id': self.partner_id.id,
                        'move_id':self.id,
                        'invoice_number':self.invoice_number,
                    })
                    for item in self.invoice_line_ids:
                        if item.concept_isrl_id:
                            for rate in item.concept_isrl_id.rate_ids:
                                #raise UserError(_('item.price_subtotal=%s ')%rate.min)
                                if self.partner_id.people_type == rate.people_type and  self.conversion_a_bs_islr(self.conv_div_nac(item.price_subtotal)) > rate.min  :
                                    base = self.conversion_a_bs_islr(item.price_subtotal) * (rate.subtotal / 100)
                                    subtotal =  base * (rate.retention_percentage / 100)
                                    #raise UserError(_('base = %s')%base)
                                    self.vat_isrl_line_id = self.env['isrl.retention.invoice.line'].create({
                                        'name': item.concept_isrl_id.id,
                                        'code':rate.code,
                                        'retention_id': self.isrl_ret_id.id,
                                        'cantidad': rate.retention_percentage,
                                        'base': self.conv_div_nac(base),
                                        'retention': self.conv_div_nac(subtotal),
                                        'sustraendo': rate.subtract,
                                        'total': self.conv_div_nac(subtotal -rate.subtract), # AQUI
                                    })
                else :
                    raise UserError("the Partner does not have identified the type of person.")

        if self.type =='in_invoice' or self.type =='in_refund' or self.type =='in_receipt':#darrell
        #if self.type=='in_invoice':
            self.isrl_ret_id.action_post()

    def conversion_a_bs_islr(self,monto):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=monto*det.rate
            return valor

    """def conv_div_nac(self,valor):
        self.currency_id.id
        fecha_contable_doc=self.date
        monto_factura=self.amount_total
        valor_aux=0
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        
        tasa= self.env['res.currency.rate'].search([('currency_id','=',self.env.company.currency_secundaria_id.id),('name','<=',self.date)],order="name asc")
        for det_tasa in tasa:
            valor_aux=det_tasa.rate
        rate=round(1*valor_aux,2)
        resultado=valor*rate
        
        return resultado"""

class  AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    balance_aux_bs=fields.Float()
    credit_aux=fields.Float(compute='_compute_monto_credit_conversion')
    debit_aux=fields.Float(compute='_compute_monto_debit_conversion')

    def _compute_monto_credit_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.move_id.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=(selff.credit*det.rate)
            selff.credit_aux=abs(valor)

    def _compute_monto_debit_conversion(self):
        valor=0
        self.env.company.currency_secundaria_id.id
        for selff in self:
            lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', self.env.company.currency_secundaria_id.id),('hora','<=',selff.move_id.date)],order='id ASC')
            if lista_tasa:
                for det in lista_tasa:
                    valor=(selff.debit*det.rate)
            selff.debit_aux=abs(valor)
        