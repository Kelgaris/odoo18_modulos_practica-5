# models/profesor.py

from odoo import models, fields

class Profesor(models.Model):
    _name = 'instituto.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre', required=True)
    especialidad = fields.Char(string='Especialidad')
    modulo_ids = fields.One2many(
        'instituto.modulo',
        'profesor_id',
        string='Módulos'
    )