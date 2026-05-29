import streamlit as st
import calendar
from datetime import date, datetime

from utils import cek_deadline


NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]


def potong_teks(teks, batas=55):
    teks = str(teks or "")
    if len(teks) <= batas:
        return teks
    return teks[:batas].rstrip() + "..."


def ambil_catatan_pada_tanggal(catatan_list, tanggal_target):
    hasil = []

    for index, catatan in enumerate(catatan_list):
        deadline = catatan.get("deadline", "")

        try:
            tanggal_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except:
            continue

        if tanggal_deadline == tanggal_target:
            hasil.append((index, catatan))

    return hasil


def label_status(status):
    if status == "Selesai":
        return "✅"
    elif status == "Proses":
        return "🔧"
    return "🕒"


def label_prioritas(prioritas):
    if prioritas == "Tinggi":
        return "🔴"
    elif prioritas == "Sedang":
        return "🟡"
    return "🟢"


def render_kalender_deadline():
    st.title("📅 Kalender Deadline")
    st.write(
        "Lihat catatan berdasarkan tanggal deadline agar lebih mudah memantau tugas, revisi, "
        "bimbingan, dan praktikum."
    )

    st.divider()

    hari_ini = date.today()

    col_bulan, col_tahun = st.columns(2)

    with col_bulan:
        bulan = st.selectbox(
            "Bulan",
            list(range(1, 13)),
            index=hari_ini.month - 1,
            format_func=lambda x: NAMA_BULAN[x - 1]
        )

    with col_tahun:
        tahun = st.number_input(
            "Tahun",
            min_value=2020,
            max_value=2100,
            value=hari_ini.year,
            step=1
        )

    tahun = int(tahun)

    st.divider()

    catatan_list = st.session_state.catatan_list

    total_bulan_ini = 0
    selesai_bulan_ini = 0
    belum_bulan_ini = 0

    for catatan in catatan_list:
        try:
            tanggal_deadline = datetime.strptime(
                catatan.get("deadline", ""),
                "%Y-%m-%d"
            ).date()
        except:
            continue

        if tanggal_deadline.month == bulan and tanggal_deadline.year == tahun:
            total_bulan_ini += 1

            if catatan.get("status") == "Selesai":
                selesai_bulan_ini += 1
            else:
                belum_bulan_ini += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bulan Ini", total_bulan_ini)
    col2.metric("Belum/Proses", belum_bulan_ini)
    col3.metric("Selesai", selesai_bulan_ini)

    st.divider()

    st.subheader(f"{NAMA_BULAN[bulan - 1]} {tahun}")

    nama_hari = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    header_cols = st.columns(7)

    for i, nama in enumerate(nama_hari):
        header_cols[i].markdown(f"**{nama}**")

    kalender = calendar.monthcalendar(tahun, bulan)

    for minggu in kalender:
        cols = st.columns(7)

        for i, nomor_hari in enumerate(minggu):
            with cols[i]:
                if nomor_hari == 0:
                    st.write("")
                    continue

                tanggal_ini = date(tahun, bulan, nomor_hari)
                catatan_hari_ini = ambil_catatan_pada_tanggal(
                    catatan_list,
                    tanggal_ini
                )

                if tanggal_ini == hari_ini:
                    st.info(f"**{nomor_hari}**\n\nHari ini")
                elif len(catatan_hari_ini) > 0:
                    st.warning(f"**{nomor_hari}**\n\n{len(catatan_hari_ini)} catatan")
                else:
                    st.caption(f"**{nomor_hari}**")

                for index, catatan in catatan_hari_ini[:2]:
                    status = label_status(catatan.get("status", "Belum dikerjakan"))
                    prioritas = label_prioritas(catatan.get("prioritas", "Sedang"))

                    st.caption(
                        f"{status} {prioritas} "
                        f"{potong_teks(catatan.get('judul', '-'))}"
                    )

                    if st.button(
                        "Detail",
                        key=f"kalender_detail_{index}_{tanggal_ini}",
                        use_container_width=True
                    ):
                        st.session_state.selected_catatan_index = index
                        st.session_state.halaman = "Detail Catatan"
                        st.rerun()

                if len(catatan_hari_ini) > 2:
                    st.caption(f"+{len(catatan_hari_ini) - 2} lainnya")

    st.divider()

    st.subheader("📌 Daftar Deadline Bulan Ini")

    data_bulan_ini = []

    for index, catatan in enumerate(catatan_list):
        try:
            tanggal_deadline = datetime.strptime(
                catatan.get("deadline", ""),
                "%Y-%m-%d"
            ).date()
        except:
            continue

        if tanggal_deadline.month == bulan and tanggal_deadline.year == tahun:
            data_bulan_ini.append((index, tanggal_deadline, catatan))

    data_bulan_ini.sort(key=lambda x: x[1])

    if len(data_bulan_ini) == 0:
        st.info("Tidak ada deadline pada bulan ini.")
    else:
        for index, tanggal_deadline, catatan in data_bulan_ini:
            with st.container(border=True):
                col_info, col_aksi = st.columns([3, 1])

                with col_info:
                    st.markdown(f"### {catatan.get('judul', '-')}")
                    st.caption(
                        f"📅 {tanggal_deadline} | "
                        f"{catatan.get('kategori', '-')} | "
                        f"Prioritas: {catatan.get('prioritas', 'Sedang')} | "
                        f"Status: {catatan.get('status', '-')}"
                    )
                    st.write(cek_deadline(str(tanggal_deadline)))

                with col_aksi:
                    if st.button(
                        "Buka Detail",
                        key=f"list_kalender_detail_{index}",
                        use_container_width=True
                    ):
                        st.session_state.selected_catatan_index = index
                        st.session_state.halaman = "Detail Catatan"
                        st.rerun()