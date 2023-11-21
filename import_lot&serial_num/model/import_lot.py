# -*- coding: utf-8 -*-
import binascii
import xlrd
from odoo import models, fields, _
from odoo.exceptions import UserError


class ImportLot(models.TransientModel):
   _name = 'import.lot'

   file = fields.Binary(string='File')

   def import_lot_serial(self):
      try:
         data = binascii.a2b_base64(self.file)
         book = xlrd.open_workbook(file_contents=data)
      except FileNotFoundError:
         raise UserError(
            'No such file or directory found. \n%s.' % self.file)
      except xlrd.biffh.XLRDError:
         raise UserError('Only excel files are supported.')
      for sheet in book.sheets():
         try:
            if sheet.name == 'Sheet1':
               for row in range(sheet.nrows):
                  if row >= 1:
                     row_values = sheet.row_values(row)
                     vals = self._create_lot_serial(row_values)
                     if vals == False:
                        continue
                     if vals['name'] and vals['product_id']:
                        self.env['stock.lot'].create(vals)
               return {
                  'effect': {
                     'fadeout': 'slow',
                     'message': 'Lot & Serial Importing is successfull',
                     'type': 'rainbow_man',
                  }
               }
         except IndexError:
            pass

   def _create_lot_serial(self, record):
      values = self.env['stock.lot'].search([('name', '=', record[0])],
                                                      limit=1)
      if values or record[2] == '':
         return False
      product_id = self.env['product.template'].search([('name', 'ilike', record[2])],
                                            limit=1)
      if not product_id:
         product_id = self.env['product.product'].create({
            'name': record[2]
         })
      line_ids = {
         'name': record[0],
         'product_id': product_id.product_variant_id.id
      }
      return line_ids

