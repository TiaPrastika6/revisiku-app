import streamlit as st

from utils import (
    STATUS_LIST,
    KATEGORI_LIST,
    PRIORITAS_LIST,
    cek_deadline,
    deadline_untuk_sorting
)


def potong_teks(teks, batas=240):
    teks = str(teks or "")

    if len(teks) <= batas:
        return teks

    return teks[:batas].rstrip() + "..."


def cocok_dengan_keyword(catatan, keyword):
    keyword = keyword.lower().strip()

    if keyword == "":
        return True

    teks_catatan = " ".join([
        str(catatan.get("judul", "")),
        str(catatan.get("isi", "")),
        str(catatan.get("kategori", "")),
        str(catatan.get("prioritas", "")),
        str(catatan.get("status", "")),
        str(catatan.get("deadline", ""))
    ]).lower()

    if keyword in teks_catatan:
        return True

    checklist = catatan.get("checklist", [])

    if isinstance(checklist, list):
        for item in checklist:
            if isinstance(item, dict):
                teks_item = str(item.get("teks", "")).lower()
            else:
                teks_item = str(item).lower()

            if keyword in teks_item:
                return True

    return False


def hitung_checklist(catatan):
    checklist = catatan.get("checklist", [])

    if not isinstance(checklist, list):
        return 0, 0

    total = len(checklist)
    selesai = 0

    for item in checklist:
        if isinstance(item, dict) and item.get("selesai"):
            selesai += 1

    return total, selesai


def render_pencarian_global():
    st.title("🔍 Cari Catatan")
    st.write(
        "Cari catatan dari judul, isi, kategori, prioritas, status, deadline, "
        "atau item checklist."
    )

    st.divider()

    with st.container(border=True):
        st.subheader("Filter Pencarian")

        keyword = st.text_input(
            "Kata kunci",
            placeholder="Contoh: Bab 2, bimbingan, deadline, revisi, state of the art..."
        )

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

        urutkan = st.selectbox(
            "Urutkan",
            [
                "Deadline terdekat",
                "Deadline terlama",
                "Terbaru ditambahkan",
                "Judul A-Z"
            ]
        )

    st.divider()

    hasil = []

    for index, catatan in enumerate(st.session_state.catatan_list):
        cocok_keyword = cocok_dengan_keyword(catatan, keyword)

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

        if cocok_keyword and cocok_kategori and cocok_status and cocok_prioritas:
            hasil.append((index, catatan))

    if urutkan == "Deadline terdekat":
        hasil.sort(key=lambda x: deadline_untuk_sorting(x[1].get("deadline", "")))
    elif urutkan == "Deadline terlama":
        hasil.sort(
            key=lambda x: deadline_untuk_sorting(x[1].get("deadline", "")),
            reverse=True
        )
    elif urutkan == "Terbaru ditambahkan":
        hasil.reverse()
    elif urutkan == "Judul A-Z":
        hasil.sort(key=lambda x: str(x[1].get("judul", "")).lower())

    st.subheader(f"📌 {len(hasil)} hasil ditemukan")

    if len(hasil) == 0:
        st.info("Tidak ada catatan yang sesuai dengan pencarian.")
        return

    for index, catatan in hasil:
        judul = catatan.get("judul", "-")
        isi = catatan.get("isi", "-")
        kategori = catatan.get("kategori", "-")
        prioritas = catatan.get("prioritas", "Sedang")
        status = catatan.get("status", "Belum dikerjakan")
        deadline = catatan.get("deadline", "-")

        total_checklist, selesai_checklist = hitung_checklist(catatan)

        with st.container(border=True):
            col_info, col_aksi = st.columns([4, 1])

            with col_info:
                st.markdown(f"### {judul}")
                st.write(potong_teks(isi))

                st.caption(
                    f"📂 {kategori} | ⭐ {prioritas} | 📌 {status} | "
                    f"📅 {deadline} | {cek_deadline(deadline)}"
                )

                if total_checklist > 0:
                    st.caption(
                        f"✅ Checklist: {selesai_checklist}/{total_checklist} selesai"
                    )

            with col_aksi:
                if st.button(
                    "Buka Detail",
                    key=f"global_detail_{index}",
                    use_container_width=True
                ):
                    st.session_state.selected_catatan_index = index
                    st.session_state.halaman = "Detail Catatan"
                    st.rerun()