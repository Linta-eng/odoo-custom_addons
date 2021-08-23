# -*- coding: utf-8

from odoo import fields, models, api


class Tryuol(models.Model):
    _inherit = 'sale.order'

    status_button = fields.Boolean(string="status button", compute="test_b")
    storage_lines_id = fields.One2many('storage.inherit.productss', 'sale_order_id')

    @api.depends('partner_id')
    def test_b(self):
        for rec in self:
            a = self.env['storage.inherit.productss'].search_count([('user_id.customer', '=', rec.partner_id.id)])
            rec.status_button = bool(a)


class Sale_order_line_inherit(models.Model):
    _inherit = 'sale.order.line'

    storage_liness_id = fields.One2many('storage.inherit.productss', 'sale_order_ids')
    remaining_qty = fields.Integer()
