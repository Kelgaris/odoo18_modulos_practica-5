# comando para instalar las libreria de request                pip install python-telegram-bot requests 
# import de la librerias
from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler, MessageHandler, ContextTypes, filters
import requests
import json


# el token que nos pasara el bot de telegram
TOKEN = "8321363961:AAEEtV4BiTlTYKQicuFMR__UwZ0w9m-dI8g"
API_URL = "http://localhost:8069/gestion/apirest/socio"
API_URL_MOSTRAR_TODOS = "http://localhost:8069/gestion/socio"


# funcion para las ordenes
async def ordenes_comandos_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_que_le_mandamos = update.message.text

    try:

        partes = mensaje_que_le_mandamos.split(",") 

        # Indicamos que la orden es la posicion 0 osea la primera parte, usamos strip por si hay algun espacion para evitar problemas y pasarlo a minusculas
        orden = partes[0].strip().lower()

        # Guardamos los datos del usuarios, los campos y sus valores por ejemplo "nombre": "juan" y el resto si se lo mandasmos
        datos_orden = {}

        # Recorremos cada parte del rsto de las instrucciones, pero empezamos a partir de la orden, se cogeria la parte de por ejemplo nombre= ivan y lo que siga
        for cada_parte in partes[1:]:
            cada_parte = cada_parte.strip()

            if "=" not in cada_parte:
                raise ValueError("Formato incorrecto")

            tipo_orden, cada_campo = cada_parte.split("=", 1)
            datos_orden[tipo_orden.strip()] = cada_campo.strip()

        # Creamos
        if orden == "crear":
            print(datos_orden)
            datos_parseados=json.dumps(datos_orden)
            print("Socio Creado: "+datos_parseados)
            # con la libreria de requests le indicamos el tipo de peticion que es(en este caso post), la parte de la url y los datos
            respuesta = requests.post(API_URL, datos_parseados)
            #mesajes para verlos en la terminal
            print(f"Se ha creado el socio: {datos_orden}")
            
            # lo que te devuelve el bot de telegram con los que le hallas pasado
            await update.message.reply_text("se ha creado al socio correctamente: "+ respuesta.text)

        # Mostramos
        elif orden == 'consultar':
            identificador_socio=json.dumps(datos_orden)
            respuesta = requests.get(f"{API_URL}?data={identificador_socio}")
            print(f"Se encontró el socio: {respuesta}")
            await update.message.reply_text(respuesta.text)
                
        # Borramos
        elif orden =='borrar':

            socio_borrar=json.dumps(datos_orden)
            respuesta = requests.delete(f'{API_URL}?data={socio_borrar}')

            print(f"Se ha borrado el socio: {datos_orden}")

            await update.message.reply_text("se ha borrado al socio correctamente: "+respuesta.text)
        
        # Modificamos
        elif orden == 'modificar':
            modificar_socio=json.dumps(datos_orden)
            respuesta = requests.put(API_URL, data=modificar_socio)
            print(f"Se ha modificado el socio: {datos_orden}")

            await update.message.reply_text("se ha modificado al socio correctamente: "+ respuesta.text)

    except Exception as e:
        await update.message.reply_text("has puesto mal el formato de la orden, prueba de nuevo")


# comando /help 
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_aiuda = """
    Lo que puedes hacer:

    • **Ver todos los socios**: todos\n
    • **Crear socio**: Crear, nombre=Juan, apellidos=fonso, num_socio=777 \n
    • **Borrar socio**: borrar, num_socio= [ numero del socio ]\n
    • **Modificar socio**: put ,num_socio=[ numero del socio para modificar ], [ campo a modificar]= valor a modificar\n
    """
    await update.message.reply_text(mensaje_aiuda)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    #cuando hacer /help llama a la funcion que mostrara el mensaje de ayuda, esto es gracias al commandhandler que son todos los mensajes  que empeicen por "/" mas el texto en nuestro caso es help y la fucnio
    app.add_handler(CommandHandler("help", ayuda))

    # para el resto de las ordenes que le ponemso 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ordenes_comandos_telegram))
    #mesaje en la terminal del proyecto para ver si inicio correctamente
    print("Bot de Telegram iniciado correctamente")
    
    app.run_polling()

if __name__ == "__main__":
    main()
