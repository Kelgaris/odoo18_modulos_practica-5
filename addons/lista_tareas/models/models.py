# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

#Definimos el modelo de datos
class ListaTareas(models.Model):
    _name = 'lista_tareas.lista_tareas'
    _description = 'Lista de tareas.'
    _order = 'fecha_limite asc, prioridad desc'
    
    name = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción')
    responsable_id = fields.Many2one('res.users', string='Responsable', required=True, default=lambda self: self.env.user)
    fecha_limite = fields.Date(string='Fecha límite')
    
    prioridad = fields.Selection([
        ('baja','Baja'),
        ('media','Media'),
        ('alta','Alta')
    ], string='Prioridad', default='media')
    
    estado = fields.Selection([
        ('pendiente','Pendiente'),
        ('progreso', 'En Progreso'),
        ('completada','Completada'),
    ], string='Estado', default='pendiente')
    
    atrasada = fields.Boolean(
        string='Atrasada',
        compute='_compute_atrasada',
        store=True
    )
    
    color = fields.Integer(string='Color',compute='_compute_color', store=True)
    
    
    @api.depends('fecha_limite','estado')
    def _compute_atrasada(self):
        for record in self:
            if record.fecha_limite and record.estado != 'completada':
                record.atrasada = record.fecha_limite < date.today()
            else:
                record.atrasada = False
    
    @api.depends('prioridad','atrasada')
    def _compute_color(self):
        for record in self:
            if record.atrasada:
                record.color = 1 #rojo
            elif record.prioridad == 'alta':
                record.color = 2 #naranja
            elif record.prioridad == 'media':
                record.color = 3 #amarillo
            else:
                record.color = 0 #sin color
                