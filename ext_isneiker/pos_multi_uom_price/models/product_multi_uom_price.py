# -*- coding: utf-8 -*-

from odoo.addons import decimal_precision as dp
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class multi_uom(models.Model):
    _name = 'product.multi.uom.price'
    _description = 'Product multiple uom price'     

    product_id = fields.Many2one('product.template', _('Product'), ondelete='set null', readonly=False)
    category_id = fields.Many2one('uom.category', _('Category'), ondelete='set null', readonly=False)
    #product_id = fields.Many2one('product.template',_('Product'), ondelete='set null')
    #category_id = fields.Many2one('uom.category', _('Category'), ondelete='set null')
    uom_id = fields.Many2one('uom.uom', string=_("Unit of Measure"), required=True)
    price = fields.Float(_('Price'), required=True, digits=dp.get_precision('Product Price'))

    list_price2 = fields.Float(_('list_price2'))
    list_price_comp = fields.Float(_('list_price_comp'), compute='_compute_monto')
    moneda_divisa_venta = fields.Many2one("res.currency",digits=(12, 2))#,required=True
    habilita_precio_div = fields.Boolean(related='product_id.habilita_precio_div')
    
    @api.onchange('list_price2','moneda_divisa_venta')
    def _compute_monto(self):
        for selff in self:
            selff.list_price_comp=0
            if selff.product_id.habilita_precio_div==True:
                if selff.moneda_divisa_venta:
                    lista_tasa = selff.env['res.currency.rate'].search([('currency_id', '=', selff.moneda_divisa_venta.id)],order='id ASC')
                    if lista_tasa:
                        for det in lista_tasa:
                            precio_actualizado=det.rate_real*selff.list_price2
                            selff.list_price_comp=precio_actualizado
                            selff.price=precio_actualizado
                    else:
                        raise ValidationError(_('Debe colocar Una tasa de conversion para esta moneda. Vaya a contabilidad-->configuracion-->Monedas y coloque la tasa'))
                if selff.list_price2>0 and not self.moneda_divisa_venta:
                     raise ValidationError(_('Debe seleccionar una moneda de divisa'))
            if selff.product_id.habilita_precio_div!=True:
                selff.list_price_comp=0

    # EHDLF Categoría del producto
    @api.onchange('product_id')
    def categorydefault(self):
        if not (self.product_id):
            self.category_id = False
        else:
            self.category_id = self.product_id.uom_id.category_id.id
    
    # EHDLF UOM's de la categoria
    @api.onchange('product_id')
    def categorysuom(self):
        if not self.product_id:
            return
        # EHDLF misma categoría y diferente base
        domain = {'uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id),'!',('id', '=', self.product_id.uom_id.id)]}
        return {'domain': domain}
    
    # EHDLF Convinación Producto-UOM debe ser única
    _sql_constraints = [
        ('product_multi_uom_price_uniq',
         'UNIQUE (product_id,uom_id)',
         _('Product-UOM must be unique and there are duplicates!'))]
    
