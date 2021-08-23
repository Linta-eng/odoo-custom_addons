#-*- coding: utf-8 -*-
import datetime
from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
	
class Customerprofile(models.Model):
	_name = "customer.profile"
	_description = "Customer System"
	_rec_name = 'fullname'


	firstname = fields.Char(required=True)
	lastname = fields.Char(required=True)
	fullname = fields.Char(compute="full_pc", store=True )
	gender = fields.Selection([('male','Male'),('female','Female'),('transgender','Transgender')],default='male')
	state = fields.Char(string="State")
	street = fields.Char(string="Street")
	city = fields.Char(String="City")
	country_id = fields.Many2one('res.country', string='Country')
	location = fields.Char(string="Location")
	states = fields.Selection([('draft','Draft'),('not_ready','Not_ready'),('ready','ready')],default='draft')
	document = fields.Binary()
	filename = fields.Char()
	image = fields.Image(store=True)
	date_of_birth = fields.Date(string="Date of birth")
	ages = fields.Char(compute="date_calculator")
	phone = fields.Integer(string="Phone number")
	reference= fields.Char(string='Customer Registration ID', required=True, copy=False, readonly=True,default=lambda self: _('New'))

	@api.depends('date_of_birth')
	def date_calculator(self):
		today_date = datetime.date.today()
		for cust in self:
			if cust.date_of_birth:
				date_of_birth = fields.Datetime.to_datetime(cust.date_of_birth).date()
				total_age = str(int((today_date - date_of_birth).days/365))
				cust.ages = total_age
			else:
				cust.ages ="not provided"


	@api.depends('firstname','lastname')
	def full_pc(self):
		for a in self:
			if a.firstname and a.lastname:
				a.fullname = a.firstname +" "+ a.lastname
	

	@api.constrains('phone')
	def check_name(self):
		for a in self:
			if a.phone == 0:
				raise ValidationError(("phone number must be give"))


	@api.model
	def create(self, vals):
		if vals.get('reference', _('New')) == _('New'):
			vals['reference'] = self.env['ir.sequence'].next_by_code('registration_customer') or _('New')
		res = super(Customerprofile,self).create(vals)
		return res


	def donee(self):
		self.states = 'ready'


	def unlink(self):
		print("deleted record")
		for a in self:
			if a.states=='ready':
				raise ValidationError("you cannot delete the name %s because it is in ready state" %a.fullname)
			return super(Customerprofile,a).unlink()


	def copy(self, default=None):
		if default is None:
			default={}
		if not default.get('firstname'):
			default['firstname'] = _("%s (duplicate)",self.firstname)
		return super(Customerprofile,self).copy(default)