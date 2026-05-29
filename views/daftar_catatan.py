import streamlit as st
from datetime import datetime

from data import simpan_catatan
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


def render_daftar_catatan():
    st.title("📋 Daftar Catatan")
    st.write("Lihat, cari, filter, edit, ubah status, atau hapus catatan yang sudah kamu buat.")

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

    for index, catatan in data_tampil:
        judul = catatan.get("judul", "-")
        isi = catatan.get("isi", "-")
        kategori = catatan.get("kategori", "-")
        prioritas = catatan.get("prioritas", "Sedang")
        status = catatan.get("status", "Belum dikerjakan")
        deadline = catatan.get("deadline", "-")

        with st.container(border=True):
            col_judul, col_status = st.columns([3, 1])

            with col_judul:
                st.markdown(f"### {judul}")
                st.caption(f"📅 Deadline: {deadline} | {cek_deadline(deadline)}")

            with col_status:
                st.write(label_status(status))
                st.write(label_prioritas(prioritas))

            st.write(isi)

            col_meta1, col_meta2, col_meta3 = st.columns(3)
            col_meta1.info(f"Kategori: {kategori}")
            col_meta2.info(f"Prioritas: {prioritas}")
            col_meta3.info(f"Status: {status}")

            st.divider()

            col_update, col_edit, col_hapus = st.columns([2, 2, 1])

            # =========================
            # UBAH STATUS CEPAT
            # =========================
            with col_update:
                status_sekarang = status

                if status_sekarang not in STATUS_LIST:
                    status_sekarang = "Belum dikerjakan"

                status_baru = st.selectbox(
                    "Ubah status",
                    STATUS_LIST,
                    index=STATUS_LIST.index(status_sekarang),
                    key=f"status_{index}"
                )

                if status_baru != catatan.get("status"):
                    st.session_state.catatan_list[index]["status"] = status_baru
                    simpan_catatan(st.session_state.catatan_list)
                    st.success("Status berhasil diperbarui.")
                    st.rerun()

            # =========================
            # EDIT CATATAN
            # =========================
            with col_edit:
                with st.expander("✏️ Edit"):
                    with st.form(f"form_edit_{index}"):
                        edit_judul = st.text_input(
                            "Judul",
                            value=judul,
                            key=f"edit_judul_{index}"
                        )

                        edit_isi = st.text_area(
                            "Isi",
                            value=isi,
                            key=f"edit_isi_{index}"
                        )

                        edit_kategori = st.selectbox(
                            "Kategori",
                            KATEGORI_LIST,
                            index=KATEGORI_LIST.index(kategori)
                            if kategori in KATEGORI_LIST else 0,
                            key=f"edit_kategori_{index}"
                        )

                        edit_prioritas = st.selectbox(
                            "Prioritas",
                            PRIORITAS_LIST,
                            index=PRIORITAS_LIST.index(prioritas)
                            if prioritas in PRIORITAS_LIST else 1,
                            key=f"edit_prioritas_{index}"
                        )

                        try:
                            deadline_value = datetime.strptime(
                                deadline, "%Y-%m-%d"
                            ).date()
                        except:
                            deadline_value = datetime.today().date()

                        edit_deadline = st.date_input(
                            "Deadline",
                            value=deadline_value,
                            key=f"edit_deadline_{index}"
                        )

                        tombol_update = st.form_submit_button(
                            "Simpan Perubahan",
                            use_container_width=True
                        )

                        if tombol_update:
                            if edit_judul.strip() == "" or edit_isi.strip() == "":
                                st.warning("Judul dan isi tidak boleh kosong.")
                            else:
                                st.session_state.catatan_list[index]["judul"] = edit_judul
                                st.session_state.catatan_list[index]["isi"] = edit_isi
                                st.session_state.catatan_list[index]["kategori"] = edit_kategori
                                st.session_state.catatan_list[index]["prioritas"] = edit_prioritas
                                st.session_state.catatan_list[index]["deadline"] = str(edit_deadline)

                                simpan_catatan(st.session_state.catatan_list)
                                st.success("Catatan berhasil diperbarui.")
                                st.rerun()

            # =========================
            # HAPUS CATATAN
            # =========================
            with col_hapus:
                st.write("")
                st.write("")
                if st.button("🗑️ Hapus", key=f"hapus_{index}", use_container_width=True):
                    st.session_state.catatan_list.pop(index)
                    simpan_catatan(st.session_state.catatan_list)
                    st.rerun()