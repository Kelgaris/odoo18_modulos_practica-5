# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

#Clase del controlador web
class Main(http.Controller):
    #Decorador que indica que la url "/ligafutbol/equipo/json" atendera por HTTP, sin autentificacion
    #Devolvera texto que estará en formato JSON
    #Se puede probar accediendo a http://localhost:8069/ligafutbol/equipo/json
    @http.route('/ligafutbol/equipo/json', type='http', auth='none')
    def obtenerDatosEquiposJSON(self):
        #Obtenemos la referencia al modelo de Equipo
        equipos = request.env['liga.equipo'].sudo().search([])
        
        #Generamos una lista con informacion que queremos sacar en JSON
        listaDatosEquipos=[]
        for equipo in equipos:
             listaDatosEquipos.append([equipo.nombre,str(equipo.fecha_fundacion),equipo.jugados,equipo.puntos,equipo.victorias,equipo.empates,equipo.derrotas])
        #Convertimos la lista generada a JSON
        json_result=json.dumps(listaDatosEquipos)

        return json_result



class EliminarEmpates(http.Controller):

    @http.route('/eliminarempates', type='http', auth='none', csrf=False)
    def eliminar_empates(self):
        # Obtenemos todos los partidos con privilegios de superusuario
        Partidos = request.env['liga.partido'].sudo()
        partidos = Partidos.search([])

        # Filtramos solo los empates de manera segura (maneja None)
        empates = partidos.filtered(lambda p: p.goles_casa is not None and p.goles_fuera is not None and p.goles_casa == p.goles_fuera)

        # Contamos antes de eliminar
        contador = len(empates)

        if contador > 0:
            # Eliminamos todos los empates de una vez
            empates.unlink()

            # Actualizamos clasificación de equipos
            Partidos.actualizoRegistrosEquipo()

        return f'Se han eliminado {contador} partidos que terminaron en empate.'