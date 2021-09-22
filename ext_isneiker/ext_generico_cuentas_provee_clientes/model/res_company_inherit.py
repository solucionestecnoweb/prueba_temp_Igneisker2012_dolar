# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class ResCompany(models.Model):
    _inherit = 'res.company'

    account_payable_aux_id = fields.Many2one('account.account')
    account_receivable_aux_id = fields.Many2one('account.account')

    account_anti_payable_aux_id = fields.Many2one('account.account')
    account_anti_receivable_aux_id = fields.Many2one('account.account')
   
    #uni_neg_id = fields.Many2one('stock.unidad.negocio')