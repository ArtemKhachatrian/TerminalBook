from collections import UserDict

from models import Note


class Notebook(UserDict):

    def add(
        self,
        name: str,
        note: Note
    ) -> None:
        self.data[name] = note

    def find(
        self,
        name: str
    ) -> Note | None:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        if name in self.data:
            del self.data[name]
            return True

        return False

    def sort_by_label(self) -> dict:
        result = {}

        for name, note in self.items():
            for label in note.label:
                label = label.lower()

                if label not in result:
                    result[label] = []

                result[label].append(
                    (name, note)
                )

        return dict(sorted(result.items()))