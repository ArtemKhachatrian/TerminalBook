import pickle


def save_data(data, filename):
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data(filename):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None