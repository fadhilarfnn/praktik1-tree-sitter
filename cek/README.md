# `cek.py` — Pendeteksi TODO/FIXME, Fungsi Panjang, dan Error Sintaks

CLI sederhana berbasis **Tree-sitter** (`tree-sitter-python`) untuk memeriksa semua file `.py` di dalam suatu folder (atau satu file tunggal).

## Fitur

1. **Deteksi komentar `TODO` / `FIXME`**  
   Menggunakan query Tree-sitter `((comment) @c (#match? @c "TODO|FIXME"))` sehingga hanya komentar asli yang dilaporkan (string yang berisi kata `TODO` tidak ikut terdeteksi).
2. **Deteksi fungsi panjang (> 30 baris)**  
   Menggunakan query `(function_definition name: (identifier) @nama) @fungsi` dan menghitung panjang baris dari `start_point` hingga `end_point`. Semua fungsi — termasuk method di dalam kelas dan fungsi bersarang — ikut diperiksa.
3. **Deteksi file dengan error sintaks**  
   Memeriksa `tree.root_node.has_error`, lalu mencari node `ERROR` atau `MISSING` pertama secara rekursif (DFS) untuk melaporkan baris dan kolom pertama yang bermasalah.
4. **Filter direktori otomatis**  
   Folder `venv/`, `.venv/`, `.git/`, `node_modules/`, dan `__pycache__/` dilewati secara otomatis.

## Cara Memasang Dependensi

Pastikan Python 3.10+ sudah terpasang, lalu jalankan:

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan

```bash
python cek.py <folder_atau_file>
```

Contoh menjalankan pada folder uji bawaan:

```bash
python cek.py uji
```

Contoh menjalankan pada repositori nyata (misalnya `pallets/itsdangerous`):

```bash
git clone --depth 1 https://github.com/pallets/itsdangerous.git itsdangerous
python cek.py itsdangerous
```

## Contoh Output

### 1. Pengujian pada folder `uji/`

```text
[TODO]    uji\dengan_todo.py:4: # TODO: tambahkan caching Redis agar query database lebih cepat
[TODO]    uji\dengan_todo.py:7: # FIXME: ganti ValueError dengan custom exception aplikasi
[PANJANG] uji\fungsi_panjang.py:8: fungsi 'proses_pesanan_lengkap' (36 baris)
[ERROR]   uji\sintaks_rusak.py:3: syntax error (ERROR di kolom 0)
------------------------------------------------------------
Selesai: 3 file diperiksa | 2 TODO/FIXME | 1 fungsi > 30 baris | 1 file error
```

### 2. Pengujian pada repositori nyata (`pallets/itsdangerous`)

```text
[PANJANG] itsdangerous\src\itsdangerous\serializer.py:190: fungsi '__init__' (45 baris)
[PANJANG] itsdangerous\src\itsdangerous\signer.py:129: fungsi '__init__' (45 baris)
[PANJANG] itsdangerous\src\itsdangerous\signer.py:182: fungsi 'derive_key' (32 baris)
[TODO]    itsdangerous\src\itsdangerous\timed.py:182: # TODO: Signature is incompatible because parameters were added
[PANJANG] itsdangerous\src\itsdangerous\timed.py:72: fungsi 'unsign' (87 baris)
[PANJANG] itsdangerous\src\itsdangerous\timed.py:185: fungsi 'loads' (36 baris)
[PANJANG] itsdangerous\src\itsdangerous\url_safe.py:23: fungsi 'load_payload' (31 baris)
------------------------------------------------------------
Selesai: 15 file diperiksa | 1 TODO/FIXME | 6 fungsi > 30 baris | 0 file error
```

### Verifikasi Manual (2 File Acak)

| File | Hasil `cek.py` | Pengecekan Manual | Status |
| --- | --- | --- | --- |
| `src/itsdangerous/timed.py` | 1 TODO (baris 182), 2 fungsi > 30 baris (`unsign` 87 baris, `loads` 36 baris), 0 error | Baris 182 berisi `# TODO: Signature is incompatible...`; `unsign` baris 72–158 (87 baris); `loads` baris 185–220 (36 baris); fungsi lain ≤ 9 baris; sintaks valid | Cocok |
| `src/itsdangerous/url_safe.py` | 0 TODO, 1 fungsi > 30 baris (`load_payload` 31 baris), 0 error | Tidak ada komentar TODO/FIXME; `load_payload` baris 23–53 (31 baris); `dump_payload` baris 55–69 (15 baris); sintaks valid | Cocok |
