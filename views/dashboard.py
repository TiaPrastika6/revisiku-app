import streamlit as st

from utils import (
    hitung_statistik,
    cek_deadline,
    deadline_untuk_sorting,
    hitung_sisa_hari
)


def potong_teks(teks, batas=170):
    teks = str(teks or "")
    if len(teks) <= batas:
        return teks
    return teks[:batas].rstrip() + "..."


def buka_detail(index):
    st.session_state.selected_catatan_index = index
    st.session_state.halaman = "Detail Catatan"
    st.rerun()


def render_kartu_deadline(index, catatan, label_tombol):
    with st.container(border=True):
        st.markdown(f"### {catatan.get('judul', '-')}")
        st.write(potong_teks(catatan.get("isi", "-"), 180))

        if catatan.get("mata_kuliah"):
            st.caption(f"📚 Mata Kuliah: {catatan.get('mata_kuliah')}")

        if catatan.get("nama_dosen"):
            st.caption(f"👩‍🏫 Nama Dosen: {catatan.get('nama_dosen')}")

        st.caption(
            f"📂 {catatan.get('kategori', '-')} | "
            f"⭐ {catatan.get('prioritas', 'Sedang')} | "
            f"📌 {catatan.get('status', '-')}"
        )

        st.write(f"**Deadline:** {catatan.get('deadline', '-')}")
        st.caption(cek_deadline(catatan.get("deadline", "")))

        if st.button(
            label_tombol,
            key=f"dashboard_detail_{label_tombol}_{index}",
            use_container_width=True
        ):
            buka_detail(index)

def render_empty_deadline(icon, judul, pesan):
    with st.container(border=True):
        st.markdown(f"### {icon} {judul}")
        st.success(pesan)


def render_deadline_summary(jumlah_telat, jumlah_hari_ini, jumlah_h3):
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("🚨 Terlambat")
            st.metric("Catatan", jumlah_telat)
            st.caption("Catatan yang sudah melewati deadline.")

    with col2:
        with st.container(border=True):
            st.subheader("🔥 Hari Ini")
            st.metric("Catatan", jumlah_hari_ini)
            st.caption("Catatan yang harus diperhatikan hari ini.")

    with col3:
        with st.container(border=True):
            st.subheader("⏳ H-3")
            st.metric("Catatan", jumlah_h3)
            st.caption("Catatan dengan deadline 1–3 hari lagi.")

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

    # Catatan arsip tidak dihitung di dashboard utama
    catatan_list = [
        catatan for catatan in st.session_state.catatan_list
        if not catatan.get("arsip", False)
    ]

    total, belum, proses, selesai, terlambat = hitung_statistik(catatan_list)

    progress = 0
    if total > 0:
        progress = round((selesai / total) * 100)

    # Ambil catatan aktif beserta index aslinya
    catatan_aktif = []

    for index, catatan in enumerate(st.session_state.catatan_list):
        if catatan.get("arsip", False):
            continue

        if catatan.get("status") == "Selesai":
            continue

        catatan_aktif.append((index, catatan))

    catatan_aktif.sort(
        key=lambda item: deadline_untuk_sorting(item[1].get("deadline", ""))
    )

    deadline_terlambat = []
    deadline_hari_ini = []
    deadline_h3 = []

    for index, catatan in catatan_aktif:
        sisa_hari = hitung_sisa_hari(catatan.get("deadline", ""))

        if sisa_hari is None:
            continue

        if sisa_hari < 0:
            deadline_terlambat.append((index, catatan))
        elif sisa_hari == 0:
            deadline_hari_ini.append((index, catatan))
        elif 1 <= sisa_hari <= 3:
            deadline_h3.append((index, catatan))

    jumlah_fokus = (
        len(deadline_terlambat)
        + len(deadline_hari_ini)
        + len(deadline_h3)
    )

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
            st.subheader("Fokus Deadline")
            st.metric("Perlu Dipantau", jumlah_fokus)
            st.caption("Catatan terlambat, deadline hari ini, dan deadline H-3.")

    st.write("")

    # =========================
    # STATISTIK
    # =========================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("📚 Total", total)
    col2.metric("🕒 Belum", belum)
    col3.metric("🔧 Proses", proses)
    col4.metric("✅ Selesai", selesai)
    col5.metric("🚨 Terlambat", len(deadline_terlambat))

    st.divider()

    # =========================
    # REMINDER DEADLINE
    # =========================
    st.subheader("🚨 Reminder Deadline")
    st.caption(
        "Ringkasan catatan yang perlu kamu perhatikan berdasarkan jarak deadline."
    )

    render_deadline_summary(
        len(deadline_terlambat),
        len(deadline_hari_ini),
        len(deadline_h3)
    )

    st.write("")

    if jumlah_fokus == 0:
        with st.container(border=True):
            st.subheader("✅ Semua aman")
            st.write(
                "Belum ada catatan yang terlambat, deadline hari ini, atau deadline H-3."
            )
            st.caption("Kamu bisa lanjut mengerjakan catatan lain yang deadline-nya lebih jauh.")
    else:
        tab_telat, tab_hari_ini, tab_h3 = st.tabs([
            f"🚨 Terlambat ({len(deadline_terlambat)})",
            f"🔥 Hari Ini ({len(deadline_hari_ini)})",
            f"⏳ H-3 ({len(deadline_h3)})"
        ])

        with tab_telat:
            if len(deadline_terlambat) == 0:
                render_empty_deadline(
                    "✅",
                    "Tidak ada yang terlambat",
                    "Semua catatan masih aman dari keterlambatan."
                )
            else:
                cols = st.columns(2)
                for posisi, (index, catatan) in enumerate(deadline_terlambat):
                    with cols[posisi % 2]:
                        render_kartu_deadline(index, catatan, "Buka Detail")

        with tab_hari_ini:
            if len(deadline_hari_ini) == 0:
                render_empty_deadline(
                    "🌿",
                    "Tidak ada deadline hari ini",
                    "Hari ini tidak ada catatan yang harus diselesaikan tepat hari ini."
                )
            else:
                cols = st.columns(2)
                for posisi, (index, catatan) in enumerate(deadline_hari_ini):
                    with cols[posisi % 2]:
                        render_kartu_deadline(index, catatan, "Buka Detail")

        with tab_h3:
            if len(deadline_h3) == 0:
                render_empty_deadline(
                    "🕊️",
                    "Tidak ada deadline H-3",
                    "Tidak ada catatan dengan deadline 1–3 hari lagi."
                )
            else:
                cols = st.columns(2)
                for posisi, (index, catatan) in enumerate(deadline_h3):
                    with cols[posisi % 2]:
                        render_kartu_deadline(index, catatan, "Buka Detail")

    # =========================
    # BAGIAN BAWAH
    # =========================
    col_progress, col_deadline = st.columns([1, 1.5], gap="large")

    with col_progress:
        with st.container(border=True):
            st.subheader("📈 Progress Pengerjaan")
            st.caption("Persentase catatan aktif yang sudah ditandai selesai.")

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
                for index, catatan in catatan_aktif[:4]:
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
                            st.write("**Deadline:**")
                            st.write(catatan.get("deadline", "-"))
                            st.caption(cek_deadline(catatan.get("deadline", "")))

                            if st.button(
                                "Detail",
                                key=f"deadline_terdekat_{index}",
                                use_container_width=True
                            ):
                                buka_detail(index)