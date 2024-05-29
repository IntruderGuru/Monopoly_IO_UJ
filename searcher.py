import os
from pathlib import Path


def get_all_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    return python_files


def save_files_content_to_text(python_files, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for file in python_files:
            with open(file, "r", encoding="utf-8") as py_file:
                content = py_file.read()
                f.write(f"{file}\n{content}\n\n")


def main():
    directory = "C:/Users/barte/OneDrive/Pulpit/Studia/ROK II/Semestr 4/IO/ProjektFUN/Monopoly_IO_UJ"  # Zmień na właściwą ścieżkę do katalogu
    output_file = "output.txt"

    python_files = get_all_python_files(directory)
    save_files_content_to_text(python_files, output_file)
    print(f"Zapisano zawartość {len(python_files)} plików .py do {output_file}")


if __name__ == "__main__":
    main()
