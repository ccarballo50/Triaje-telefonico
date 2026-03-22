import streamlit as st
import tempfile
import os

import imageio_ffmpeg

from dotenv import load_dotenv

from prompts import PROMPT_NARRATIVO, PROMPT_CLINICO
from openai import OpenAI

texto_narrativo = None
texto_clinico = None

# ------------------------------
# Cargar variables de entorno
# ------------------------------

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# ------------------------------
# Añadir ffmpeg al PATH
# ------------------------------

os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())


# ------------------------------
# Configuración Streamlit
# ------------------------------

st.set_page_config(
    page_title="Demo análisis de llamadas",
    layout="wide"
)

st.title("Demo - Análisis de llamadas sanitarias")

st.write(
"""
Sube un archivo de audio de una llamada sanitaria.

La aplicación realizará automáticamente:

• Transcripción del audio  
• Análisis narrativo  
• Análisis clínico
"""
)

st.divider()


# ------------------------------
# Subida de audio
# ------------------------------

uploaded_audio = st.file_uploader(
    "Sube el archivo de audio",
    type=["mp3","wav","m4a","ogg"]
)


# ------------------------------
# Procesar audio
# ------------------------------

if uploaded_audio is not None:

    st.success("Audio cargado correctamente")

    st.write("Nombre del archivo:", uploaded_audio.name)
    st.write("Tipo:", uploaded_audio.type)
    st.write("Tamaño:", uploaded_audio.size, "bytes")

    st.audio(uploaded_audio)

    st.divider()

    st.subheader("Transcripción")

    # Guardar audio temporal
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_audio.read())
        temp_audio_path = tmp_file.name

    # Transcripción Whisper
    with st.spinner("Transcribiendo audio..."):

        with open(temp_audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )
    
        texto_transcrito = transcription.text

    st.write(texto_transcrito)

    st.divider()

    # Inicializar variables para evitar errores
    texto_narrativo = ""
    texto_clinico = ""

    st.subheader("Análisis de la llamada")

    # ------------------------------
    # Ejecutar análisis con IA
    # ------------------------------

    with st.spinner("Analizando llamada con IA..."):

        prompt_narrativo = PROMPT_NARRATIVO.format(texto=texto_transcrito)

        respuesta_narrativa = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt_narrativo}
            ]
        )

        texto_narrativo = respuesta_narrativa.choices[0].message.content


        prompt_clinico = PROMPT_CLINICO.format(texto=texto_transcrito)

        respuesta_clinica = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt_clinico}
            ]
        )

        texto_clinico = respuesta_clinica.choices[0].message.content


    # ------------------------------
    # Mostrar resultados
    # ------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Análisis narrativo")
        st.write(texto_narrativo)

    with col2:
        st.subheader("Análisis clínico")
        st.write(texto_clinico)
