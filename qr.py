import pyodbc
import qrcode
import os

# ... Código de conexión a la base de datos ...
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
        UPPER(LTRIM(RTRIM(TLPHC.FIRSTNAME))) + ' ' + UPPER(LTRIM(RTRIM(TLPHC.LASTNAME))) AS HELPCARE,
        UPPER(LD.LEADER) AS LIDER,
        CASE
            WHEN TPC.Photo LIKE '%C:\inetpub\wwwroot\Periticket\%' THEN REPLACE(TPC.PHOTO, 'C:\inetpub\wwwroot\Periticket\', 'https://periticket.periferia-it.com/')
            WHEN TPC.Photo LIKE '%C:\inetpub\wwwroot\PeriticketProduccion\%' THEN REPLACE(TPC.PHOTO, 'C:\inetpub\wwwroot\PeriticketProduccion\', 'https://periticket.periferia-it.com/')
        END AS FOTO_COLABORADOR
    FROM PeriticketDev..COLLABORATOR C
        INNER JOIN PeriticketDev..TALENT_PRECOLLABORATOR TPC ON TPC.IDPRECOLLABORATOR = C.IDPRECOLLABORATOR
        INNER JOIN PeriticketDev..HIRE H ON H.IDCOLLABORATOR = C.IDCOLLABORATOR
        INNER JOIN PeriticketDev..CUSTOMER_PROFILE CP ON CP.ID_CUSTOMER_PROFILE = H.ID_CUSTOMER_PROFILE
        INNER JOIN PeriticketDev..ASPNETUSERS ANU ON ANU.ID = C.IDUSER
        INNER JOIN PeriticketDev..LEADERDESK LD ON LD.IDLEADER = H.LEADER
        INNER JOIN PeriticketDev..COLLABORATOR HC ON HC.IDCOLLABORATOR = LD.IDCOLLABORATORHELPCARE
        INNER JOIN PeriticketDev..TALENT_PRECOLLABORATOR TLPHC ON TLPHC.IDPRECOLLABORATOR = HC.IDPRECOLLABORATOR
    WHERE H.STATUS = 1
''')

# Lista de enlaces
enlaces = [
    "https://ibb.co/WV0sbL1",
    "https://ibb.co/L05n7ZG",
    "https://ibb.co/jr8TLsF",
    "https://ibb.co/Zx3DWFC",
    "https://ibb.co/s6Qpbh8",
    "https://ibb.co/r6f4zR3",
    "https://ibb.co/xjWm8F7",
    "https://ibb.co/7Wc3330",
    "https://ibb.co/YDnf3Yk",
    "https://ibb.co/FspgbBq",
    "https://ibb.co/cwGy66b",
    "ttps://ibb.co/NrzXHBk",
    "https://ibb.co/CzcTS2f",
    "https://ibb.co/KKvwLcg",
    "https://ibb.co/0nRwvdd",
    "https://ibb.co/ZcTtdRz",
    "https://ibb.co/qdqz9Lp",
    "https://ibb.co/4fZK1dM",
    "https://ibb.co/858Tpp2",
    "https://ibb.co/RP61G7k",
    "https://ibb.co/FJQDtNN",
    "https://ibb.co/h2x9HHv",
    "https://ibb.co/JdyGDkf",
    "https://ibb.co/K2fWtH8",
    "https://ibb.co/4tZyMQb",
    "https://ibb.co/99ZL6ft",
    "https://ibb.co/fkx7hBk",
    "https://ibb.co/KLJGfst",
    "https://ibb.co/4fspKDW",
    "https://ibb.co/jhHBv3R",
    "https://ibb.co/bXq8nz2",
    "https://ibb.co/sHNVD6j",
    "https://ibb.co/9wLng1b",
    "https://ibb.co/Hqp1cjD",
    "https://ibb.co/NCZwymQ",
    "https://ibb.co/7b4M6ft",
    "https://ibb.co/h8xrLdJ",
    "https://ibb.co/Tm3nYM3",
    "https://ibb.co/q7D71DN",
    "https://ibb.co/VHy00nF",
    "https://ibb.co/Fw6wbvr",
    "https://ibb.co/nn5TSnG",
    "https://ibb.co/PwwTmCJ",
    "https://ibb.co/pR7BDCN",
    "https://ibb.co/F6j4128",
    "https://ibb.co/NKZb0Pd",
    "https://ibb.co/TM6HH4y",
    "https://ibb.co/3hyYZHW",
    "https://ibb.co/W35LYky",
    "https://ibb.co/KLfNDRq",
    "https://ibb.co/XWbCH48",
    "https://ibb.co/C80zjTf",
    "https://ibb.co/3yPwfvj",
    "https://ibb.co/rpZfw7s",
    "https://ibb.co/MMTsySr",
    "https://ibb.co/b7VkB1m",
    "https://ibb.co/5nhznCp",
    "https://ibb.co/jDrLzYx",
    "https://ibb.co/nmVX8KM",
    "https://ibb.co/qkFFcQh",
    # ... Resto de los enlaces ...
]

# Carpeta para almacenar los códigos QR
carpeta_codigos_qr = 'codigos_qr'
if not os.path.exists(carpeta_codigos_qr):
    os.makedirs(carpeta_codigos_qr)

# Iterar sobre los resultados de la consulta y asignar un enlace a cada código QR
for i, row in enumerate(cursor):
    nombre_completo = row[0]
    documento = row[1]
    perfil = row[2]
    telefono = row[3]
    tipo_sangre = row[4]
    correo = row[5]
    helpcare = row[6]
    lider = row[7]
    foto_colaborador = row[8]
    
    # Verificar si hay suficientes enlaces en la lista
    if i >= len(enlaces):
        break
    
    # Obtener el enlace correspondiente
    enlace_carnet = enlaces[i]
    
    # Generar el código QR con el enlace
    qr = qrcode.QRCode()
    qr.add_data(enlace_carnet)
    qr.make(fit=True)
    imagen_qr = qr.make_image()
    
    # Guardar el código QR en la carpeta
    nombre_archivo = f'{documento}.png'
    ruta_archivo = os.path.join(carpeta_codigos_qr, nombre_archivo)
    imagen_qr.save(ruta_archivo)
