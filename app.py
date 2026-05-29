import streamlit as st

from data import init_session
from styles import load_css
from views.dashboard import render_dashboard
from views.tambah_catatan import render_tambah_catatan
from views.daftar_catatan import render_daftar_catatan
from views.detail_catatan import render_detail_catatan
from views.backup_data import render_backup_data
from views.kalender_deadline import render_kalender_deadline
from views.pencarian_global import render_pencarian_global
from views.arsip_catatan import render_arsip_catatan


st.set_page_config(
    page_title="RevisiKu",
    page_icon="📘",
    layout="wide"
)

load_css()
init_session()


# =========================
# SESSION HALAMAN
# =========================
if "halaman" not in st.session_state:
    st.session_state.halaman = "Dashboard"


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 📘 RevisiKu")
    st.caption("Academic Notes Tracker")

    st.divider()

    st.markdown("#### Menu")

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.halaman = "Dashboard"
        st.rerun()

    if st.button("➕ Tambah Catatan", use_container_width=True):
        st.session_state.halaman = "Tambah Catatan"
        st.rerun()

    if st.button("📋 Daftar Catatan", use_container_width=True):
        st.session_state.halaman = "Daftar Catatan"
        st.rerun()

    if st.button("🗃️ Arsip Catatan", use_container_width=True):
        st.session_state.halaman = "Arsip Catatan"
        st.rerun()

    if st.button("🔍 Cari Catatan", use_container_width=True):
        st.session_state.halaman = "Cari Catatan"
        st.rerun()

    if st.button("📅 Kalender Deadline", use_container_width=True):
        st.session_state.halaman = "Kalender Deadline"
        st.rerun()

    if st.button("💾 Backup Data", use_container_width=True):
        st.session_state.halaman = "Backup Data"
        st.rerun()

    st.divider()

    st.caption(
        "Catat tugas, revisi, bimbingan, dan deadline dalam satu tempat."
    )


# =========================
# ROUTING HALAMAN
# =========================
if st.session_state.halaman == "Dashboard":
    render_dashboard()

elif st.session_state.halaman == "Tambah Catatan":
    render_tambah_catatan()

elif st.session_state.halaman == "Daftar Catatan":
    render_daftar_catatan()

elif st.session_state.halaman == "Arsip Catatan":
    render_arsip_catatan()

elif st.session_state.halaman == "Cari Catatan":
    render_pencarian_global()

elif st.session_state.halaman == "Detail Catatan":
    render_detail_catatan()

elif st.session_state.halaman == "Kalender Deadline":
    render_kalender_deadline()

elif st.session_state.halaman == "Backup Data":
    render_backup_data()