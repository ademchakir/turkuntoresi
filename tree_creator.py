from pathlib import Path
from rich.console import Console
from rich.tree import Tree


def build_tree(directory: Path, tree: Tree, ignore_list: list[str] = None) -> None:
    if ignore_list is None:
        ignore_list = []

    # Önce mevcut dizinin içeriğini filtrele
    paths = []
    for path in sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
        # Dosya/klasör adı ignore listesinde mi?
        if path.name in ignore_list:
            continue

        # Dosya uzantısı ignore listesinde mi?
        if path.is_file():
            file_extension = f".{path.name.split('.')[-1]}" if '.' in path.name else ''
            if file_extension in ignore_list:
                continue

        paths.append(path)

    # Eğer filtrelenmiş liste boşsa, bu klasörü gösterme
    if not paths:
        return

    # Filtrelenmiş listedeki dosya ve klasörleri işle
    for path in paths:
        if path.is_dir():
            branch = tree.add(f"[bold]{path.name}[/]")
            build_tree(path, branch, ignore_list)
        else:
            tree.add(path.name)


console = Console()
root_path = Path("")
tree = Tree(f":open_file_folder: [link=file://{root_path.resolve()}]{root_path.name}[/link]")

build_tree(root_path, tree, ignore_list=[
    "node_modules",
    ".git",
    ".venv",
    "postgres_data",
    "__pycache__",
    ".idea",
    "versions",
    ".ttf",
    ".svg",
    ".TAG",
    ".gitignore",
    ".md",
    ".pytest_cache",
    ".vscode",
    "__init__.py",
    "apkcikti",
    "data",
    "nifti_output",
    "probe_payloads",
    "prostate_mri_anatomy",
    "constructed_images",
    "templates",
    "prostate-mri-T2w-v05",
    "unet",
    "ultrasound_images",
])

console.print(tree)

print("Klasör yapım bu şekildedir.")
print("Frontend ve backendi olan bir proje yapısıdır.")
print("Backenddeki veriler JSON dosyalarında tutulmaktadır.")
print("Lütfen düzelteceğin kodlarda terminalde bulunmam gereken klasöre dikkat et.")
print("Değişmesi gerekiyorsa kendin değiştir.")
print("Yukarıdaki proje ağacıma göre kodları düzenle.")
print("Aldığım hatalar aşağıdaki gibidir:")
print("")
