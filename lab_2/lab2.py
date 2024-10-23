import os
import csv
import argparse
from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler


def download_images(keyword: str, num_images: int, download_path: str) -> None:
    """
    Скачивает изображения по заданному ключевому слову.

    :param keyword: Ключевое слово для поиска изображений (строка).
    :param num_images: Количество изображений для загрузки (целое число).
    :param download_path: Путь к папке для сохранения загруженных изображений (строка).
    :return: None
    """
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    crawler = GoogleImageCrawler(storage={"root_dir": download_path},
        feeder_threads=1,
        parser_threads=2,
        downloader_threads=4)
    crawler.crawl(keyword=keyword, max_num=num_images)


def create_annotation_csv(download_path: str, csv_path: str) -> None:
    """
    Создает CSV-файл с аннотацией для загруженных изображений.

    :param download_path: Путь к папке с изображениями (строка).
    :param csv_path: Путь к CSV-файлу для сохранения аннотации (строка).
    :return: None
    """
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['absolute_path', 'relative_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(download_path):
            for file in files:
                absolute_path = os.path.join(root, file)
                relative_path = os.path.relpath(absolute_path, download_path)
                writer.writerow({'absolute_path': absolute_path, 'relative_path': relative_path})


class ImageIterator:
    def __init__(self, annotation_file: str) -> None:
        """
        Итератор для обработки изображений на основе файла с аннотацией.

        :param annotation_file: Путь к CSV-файлу с аннотацией (строка).
        """
        self.file = open(annotation_file, newline='', encoding='utf-8')
        self.reader = csv.DictReader(self.file)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        """
        Возвращает путь к следующему изображению.

        :return: Путь к изображению (строка).
        :raises StopIteration: Если изображения закончились.
        """
        try:
            return next(self.reader)['absolute_path']
        except StopIteration:
            self.file.close()
            raise

# Функция для демонстрации итератора
def display_images(image_iterator)-> None:
    """
    Выводит пути изображений в цикле

    :param image_iterator: Итератор.
    """
    for img_path in image_iterator:
        print(img_path)

def main():
    parser = argparse.ArgumentParser(description='Скачать изображения коров и создать аннотацию.')
    parser.add_argument('keyword', type=str, help='Ключевое слово для поиска изображений.')
    parser.add_argument('num_images', type=int, help='Количество изображений для загрузки (от 50 до 1000).')
    parser.add_argument('download_path', type=str, help='Путь к папке для сохранения изображений.')
    parser.add_argument('csv_path', type=str, help='Путь к файлу аннотации в формате CSV.')

    args = parser.parse_args()

    download_images(args.keyword, args.num_images, args.download_path)
    create_annotation_csv(args.download_path, args.csv_path)

    image_iterator = ImageIterator(args.csv_path)

    display_images(image_iterator)

if __name__ == '__main__':
    main()