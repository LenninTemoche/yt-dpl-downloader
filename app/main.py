import streamlit as st
import os
import time
import pandas as pd
from app.core.downloader import Downloader
from app.data.history_manager import HistoryManager

# ──────────────────────────────────────────────
# Configuración de página
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="yt-dpl Downloader",
    page_icon="⬇️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CSS Futurista (Replicando Stitch Design)
# ──────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    /* ═══ Global Reset ═══ */
    *, *::before, *::after { font-family: 'Inter', sans-serif !important; }

    /* ═══ Background ═══ */
    .stApp {
        background-color: #0f172a !important;
        background-image: 
            radial-gradient(ellipse at top right, rgba(34,211,238,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at bottom left, rgba(168,85,247,0.05) 0%, transparent 50%) !important;
    }

    /* ═══ Scrollbar ═══ */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* ═══ Sidebar ═══ */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #94a3b8 !important;
    }

    /* ═══ Glass Card ═══ */
    .glass-card {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 16px !important;
    }

    /* ═══ Header Titles ═══ */
    h1 { color: #ffffff !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
    h2 { color: #22d3ee !important; font-size: 13px !important; font-weight: 600 !important; 
         text-transform: uppercase !important; letter-spacing: 1.5px !important; }
    h3 { color: #e2e8f0 !important; }
    p, span, label, .stMarkdown { color: #94a3b8 !important; }

    /* ═══ Section Headers ═══ */
    .section-cyan { color: #22d3ee !important; font-size: 12px !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 2px !important; margin-bottom: 16px !important; }
    .section-purple { color: #a855f7 !important; font-size: 12px !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 2px !important; margin-bottom: 16px !important; }

    /* ═══ Input Fields ═══ */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        color: #e2e8f0 !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #22d3ee !important;
        box-shadow: 0 0 0 2px rgba(34,211,238,0.25) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #475569 !important; }

    /* ═══ Select Box ═══ */
    .stSelectbox > div > div {
        background: rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(71,85,105,0.5) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    .stSelectbox label { color: #cbd5e1 !important; font-weight: 500 !important; font-size: 14px !important; }

    /* ═══ Download Button (Gradient Cyan → Purple + Glow) ═══ */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #22d3ee 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 0 20px -5px rgba(168,85,247,0.5) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 0 30px -5px rgba(168,85,247,0.7) !important;
        transform: translateY(-1px) !important;
    }

    /* ═══ Progress Bar ═══ */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22d3ee 0%, #a855f7 100%) !important;
        border-radius: 999px !important;
        box-shadow: 0 0 10px rgba(34,211,238,0.5) !important;
    }
    .stProgress > div > div > div {
        background: rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 999px !important;
    }

    /* ═══ AI Suite Card ═══ */
    .ai-suite-card {
        position: relative;
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 24px !important;
        padding: 40px !important;
        text-align: center !important;
        box-shadow: 0 0 30px -10px rgba(168,85,247,0.2) !important;
    }
    .ai-badge {
        display: inline-block;
        background: rgba(168,85,247,0.2);
        color: #a855f7;
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 999px;
        padding: 6px 16px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .ai-icon-box {
        background: rgba(30,41,59,0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        transition: all 0.3s;
    }

    /* ═══ History Table ═══ */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
    }

    /* ═══ Sidebar Nav Items ═══ */
    .nav-item {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 16px; border-radius: 12px;
        color: #94a3b8; text-decoration: none;
        transition: all 0.2s; margin-bottom: 4px;
        font-weight: 500; font-size: 14px;
    }
    .nav-item:hover { background: rgba(255,255,255,0.05); color: #ffffff; }
    .nav-active {
        background: rgba(14,165,233,0.1) !important;
        color: #22d3ee !important;
        border: 1px solid rgba(14,165,233,0.2);
        box-shadow: 0 0 15px -2px rgba(34,211,238,0.4);
    }
    .nav-disabled {
        color: #334155 !important; cursor: not-allowed;
    }
    .coming-soon-badge {
        background: rgba(30,41,59,0.5); color: #475569;
        font-size: 9px; padding: 2px 8px; border-radius: 4px;
        font-weight: 700; letter-spacing: 1px; margin-left: auto;
    }

    /* ═══ User Avatar ═══ */
    .user-card {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 16px; background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
    }
    .avatar {
        width: 36px; height: 36px; border-radius: 8px;
        background: linear-gradient(135deg, #22d3ee, #a855f7);
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 13px; color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* ═══ Status Badges ═══ */
    .badge-completed {
        background: rgba(132,204,22,0.1); color: #84cc16;
        border: 1px solid rgba(132,204,22,0.2);
        padding: 4px 10px; border-radius: 6px;
        font-size: 10px; font-weight: 700;
        box-shadow: 0 0 10px rgba(132,204,22,0.1);
    }
    .badge-failed {
        background: rgba(244,63,94,0.1); color: #f43f5e;
        border: 1px solid rgba(244,63,94,0.2);
        padding: 4px 10px; border-radius: 6px;
        font-size: 10px; font-weight: 700;
    }

    /* ═══ Download Path Display ═══ */
    .path-display {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(71,85,105,0.5);
        border-radius: 12px;
        padding: 10px 16px;
        color: #94a3b8;
        font-size: 13px;
        font-family: 'Inter', monospace !important;
    }

    /* ═══ Dividers ═══ */
    hr { border-color: rgba(255,255,255,0.05) !important; }

    /* ═══ Hide Streamlit Branding ═══ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Inicialización de servicios
# ──────────────────────────────────────────────
DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "descargas")

if 'download_path' not in st.session_state:
    st.session_state.download_path = DEFAULT_DOWNLOAD_PATH
if 'downloader' not in st.session_state:
    st.session_state.downloader = Downloader(output_path=st.session_state.download_path)
if 'history' not in st.session_state:
    st.session_state.history = HistoryManager()

# ──────────────────────────────────────────────
# SIDEBAR (Navegación Futurista)
# ──────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; padding:8px 0 24px 0;">
        <span style="font-size:28px;">⬇️</span>
        <span style="font-size:20px; font-weight:700; color:#ffffff; letter-spacing:-0.5px;">yt-dpl Downloader</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegación
    st.markdown("""
    <div class="nav-item nav-active">📥 Download</div>
    <div class="nav-item">📋 History</div>
    <div class="nav-item">⚙️ Settings</div>
    <div style="padding:24px 0 8px 16px;">
        <span style="font-size:10px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:2px;">Advanced</span>
    </div>
    <div class="nav-item nav-disabled">
        ✨ AI Services
        <span class="coming-soon-badge">COMING SOON</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>" * 2, unsafe_allow_html=True)

    # Ruta de descarga (editable)
    st.markdown('<span style="font-size:10px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:2px;">📂 Download Path</span>', unsafe_allow_html=True)
    new_path = st.text_input("Ruta de descarga", value=st.session_state.download_path, label_visibility="collapsed", key="path_input")
    if new_path != st.session_state.download_path:
        st.session_state.download_path = new_path
        st.session_state.downloader = Downloader(output_path=new_path)

    # Avatar / Proyecto
    st.markdown("""
    <div class="user-card">
        <div class="avatar">YT</div>
        <div>
            <div style="font-size:14px; font-weight:600; color:#ffffff;">yt-dpl Downloader</div>
            <div style="font-size:12px; color:#94a3b8;">V0.2 · Etapa 1</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────

# Header
st.markdown("""
<h1 style="font-size:36px; margin-bottom:4px;">Video Downloader</h1>
<p style="color:#94a3b8; font-size:15px; margin-top:0;">Paste a link and choose your preferred quality settings.</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# URL Input
url = st.text_input("URL del video", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── Grid: Options + Status ──
col_opts, col_status = st.columns(2, gap="large")

with col_opts:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-cyan">⚡ Options</div>', unsafe_allow_html=True)
    
    # Format Toggle
    mode = st.selectbox("Format", ["Video (MP4)", "Audio (MP3)"])
    
    # Quality
    quality = st.selectbox("Quality", ["720", "1080", "360"], index=0,
                          format_func=lambda x: f"{x}p (HD)" if x == "720" else f"{x}p (Full HD)" if x == "1080" else f"{x}p (SD)")
    
    # Output Path
    st.markdown(f"""
    <div style="margin-top:8px;">
        <label style="font-size:14px; font-weight:500; color:#cbd5e1 !important; margin-bottom:8px; display:block;">Output Path</label>
        <div class="path-display">📁 {st.session_state.download_path}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_status:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-purple">📡 Status</div>', unsafe_allow_html=True)
    
    # Download Button
    btn_dl = st.button("⬇️  Download Now")
    
    # Placeholder para progreso
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LÓGICA DE DESCARGA
# ──────────────────────────────────────────────
if btn_dl:
    if not url:
        status_placeholder.error("⚠️ Please enter a valid URL.")
    else:
        with status_placeholder.container():
            st.markdown('<p style="color:#cbd5e1 !important; font-style:italic;">🔍 Fetching video info...</p>', unsafe_allow_html=True)
        
        info = st.session_state.downloader.get_video_info(url)
        
        if "error" in info:
            status_placeholder.error(f"Error: {info['error']}")
        else:
            title = info.get('title', 'Video_descargado')
            
            with status_placeholder.container():
                st.markdown(f'<p style="color:#cbd5e1 !important; font-style:italic; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Downloading: {title[:50]}...</p>', unsafe_allow_html=True)
            
            progress_bar = progress_placeholder.progress(0, text="Starting...")
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    p = d.get('_percent_str', '0%').replace('%', '').strip()
                    try:
                        val = min(float(p) / 100, 1.0)
                        progress_bar.progress(val, text=f"⚡ Downloading: {p}%")
                    except:
                        pass
                elif d['status'] == 'finished':
                    progress_bar.progress(1.0, text="✅ Download complete. Merging files...")

            mode_clean = "audio" if "MP3" in mode else "video"
            result = st.session_state.downloader.download(
                url,
                mode=mode_clean,
                quality=quality,
                output_path=st.session_state.download_path,
                progress_hook=progress_hook
            )
            
            if result.get("success"):
                st.session_state.history.add_entry(title, url, mode_clean, quality)
                status_placeholder.success(f"✅ Saved to: {st.session_state.download_path}")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                status_placeholder.error(f"❌ Error: {result.get('error')}")

# ──────────────────────────────────────────────
# AI INTELLIGENCE SUITE (Etapa 2 Teaser)
# ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="ai-suite-card">
    <span class="ai-badge">Future Roadmap</span>
    <h3 style="font-size:28px; font-weight:700; color:#ffffff !important; margin:16px 0 8px 0;">AI Intelligence Suite</h3>
    <p style="color:#94a3b8; max-width:500px; margin:0 auto 32px auto; font-size:15px;">
        Automate your workflow with integrated AI post-processing tools currently in development.
    </p>
    <div style="display:flex; justify-content:center; gap:48px; flex-wrap:wrap;">
        <div style="text-align:center;">
            <div class="ai-icon-box">🌐</div>
            <div style="font-size:10px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:2px; margin-top:8px;">Transcription</div>
        </div>
        <div style="text-align:center;">
            <div class="ai-icon-box">📄</div>
            <div style="font-size:10px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:2px; margin-top:8px;">AI Summary</div>
        </div>
        <div style="text-align:center;">
            <div class="ai-icon-box">💬</div>
            <div style="font-size:10px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:2px; margin-top:8px;">Chat with Video</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# HISTORIAL DE DESCARGAS (Tabla Futurista)
# ──────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; padding:0 4px;">
    <span style="font-size:16px; font-weight:700; color:#ffffff;">Recent Downloads</span>
</div>
""", unsafe_allow_html=True)

history_data = st.session_state.history.get_history()

if history_data:
    df = pd.DataFrame(history_data)
    df = df.rename(columns={
        "title": "Video Title",
        "mode": "Format",
        "quality": "Quality",
        "date": "Date"
    })
    # Formatear columnas
    df["Format"] = df["Format"].apply(lambda x: "MP4" if x == "video" else "MP3")
    df["Quality"] = df["Quality"].apply(lambda x: f"{x}p" if x != "MP3" else "320kbps")
    df["Status"] = "✅ COMPLETED"
    
    # Mostrar solo columnas relevantes
    display_df = df[["Video Title", "Format", "Quality", "Date", "Status"]]
    
    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Video Title": st.column_config.TextColumn("Video Title", width="large"),
            "Format": st.column_config.TextColumn("Format", width="small"),
            "Quality": st.column_config.TextColumn("Quality", width="small"),
            "Date": st.column_config.TextColumn("Date", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
        }
    )
else:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:40px !important;">
        <p style="color:#475569 !important; font-size:14px;">No downloads yet. Paste a URL above to get started.</p>
    </div>
    """, unsafe_allow_html=True)
