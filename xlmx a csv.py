# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:17:17 2023

@author: el_ni
"""

import pandas as pd

# Ruta al archivo Excel
excel_file_path = r'C:\Users\el_ni\OneDrive\Escritorio\Xios\PROGAMA/BD-XIOS2.xlsx'

# Ruta de salida para el archivo CSV
csv_file_path = r'C:\Users\el_ni\OneDrive\Escritorio\Xios\PROGAMA/BD-XIOS.csv'

# Leer el archivo Excel
df = pd.read_excel(excel_file_path)

# Guardar el DataFrame en formato CSV
df.to_csv(csv_file_path, index=False, encoding='utf-8')

print('La transformación de Excel a CSV se ha completado correctamente.')
