import pyodbc
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

# Conexión a la base de datos SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.168.10.106\PERITICKET;DATABASE=PeriticketDev;UID=sa;PWD=Periferia2019')

# Consulta a la base de datos
cursor = conn.cursor()
cursor.execute('''
    SELECT 
        UPPER(LTRIM(RTRIM(TPC.FIRSTNAME))) + ' ' + UPPER(LTRIM(RTRIM(TPC.LASTNAME))) AS NOMBRE_COMPLETO,
        C.IDENTIFICATIONNUMBER AS DOCUMENTO,
        UPPER(LTRIM(RTRIM(CP.PROFILE))) AS PERFIL,
        TPC.TELPHONE AS TELEFONO,
        UPPER(LTRIM(RTRIM(TPC.RH))) AS TIPO_SANGRE,
        ANU.EMAIL AS CORREO,
        CASE
            WHEN TPC.Photo LIKE '%C:\inetpub\wwwroot\Periticket\%' THEN REPLACE(TPC.PHOTO, 'C:\inetpub\wwwroot\Periticket\', 'https://periticket.periferia-it.com/')
            WHEN TPC.Photo LIKE '%C:\inetpub\wwwroot\PeriticketProduccion\%' THEN REPLACE(TPC.PHOTO, 'C:\inetpub\wwwroot\PeriticketProduccion\', 'https://periticket.periferia-it.com/')
        END AS FOTO_COLABORADOR
    FROM PeriticketDev..COLLABORATOR C
        INNER JOIN PeriticketDev..TALENT_PRECOLLABORATOR TPC ON TPC.IDPRECOLLABORATOR = C.IDPRECOLLABORATOR
        INNER JOIN PeriticketDev..HIRE H ON H.IDCOLLABORATOR = C.IDCOLLABORATOR
        INNER JOIN PeriticketDev..CUSTOMER_PROFILE CP ON CP.ID_CUSTOMER_PROFILE = H.ID_CUSTOMER_PROFILE
        INNER JOIN PeriticketDev..ASPNETUSERS ANU ON ANU.ID = C.IDUSER
    WHERE H.STATUS = 1
''')

# Configuración del diseño del carnet
carnet_width = 500  # Anchura de la tarjeta
carnet_height = 600
background_color = (255, 255, 255)  # Color de fondo blanco
text_color = (0, 0, 0)  # Color de texto negro
font_path = "arial.ttf"  # Ruta a la fuente Arial en tu sistema
font_size = 12  # Tamaño de fuente
padding = 10

# Logo configuration
logo_path = "logo.png"
logo_width = 100
logo_height = 100

# Triángulo configuration
triangle_width = 30
triangle_height = 30

# Crear una carpeta para los carnets
if not os.path.exists("carnets"):
    os.makedirs("carnets")

# Iterar sobre los resultados de la consulta
for row in cursor:
    row = dict(zip([column[0] for column in cursor.description], row))  # Convertir el objeto row en un diccionario
    
    nombre_completo = row['NOMBRE_COMPLETO']
    documento = row['DOCUMENTO']
    perfil = row['PERFIL']
    telefono = row['TELEFONO']
    tipo_sangre = row['TIPO_SANGRE']
    correo = row['CORREO']
    foto_url = row['FOTO_COLABORADOR']

    if foto_url is not None:
        # Descargar la foto del colaborador desde la URL
        response = requests.get(foto_url)
        foto = Image.open(BytesIO(response.content))

        # Redimensionar la foto al tamaño deseado
        foto_width = 150
        foto_height = 150
        foto = foto.resize((foto_width, foto_height))

        # Crear una nueva imagen para el carnet
        carnet_image = Image.new("RGB", (carnet_width, carnet_height), background_color)

        # Calcular las coordenadas para centrar la foto en el carnet
        foto_x = (carnet_width - foto_width) // 2
        foto_y = (carnet_height - foto_height) // 2

        # Pegar la foto del colaborador en el carnet
        carnet_image.paste(foto, (foto_x, foto_y))

        # Pegar el logo en una esquina arriba del carnet
        logo = Image.open(logo_path)
        logo = logo.resize((logo_width, logo_height))
        carnet_image.paste(logo, (padding, padding))

        # Agregar el nombre completo encima de la foto
        draw = ImageDraw.Draw(carnet_image)
        font = ImageFont.truetype(font_path, font_size + 4)
        text_width, text_height = draw.textsize(nombre_completo, font=font)
        text_x = carnet_width // 2 - text_width // 2
        text_y = padding + text_height + 30  # Ajuste para subir la foto un poco más debajo del nombre
        draw.text((text_x, text_y), nombre_completo, font=font, fill=text_color)

        # Agregar los datos debajo de la foto
        data_x = padding
        data_y = foto_y + foto_height + padding
        line_spacing = 2

        datos = [
            f"Perfil: {perfil}",
            f"Documento: {documento}",
            f"Teléfono: {telefono}",
            f"Tipo de Sangre: {tipo_sangre}",
            f"Correo: {correo}"
        ]

        # Colores de fondo y colores de letra
        fondo_verde_claro = (178, 255, 178)
        fondo_verde_agua_marina = (128, 255, 212)
        fondo_azul_medio_oscuro = (0, 0, 102)

        colores_fondo = [fondo_verde_claro, fondo_verde_claro, fondo_verde_agua_marina, fondo_verde_agua_marina, fondo_azul_medio_oscuro]
        colores_letra = [text_color, text_color, text_color, text_color, text_color]

        for i, dato in enumerate(datos):
            text_width, text_height = draw.textsize(dato, font=font)
            text_x = carnet_width // 2 - text_width // 2
            text_y = data_y + (text_height + line_spacing) * i

            # Dibujar el fondo con el color correspondiente
            fondo_color = colores_fondo[i]
            draw.rectangle([(padding, text_y), (carnet_width - padding, text_y + text_height)], fill=fondo_color)

            # Dibujar el texto con el color negro
            letra_color = (0, 0, 0)  # Letra negra
            draw.text((text_x, text_y), dato, font=font, fill=letra_color)

        # Agregar los triángulos en el lado izquierdo
        triangle_x = padding
        triangle_y = data_y
        triangle_spacing = 10

        # Colores de los triángulos
        color_azul = (0, 0, 255)
        color_verde = (0, 255, 0)
        color_rojo = (255, 0, 0)

        colores_triangulo = [color_azul, color_verde, color_rojo]

        for i, color_triangulo in enumerate(colores_triangulo):
            triangle_top = triangle_y + (triangle_height + triangle_spacing) * i
            triangle_bottom = triangle_top + triangle_height

            # Crear el objeto de dibujo para el triángulo
            draw_triangle = ImageDraw.Draw(carnet_image)

            # Dibujar el triángulo
            draw_triangle.polygon([(triangle_x + triangle_width, triangle_top), (triangle_x, triangle_top + triangle_height // 2),
                                   (triangle_x + triangle_width, triangle_bottom)], fill=color_triangulo)

        # Guardar el carnet
        carnet_filename = f"carnets/carnet_{nombre_completo.replace(' ', '_')}.png"
        carnet_image.save(carnet_filename)

# Cerrar la conexión a la base de datos
conn.close()
