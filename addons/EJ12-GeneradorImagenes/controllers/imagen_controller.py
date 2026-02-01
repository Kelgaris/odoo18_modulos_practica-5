# -*- coding: utf-8 -*-
# Importamos clases necesarias de Odoo para definir controladores HTTP
from odoo import http
from odoo.http import request

# Importamos bibliotecas externas necesarias
import base64                    # Para codificar la imagen en base64
from io import BytesIO           # Para trabajar con flujos en memoria
import random                    # Para generar valores aleatorios

# Importamos Pillow (PIL) para la generación de imágenes
from PIL import Image


# Clase controladora para las rutas HTTP
class GenerarImagenAleatoria(http.Controller):

    '''
    Este método genera una imagen PNG formada por píxeles aleatorios,
    recibiendo por URL el ancho y el alto de la imagen.

    Ejemplo de uso:
    http://localhost:8069/imagen/aleatoria/300/200

    Mostrará una imagen HTML generada dinámicamente.
    '''

    # Ruta expuesta públicamente
    @http.route(
        '/imagen/aleatoria/<int:ancho>/<int:alto>',
        auth='public',
        cors='*',
        type='http'
    )
    def crearImagen(self, ancho, alto, **kw):

        # Creamos una imagen RGB con las dimensiones indicadas
        imagen = Image.new('RGB', (ancho, alto))
        pixeles = imagen.load()

        # Recorremos cada píxel y le asignamos un color aleatorio
        for x in range(ancho):
            for y in range(alto):
                pixeles[x, y] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

        # Creamos un flujo en memoria para guardar la imagen
        fp = BytesIO()

        # Guardamos la imagen en formato PNG dentro del flujo
        imagen.save(fp, format='PNG')

        # Codificamos el contenido del flujo en base64
        img_str = base64.b64encode(fp.getvalue()).decode("utf-8")

        # Devolvemos una vista HTML con la imagen embebida
        return '<div><img src="data:image/png;base64,' + img_str + '"/></div>'
