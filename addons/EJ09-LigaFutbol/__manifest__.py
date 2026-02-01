# -*- coding: utf-8 -*-
{
    'name': "Gestionar liga de futbol",  # Titulo del módulo
    'summary': "Gestionar una liga de futbol :) (Version avanzada)",  # Resumen de la funcionaliadad
    'description': """
    Gestor de Liga de futbol (Version avanzada)
    ==============
    """,  

    #Indicamos que es una aplicación
    'application': True,
    'author': "Sergi García",
    'website': "http://apuntesfpinformatica.es",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],

    'data': [

      
        #Estos dos primeros ficheros:
        #1) El primero indica grupo de seguridad basado en rol
        #2) El segundo indica la politica de acceso del modelo
        #Mas información en https://www.odoo.com/documentation/17.0/es/developer/howtos/rdtraining/05_securityintro.html
        #Y en www.odoo.yenthevg.com/creating-security-groups-odoo/
        #'security/groups.xml',
        'security/ir.model.access.csv',

        'views/liga_equipo.xml',
        'views/liga_equipo_clasificacion.xml',

        # PRIMERO el wizard
        'wizard/liga_equipo_wizard.xml',
        'wizard/liga_partido_wizard.xml',

        # DESPUÉS las vistas que lo llaman
        'views/liga_partido.xml',

        'report/report_liga_partido.xml',

    ],
    # Fichero con data de demo si se inicializa la base de datos con "demo data" (No incluido en ejemplo)
    # 'demo': [
    #     'demo.xml'
    # ],
}
