from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import openerp.addons.decimal_precision as dp
import logging

import io
from io import BytesIO

import xlsxwriter
import shutil
import base64
import csv
import xlwt

_logger = logging.getLogger(__name__)

class LibroVentasPosModelo(models.Model):
    _name = "pos.wizard.pdf.ventas" 

    name = fields.Date(string='Fecha')
    document = fields.Char(string='Rif')
    partner  = fields.Many2one(comodel_name='res.partner', string='Partner')
    tipo_doc = fields.Char(string='tipo_doc')
    sale_total = fields.Float(string='invoice_ctrl_number')
    base_imponible = fields.Float(string='invoice_ctrl_number')
    iva = fields.Float(string='iva')
    iva_retenido = fields.Float(string='iva retenido')
    alicuota = fields.Char(string='alicuota')
    alicuota_type = fields.Char(string='alicuota type')
    state_retantion = fields.Char(string='state')
    state = fields.Char(string='state')
    currency_id = fields.Many2one('res.currency', 'Currency')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    ref = fields.Char(string='ref')

    total_exento = fields.Float(string='Total Excento')
    alicuota_reducida = fields.Float(string='Alicuota Reducida')
    alicuota_general = fields.Float(string='Alicuota General')
    alicuota_adicional = fields.Float(string='Alicuota General + Reducida')

    base_general = fields.Float(string='Total Base General')
    base_reducida = fields.Float(string='Total Base Reducida')
    base_adicional = fields.Float(string='Total Base General + Reducida')

    retenido_general = fields.Float(string='retenido General')
    retenido_reducida = fields.Float(string='retenido Reducida')
    retenido_adicional = fields.Float(string='retenido General + Reducida')
    fecha_fact= fields.Datetime(string="Fecha Cierre")
    reg_maquina = fields.Char(string="Registro de Máquina Fiscal")
    nro_rep_z = fields.Char(string="Número Reporte Z")
    nro_doc = fields.Char(string="Nro de documentos")
    nro_doc_nc = fields.Char(string="Nro de nota credito")
    base_imponible_nc = fields.Float(string="Base Imponible NC")
    alicuota_nc =  fields.Float(string='Alicuota NC')
    total_nc= fields.Float(string="Total NC",default=0)
    fact_afectada = fields.Char()


    def formato_fecha2(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado
    
    def float_format(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result="0,00"
        return result


    # FUNCION QUE HACE LAS CONVERSIONES DE LAS DIVISAS
    """def conv_div(self,valor):
        self.currency_id.id
        fecha_contable_doc=self.invoice_id.date
        monto_factura=self.invoice_id.amount_total
        valor_aux=0.000000000000001
        tasa= self.env['res.currency.rate'].search([('currency_id','=',self.currency_id.id),('name','<=',fecha_contable_doc)],order="name asc")
        #raise UserError(_('tasa: %s')%tasa)
        for det_tasa in tasa:
            if fecha_contable_doc>=det_tasa.name:
                valor_aux=det_tasa.rate
        rate=round(1/valor_aux,2)  # LANTA
        #rate=round(valor_aux,2)  # ODOO SH
        resultado=monto_factura*rate
        return resultado"""

    def conv_div(self,valor):
        self.invoice_id.currency_id.id
        fecha_contable_doc=self.invoice_id.date
        monto_factura=self.invoice_id.amount_total
        valor_aux=0
        prueba=valor
        #raise UserError(_('moneda compañia: %s')%self.company_id.currency_id.id)
        if self.invoice_id.company_id.currency_id.id!=self.currency_id.id:
            tasa= self.env['account.move'].search([('id','=',self.invoice_id.id)],order="id asc")
            for det_tasa in tasa:
                monto_nativo=det_tasa.amount_untaxed_signed
                monto_extran=det_tasa.amount_untaxed
                valor_aux=abs(monto_nativo/monto_extran)
            rate=round(valor_aux,3)  # LANTA
            #rate=round(valor_aux,2)  # ODOO SH
            resultado=valor*rate
        else:
            resultado=valor
        return resultado

    def float_format_div(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result="0,00"
        return result

    def doc_cedula(self,aux):
        #nro_doc=self.partner_id.vat
        nro_doc="00000000"
        tipo_doc="V"
        busca_partner = self.env['res.partner'].search([('id','=',aux)])
        for det in busca_partner:
            tipo_doc=det.doc_type
            if det.vat:
                nro_doc=str(det.vat)
            else:
                nro_doc="00000000"
        nro_doc=nro_doc.replace('V','')
        nro_doc=nro_doc.replace('v','')
        nro_doc=nro_doc.replace('E','')
        nro_doc=nro_doc.replace('e','')
        nro_doc=nro_doc.replace('G','')
        nro_doc=nro_doc.replace('g','')
        nro_doc=nro_doc.replace('J','')
        nro_doc=nro_doc.replace('j','')
        nro_doc=nro_doc.replace('P','')
        nro_doc=nro_doc.replace('p','')
        nro_doc=nro_doc.replace('-','')
        
        if tipo_doc=="v":
            tipo_doc="V"
        if tipo_doc=="e":
            tipo_doc="E"
        if tipo_doc=="g":
            tipo_doc="G"
        if tipo_doc=="j":
            tipo_doc="J"
        if tipo_doc=="p":
            tipo_doc="P"
        if tipo_doc=="c":
            tipo_doc="C"
        resultado=str(tipo_doc)+str(nro_doc)
        return resultado


class libro_ventas(models.TransientModel):
    _name = "pos.wizard.libro.ventas" ## = nombre de la carpeta.nombre del archivo deparado con puntos

    facturas_ids = fields.Many2many('pos.order', string='Ordebes de Ventas', store=True) ##Relacion con el modelo de la vista de la creacion de facturas
   
    date_from = fields.Datetime(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d 04:00:00'))
    date_to = fields.Datetime('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d 03:59:59'))
    #date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    #date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))

    # fields for download xls
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],default='choose') ##Genera los botones de exportar xls y pdf como tambien el de cancelar
    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=32)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.company)

    line  = fields.Many2many(comodel_name='pos.wizard.pdf.ventas', string='Lineas')


    def print_libro_pos(self):
        #pass
        self.get_invoice()
        #return self.env.ref('libro_ventas.libro_factura_clientes').report_action(self)
        return {'type': 'ir.actions.report','report_name': 'ext_extension_tpdv.reporte_ventas_pos','report_type':"qweb-pdf"}

    def get_invoice(self):
        t=self.env['pos.wizard.pdf.ventas']
        d=t.search([])
        d.unlink()
        cursor_resumen = self.env['pos.order.line.resumen'].search([
            ('fecha_fact','>=',self.date_from),
            ('fecha_fact','<=',self.date_to)
            ])
        for det in cursor_resumen:
            values={
            'name':det.fecha_fact,
            #'tipo_doc': det.tipo_doc,
            'sale_total': det.total_con_iva,
            'base_imponible': det.total_base,
            'iva' : det.total_valor_iva,
            'total_exento':det.total_exento,
            'alicuota_reducida':det.alicuota_reducida,
            'alicuota_general':det.alicuota_general,
            'alicuota_adicional':det.alicuota_adicional,
            'base_adicional':det.base_adicional,
            'base_reducida':det.base_reducida,
            'base_general':det.base_general,
            'retenido_reducida':det.retenido_reducida,
            'retenido_adicional':det.retenido_adicional,
            'retenido_general':det.retenido_general,
            'fecha_fact':det.fecha_fact,
            'reg_maquina':det.reg_maquina,
            'nro_rep_z':det.nro_rep_z,
            'nro_doc':det.nro_doc,
            'nro_doc_nc':det.nro_doc_nc,
            'base_imponible_nc':det.base_imponible_nc,
            'alicuota_nc':det.alicuota_nc,
            'total_nc':det.total_nc,
            'fact_afectada':det.fact_afectada,
            }
            pdf_id = t.create(values)
        self.line = self.env['pos.wizard.pdf.ventas'].search([])

    def get_company_address(self):
        location = ''
        streets = ''
        if self.company_id:
            streets = self._get_company_street()
            location = self._get_company_state_city()
        _logger.info("\n\n\n street %s location %s\n\n\n", streets, location)
        return  (streets + " " + location)

    def _get_company_street(self):
        street2 = ''
        av = ''
        if self.company_id.street:
            av = str(self.company_id.street or '')
        if self.company_id.street2:
            street2 = str(self.company_id.street2 or '')
        result = av + " " + street2
        return result


    def _get_company_state_city(self):
        state = ''
        city = ''
        if self.company_id.state_id:
            state = "Edo." + " " + str(self.company_id.state_id.name or '')
            _logger.info("\n\n\n state %s \n\n\n", state)
        if self.company_id.city:
            city = str(self.company_id.city or '')
            _logger.info("\n\n\n city %s\n\n\n", city)
        result = city + " " + state
        _logger.info("\n\n\n result %s \n\n\n", result)
        return  result


    def doc_cedula2(self,aux):
        #nro_doc=self.partner_id.vat
        busca_partner = self.env['res.partner'].search([('id','=',aux)])
        for det in busca_partner:
            tipo_doc=det.doc_type
            nro_doc=str(det.vat)
        nro_doc=nro_doc.replace('V','')
        nro_doc=nro_doc.replace('v','')
        nro_doc=nro_doc.replace('E','')
        nro_doc=nro_doc.replace('e','')
        nro_doc=nro_doc.replace('G','')
        nro_doc=nro_doc.replace('g','')
        nro_doc=nro_doc.replace('J','')
        nro_doc=nro_doc.replace('j','')
        nro_doc=nro_doc.replace('P','')
        nro_doc=nro_doc.replace('p','')
        nro_doc=nro_doc.replace('c','')
        nro_doc=nro_doc.replace('C','')
        nro_doc=nro_doc.replace('-','')
        
        if tipo_doc=="v":
            tipo_doc="V"
        if tipo_doc=="e":
            tipo_doc="E"
        if tipo_doc=="g":
            tipo_doc="G"
        if tipo_doc=="j":
            tipo_doc="J"
        if tipo_doc=="p":
            tipo_doc="P"
        if tipo_doc=="c":
            tipo_doc="C"
        resultado=str(tipo_doc)+str(nro_doc)
        return resultado

    def cont_row(self):
        row = 0
        for record in self.facturas_ids:
            row +=1
        return row

    def float_format2(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result="0,00"
        return result

    def float_format_div2(self,valor):
        #valor=self.base_tax
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result="0,00"
        return result