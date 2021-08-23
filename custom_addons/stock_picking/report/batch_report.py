# -*- coding: utf-8 -*-

from odoo import api, models


class AdmissionReport(models.AbstractModel):
	_name = 'report.batch.report'
	_description = 'Batch Report'

	@api.model
	def _get_report_values(self, docids, data=None):
		report = self.env['ir.actions.report']._get_report_from_name('stock.batch.picking')
        # get the records selected for this rendering of the report
        obj = self.env[stock.batch.picking].browse(docids)
        # return a custom rendering context
        return {
            'lines': docids.get_lines()
        }