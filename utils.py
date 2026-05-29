from datetime import date, datetime

STATUS_LIST = ["Belum dikerjakan", "Proses", "Selesai"]
KATEGORI_LIST = ["Tugas", "Bimbingan", "Revisi", "Praktikum", "Lainnya"]
PRIORITAS_LIST = ["Rendah", "Sedang", "Tinggi"]


def cek_deadline(deadline_str):
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        hari_ini = date.today()
        selisih = (deadline - hari_ini).days

        if selisih < 0:
            return f"🔴 Terlambat {abs(selisih)} hari"
        elif selisih == 0:
            return "🟠 Deadline hari ini"
        elif selisih <= 3:
            return f"🟡 Sisa {selisih} hari"
        else:
            return f"🟢 Sisa {selisih} hari"
    except:
        return "-"


def deadline_untuk_sorting(deadline_str):
    try:
        return datetime.strptime(deadline_str, "%Y-%m-%d").date()
    except:
        return date.max


def hitung_statistik(catatan_list):
    total = len(catatan_list)
    belum = len([c for c in catatan_list if c.get("status") == "Belum dikerjakan"])
    proses = len([c for c in catatan_list if c.get("status") == "Proses"])
    selesai = len([c for c in catatan_list if c.get("status") == "Selesai"])

    terlambat = 0

    for c in catatan_list:
        try:
            deadline = datetime.strptime(c.get("deadline", ""), "%Y-%m-%d").date()
            selisih = (deadline - date.today()).days

            if c.get("status") != "Selesai" and selisih < 0:
                terlambat += 1
        except:
            pass

    return total, belum, proses, selesai, terlambat


def warna_prioritas(prioritas):
    if prioritas == "Tinggi":
        return "badge-red"
    elif prioritas == "Sedang":
        return "badge-yellow"
    return "badge-green"


def warna_status(status):
    if status == "Selesai":
        return "badge-green"
    elif status == "Proses":
        return "badge-yellow"
    return "badge-gray"