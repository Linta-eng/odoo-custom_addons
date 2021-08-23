# -*- coding: utf-8 -*-

import time
from datetime import date
from itertools import groupby


from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.tools.misc import format_date



class StockPicking(models.Model):
	_inherit = 'stock.picking'

	route_id = fields.Many2one('delivery.routes', string="Truck Route", group_expand='_read_group_route_ids' )
	batch_id = fields.Many2one(
		'stock.picking.batch', string="Batch Picking",
		check_company=True, states={'done': [('readonly', True)], 'cancel': [('readonlly', True)]},
		copy=False)


	def write(self, vals):
		route_id = vals.get('route_id')
		if route_id:
			batch = self.env['stock.picking.batch'].search([('route_id', '=', route_id)], limit=1)
			if batch:
				vals['batch_id'] = batch.id
			else:
				batch = self.env['stock.picking.batch'].create({'route_id' : route_id})
				vals['batch_id'] = batch.id
		result = super(StockPicking, self).write(vals)
		return result


	@api.model 
	def _read_group_route_ids(self, name, domain, order):
		route_ids = self.env['delivery.routes'].search([])
		return route_ids


class PickingBatch(models.Model):
	_name = 'stock.picking.batch'
	_description = "Batch Picking"
	_rec_name = 'sequence'
	_inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

	sequence = fields.Char(string="Batch Seq", required=True, copy=False, readonly=True,
						   default=lambda self: _('New'))

	partner_id = fields.Many2one('res.partner', string="Driver")

	route_id = fields.Many2one('delivery.routes', string="Route", context={'active': True})

	priority = fields.Selection(PROCUREMENT_PRIORITIES, string='Priority', default='0', index=True,
								help="Products will be reserved first for the transfers with the highest priorities.")

	scheduled_date = fields.Date(string="Scheduled Date", store=True, readonly=False)

	picking_ids = fields.One2many('stock.picking', 'batch_id', string="Picking")

	note = fields.Text(string="Description")

	state = fields.Selection([
		('draft', 'Draft'),
		('in_progress', 'In progress'),
		('done', 'Done'),
		('cancel', 'Cancelled')], default='draft',
		store=True, compute='_compute_state',
		copy=False, tracking=True, required=True, readonly=True)

	@api.model 
	def create(self, vals):
		if not vals.get('note'):
			vals['note'] = 'Batch will be dispatched soon'

		if vals.get('sequence', _('New')) == _('New'):
			vals['sequence'] = self.env['ir.sequence'].next_by_code('stock.picking.batch') or _('New')
		return super(PickingBatch, self).create(vals)

	@api.depends('picking_ids', 'picking_ids.scheduled_date')
	def _compute_scheduled_date(self):
		self.scheduled_date = min(self.picking_ids.filtered('scheduled_date').mapped('scheduled_date'), default=False)

	@api.depends('picking_ids', 'picking_ids.state')
	def _compute_state(self):
		batchs = self.filtered(lambda batch: batch.state not in ['cancel', 'done'])
		for batch in batchs:
			if not batch.picking_ids:
				return
			if all(picking.state == 'cancel' for picking in batch.picking_ids):
				batch.state = 'cancel'
			elif all(picking.state in ['cancel', 'done'] for picking in batch.picking_ids):
				batch.state = 'done'

	@api.onchange('scheduled_date')
	def onchange_scheduled_date(self):
		if self.scheduled_date:
			self.picking_ids.scheduled_date = self.scheduled_date

	# def action_send_mail(self):
	#     template_id = self.env.ref('stock_picking.email_template_batch_mail').id
	#     self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)


	def _find_mail_template(self, force_confirmation_template=False):
		template_id = False

		template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
		if not template_id:
			template_id = self.env['ir.model.data'].xmlid_to_res_id('stock_picking.email_template_batch_mail', raise_if_not_found=False)

		return template_id

	def action_quotation_send(self):
		self.ensure_one()
		template_id = self._find_mail_template()
		lang = self.env.context.get('lang')
		template = self.env['mail.template'].browse(template_id)
		if template.lang:
			lang = template._render_lang(self.ids)[self.id]
		ctx = {
			'default_model': 'stock.picking.batch',
			'default_res_id': self.ids[0],
			'default_use_template': bool(template_id),
			'default_template_id': template_id,
			'default_composition_mode': 'comment',
			'proforma': self.env.context.get('proforma', False),
			'force_email': True,
			'model_description': self.with_context(lang=lang).sequence,
		}
		return {
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(False, 'form')],
			'view_id': False,
			'target': 'new',
			'context': ctx,
		}