import pickle
from pathlib import Path



DATA_DIR = Path.home() / ".terminal_book"
DATA_DIR.mkdir(exist_ok=True)



def get_data_path(filename: str) -> Path:
    return DATA_DIR / filename


def save_data(
    data,
    filename: str
) -> None:
    filepath = get_data_path(filename)

    with open(filepath, "wb") as file:
        pickle.dump(data, file)


def load_data(filename: str):
    filepath = get_data_path(filename)

    try:
        with open(filepath, "rb") as file:
            return pickle.load(file)

    except (
        FileNotFoundError,
        pickle.UnpicklingError,
        EOFError
    ):
        return None