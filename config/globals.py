from pathlib import Path
import os
downloads_path = str(Path.home() / "Downloads")

# Tiempo de espera (en segundos para la generacion de data)
GENERATE_SEC = 60

# Pagina de ingreso al portal de proveedores de dimexa
WEB_PAGE_URL = 'http://190.116.51.180:8080/dimexaproveedor/login.zul'


# Solo cambiar si la carpeta de descargas no es al de default
DOWNLOAD_PATH = downloads_path
DOWNLOAD_FILE_PATH = os.path.join(DOWNLOAD_PATH, 'Detalle.xlsx')


# Regiones a revisar
REGIONS = ['AREQUIPA','HUANCAYO','LIMA','TACNA','TRUJILLO']