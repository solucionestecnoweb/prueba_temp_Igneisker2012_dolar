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


class libro_compras(models.TransientModel):
    _inherit = "account.wizard.libro.compras"


    def print_facturas(self):
        #raise UserError(_('coño'))
        t=self.env['account.wizard.pdf.compras']
        d=t.search([])
        d.unlink()
        cursor_compania = self.env['res.company'].search([('parent_id','=',self.env.company.id)])
        if cursor_compania:
            for comp in cursor_compania:
                self.get_invoice(comp.id)
        self.get_invoice(self.env.company.id)
        return {'type': 'ir.actions.report','report_name': 'libro_compras.libro_factura_proveedores','report_type':"qweb-pdf"}


    def get_invoice(self,comp_id):
        t=self.env['account.wizard.pdf.compras']
        #raise UserError(_('parentesco compañia: %s')%comp_id)
        cursor_resumen = self.env['account.move.line.resumen'].search([
            ('fecha_fact','>=',self.date_from),
            ('fecha_fact','<=',self.date_to),
            ('state','in',('posted','cancel' )),
            ('type','in',('in_invoice','in_refund','in_receipt')),
            ('company_id','=',comp_id)
            ])
        for det in cursor_resumen:
            if det.invoice_id.ocultar_libros!=True:
                values={
                'name':det.fecha_fact,
                'document':det.invoice_id.name,
                'partner':det.invoice_id.partner_id.id,
                'invoice_number': det.invoice_id.invoice_number,#darrell
                'tipo_doc': det.tipo_doc,
                'invoice_ctrl_number': det.invoice_id.invoice_ctrl_number,
                'sale_total': self.conv_div_nac(det.total_con_iva,det),
                'base_imponible': self.conv_div_nac(det.total_base,det),
                'iva' : self.conv_div_nac(det.total_valor_iva,det),
                'iva_retenido': self.conv_div_nac(det.total_ret_iva,det),
                'retenido': det.vat_ret_id.name,
                'retenido_date':det.vat_ret_id.voucher_delivery_date,
                'state_retantion': det.vat_ret_id.state,
                'state': det.invoice_id.state,
                'currency_id':det.invoice_id.currency_id.id,
                'ref':det.invoice_id.ref,
                'total_exento':self.conv_div_nac(det.total_exento,det),
                'alicuota_reducida':self.conv_div_nac(det.alicuota_reducida,det),
                'alicuota_general':self.conv_div_nac(det.alicuota_general,det),
                'alicuota_adicional':self.conv_div_nac(det.alicuota_adicional,det),
                'base_adicional':self.conv_div_nac(det.base_adicional,det),
                'base_reducida':self.conv_div_nac(det.base_reducida,det),
                'base_general':self.conv_div_nac(det.base_general,det),
                'retenido_reducida':self.conv_div_nac(det.retenido_reducida,det),
                'retenido_adicional':self.conv_div_nac(det.retenido_adicional,det),
                'retenido_general':self.conv_div_nac(det.retenido_general,det),
                'vat_ret_id':det.vat_ret_id.id,
                'invoice_id':det.invoice_id.id,
                'tax_id':det.tax_id.id,
                'company_id':det.company_id.id,#loca14
                }
                pdf_id = t.create(values)
        #   temp = self.env['account.wizard.pdf.ventas'].search([])
        self.line = self.env['account.wizard.pdf.compras'].search([])