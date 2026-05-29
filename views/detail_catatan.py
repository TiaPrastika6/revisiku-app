import streamlit as st
from datetime import datetime
from html import escape
from textwrap import dedent

from data import simpan_catatan
from utils import (
    STATUS_LIST,
    KATEGORI_LIST,
    PRIORITAS_LIST,
    cek_deadline
)


def label_status(status):
    if status == "Selesai":
        return "✅ Selesai"
    elif status == "Proses":
        return "🔧 Proses"
    return "🕒 Belum dikerjakan"


def label_prioritas(prioritas):
    if prioritas == "Tinggi":
        return "🔴 Tinggi"
    elif prioritas == "Sedang":
        return "🟡 Sedang"
    return "🟢 Rendah"


def rapikan_isi_catatan(teks):
    teks = str(teks or "")
    teks = teks.replace("\r\n", "\n")
    teks = dedent(teks).strip()

    baris_bersih = []
    for baris in teks.split("\n"):
        baris_bersih.append(baris.lstrip())

    return "\n".join(baris_bersih)


def kembali_ke_daftar():
    st.session_state.halaman = "Daftar Catatan"
    st.rerun()


def render_html(kode):
    st.markdown(dedent(kode).strip(), unsafe_allow_html=True)


def render_detail_catatan():
    # =========================
    # VALIDASI DATA
    # =========================
    if "selected_catatan_index" not in st.session_state:
        st.warning("Belum ada catatan yang dipilih.")

        if st.button("← Kembali ke Daftar Catatan"):
            kembali_ke_daftar()

        return

    index = st.session_state.selected_catatan_index

    if index < 0 or index >= len(st.session_state.catatan_list):
        st.warning("Catatan tidak ditemukan.")

        if st.button("← Kembali ke Daftar Catatan"):
            kembali_ke_daftar()

        return

    catatan = st.session_state.catatan_list[index]

    judul = catatan.get("judul", "-")
    isi = catatan.get("isi", "-")
    kategori = catatan.get("kategori", "-")
    prioritas = catatan.get("prioritas", "Sedang")
    status = catatan.get("status", "Belum dikerjakan")
    deadline = catatan.get("deadline", "-")

    # =========================
    # STYLE KHUSUS DETAIL
    # =========================
    render_html("""
    <style>
    .detail-wrapper {
        margin-top: 4px;
    }

    .detail-title-box {
        margin-bottom: 18px;
    }

    .detail-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .isi-catatan-box {
        background-color: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 18px;
        padding: 30px 34px;
        color: #f8fafc;
        font-size: 16px;
        line-height: 1.9;
        white-space: pre-wrap;
        text-align: left;

        /* Tinggi kotak isi catatan */
        height: 760px;
        overflow-y: auto;

        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.02);
    }

    .isi-catatan-box::-webkit-scrollbar {
        width: 8px;
    }

    .isi-catatan-box::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 999px;
    }

    .isi-catatan-box::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.45);
        border-radius: 999px;
    }

    .isi-catatan-box::-webkit-scrollbar-thumb:hover {
        background: rgba(148, 163, 184, 0.7);
    }

    .small-muted {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
    """)

    # =========================
    # TOMBOL KEMBALI
    # =========================
    if st.button("← Kembali ke Daftar Catatan"):
        kembali_ke_daftar()

    # =========================
    # HEADER
    # =========================
    render_html("""
    <div class="detail-wrapper">
        <div class="detail-label">Detail Catatan</div>
    </div>
    """)

    st.title(judul)
    st.caption(f"📅 Deadline: {deadline} | {cek_deadline(deadline)}")

    st.divider()

    # =========================
    # LAYOUT UTAMA
    # =========================
    col_kiri, col_kanan = st.columns([3.4, 1.15], gap="large")

    # =========================
    # KOLOM KIRI
    # =========================
    with col_kiri:
        tab_isi, tab_edit = st.tabs(["📝 Isi Catatan", "✏️ Edit Catatan"])

        with tab_isi:
            with st.container(border=True):
                st.subheader("Isi Catatan")

                isi_bersih = escape(rapikan_isi_catatan(isi))

                render_html(f"""
                <div class="isi-catatan-box">{isi_bersih}</div>
                """)

        with tab_edit:
            with st.container(border=True):
                st.subheader("Edit Catatan")

                with st.form("form_edit_detail"):
                    edit_judul = st.text_input(
                        "Judul catatan",
                        value=judul
                    )

                    edit_isi = st.text_area(
                        "Isi catatan",
                        value=isi,
                        height=320
                    )

                    col_edit1, col_edit2 = st.columns(2)

                    with col_edit1:
                        edit_kategori = st.selectbox(
                            "Kategori",
                            KATEGORI_LIST,
                            index=KATEGORI_LIST.index(kategori)
                            if kategori in KATEGORI_LIST else 0
                        )

                        edit_status = st.selectbox(
                            "Status",
                            STATUS_LIST,
                            index=STATUS_LIST.index(status)
                            if status in STATUS_LIST else 0
                        )

                    with col_edit2:
                        edit_prioritas = st.selectbox(
                            "Prioritas",
                            PRIORITAS_LIST,
                            index=PRIORITAS_LIST.index(prioritas)
                            if prioritas in PRIORITAS_LIST else 1
                        )

                        try:
                            deadline_value = datetime.strptime(
                                deadline, "%Y-%m-%d"
                            ).date()
                        except:
                            deadline_value = datetime.today().date()

                        edit_deadline = st.date_input(
                            "Deadline",
                            value=deadline_value
                        )

                    tombol_update = st.form_submit_button(
                        "💾 Simpan Perubahan",
                        use_container_width=True
                    )

                    if tombol_update:
                        if edit_judul.strip() == "" or edit_isi.strip() == "":
                            st.warning("Judul dan isi catatan tidak boleh kosong.")
                        else:
                            st.session_state.catatan_list[index]["judul"] = edit_judul
                            st.session_state.catatan_list[index]["isi"] = edit_isi
                            st.session_state.catatan_list[index]["kategori"] = edit_kategori
                            st.session_state.catatan_list[index]["prioritas"] = edit_prioritas
                            st.session_state.catatan_list[index]["status"] = edit_status
                            st.session_state.catatan_list[index]["deadline"] = str(edit_deadline)

                            simpan_catatan(st.session_state.catatan_list)
                            st.success("Catatan berhasil diperbarui.")
                            st.rerun()

    # =========================
    # KOLOM KANAN
    # =========================
    with col_kanan:
        with st.container(border=True):
            st.subheader("Ringkasan")

            st.info(f"📂 **Kategori**\n\n{kategori}")
            st.info(f"⭐ **Prioritas**\n\n{label_prioritas(prioritas)}")
            st.info(f"📌 **Status**\n\n{label_status(status)}")
            st.info(f"📅 **Deadline**\n\n{deadline}")

            keterangan_deadline = cek_deadline(deadline)

            if "Terlambat" in keterangan_deadline:
                st.error(keterangan_deadline)
            elif "hari ini" in keterangan_deadline:
                st.warning(keterangan_deadline)
            else:
                st.success(keterangan_deadline)

        with st.container(border=True):
            st.subheader("Ubah Status Cepat")
            st.caption("Gunakan ini kalau cuma ingin mengganti status tanpa membuka tab edit.")

            status_sekarang = status

            if status_sekarang not in STATUS_LIST:
                status_sekarang = "Belum dikerjakan"

            status_baru = st.selectbox(
                "Status baru",
                STATUS_LIST,
                index=STATUS_LIST.index(status_sekarang),
                key=f"quick_status_{index}"
            )

            if st.button("Update Status", use_container_width=True):
                st.session_state.catatan_list[index]["status"] = status_baru
                simpan_catatan(st.session_state.catatan_list)
                st.success("Status berhasil diperbarui.")
                st.rerun()

        with st.container(border=True):
            st.subheader("Zona Hapus")
            st.caption("Catatan yang dihapus tidak bisa dikembalikan.")

            konfirmasi_hapus = st.checkbox(
                "Saya yakin ingin menghapus catatan ini",
                key=f"confirm_delete_{index}"
            )

            if st.button(
                "🗑️ Hapus Catatan",
                type="primary",
                use_container_width=True,
                disabled=not konfirmasi_hapus
            ):
                st.session_state.catatan_list.pop(index)
                simpan_catatan(st.session_state.catatan_list)

                st.session_state.halaman = "Daftar Catatan"
                st.rerun()