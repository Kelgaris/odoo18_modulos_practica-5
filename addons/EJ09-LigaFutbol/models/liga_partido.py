# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LigaPartido(models.Model):
    #Nombre y descripcion del modelo
    _name = 'liga.partido'
    _description = 'Un partido de la liga'


    #Atributos del modelo


    #PARA CUANDO NO HAY UN ATRIBUTO LLAMADO NAME PARA MOSTRAR LOS Many2One en Vistas
    # https://www.odoo.com/es_ES/forum/ayuda-1/how-defined-display-name-in-custom-many2one-91657
    
   

    #Nombre del equipo que juega en casa casa
    equipo_casa = fields.Many2one(
        'liga.equipo',
        string='Equipo local',
    )
    #Goles equipo de casa
    goles_casa= fields.Integer()

    #Nombre del equipo que juega fuera
    equipo_fuera = fields.Many2one(
        'liga.equipo',
        string='Equipo visitante',
    )
    #Goles equipo de casa
    goles_fuera= fields.Integer()
    
    # Declaramos campos para guardar si existe goleada y los puntos extra adjudicados
    goleada_detectada = fields.Boolean(default=False, help='Indica si hay una diferencia de 4+ goles')
    puntos_extra_ganador = fields.Integer(default=0, help='Puntos extra para el equipo ganador')
    puntos_extra_perdedor = fields.Integer(default=0, help='Puntos extra/penalizacion para el equipo perdedor')
    
    #Constraints de atributos
    @api.constrains('equipo_casa')
    def _check_mismo_equipo_casa(self):
        for record in self:
            if not record.equipo_casa:
                raise models.ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')


     #Constraints de atributos
    @api.constrains('equipo_fuera')
    def _check_mismo_equipo_fuera(self):
        for record in self:
            if not record.equipo_fuera:
                raise models.ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_fuera and record.equipo_casa == record.equipo_fuera:
                raise models.ValidationError('Los equipos del partido deben ser diferentes.')




    
    # Declaramos metodo para incrementar 2 goles a todos los equipos locales
    def incrementar_goles_locales(self):
        for partidos in self.search([]):  # TODOS los partidos
            partidos.goles_casa += 2
            partidos._calcular_puntos_extra()
        self.actualizoRegistrosEquipo()
        return True
    
    
    # Declaramos metodo para incrementar 2 goles a todos los equipos visitantes
    def incrementar_goles_visitantes(self):
        for partidos in self.search([]):  # TODOS los partidos
            partidos.goles_fuera += 2
            partidos._calcular_puntos_extra()
        self.actualizoRegistrosEquipo()
        return True

    
    '''
    Funcion para detectar y calcular los puntos extra por goleada (diferencia >= 4 goles)
    '''
    def _calcular_puntos_extra(self):
        # Calculamos la diferencia de goles
        diferencia_goles = abs(self.goles_casa - self.goles_fuera)
        
        # Evaluamos si existe goleada (diferencia de 4 o mas goles)
        if diferencia_goles >= 4:
            # Indicamos que hay goleada
            self.goleada_detectada = True
            
            # Determinamos quien gano y asignamos puntos
            if self.goles_casa > self.goles_fuera:
                # El equipo de casa gana: gana 4 puntos extra (7 total) y el visitante pierde 1 punto
                self.puntos_extra_ganador = 4
                self.puntos_extra_perdedor = -1
            else:
                # El equipo visitante gana: gana 4 puntos extra (7 total) y el local pierde 1 punto
                self.puntos_extra_ganador = 4
                self.puntos_extra_perdedor = -1
        else:
            # No hay goleada
            self.goleada_detectada = False
            self.puntos_extra_ganador = 0
            self.puntos_extra_perdedor = 0

    '''
    Funcion para actualizar la clasificacion de los equipos, re-calculandola entera
    '''
    def actualizoRegistrosEquipo(self):
        #Recorremos partidos y equipos
        for recordEquipo in self.env['liga.equipo'].search([]):
            #Como recalculamos todo, ponemos de cada equipo todo a cero
            recordEquipo.victorias=0
            recordEquipo.empates=0
            recordEquipo.derrotas=0
            recordEquipo.goles_a_favor=0
            recordEquipo.goles_en_contra=0
            recordEquipo.puntos_extra=0
            
            for recordPartido in self.env['liga.partido'].search([]):  
        
                #Si es el equipo de casa
                if recordPartido.equipo_casa.nombre==recordEquipo.nombre:
                    
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                        # Sumamos los puntos extra si existe goleada (el ganador obtiene 4 puntos extra)
                        recordEquipo.puntos_extra=recordEquipo.puntos_extra+recordPartido.puntos_extra_ganador
                    elif recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                        # Restamos puntos si existe goleada (el perdedor pierde 1 punto)
                        recordEquipo.puntos_extra=recordEquipo.puntos_extra+recordPartido.puntos_extra_perdedor
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                        
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_casa
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_fuera

                #Si es el equipo de fuera
                if recordPartido.equipo_fuera.nombre==recordEquipo.nombre:
                    
                    #Miramos si es victoria o derrota
                    if recordPartido.goles_casa<recordPartido.goles_fuera:
                        recordEquipo.victorias=recordEquipo.victorias+1
                        # Sumamos los puntos extra si existe goleada (el ganador obtiene 4 puntos extra)
                        recordEquipo.puntos_extra=recordEquipo.puntos_extra+recordPartido.puntos_extra_ganador
                    elif recordPartido.goles_casa>recordPartido.goles_fuera:
                        recordEquipo.derrotas=recordEquipo.derrotas+1
                        # Restamos puntos si existe goleada (el perdedor pierde 1 punto)
                        recordEquipo.puntos_extra=recordEquipo.puntos_extra+recordPartido.puntos_extra_perdedor
                    else:
                        recordEquipo.empates=recordEquipo.empates+1
                    
                    #Sumamos goles a favor y en contra
                    recordEquipo.goles_a_favor=recordEquipo.goles_a_favor+recordPartido.goles_fuera
                    recordEquipo.goles_en_contra=recordEquipo.goles_en_contra+recordPartido.goles_casa


    def action_print_pdf(self):
        return self.env.ref('EJ09-LigaFutbol.action_report_liga_partido').report_action(self)



    #API onchange para cuando se modifica un partido
    #Aunque onchange envia un registro, hacemos codigo para recalcular 
    #http://www.geninit.cn/developer/reference/orm.html  
    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        # Calculamos los puntos extra basados en la diferencia de goles
        self._calcular_puntos_extra()
        # Actualizamos los registros de los equipos
        self.actualizoRegistrosEquipo()
    

    #Sobrescribo el borrado (unlink)
    def unlink(self):
        #Borro el registro, que es lo que hace el metodo normalmente
        result=super(LigaPartido,self).unlink()
        #Añado que llame a actualizoRegistroEquipo()
        self.actualizoRegistrosEquipo()
        return result

    #Sobreescribo el metodo crear
    @api.model
    def create(self, values):
        #hago lo normal del metodo create
        result = super().create(values)
        # Calculamos los puntos extra basados en la diferencia de goles
        result._calcular_puntos_extra()
        #Añado esto: llamo a la funcion que actualiza la clasificacion
        self.actualizoRegistrosEquipo()
        #hago lo normal del metodo create
        return result
