# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import timedelta, date, datetime
from odoo.exceptions import UserError

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"


    @api.onchange('rate_real', 'hora')
    def fecha_y_hora(self):
    	super(CurrencyRate, self).fecha_y_hora()
    	self.convercion_precio_product_multi_uom()

    def convercion_precio_product_multi_uom(self):
        lista_product = self.env['product.multi.uom.price'].search([('moneda_divisa_venta', '=', self.currency_id.id)],order='id asc')
        if lista_product:
            for cor in lista_product:
                precio=cor.list_price2*self.rate_real
                cor.price=precio