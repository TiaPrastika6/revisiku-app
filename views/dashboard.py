import streamlit as st

from utils import (
    hitung_statistik,
    cek_deadline,
    deadline_untuk_sorting,
    hitung_sisa_hari
)


def render_dashboard():
    catatan_list = st.session_state.catatan_list
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
        col1, col2 = st.columns([3, 1])

        with col1:
            st.caption("📘 Personal Academic Tracker")
            st.title("RevisiKu")
            st.write(
                "Tempat buat nyimpen tugas, revisi, bimbingan, dan deadline "
                "biar semuanya lebih rapi dan nggak numpuk di kepala."
            )
            st.write("📝 Catatan akademik  |  ⏰ Deadline tracker  |  ✅ Progress revisi")

        with col2:
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
        st.success("Tidak ada catatan yang deadline hari ini atau terlambat. Aman untuk sementara.")
    else:
        for catatan in fokus_hari_ini:
            with st.container(border=True):
                st.markdown(f"### {catatan.get('judul', '-')}")
                st.write(catatan.get("isi", "-"))
                st.write(f"**Kategori:** {catatan.get('kategori', '-')}")
                st.write(f"**Prioritas:** {catatan.get('prioritas', 'Sedang')}")
                st.write(f"**Deadline:** {catatan.get('deadline', '-')}")
                st.warning(cek_deadline(catatan.get("deadline", "")))

    st.divider()

    # =========================
    # BAGIAN BAWAH
    # =========================
    col_progress, col_deadline = st.columns([1, 1.4])

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
                        st.markdown(f"#### {catatan.get('judul', '-')}")
                        st.write(f"**Kategori:** {catatan.get('kategori', '-')}")
                        st.write(f"**Prioritas:** {catatan.get('prioritas', 'Sedang')}")
                        st.write(f"**Deadline:** {catatan.get('deadline', '-')}")
                        st.write(f"**Keterangan:** {cek_deadline(catatan.get('deadline', ''))}")