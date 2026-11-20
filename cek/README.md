# Pemeriksa Kode & Syntax Tree (`cek.py`)

Skrip `cek.py` digunakan untuk memeriksa file atau direktori proyek menggunakan parser Tree-sitter guna mendeteksi kesalahan sintaksis (`ERROR`), penanda `TODO/FIXME`, serta fungsi yang panjangnya lebih dari 30 baris.

## Cara Menjalankan

Jalankan dari folder `cek/`:

```powershell
python cek.py ..\tree-sitter-filter