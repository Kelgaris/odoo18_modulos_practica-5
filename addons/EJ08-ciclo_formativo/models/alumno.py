# models/alumno.py

from odoo import models, fields

class Alumno(models.Model):
    _name = 'instituto.alumno'
    _description = 'Alumno'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string='Email')
    modulo_ids = fields.Many2many(
        'instituto.modulo',
        string='Módulos'
    )