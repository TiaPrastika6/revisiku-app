# RevisiKu

RevisiKu adalah aplikasi pencatat tugas, revisi, catatan bimbingan, praktikum, dan deadline mahasiswa berbasis Python Streamlit.

Aplikasi ini dibuat untuk membantu mahasiswa menyimpan catatan akademik secara lebih rapi, memantau deadline, mengelola checklist revisi, serta mengarsipkan catatan yang sudah selesai.

## Tujuan Aplikasi

RevisiKu dikembangkan sebagai aplikasi pribadi untuk membantu mahasiswa agar tidak lupa terhadap tugas, revisi, catatan bimbingan, dan deadline penting.

## Fitur

- Dashboard ringkasan catatan
- Tambah catatan berdasarkan kategori
- Template deskripsi otomatis sesuai kategori
- Field tambahan dinamis:
  - Mata Kuliah untuk kategori Tugas
  - Nama Dosen untuk kategori Bimbingan
- Daftar catatan
- Detail catatan
- Edit catatan
- Checklist subtugas/revisi
- Ubah status catatan
- Reminder deadline:
  - Terlambat
  - Deadline hari ini
  - Deadline H-3
- Arsip catatan selesai
- Kalender deadline
- Pencarian global
- Backup data ke JSON/CSV
- Import data dari file JSON

## Kategori Catatan

Aplikasi ini mendukung beberapa kategori catatan:

- Tugas
- Bimbingan
- Revisi
- Praktikum
- Lainnya

Setiap kategori memiliki format deskripsi otomatis agar catatan lebih mudah dibuat.

## Status Catatan

Catatan dapat memiliki status:

- Belum dikerjakan
- Proses
- Selesai

Catatan yang sudah selesai dapat dipindahkan ke halaman arsip agar daftar utama tetap rapi.

## Teknologi

Project ini dibuat menggunakan:

- Python
- Streamlit
- JSON sebagai penyimpanan data lokal

## Struktur Project

```text
revisiku-app
├── app.py
├── data.py
├── utils.py
├── styles.py
├── requirements.txt
├── README.md
├── catatan.json
└── views
    ├── __init__.py
    ├── dashboard.py
    ├── tambah_catatan.py
    ├── daftar_catatan.py
    ├── detail_catatan.py
    ├── arsip_catatan.py
    ├── kalender_deadline.py
    ├── pencarian_global.py
    └── backup_data.py