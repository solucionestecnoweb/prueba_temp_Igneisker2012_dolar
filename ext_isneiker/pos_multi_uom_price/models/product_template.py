# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    multi_uom_price_id = fields.Many2many('product.multi.uom.price', 'product_id')
    #multi_uom_price_id = fields.Many2many('product.multi.uom.price')
