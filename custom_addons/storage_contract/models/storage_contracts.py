# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class Storage_contract_class(models.Model):
    _name = 'storagee.contract'
    _rec_name = 'sequence_no'

    customer = fields.Many2one('res.partner', string="customer")
    payment_methodd = fields.Many2one('account.payment.method')
    sequence_no = fields.Char(string='reference no', required=True, copy=False, readonly=True,
                              default=lambda self: _('New'))
    confirm_date = fields.Datetime(string="Confirm date",default=datetime.now())
    user_lines = fields.One2many('storage.inherit.productss', 'user_id')

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('storagee_sequence') or _('New')
        res = super(Storage_contract_class, self).create(vals)
        return res

class StorageInheritproduct(models.Model):
    _name = "storage.inherit.productss"
    _description = "storage inherit system"
    _rec_name = 'user_id'

    product_id = fields.Many2one('product.template', string="product")
    typ = fields.Selection(related='product_id.type',string="type")
    order_qty = fields.Integer(string="order qty")
    min_qty = fields.Integer(string="minimum qty")
    remaining_qty = fields.Integer(string='remaining quantity' , compute="rem_qty")
    user_id = fields.Many2one('storagee.contract')
    sale_order_id = fields.Many2one('sale.order')
    sale_order_ids = fields.Many2one('sale.order.line')

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s (%s)' % (field.user_id.sequence_no, field.product_id.name)))
        return res

    def rem_qty(self):
        for a in self:
            a.remaining_qty = a.order_qty - a.min_qty