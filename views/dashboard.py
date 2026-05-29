import streamlit as st

from utils import (
    hitung_statistik,
    cek_deadline,
    deadline_untuk_sorting,
    hitung_sisa_hari
)


def potong_teks(teks, batas=180):
    teks = str(teks or "")
    if len(teks) <= batas:
        return teks
    return teks[:batas].rstrip() + "..."


def render_dashboard():
    # =========================
    # STYLE KHUSUS DASHBOARD
    # =========================
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2.5rem !important;
        }

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.16);
            padding: 18px;
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    catatan_list = [
        catatan for catatan in st.session_state.catatan_list
        if not catatan.get("arsip", False)
    ]
    total, belum, proses, selesai, terlambat = hitung_statistik(catatan_list)

    progress = 0
    if total > 0:
        progress = round((selesai / total) * 100)

    catatan_aktif = [
        catatan for catatan in catatan_list
        if catatan.get("status") != "Selesai"
    ]

    catatan_aktif.sort(
        key=lambda catatan: deadline_untuk_sorting(catatan.get("deadline", ""))
    )

    fokus_hari_ini = []

    for catatan in catatan_aktif:
        sisa_hari = hitung_sisa_hari(catatan.get("deadline", ""))

        if sisa_hari is not None and sisa_hari <= 0:
            fokus_hari_ini.append(catatan)

    # =========================
    # HERO DASHBOARD
    # =========================
    with st.container(border=True):
        col_hero, col_focus = st.columns([3, 1.1], gap="large")

        with col_hero:
            st.caption("📘 Personal Academic Tracker")
            st.title("RevisiKu")
            st.write(
                "Tempat buat nyimpen tugas, revisi, bimbingan, dan deadline "
                "biar semuanya lebih rapi dan nggak numpuk di kepala."
            )

            col_chip1, col_chip2, col_chip3 = st.columns(3)

            with col_chip1:
                st.info("📝 Catatan akademik")

            with col_chip2:
                st.info("⏰ Deadline tracker")

            with col_chip3:
                st.info("✅ Progress revisi")

        with col_focus:
            st.subheader("Fokus Hari Ini")
            st.metric("Perlu Dikerjakan", len(fokus_hari_ini))
            st.caption("Catatan yang deadline hari ini atau sudah terlambat.")

    st.write("")

    # =========================
    # STATISTIK
    # =========================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📚 Total", total)
    col2.metric("🕒 Belum", belum)
    col3.metric("🔧 Proses", proses)
    col4.metric("✅ Selesai", selesai)
    col5.metric("🚨 Terlambat", terlambat)

    st.divider()

    # =========================
    # FOKUS HARI INI
    # =========================
    st.subheader("🔥 Fokus Hari Ini")

    if len(fokus_hari_ini) == 0:
        st.success(
            "Tidak ada catatan yang deadline hari ini atau terlambat. "
            "Aman untuk sementara."
        )
    else:
        for catatan in fokus_hari_ini:
            with st.container(border=True):
                col_info, col_deadline = st.columns([3, 1])

                with col_info:
                    st.markdown(f"### {catatan.get('judul', '-')}")
                    st.write(potong_teks(catatan.get("isi", "-"), 260))
                    st.caption(
                        f"Kategori: {catatan.get('kategori', '-')} | "
                        f"Prioritas: {catatan.get('prioritas', 'Sedang')}"
                    )

                with col_deadline:
                    st.warning(cek_deadline(catatan.get("deadline", "")))

    st.divider()

    # =========================
    # BAGIAN BAWAH
    # =========================
    col_progress, col_deadline = st.columns([1, 1.5], gap="large")

    with col_progress:
        with st.container(border=True):
            st.subheader("📈 Progress Pengerjaan")
            st.caption("Persentase catatan yang sudah ditandai selesai.")

            st.metric("Progress", f"{progress}%")
            st.progress(progress / 100)

            st.write(f"{selesai} dari {total} catatan sudah selesai.")

    with col_deadline:
        with st.container(border=True):
            st.subheader("⏳ Deadline Terdekat")
            st.caption("Catatan aktif yang perlu kamu perhatikan duluan.")

            if len(catatan_aktif) == 0:
                st.info(
                    "Belum ada catatan aktif. Buka halaman Tambah Catatan "
                    "buat mulai nyatet tugas atau revisi baru."
                )
            else:
                for catatan in catatan_aktif[:4]:
                    with st.container(border=True):
                        col_teks, col_status = st.columns([3, 1])

                        with col_teks:
                            st.markdown(f"#### {catatan.get('judul', '-')}")
                            st.write(potong_teks(catatan.get("isi", "-"), 220))
                            st.caption(
                                f"Kategori: {catatan.get('kategori', '-')} | "
                                f"Prioritas: {catatan.get('prioritas', 'Sedang')}"
                            )

                        with col_status:
                            st.write(f"**Deadline:**")
                            st.write(catatan.get("deadline", "-"))
                            st.caption(cek_deadline(catatan.get("deadline", "")))