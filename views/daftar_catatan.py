import streamlit as st

from utils import (
    STATUS_LIST,
    KATEGORI_LIST,
    PRIORITAS_LIST,
    cek_deadline,
    deadline_untuk_sorting
)


def label_prioritas(prioritas):
    if prioritas == "Tinggi":
        return "🔴 Tinggi"
    elif prioritas == "Sedang":
        return "🟡 Sedang"
    return "🟢 Rendah"


def label_status(status):
    if status == "Selesai":
        return "✅ Selesai"
    elif status == "Proses":
        return "🔧 Proses"
    return "🕒 Belum dikerjakan"


def potong_teks(teks, batas=220):
    if len(teks) <= batas:
        return teks
    return teks[:batas].rstrip() + "..."


def render_daftar_catatan():
    st.title("📋 Daftar Catatan")
    st.write(
        "Lihat semua catatan dalam bentuk ringkas. "
        "Klik tombol detail untuk membaca isi lengkap atau mengedit catatan."
    )

    st.divider()

    # =========================
    # FILTER
    # =========================
    with st.container(border=True):
        st.subheader("🔎 Filter Catatan")

        col1, col2, col3 = st.columns(3)

        with col1:
            filter_kategori = st.selectbox(
                "Kategori",
                ["Semua"] + KATEGORI_LIST
            )

        with col2:
            filter_status = st.selectbox(
                "Status",
                ["Semua"] + STATUS_LIST
            )

        with col3:
            filter_prioritas = st.selectbox(
                "Prioritas",
                ["Semua"] + PRIORITAS_LIST
            )

        col4, col5 = st.columns([2, 1])

        with col4:
            keyword = st.text_input(
                "Cari catatan",
                placeholder="Cari berdasarkan judul atau isi..."
            )

        with col5:
            urutkan = st.selectbox(
                "Urutkan",
                ["Deadline terdekat", "Deadline terlama", "Terbaru ditambahkan"]
            )

    st.divider()

    # =========================
    # FILTER DATA
    # =========================
    data_tampil = []

    for index, catatan in enumerate(st.session_state.catatan_list):
        cocok_kategori = (
            filter_kategori == "Semua"
            or catatan.get("kategori") == filter_kategori
        )

        cocok_status = (
            filter_status == "Semua"
            or catatan.get("status") == filter_status
        )

        cocok_prioritas = (
            filter_prioritas == "Semua"
            or catatan.get("prioritas", "Sedang") == filter_prioritas
        )

        teks = f"{catatan.get('judul', '')} {catatan.get('isi', '')}".lower()
        cocok_keyword = keyword.lower() in teks

        if cocok_kategori and cocok_status and cocok_prioritas and cocok_keyword:
            data_tampil.append((index, catatan))

    if urutkan == "Deadline terdekat":
        data_tampil.sort(
            key=lambda x: deadline_untuk_sorting(x[1].get("deadline", ""))
        )
    elif urutkan == "Deadline terlama":
        data_tampil.sort(
            key=lambda x: deadline_untuk_sorting(x[1].get("deadline", "")),
            reverse=True
        )
    else:
        data_tampil.reverse()

    # =========================
    # TAMPILKAN DATA
    # =========================
    if len(data_tampil) == 0:
        st.info("Belum ada catatan yang sesuai.")
        return

    st.subheader(f"📌 {len(data_tampil)} Catatan Ditemukan")

    kolom_kartu = st.columns(2)

    for posisi, (index, catatan) in enumerate(data_tampil):
        judul = catatan.get("judul", "-")
        isi = catatan.get("isi", "-")
        kategori = catatan.get("kategori", "-")
        prioritas = catatan.get("prioritas", "Sedang")
        status = catatan.get("status", "Belum dikerjakan")
        deadline = catatan.get("deadline", "-")

        with kolom_kartu[posisi % 2]:
            with st.container(border=True):
                st.markdown(f"### {judul}")

                st.caption(f"📅 Deadline: {deadline}")
                st.caption(cek_deadline(deadline))

                col_badge1, col_badge2 = st.columns(2)
                col_badge1.info(f"📂 {kategori}")
                col_badge2.info(label_prioritas(prioritas))

                st.write(potong_teks(isi))

                st.caption(label_status(status))

                if st.button(
                    "Buka Detail",
                    key=f"detail_{index}",
                    use_container_width=True
                ):
                    st.session_state.selected_catatan_index = index
                    st.session_state.halaman = "Detail Catatan"
                    st.rerun()