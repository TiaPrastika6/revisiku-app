import streamlit as st
from datetime import date

from data import simpan_catatan
from utils import STATUS_LIST, KATEGORI_LIST, PRIORITAS_LIST


def get_template_deskripsi(kategori):
    if kategori == "Tugas":
        return """Deskripsi tugas:
Ketentuan pengerjaan:
File/link pendukung:
Catatan tambahan:"""

    elif kategori == "Bimbingan":
        return """Tanggal bimbingan:
Topik bimbingan:
Arahan dosen:
Revisi yang harus dilakukan:
Catatan penting:
Target sebelum bimbingan berikutnya:"""

    elif kategori == "Revisi":
        return """Bagian yang direvisi:
Masukan/perbaikan:
Referensi yang perlu ditambahkan:
Hal yang harus dicek ulang:
Status pengerjaan:"""

    elif kategori == "Praktikum":
        return """Nama praktikum:
Materi/topik:
Langkah yang dikerjakan:
Kendala:
Solusi:
Hasil akhir:
Catatan tambahan:"""

    return ""


def render_tambah_catatan():
    st.title("➕ Tambah Catatan")
    st.write(
        "Tambahkan tugas, revisi, catatan bimbingan, praktikum, atau deadline penting "
        "yang perlu kamu ingat."
    )

    st.divider()

    col_info, col_form = st.columns([1, 2])

    # =========================
    # PANEL INFO
    # =========================
    with col_info:
        with st.container(border=True):
            st.subheader("📌 Tips")
            st.write(
                "Pilih kategori terlebih dahulu. Deskripsi catatan akan otomatis "
                "menyesuaikan dengan kategori yang dipilih."
            )
            st.info(
                "Contoh: kalau memilih kategori Bimbingan, bagian deskripsi akan "
                "langsung berisi format arahan dosen, revisi, dan target berikutnya."
            )

        with st.container(border=True):
            st.subheader("Kategori")
            st.write("📚 Tugas")
            st.write("👩‍🏫 Bimbingan")
            st.write("📝 Revisi")
            st.write("💻 Praktikum")
            st.write("📌 Lainnya")

    # =========================
    # FORM CATATAN
    # =========================
    with col_form:
        with st.container(border=True):
            st.subheader("Form Catatan Baru")

            # Kategori dibuat di luar form supaya field tambahan dan template
            # deskripsi bisa langsung berubah saat kategori dipilih.
            kategori = st.selectbox("Kategori", KATEGORI_LIST)

            isi_template = get_template_deskripsi(kategori)

            with st.form("form_catatan", clear_on_submit=True):
                judul = st.text_input(
                    "Judul catatan",
                    placeholder="Contoh: Revisi Bab 2"
                )

                mata_kuliah = ""
                nama_dosen = ""

                # =========================
                # FIELD TAMBAHAN DINAMIS
                # =========================
                if kategori == "Tugas":
                    mata_kuliah = st.text_input(
                        "Mata Kuliah",
                        placeholder="Contoh: Metodologi Penelitian"
                    )

                elif kategori == "Bimbingan":
                    nama_dosen = st.text_input(
                        "Nama Dosen",
                        placeholder="Contoh: Pak AW"
                    )

                isi = st.text_area(
                    "Deskripsi / Isi Catatan",
                    value=isi_template,
                    placeholder=(
                        "Tulis detail tugas, revisi, arahan dosen, "
                        "atau hal yang perlu dikerjakan..."
                    ),
                    height=240,
                    key=f"isi_catatan_{kategori}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    prioritas = st.selectbox("Prioritas", PRIORITAS_LIST)

                with col2:
                    status = st.selectbox("Status", STATUS_LIST)

                deadline = st.date_input(
                    "Deadline / Tanggal Target",
                    value=date.today()
                )

                tombol_simpan = st.form_submit_button(
                    "💾 Simpan Catatan",
                    use_container_width=True
                )

                # =========================
                # VALIDASI DAN SIMPAN DATA
                # =========================
                if tombol_simpan:
                    if judul.strip() == "" or isi.strip() == "":
                        st.warning("Judul dan deskripsi catatan wajib diisi.")

                    elif kategori == "Tugas" and mata_kuliah.strip() == "":
                        st.warning("Mata kuliah wajib diisi untuk kategori Tugas.")

                    elif kategori == "Bimbingan" and nama_dosen.strip() == "":
                        st.warning("Nama dosen wajib diisi untuk kategori Bimbingan.")

                    else:
                        catatan_baru = {
                            "judul": judul,
                            "isi": isi,
                            "kategori": kategori,
                            "mata_kuliah": mata_kuliah,
                            "nama_dosen": nama_dosen,
                            "prioritas": prioritas,
                            "deadline": str(deadline),
                            "status": status,
                            "tanggal_dibuat": str(date.today()),
                            "checklist": [],
                            "arsip": False
                        }

                        st.session_state.catatan_list.append(catatan_baru)
                        simpan_catatan(st.session_state.catatan_list)

                        st.success("Catatan berhasil disimpan.")