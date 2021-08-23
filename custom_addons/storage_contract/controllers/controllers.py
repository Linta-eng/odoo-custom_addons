# -*- coding: utf-8 -*-
# from odoo import http


# class ExtraAddons/storageContract(http.Controller):
#     @http.route('/extra_addons/storage_contract/extra_addons/storage_contract/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extra_addons/storage_contract/extra_addons/storage_contract/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extra_addons/storage_contract.listing', {
#             'root': '/extra_addons/storage_contract/extra_addons/storage_contract',
#             'objects': http.request.env['extra_addons/storage_contract.extra_addons/storage_contract'].search([]),
#         })

#     @http.route('/extra_addons/storage_contract/extra_addons/storage_contract/objects/<model("extra_addons/storage_contract.extra_addons/storage_contract"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extra_addons/storage_contract.object', {
#             'object': obj
#         })
