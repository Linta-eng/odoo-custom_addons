# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class StorageWizard(models.TransientModel):
    _name = "storage.wizard"

    partner_id = fields.Many2one('res.partner')
    storage_contract = fields.Many2one('storage.inherit.productss', string="storage contract")

    order_quantity = fields.Integer(related="storage_contract.order_qty", readonly=False, store=True)

    def add_contract(self):
        sto_line = self.storage_contract
        print(sto_line)
        kk = self.env['sale.order.line'].create({'product_id': sto_line.product_id.id,
                                                 'product_uom_qty': self.order_quantity,

                                                'remaining_qty' : sto_line.remaining_qty,
                                                 'order_id': self._context.get('active_id')})


    @api.onchange('order_quantity')
    def onchange_order_qty(self):
        r = {}
        if self.order_quantity < self.storage_contract.min_qty:
            message = {
                'title': _('Less'),
                'message': _('its less tha min quantity')
            }
            self.order_quantity = self.storage_contract.order_qty
            r.update({'warning': message})

        elif self.order_quantity > self.storage_contract.order_qty:
            message = {
                'title': _('More'),
                'message': _('greater tha order quantity')
            }
            self.order_quantity = self.storage_contract.order_qty
            r.update({'warning': message})

        return r

# @api.constrains('order_quantity')
# def check_qty(self, order_quantity=None):
# 	if self.order_quantity and self.order_quantity < order_quantity:
# 		raise ValidationError(("highh"))

# @api.depends('storage_contract')
# def test_1(self):
# 	aa = self.env['storagee.contract'].search([('sequence_no','=',self.storage_contract)])
#
# 	print(aa)
# 	self.order_quantity = aa

# @api.depends('storage_contract')

# @api.depends('storage_contract')
# def test_2(self):
# 	# aa = self.env['storage.inherit.products'].search([()].mapped('')
# 	print("hello")
