import os

def show_branches():
    branches_dir = "promts"
    if not os.path.exists(branches_dir):
        return "Ветки не найдены. Каталог веток не существует."

    branches = os.listdir(branches_dir)
    if not branches:
        return "Ветки не найдены."

    return "Доступные ветки:\n" + "\n".join(sorted(branches))
