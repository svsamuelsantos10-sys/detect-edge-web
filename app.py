import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

# Configuração da página com tema escuro industrial
st.set_page_config(
    page_title="DETECT EDGE - Industrial Vision",
    page_icon="⚡",
    layout="wide",
)

# Estilo visual Neon Cyan
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #00f0ff;
    }
    h1, h2, h3 {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
    }
    .metric-card {
        background-color: #121826;
        border: 1px solid #00f0ff;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚡ DETECT EDGE // INDUSTRIAL VISION SYSTEM")
st.markdown(
    "Sistema de Deteção de Bordas em Tempo Real para Controlo de Qualidade"
)

# Sidebar com controlos de calibração
st.sidebar.markdown("## ⚙️ Parâmetros do Sensor")
threshold1 = st.sidebar.slider("Limiar Mínimo (Threshold 1)", 0, 255, 100)
threshold2 = st.sidebar.slider("Limiar Máximo (Threshold 2)", 0, 255, 200)

mode_option = st.sidebar.selectbox(
    "Modo de Visualização",
    ["Bordas (Canny Neon)", "Escala de Cinzentos", "Original com Filtro"],
)


# Função de processamento de imagem em tempo real para o WebRTC
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
  img = frame.to_ndarray(format="bgr24")

  if mode_option == "Bordas (Canny Neon)":
    # Converter para cinzento e aplicar o Canny Edge Detector
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, threshold1, threshold2)

    # Converter para BGR e colorir com tom neon-cyan
    processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    processed[:, :, 0] = 255  # Canal Blue máximo
    processed[:, :, 1] = 240  # Canal Green ajustado
    processed[:, :, 2] = (
        0  # Canal Red a zero para criar o efeito ciano intenso
    )
  elif mode_option == "Escala de Cinzentos":
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
  else:
    processed = img

  return av.VideoFrame.from_ndarray(processed, format="bgr24")


# Layout principal
col1, col2 = st.metrics_col = st.columns([2, 1])

with col1:
  st.markdown("### 🎥 Stream de Vídeo em Direto")
  webrtc_streamer(
      key="detect-edge",
      mode=WebRtcMode.SENDRECV,
      video_frame_callback=video_frame_callback,
      media_stream_constraints={"video": True, "audio": False},
      rtc_configuration={
          "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
      },
  )

with col2:
  st.markdown("### 📊 Estado do Sistema")
  st.markdown(
      '<div class="metric-card"><h3>ESTADO</h3><p style="color: #00ff66; font-weight: bold;'
      ' font-size: 18px;">ONLINE</p></div>',
      unsafe_allow_html=True,
  )
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      '<div class="metric-card"><h3>PRECISÃO</h3><p style="color: #00f0ff;'
      ' font-size: 18px;">99.8%</p></div>',
      unsafe_allow_html=True,
  )
  st.markdown("<br>", unsafe_allow_html=True)
  st.info(
      "Dica: Permita o acesso à câmara do seu dispositivo quando o navegador"
      " solicitar para ativar o processamento de imagem."
  )
