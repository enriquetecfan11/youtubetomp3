import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import os

# Función para descargar el video de YouTube
def descargar_video(url, ruta):
    yt = YouTube(url)
    # Seleccionar la mejor calidad disponible
    video = yt.streams.filter(only_audio=True).first()
    # Descargar el video
    video.download(ruta)
    return video.default_filename

# Función para convertir el video descargado a mp3
def convertir_a_mp3(video_file, ruta):
    # Construir la ruta completa al archivo de video
    video_file_path = os.path.join(ruta, video_file)
    # Cargar el archivo de audio usando pydub
    audio = AudioSegment.from_file(video_file_path)
    # Crear el nombre del archivo mp3
    mp3_file = os.path.splitext(video_file)[0] + '.mp3'
    # Guardar el archivo de audio como mp3 en la carpeta music
    # mp3_file_path = os.path.join(ruta, 'music', mp3_file)
    mp3_file_path = os.path.join(ruta, mp3_file)
    audio.export(mp3_file_path, format='mp3')
    # Eliminar el archivo de video
    os.remove(video_file_path)
    return mp3_file, mp3_file_path

# Función principal de la aplicación
def main(ruta=os.getcwd()):
    mp3_file = None  # Inicializa mp3_file con None fuera del bloque try-except
    # Importa la imagen de la portada que se llama youtubetomp3.png
    st.image("portadayoutube.jpg", use_column_width=True)
    
    # st.title("De video a MP3")
    st.write("Esta aplicación te permite descargar y convertir videos de YouTube a archivos de audio MP3.")
    st.write("Para poder utilizar esta aplicación, simplemente introduce la URL del video de YouTube en el cuadro de texto y haz clic en el botón 'Descargar y Convertir'")


    # Entrada de URL de YouTube
    url = st.text_input("Introduce la URL del video de YouTube:")

    if st.button("Descargar y Convertir"):
        # Validar la URL
        if url.strip() == "":
            st.error("Por favor, introduce una URL válida.")
        else:
            try:
                # Ruta donde se guardarán los archivos
                ruta = os.path.abspath(os.path.dirname(__file__))
                # Descargar el video, meterlo en la carpeta music y obtener su nombre de archivo
                video_file = descargar_video(url, ruta)
                # Convertir el video a MP3
                mp3_file, mp3_file_path = convertir_a_mp3(video_file, ruta)
                st.success("El video se ha descargado y convertido a MP3 con éxito.")
                st.audio(mp3_file, format='audio/mp3')
                st.write("Para descargar el archivo MP3, haz click en los puntos de del reproductor de audio y selecciona 'Descargar'.")
                st.write("Recuerda escribe el nombre de archivo que desees y seguido .mp3 para que se descargue correctamente. Ejemplo: 'cancion.mp3'")
                st.markdown(f"[Descargar archivo MP3]({mp3_file_path})")
            except Exception as e:
                st.error(f"Ha ocurrido un error: {e}")

    st.write("Hecho por Enrique Rodriguez Vela")

if __name__ == "__main__":
    main()
