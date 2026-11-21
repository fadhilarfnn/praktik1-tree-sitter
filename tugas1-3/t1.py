import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parse
r(Language(tspython.language()))

kode = b"x = 1\n"
tree = parser.parse(kode)
print(tree.root_node)

kode = b"def kali(x, y):\n  return x*y\n"
tree = parser.parse(kode)
print(tree.root_node)

kode = b"if x == y:\n    print('sama')\nelse: print('beda')"
tree = parser.parse(kode)
print(tree.root_node)

kode = b"class angka:\n def kuadrat(self, x):\n return x*x"
tree = parser.parse(kode)
print(tree.root_node)

kode_fungsi = b"def kali(x, y):\n    return x*y\n"
tree_fungsi = parser.parse(kode_fungsi)
fungsi_node = tree_fungsi.root_node.children[0]

print()
for c in fungsi_node.children:
    print(c.type, "bernama" if c.is_named else "anonim")
    if c.type == "parameters":
        for p in c.children:
            print("   ", p.type, "bernama" if p.is_named else "anonim")

print()
kode_rusak = b"def kaii(x, y)\n    return x*y\n"
tree_rusak = parser.parse(kode_rusak)
print(tree_rusak.root_node)