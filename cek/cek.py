import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

BATAS_BARIS = 30
FOLDER_DILEWATI = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def cari_error_pertama(node):
    """Cari node pertama yang bertipe ERROR atau MISSING secara rekursif (DFS)."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_error or child.is_missing:
            hasil = cari_error_pertama(child)
            if hasil is not None:
                return hasil
    return None


def cek_file(path: Path, ringkasan: dict):
    tree = parser.parse(path.read_bytes())
    root = tree.root_node
    ringkasan["file"] += 1

    # Fitur 1: komentar TODO / FIXME
    captures = QueryCursor(Q_TODO).captures(root)
    for node in sorted(captures.get("c", []), key=lambda n: n.start_byte):
        baris = node.start_point[0] + 1
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO]    {path}:{baris}: {teks}")
        ringkasan["todo"] += 1

    # Fitur 2: fungsi dengan panjang > 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(root):
        fungsi_list = cap.get("fungsi", [])
        nama_list = cap.get("nama", [])
        if not fungsi_list or not nama_list:
            continue
        fungsi = fungsi_list[0]
        nama = nama_list[0].text.decode(errors="replace")
        jumlah_baris = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah_baris > BATAS_BARIS:
            baris = fungsi.start_point[0] + 1
            print(f"[PANJANG] {path}:{baris}: fungsi '{nama}' ({jumlah_baris} baris)")
            ringkasan["panjang"] += 1

    # Fitur 3: file yang pohon sintaksnya mengandung error
    if root.has_error:
        err = cari_error_pertama(root)
        if err is not None:
            baris = err.start_point[0] + 1
            kolom = err.start_point[1]
            if err.is_missing:
                detail = f"MISSING '{err.type}' di kolom {kolom}"
            else:
                detail = f"ERROR di kolom {kolom}"
            print(f"[ERROR]   {path}:{baris}: syntax error ({detail})")
        else:
            print(f"[ERROR]   {path}: syntax error terdeteksi")
        ringkasan["error"] += 1


def main():
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder_atau_file>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Path tidak ditemukan: {target}")
        sys.exit(1)

    ringkasan = {"file": 0, "todo": 0, "panjang": 0, "error": 0}

    if target.is_file():
        cek_file(target, ringkasan)
    else:
        for path in sorted(target.rglob("*.py")):
            if any(part in FOLDER_DILEWATI for part in path.parts):
                continue
            cek_file(path, ringkasan)

    print("-" * 60)
    print(
        f"Selesai: {ringkasan['file']} file diperiksa | "
        f"{ringkasan['todo']} TODO/FIXME | "
        f"{ringkasan['panjang']} fungsi > {BATAS_BARIS} baris | "
        f"{ringkasan['error']} file error"
    )


if __name__ == "__main__":
    main()
