import argparse
import pandas as pd
import cv2
import matplotlib.pyplot as plt

def create_dataframe_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Загружает пути к изображениям из файла CSV, считывает изображения и записывает их высоту, ширину и глубину. Также печатает статистическую информацию.
    :param csv_path: Путь к CSV-файлу, содержащему пути к изображениям.
    :return: DataFrame, содержащий свойства изображений, пути и статистическую информацию.
    """
    try:
        df = pd.read_csv(csv_path, names=['absolute_path', 'relative_path'])
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")

    if 'absolute_path' not in df.columns:
        raise ValueError("The CSV must contain the 'absolute_path' column.")

    heights = []
    widths = []
    depths = []

    for img_path in df['absolute_path']:
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}. Check the path!")
            heights.append(None)
            widths.append(None)
            depths.append(None)
        else:
            heights.append(img.shape[0])
            widths.append(img.shape[1])
            depths.append(img.shape[2])

    df['Height'] = heights
    df['Width'] = widths
    df['Depth'] = depths

    # Вычисляем статистическую информацию
    stats = df[['Height', 'Width', 'Depth']].describe()
    print(stats)

    return df

def filter_dataframe(df: pd.DataFrame, max_height: str, max_width: str)-> pd.DataFrame:
    """
    Фильтрует DataFrame по максимальной высоте и ширине.
    :param df: DataFrame, содержащий свойства и пути изображений.
    :param max_height: Максимально допустимая высота изображений.
    :param max_width: Максимально допустимая ширина изображений.
    :return: Отфильтрованный DataFrame, содержащий только изображения указанных размеров.
    """
    return df[(df['Width'] <= int(max_width)) & (df['Height'] <= int(max_height))]

def add_area_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Вычисляет площадь изображения
    :param df: DataFrame, содержащий свойства и пути изображений.
    :return: DataFrame, содержащий свойства изображений, пути и площади.
    """
    df['Area'] = df['Height'] * df['Width']
    return df

def plot_area_distribution(df: pd.DataFrame) -> None:
    """
    Рисует гистограмму по площади
    :param df: DataFrame, содержащий свойства изображений, пути и площади.
    """
    if 'Area' in df.columns:
        df.hist(column="Area", bins=len(df))
        plt.title("Histogram by area")
        plt.xlabel("Area")
        plt.ylabel("Count")
        plt.show()
    else:
        print("Column 'Area' is missing from DataFrame.")

def main() -> None:
    try:
        parser = argparse.ArgumentParser(description='Processing images from a CSV file.')

        parser.add_argument('csv_path', type=str, help='Path to the annotation file in CSV format.')
        parser.add_argument('max_width', type=str, help='Maximum width (integer).')
        parser.add_argument('max_height', type=str, help='Maximum height (integer).')

        args = parser.parse_args()

        #Демонстрация работы
        df_images = create_dataframe_from_csv(args.csv_path)
        print("Source DataFrame:")
        print(df_images)

        filtered_df = filter_dataframe(df_images, args.max_height, args.max_width)
        print("Filtered DataFrame:")
        print(filtered_df)

        filtered_df = add_area_column(df_images)
        sorted_df = filtered_df.sort_values(by='Area')
        print("Sorted DataFrame by area:")
        print(sorted_df)

        plot_area_distribution(sorted_df)

    except Exception as exp:
        print(f"An error occurred: {exp}")


if __name__ == "__main__":
    main()
