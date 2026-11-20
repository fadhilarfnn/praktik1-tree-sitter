# File uji untuk fitur 1: deteksi komentar penanda tugas

def ambil_pengguna(user_id):
    # TODO: tambahkan caching Redis agar query database lebih cepat
    pesan = "Teks TODO di dalam string ini tidak boleh terdeteksi"
    if user_id <= 0:
        # FIXME: ganti ValueError dengan custom exception aplikasi
        raise ValueError("user_id tidak valid")
    # komentar biasa tidak ikut dilaporkan
    return {"id": user_id, "info": pesan}
