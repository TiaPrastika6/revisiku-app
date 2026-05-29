import streamlit as st
from datetime import date

from data import simpan_catatan
from utils import STATUS_LIST, KATEGORI_LIST, PRIORITAS_LIST


def render_tambah_catatan():
    st.title("➕ Tambah Catatan")
    st.write(
        "Tambahkan tugas, revisi, catatan bimbingan, praktikum, atau deadline penting "
        "yang perlu kamu ingat."
    )

    st.divider()

    col_info, col_form = st.columns([1, 2])

    with col_info:
        with st.container(border=True):
            st.subheader("📌 Tips")
            st.write(
                "Isi catatan dengan detail supaya nanti gampang dipahami lagi."
            )
            st.write("Contoh catatan:")
            st.info(
                "Revisi Bab 2: tambahkan penelitian terdahulu, perbaiki state of the art, "
                "dan sesuaikan kutipan."
            )

        with st.container(border=True):
            st.subheader("Kategori")
            st.write("📚 Tugas")
            st.write("👩‍🏫 Bimbingan")
            st.write("📝 Revisi")
            st.write("💻 Praktikum")
            st.write("📌 Lainnya")

    with col_form:
        with st.container(border=True):
            st.subheader("Form Catatan Baru")

            with st.form("form_catatan", clear_on_submit=True):
                judul = st.text_input(
                    "Judul catatan",
                    placeholder="Contoh: Revisi Bab 2"
                )

                isi = st.text_area(
                    "Isi catatan",
                    placeholder="Tulis detail tugas, revisi, arahan dosen, atau hal yang perlu dikerjakan...",
                    height=160
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    kategori = st.selectbox("Kategori", KATEGORI_LIST)

                with col2:
                    prioritas = st.selectbox("Prioritas", PRIORITAS_LIST)

                with col3:
                    status = st.selectbox("Status", STATUS_LIST)

                deadline = st.date_input(
                    "Deadline / Tanggal Target",
                    value=date.today()
                )

                tombol_simpan = st.form_submit_button(
                    "💾 Simpan Catatan",
                    use_container_width=True
                )

                if tombol_simpan:
                    if judul.strip() == "" or isi.strip() == "":
                        st.warning("Judul dan isi catatan wajib diisi.")
                    else:
                        catatan_baru = {
                            "judul": judul,
                            "isi": isi,
                            "kategori": kategori,
                            "prioritas": prioritas,
                            "deadline": str(deadline),
                            "status": status,
                            "tanggal_dibuat": str(date.today())
                        }

                        st.session_state.catatan_list.append(catatan_baru)
                        simpan_catatan(st.session_state.catatan_list)

                        st.success("Catatan berhasil disimpan.")