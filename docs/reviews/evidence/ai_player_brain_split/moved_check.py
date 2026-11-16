"""Is the package the file, moved? Every top-level definition of the old brain.py, and every method of Brain, is
looked up in the package's files and compared as source text. Prints what differs, what is missing, what is new."""
import ast, difflib, subprocess, sys
base, files = sys.argv[1], sys.argv[2:]
def defs(src):
    tree, out = ast.parse(src), {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out[n.name] = ast.get_source_segment(src, n)
            if isinstance(n, ast.ClassDef):
                for m in n.body:
                    if isinstance(m, ast.FunctionDef):
                        out[f"{n.name}.{m.name}"] = ast.get_source_segment(src, m)
                out[n.name] = ast.get_source_segment(src, n)
        elif isinstance(n, ast.Assign):
            out[n.targets[0].id] = ast.get_source_segment(src, n)
    return out
old = defs(subprocess.run(["git", "show", f"{base}:player/brain.py"], capture_output=True, text=True, check=True).stdout)
new, where = {}, {}
for path in files:
    for name, text in defs(open(path, encoding="utf8").read()).items():
        assert name not in new, f"{name} is defined twice"
        new[name], where[name] = text, path.split("/")[-1]
same = [n for n in old if new.get(n) == old[n]]
print(f"{len(old)} definitions in the old file; {len(same)} are the same text in the package")
for n in old:
    if n not in new:
        print("MISSING:", n)
    elif new[n] != old[n] and not (n == "Brain"):
        print(f"DIFFERS: {n} ({where[n]})")
        for line in difflib.unified_diff(old[n].split("\n"), new[n].split("\n"), lineterm="", n=0):
            if line[:1] in "+-" and line[:3] not in ("+++", "---"):
                print("   ", line)
print("NEW:", sorted(n for n in new if n not in old))
print("by file:", {f: sum(1 for n in old if where.get(n) == f and "." not in n) for f in sorted(set(where.values()))})
