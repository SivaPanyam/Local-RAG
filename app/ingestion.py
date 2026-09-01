from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_documents(folder_path: str = "./watch_folder"):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    documents = []

    for file_path in folder.iterdir():
        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

        elif extension in {".txt", ".md"}:
            loader = TextLoader(
                str(file_path),
                encoding="utf-8",
            )
            documents.extend(loader.load())

    return documents