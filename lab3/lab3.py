import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def read_image(file_path) -> np.ndarray:
    """
    Считывает изображение из файла.

    :param file_path: Путь к файлу изображения
    :return: Изображение как массив NumPy, если считывание успешно; иначе None
    """
    image = cv2.imread(file_path)
    return image

def get_image_size(image) -> tuple:
    """
    Получает размер изображения.

    :param image: Изображение как массив NumPy
    :return: Кортеж с размерами (высота, ширина)
    """
    height, width = image.shape[:2]
    return height, width

def plot_histogram(image) -> None:
    """
    Строит гистограмму для цветного изображения.

    :param image: Изображение как массив NumPy
    """
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])
    plt.title('Image histogram')
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.show()

def crop_image(image, size) -> np.ndarray:
    """
    Обрезает изображение до заданных размеров, начиная от левого верхнего угла.

    :param image: Исходное изображение как массив NumPy
    :param size: Кортеж (высота, ширина) для обрезки
    :return: Обрезанное изображение
    """
    height, width = size
    return image[0:height, 0:width]

def display_image(image, title='Image') -> None:
    """
    Отображает изображение с заданным заголовком.

    :param image: Изображение как массив NumPy
    :param title: Заголовок окна
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)

def save_image(image) -> None:
    """
    Сохраняет изображение в файл.

    :param image: Изображение как массив NumPy
    """
    cv2.imwrite('edited6.png', image)

def main(input_path, crop_height, crop_width):
    """
    Основная функция для выполнения всех операций.

    :param input_path: Путь к входному файлу изображения
    :param crop_height: Высота для обрезки
    :param crop_width: Ширина для обрезки
    """
    try:
        # Считываем изображение
        image = read_image(input_path)
        if image is None:
            raise ValueError(f"Failed to load image.")

        # Получаем размер изображения
        height, width = get_image_size(image)
        print(f"Image Size: {height}x{width}")

        # Строим гистограмму
        plot_histogram(image)

        # Если указаны размеры для обрезки, выполняем обрезку
        if crop_height and crop_width:
            if crop_height > height or crop_width > width:
                raise ValueError(f"Crop dimensions exceed image dimensions.")
            image = crop_image(image, (crop_height, crop_width))

        # Отображаем изображение
        display_image(image, title='Cropped image')

        # Сохраняем изображение
        save_image(image)

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Обработка изображения.')
    parser.add_argument('input_path', type=str, help='Путь к файлу изображения')
    parser.add_argument('crop_height', type=int, help='Высота для обрезки')
    parser.add_argument('crop_width', type=int, help='Ширина для обрезки')

    args = parser.parse_args()

    main(args.input_path, args.crop_height, args.crop_width)