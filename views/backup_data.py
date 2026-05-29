import streamlit as st
import json
import csv
import io
from datetime import datetime

from data import simpan_catatan


FIELDNAMES = [
    "judul",
    "isi",
    "kategori",
    "prioritas",
    "deadline",
    "status",
    "tanggal_dibuat"
]


def catatan_ke_json(catatan_list):
    return json.dumps(
        catatan_list,
        indent=4,
        ensure_ascii=False
    )


def catatan_ke_csv(catatan_list):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=FIELDNAMES)

    writer.writeheader()

    for catatan in catatan_list:
        row = {}

        for field in FIELDNAMES:
            row[field] = catatan.get(field, "")

        writer.writerow(row)

    return output.getvalue()


def validasi_data_json(data):
    if not isinstance(data, list):
        return False

    for item in data:
        if not isinstance(item, dict):
            return False

        if "judul" not in item or "isi" not in item:
            return False

    return True


def render_backup_data():
    st.title("💾 Backup & Export Data")
    st.write(
        "Kelola data catatan kamu. Kamu bisa mengunduh data sebagai file JSON/CSV "
        "atau mengimpor kembali data dari file JSON."
    )

    st.divider()

    catatan_list = st.session_state.catatan_list
    total_catatan = len(catatan_list)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Catatan", total_catatan)
    col2.metric(
        "Selesai",
        len([c for c in catatan_list if c.get("status") == "Selesai"])
    )
    col3.metric(
        "Belum/Proses",
        len([c for c in catatan_list if c.get("status") != "Selesai"])
    )

    st.divider()

    # =========================
    # EXPORT DATA
    # =========================
    st.subheader("⬇️ Export Data")

    with st.container(border=True):
        st.write(
            "Gunakan fitur ini untuk menyimpan cadangan catatan kamu ke laptop."
        )

        if total_catatan == 0:
            st.info("Belum ada catatan yang bisa diexport.")
        else:
            tanggal_export = datetime.now().strftime("%Y%m%d_%H%M%S")

            json_data = catatan_ke_json(catatan_list)
            csv_data = catatan_ke_csv(catatan_list)

            col_json, col_csv = st.columns(2)

            with col_json:
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"backup_revisiku_{tanggal_export}.json",
                    mime="application/json",
                    use_container_width=True
                )

            with col_csv:
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"catatan_revisiku_{tanggal_export}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    st.divider()

    # =========================
    # IMPORT DATA
    # =========================
    st.subheader("⬆️ Import Data JSON")

    with st.container(border=True):
        st.write(
            "Upload file JSON hasil backup RevisiKu untuk memulihkan data."
        )

        file_json = st.file_uploader(
            "Pilih file JSON",
            type=["json"]
        )

        mode_import = st.radio(
            "Mode Import",
            ["Gabungkan dengan data lama", "Ganti semua data lama"],
            horizontal=True
        )

        if file_json is not None:
            try:
                data_baru = json.load(file_json)

                if not validasi_data_json(data_baru):
                    st.error(
                        "Format JSON tidak sesuai. File harus berisi daftar catatan "
                        "dengan minimal field judul dan isi."
                    )
                    return

                st.success(f"File valid. Ditemukan {len(data_baru)} catatan.")

                with st.expander("Preview data yang akan diimport"):
                    for i, item in enumerate(data_baru[:5], start=1):
                        st.write(f"**{i}. {item.get('judul', '-')}**")
                        st.caption(item.get("isi", "-")[:160] + "...")

                    if len(data_baru) > 5:
                        st.caption(f"Dan {len(data_baru) - 5} catatan lainnya.")

                if st.button("Import Data", type="primary", use_container_width=True):
                    if mode_import == "Gabungkan dengan data lama":
                        st.session_state.catatan_list.extend(data_baru)
                    else:
                        st.session_state.catatan_list = data_baru

                    simpan_catatan(st.session_state.catatan_list)

                    st.success("Data berhasil diimport.")
                    st.rerun()

            except json.JSONDecodeError:
                st.error("File tidak bisa dibaca. Pastikan file benar-benar berformat JSON.")
            except Exception as e:
                st.error(f"Terjadi error saat import data: {e}")

    st.divider()

    # =========================
    # INFO
    # =========================
    with st.container(border=True):
        st.subheader("Catatan")
        st.write(
            "- Format **JSON** cocok untuk backup dan import kembali ke aplikasi."
        )
        st.write(
            "- Format **CSV** cocok untuk dibuka di Excel atau Google Sheets."
        )
        st.write(
            "- Kalau memilih **Ganti semua data lama**, data lama akan ditimpa oleh data dari file JSON."
        )