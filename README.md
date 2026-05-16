# Detección de Fracturas Óneas - FracAtlas (Hito 1)

Este repositorio contiene el desarrollo del Hito 1 (Trabajo Parcial) para el curso de Procesamiento de Imágenes. El objetivo de esta etapa es realizar un Análisis Exploratorio de Datos (EDA) estadístico y geométrico, además de implementar un pipeline de preprocesamiento de alta fidelidad diseñado para optimizar el entrenamiento de una Red Neuronal Convolucional (CNN) en el Hito 2.

---

## Estructura del Repositorio

El proyecto se encuentra organizado bajo la siguiente estructura limpia y estandarizada:

mi-proyecto-fracatlas/
├── FracAtlas_orvile/                 # Dataset original (Excluido de Git - Se descarga aparte)
├── Dataset_Procesado/                # Output generado por el script (Excluido de Git)
├── notebooks/                        # Cuadernos interactivos de Jupyter
│   └── Hito1_EDA_Personalizado_v2.ipynb
├── src/                              # Código fuente ejecutable
│   ├── Batch_Procesamiento.py        # Script de procesamiento por lote
│   └── analisis_histogramas_impacto.py
├── .gitignore                        # Exclusión de archivos pesados en Git
├── README.md                         # Documentación del proyecto
└── requirements.txt                  # Librerías necesarias para el entorno

---

## ¡IMPORTANTE! Descarga e Instalación del Dataset

Debido a restricciones de almacenamiento y límites de peso en GitHub, este repositorio no incluye las imágenes crudas ni procesadas del dataset. Para poder ejecutar el código en tu entorno local, debes seguir estos pasos en orden:

1. Clonar el repositorio
Clona este repositorio en tu máquina local y colócate en la raíz del proyecto:
git clone https://github.com/tu-usuario/tu-repositorio-fracatlas.git
cd tu-repositorio-fracatlas

2. Colocar el Dataset FracAtlas
- Descarga el dataset original FracAtlas (versión de orvile) desde Kaggle.
- Descomprime la carpeta del dataset directamente en la raíz de tu clon local del repositorio (al mismo nivel que las carpetas src/ y notebooks/).
- Asegúrate de respetar la siguiente estructura exacta para la metadata y archivos: 
  FracAtlas_orvile/FracAtlas/dataset.csv

3. Instalar dependencias
Instala todas las librerías necesarias ejecutando el archivo de requerimientos desde tu terminal:
pip install -r requirements.txt

---

## Orden de Ejecución

Una vez que el dataset original esté colocado correctamente en la raíz del proyecto, sigue este flujo para ejecutar el proyecto:

Paso 1: Ejecutar el Procesamiento en Batch
Para procesar las 4,083 imágenes del dataset (tanto sanas como fracturadas) utilizando el pipeline optimizado de alta fidelidad, ejecuta el script de automatización desde la terminal:

python src/Batch_Procesamiento.py

* ¿Qué hace? Lee los archivos en escala de grises, aplica filtros de reducción de ruido dinámicos, realiza un realce agresivo de bordes óseos y guarda automáticamente las nuevas imágenes optimizadas dentro de la carpeta autogenerada Dataset_Procesado/ en la raíz. Cuenta con una barra de progreso en tiempo real (tqdm) para monitorear el avance.

Paso 2: Explorar el Notebook Principal
Abre tu entorno de Jupyter y ejecuta el notebook interactivo:

jupyter notebook notebooks/Hito1_EDA_Personalizado_v2.ipynb

* ¿Qué hace? Contiene el Análisis Exploratorio de Datos (EDA) completo, los gráficos de distribución de clases anatómicas, el análisis geométrico de dimensiones, y las visualizaciones de recortes dinámicos (Crops) basados en los Bounding Boxes de las anotaciones COCO para centrar la atención exactamente en la patología.

---

## Detalles del Pipeline de Alta Fidelidad

Para maximizar la visibilidad de las microfracturas y fisuras sutiles, las imágenes sufren la siguiente transformación matemática en bloque antes de guardarse:

1. Filtro de Mediana (3x3): Se aplica en primer lugar sobre la radiografía cruda para eliminar el ruido estático granular típico de los rayos X sin difuminar los bordes estructurales primarios.
2. CLAHE (clipLimit=4.0, tileGridSize=(8,8)): Ecualización adaptativa de histograma por bloques que rescata texturas óseas ocultas e ilumina de forma inteligente zonas subexpuestas.
3. Unsharp Masking Agresivo (k=2.0): Se realiza una resta ponderada de frecuencias con un suavizado Gaussiano para afilar los contornos del hueso, haciendo que cualquier interrupción en el córtex cortical se visualice como una línea nítida de alto contraste.