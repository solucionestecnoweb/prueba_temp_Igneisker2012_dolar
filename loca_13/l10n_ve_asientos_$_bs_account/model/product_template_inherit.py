# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class Productos(models.Model):
    _inherit = 'product.template'

    #sublineas=fields.Char(string="Sub Lineas")
    #modelo_id = fields.Many2one('stock.modelo')
    #tipo_id = fields.Many2one('stock.tipo')
    #color=fields.Char(string="Color")
    #formato=fields.Char(string="Formato")
    #uso=fields.Char(string="Uso")
    #material=fields.Char(string="Material")
    #calidad=fields.Char(string="Calidad")
    #uni_neg_id = fields.Many2one('stock.unidad.negocio')
    marca_comercial=fields.Char(string="Marca Comercial")

"""class ModeloStock(models.Model):
    _name = 'stock.modelo'

    name=fields.Char()

class TipoStock(models.Model):
    _name = 'stock.tipo'

    name=fields.Char()

class UnidadNegocioStock(models.Model):
    _name = 'stock.unidad.negocio'

    name=fields.Char()"""
        