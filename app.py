import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import numpy as np
import cv2
import av
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt
import time
import asyncio
from io import BytesIO

st.set_page_config(page_title="Monitoramento de Valores Médios RGB")

N = 300  # Número máximo de pontos no gráfico

# Classe para processar o vídeo
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.result_queue = asyncio.Queue()
        self.start_time = time.time()
        self.frame_count = 0
        self.r_accum = 0
        self.g_accum = 0
        self.b_accum = 0
        self.seconds_elapsed = 0  # Contador de segundos

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        current_time = time.time() - self.start_time
        self.frame_count += 1

        # Extrai os canais de cor
        b_channel = img[:, :, 0]
        g_channel = img[:, :, 1]
        r_channel = img[:, :, 2]

        # Acumula os valores RGB
        self.r_accum += float(np.mean(r_channel))
        self.g_accum += float(np.mean(g_channel))
        self.b_accum += float(np.mean(b_channel))

        # Verifica se passou 1 segundo
        if int(current_time) > self.seconds_elapsed:
            avg_r = self.r_accum / self.frame_count
            avg_g = self.g_accum / self.frame_count
            avg_b = self.b_accum / self.frame_count

            # Coloca os dados na fila
            asyncio.run_coroutine_threadsafe(
                self.result_queue.put((self.seconds_elapsed, avg_r, avg_g, avg_b)),
                asyncio.get_event_loop()
            )

            # Reseta os acumuladores e o contador de frames
            self.frame_count = 0
            self.r_accum = 0
            self.g_accum = 0
            self.b_accum = 0

            # Atualiza o contador de segundos
            self.seconds_elapsed += 1

        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Monitoramento de Valores Médios RGB")

# Função para limpar os dados
def reset_data():
    st.session_state.r_values.clear()
    st.session_state.g_values.clear()
    st.session_state.b_values.clear()
    st.session_state.timestamps.clear()

# Inicializa as listas para armazenar os dados
if 'r_values' not in st.session_state:
    st.session_state.r_values = deque(maxlen=N)
    st.session_state.g_values = deque(maxlen=N)
    st.session_state.b_values = deque(maxlen=N)
    st.session_state.timestamps = deque(maxlen=N)

# Organiza a interface em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Webcam")

    # Monitora o estado do webrtc para reinicializar os dados ao iniciar
    webrtc_ctx = webrtc_streamer(
        key="rgb-monitor",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    )

    # Resetar os dados quando o streaming começa
    if webrtc_ctx.state.playing:
        reset_data()

with col2:
    st.header("Gráfico")
    placeholder = st.empty()

    if webrtc_ctx.state.playing and webrtc_ctx.video_processor:
        last_render_time = time.time()  # Controle de renderização
        while True:
            try:
                # Tenta pegar os dados agregados por segundo
                result = webrtc_ctx.video_processor.result_queue.get_nowait()
                timestamp, avg_r, avg_g, avg_b = result
                st.session_state.timestamps.append(timestamp)
                st.session_state.r_values.append(avg_r)
                st.session_state.g_values.append(avg_g)
                st.session_state.b_values.append(avg_b)
            except asyncio.QueueEmpty:
                pass

            current_time = time.time()
            # Renderiza a cada 1 segundo
            if current_time - last_render_time >= 1:
                last_render_time = current_time

                if len(st.session_state.timestamps) > 0:
                    data_df = pd.DataFrame({
                        'Tempo': list(st.session_state.timestamps),
                        'R': list(st.session_state.r_values),
                        'G': list(st.session_state.g_values),
                        'B': list(st.session_state.b_values)
                    })

                    # Log para depuração
                    #print(f"Dados coletados: {data_df.tail(1)}")

                    fig, ax = plt.subplots()
                    ax.plot(data_df['Tempo'], data_df['R'], 'r-', label='R')
                    ax.plot(data_df['Tempo'], data_df['G'], 'g-', label='G')
                    ax.plot(data_df['Tempo'], data_df['B'], 'b-', label='B')
                    ax.legend(loc='upper right')
                    ax.set_xlabel('Tempo (s)')
                    ax.set_ylabel('Valor médio RGB')
                    ax.set_ylim(0, 255)
                    ax.set_xlim(left=max(0, data_df['Tempo'].iloc[-1] - 300), right=data_df['Tempo'].iloc[-1])  # Últimos 300 segundos
                    placeholder.pyplot(fig)
                    plt.close(fig)
                else:
                    placeholder.write("Aguardando dados...")

            # Pausa para evitar sobrecarga
            time.sleep(0.1)

# Função para gerar o arquivo Excel
def gerar_excel():
    data_df = pd.DataFrame({
        'Tempo (s)': list(st.session_state.timestamps),
        'R': list(st.session_state.r_values),
        'G': list(st.session_state.g_values),
        'B': list(st.session_state.b_values)
    })

    # Salvar o DataFrame em um arquivo Excel na memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data_df.to_excel(writer, index=False, sheet_name='Valores RGB')
    
    # Retornar o conteúdo do arquivo para ser baixado
    output.seek(0)
    return output

# Botão de download
if st.button('Salvar Dados em Excel'):
    excel_data = gerar_excel()
    st.download_button(
        label="Download Excel",
        data=excel_data,
        file_name="valores_rgb.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
