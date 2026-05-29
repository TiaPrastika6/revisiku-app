import streamlit as st

from data import simpan_catatan
from utils import cek_deadline, deadline_untuk_sorting


def potong_teks(teks, batas=220):
    teks = str(teks or "")

    if len(teks) <= batas:
        return teks

    return teks[:batas].rstrip() + "..."


def render_arsip_catatan():
    st.title("🗃️ Arsip Catatan")
    st.write(
        "Halaman ini berisi catatan yang sudah diarsipkan. "
        "Catatan arsip tidak muncul di daftar catatan utama."
    )

    st.divider()

    data_arsip = []

    for index, catatan in enumerate(st.session_state.catatan_list):
        if catatan.get("arsip", False):
            data_arsip.append((index, catatan))

    data_arsip.sort(
        key=lambda x: deadline_untuk_sorting(x[1].get("deadline", "")),
        reverse=True
    )

    col1, col2 = st.columns(2)
    col1.metric("Total Arsip", len(data_arsip))
    col2.metric(
        "Selesai",
        len([c for _, c in data_arsip if c.get("status") == "Selesai"])
    )

    st.divider()

    if len(data_arsip) == 0:
        st.info("Belum ada catatan yang diarsipkan.")
        return

    for index, catatan in data_arsip:
        judul = catatan.get("judul", "-")
        isi = catatan.get("isi", "-")
        kategori = catatan.get("kategori", "-")
        prioritas = catatan.get("prioritas", "Sedang")
        status = catatan.get("status", "Belum dikerjakan")
        deadline = catatan.get("deadline", "-")

        with st.container(border=True):
            col_info, col_aksi = st.columns([4, 1])

            with col_info:
                st.markdown(f"### {judul}")
                st.write(potong_teks(isi))
                st.caption(
                    f"📂 {kategori} | ⭐ {prioritas} | 📌 {status} | "
                    f"📅 {deadline} | {cek_deadline(deadline)}"
                )

                if catatan.get("mata_kuliah"):
                    st.caption(f"📚 Mata Kuliah: {catatan.get('mata_kuliah')}")

                if catatan.get("nama_dosen"):
                    st.caption(f"👩‍🏫 Nama Dosen: {catatan.get('nama_dosen')}")

            with col_aksi:
                if st.button(
                    "Pulihkan",
                    key=f"pulihkan_arsip_{index}",
                    use_container_width=True
                ):
                    st.session_state.catatan_list[index]["arsip"] = False
                    simpan_catatan(st.session_state.catatan_list)
                    st.success("Catatan berhasil dipulihkan.")
                    st.rerun()

                if st.button(
                    "Buka Detail",
                    key=f"detail_arsip_{index}",
                    use_container_width=True
                ):
                    st.session_state.selected_catatan_index = index
                    st.session_state.halaman = "Detail Catatan"
                    st.rerun()

                st.write("")

                konfirmasi = st.checkbox(
                    "Hapus?",
                    key=f"konfirmasi_hapus_arsip_{index}"
                )

                if st.button(
                    "Hapus Permanen",
                    key=f"hapus_arsip_{index}",
                    type="primary",
                    use_container_width=True,
                    disabled=not konfirmasi
                ):
                    st.session_state.catatan_list.pop(index)
                    simpan_catatan(st.session_state.catatan_list)
                    st.rerun()