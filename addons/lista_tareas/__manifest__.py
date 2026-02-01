# -*- coding: utf-8 -*-
{
    'name': "Gestor de tareas Avanzado",

    'summary': "Gestión de tareas personales con prioridades y fechas límite.",

    'description': """
        Módulo de ejemplo para Odoo 18 - Gestior de tareas Avanzado.
    """,

    'author': "David Priego",
    'website': "https://www.yourcompany.com",
    'application': True,
    'installable': True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ]
}

