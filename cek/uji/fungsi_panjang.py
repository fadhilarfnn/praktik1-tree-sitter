# File uji untuk fitur 2: deteksi fungsi lebih dari 30 baris

def fungsi_pendek(a, b):
    hasil = a + b
    return hasil


def proses_pesanan_lengkap(pesanan):
    total = 0
    diskon = 0
    pajak = 0
    catatan = []

    if not pesanan:
        return {"status": "kosong", "total": 0}

    for item in pesanan.get("items", []):
        harga = item.get("harga", 0)
        qty = item.get("qty", 1)
        subtotal = harga * qty
        total += subtotal
        catatan.append(f"{item.get('nama', 'item')}: {subtotal}")

    if total >= 1_000_000:
        diskon = total * 0.10
    elif total >= 500_000:
        diskon = total * 0.05
    else:
        diskon = 0

    setelah_diskon = total - diskon
    pajak = setelah_diskon * 0.11
    grand_total = setelah_diskon + pajak

    ringkasan = {
        "status": "diproses",
        "subtotal": total,
        "diskon": diskon,
        "pajak": pajak,
        "grand_total": grand_total,
        "catatan": catatan,
    }
    return ringkasan
