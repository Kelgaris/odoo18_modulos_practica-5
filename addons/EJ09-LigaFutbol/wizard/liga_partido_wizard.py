from odoo import models, fields

class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Wizard crear partido'

    equipo_local_id = fields.Many2one(
        'liga.equipo',
        string='Equipo Local',
        required=True
    )

    equipo_visitante_id = fields.Many2one(
        'liga.equipo',
        string='Equipo Visitante',
        required=True
    )

    goles_local = fields.Integer(string='Goles Local', required=True)
    goles_visitante = fields.Integer(string='Goles Visitante', required=True)

    def action_crear_partido(self):
        self.env['liga.partido'].create({
            'equipo_casa': self.equipo_local_id.id,
            'equipo_fuera': self.equipo_visitante_id.id,
            'goles_casa': self.goles_local,
            'goles_fuera': self.goles_visitante
        })