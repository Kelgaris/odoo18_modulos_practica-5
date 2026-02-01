# -*- coding: utf-8 -*-
# from odoo import http


# class Ej08-cicloFormativo(http.Controller):
#     @http.route('/ej08-ciclo_formativo/ej08-ciclo_formativo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ej08-ciclo_formativo/ej08-ciclo_formativo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ej08-ciclo_formativo.listing', {
#             'root': '/ej08-ciclo_formativo/ej08-ciclo_formativo',
#             'objects': http.request.env['ej08-ciclo_formativo.ej08-ciclo_formativo'].search([]),
#         })

#     @http.route('/ej08-ciclo_formativo/ej08-ciclo_formativo/objects/<model("ej08-ciclo_formativo.ej08-ciclo_formativo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ej08-ciclo_formativo.object', {
#             'object': obj
#         })

