import os
import cv2
import pandas as pd
import numpy as np
from tqdm import tqdm  # Barra de progreso para el CLI

# 1. Configuración de rutas para tu estructura ACTUAL en TP
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sube un nivel (a 'TP') y entra directo a 'FracAtlas_orvile'
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'FracAtlas_orvile', 'FracAtlas'))

CSV_PATH = os.path.join(BASE_DIR, 'dataset.csv')
IMG_FRAC_DIR = os.path.join(BASE_DIR, 'images', 'Fractured')
IMG_NON_FRAC_DIR = os.path.join(BASE_DIR, 'images', 'Non_fractured')

# Destino: Carpeta 'Dataset_Procesado' directo en la raíz de 'TP'
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Dataset_Procesado'))

# Asegurar que la carpeta nueva exista antes de empezar
os.makedirs(OUTPUT_DIR, exist_ok=True)


def aplicar_pipeline_optimizado(img_gray):
    # 1. Filtro Mediana PRIMERO para eliminar ruido estático
    img_median = cv2.medianBlur(img_gray, 3)

    # 2. CLAHE con clipLimit=4.0
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_median)
    
    # 3. Unsharp Masking AGRESIVO Corregido (k=2.0 => beta=-2.0)
    gaussian_blur = cv2.GaussianBlur(img_clahe, (0, 0), 1.5)
    img_enhanced = cv2.addWeighted(img_clahe, 3.0, gaussian_blur, -2.0, 0)
    
    return img_enhanced


def ejecutar_procesamiento_lote():
    print("\n" + "=" * 50)
    print("      VERIFICACIÓN DE RUTAS DEL SISTEMA       ")
    print("=" * 50)
    print(f"Buscando CSV en:   {CSV_PATH}")
    print(f"¿CSV encontrado?:  {os.path.exists(CSV_PATH)}")
    print(f"Carpeta destino:   {OUTPUT_DIR}")
    print("=" * 50 + "\n")

    if not os.path.exists(CSV_PATH):
        print("Error crítico: No se encontró 'dataset.csv'. Verifica las carpetas.")
        return
        
    df = pd.read_csv(CSV_PATH)
    total_imgs = len(df)
    print(f"Iniciando lote. Muestras detectadas: {total_imgs}\n")
    
    conteo_exitos = 0
    conteo_errores = 0
    
    for _, row in tqdm(df.iterrows(), total=total_imgs, desc="Procesando Batch"):
        img_id = row['image_id']
        es_fracturada = row['fractured']
        
        folder_origen = IMG_FRAC_DIR if es_fracturada == 1 else IMG_NON_FRAC_DIR
        ruta_entrada = os.path.join(folder_origen, img_id)
        ruta_salida = os.path.join(OUTPUT_DIR, img_id)
        
        # 1. LECTURA ROBUSTA (Soporta tildes)
        try:
            with open(ruta_entrada, 'rb') as f:
                img_array = np.frombuffer(f.read(), np.uint8)
                img_orig = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        except Exception:
            img_orig = None
            
        if img_orig is None:
            conteo_errores += 1
            continue
            
        # 2. PROCESAMIENTO
        img_procesada = aplicar_pipeline_optimizado(img_orig)
        
        # 3. ESCRITURA ROBUSTA (Soporta tildes - Reemplaza cv2.imwrite)
        try:
            # Codifica la imagen matriz a un buffer JPG en memoria
            suceso, img_codificada = cv2.imencode('.jpg', img_procesada)
            if suceso:
                # Escribe los bytes directamente usando Python nativo
                with open(ruta_salida, 'wb') as f:
                    f.write(img_codificada)
                conteo_exitos += 1
            else:
                conteo_errores += 1
        except Exception:
            conteo_errores += 1
        
    print(f"\n¡Proceso terminado! Éxitos: {conteo_exitos} | Errores: {conteo_errores}")


if __name__ == '__main__':
    ejecutar_procesamiento_lote()