# models/ciclo.py

from odoo import models, fields

class CicloFormativo(models.Model):
    _name = 'instituto.ciclo'
    _description = 'Ciclo Formativo'

    name = fields.Char(string='Nombre', required=True)
    codigo = fields.Char(string='Código')
    modulo_ids = fields.One2many(
        'instituto.modulo',
        'ciclo_id',
        string='Módulos'
    )