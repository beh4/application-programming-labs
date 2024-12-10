import csv

class ImageIterator:
    def __init__(self, annotation_file: str) -> None:
        """
        Итератор для обработки изображений на основе файла с аннотацией.

        :param annotation_file: Путь к CSV-файлу с аннотацией.
        """
        self.file = open(annotation_file, newline='', encoding='utf-8')
        self.reader = csv.reader(self.file, delimiter=';')
        self.header = next(self.reader, None)

    def __iter__(self) -> 'ImageIterator':
        return self

    def __next__(self) -> str:
        """
        Возвращает абсолютный путь к следующему изображению.

        :return: Абсолютный путь к изображению.
        :raises StopIteration: Если изображения закончились.
        """
        try:
            absolute_path = next(self.reader)[0]
            return absolute_path.strip()
        except StopIteration:
            self.file.close()
            raise
