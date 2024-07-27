import os
from sqlalchemy import create_engine
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt

TARGET_WIDTH = 150

DEBUG = False
if DEBUG:
    con = create_engine(
        'postgresql+psycopg2://postgres:iloveai@localhost:5432/postgres')
else:
    con = create_engine(
        f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_ADDRESS")}:5432/{os.getenv("POSTGRES_DB")}')


def get_available_images():
    """
    Retrieves a list of available images from the database.

    SOME DETAILED DCRIPTION blah-blah-blah :)

    Returns:
        dict: A dictionary with a single key "list_available_images". The value 
        associated with this key is a list of table names if the query is 
        successful, or an exception message if an error occurs.

    Example:
        >>> get_available_images()
        {'list_available_images': ['example_image_5460_150', 'example_image_4242_100']}
    """
    try:
        list_available_images = pd.read_sql('''SELECT *
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
        ''', con)['tablename'].to_list()
        response = {"list_available_images": list_available_images}
        return response

    except Exception as e:
        print(f"Ошибка: {e}")
        response = {"list_available_images": e}
        return response


def get_image_slice(min_depth: float, max_depth: float, image_name="example_image_5460_150"):
    """
    Retrieves a slice of image data from the database based on the specified depth range.

    SOME DETAILED DCRIPTION blah-blah-blah :)

    Args:
        min_depth (float): The minimum depth value for the slice.
        max_depth (float): The maximum depth value for the slice.
        image_name (str): The name of the image table in the database. Defaults to "example_image_5460_150".

    Returns:
        np.ndarray: A NumPy array representing the image slice if the operation is successful

    Example:
        >>> get_image_slice(9100.2, 9130.5, "example_image_5460_150")
        array([[[ 42,  42, 42, 42],
                [ 42, 42, 42, 42],
                ...,
                [ 42, 42, 42, 42],
                [ 42, 42, 42, 42]]], dtype=uint8)
    """
    try:
        list_available_images = pd.read_sql('''
            SELECT *
            FROM pg_catalog.pg_tables
            WHERE schemaname = 'public'
        ''', con)['tablename'].to_list()
        if image_name in list_available_images:
            sql = f"""
            SELECT * FROM {image_name}
            WHERE depth >= {min_depth}
                AND depth <= {max_depth}
            """
            image_slice = pd.read_sql(
                sql=sql,
                con=con
            ).iloc[:, :-1].values

            # Custom color map
            color_map = plt.get_cmap("viridis")
            image_slice = color_map(image_slice)
            image_slice = np.round(image_slice * 255).astype(np.uint8)
            response = image_slice
        else:
            response = {
                "Error": f"Requested image '{image_name}' not found. Please check available images using '/api/available_images'"}
        return response
    except Exception as e:
        print(f"Ошибка: {e}")
        response = {"db_response": e}
        return response


def upload_image(csv_path: str, name_in_db='example_image'):
    """
    Uploads an image from a CSV file to the database after processing.

    SOME DETAILED DCRIPTION blah-blah-blah :)

    Args:
        csv_path (str): The path to the CSV file containing the image data.
        name_in_db (str): The name to use for the image table in the database. The final table name 
        will include the dimensions of the resized image (for example n_cols=150). Default name is 'example_image'.

    Returns:
        str: A success message with the name of the uploaded image table, or an exception message if an 
        error occurs.

    Example:
        >>> upload_image('path/to/image.csv', 'my_image')
        "Success. Image has been uploaded to db with name 'my_image_100_256'"
    """
    df = pd.read_csv(csv_path)
    df.dropna(inplace=True)
    depth_col = df['depth'].values
    cols = [col for col in df.columns.to_list() if col.startswith("col")]
    df = df[cols]

    image = df.to_numpy(dtype=np.int16)
    resized_image = cv2.resize(
        src=image,
        dsize=(TARGET_WIDTH, image.shape[0]),
        interpolation=cv2.INTER_LINEAR
    ).astype(np.int16)

    resized_df = pd.DataFrame(resized_image)
    resized_df['depth'] = depth_col

    try:
        resized_df.to_sql(
            name=f"{name_in_db}_{resized_df.shape[0]}_{resized_df.shape[1]-1}",
            con=con,
            index=False,
            if_exists="replace"
        )
        return f"Success. Image has been uploaded to db with name '{name_in_db}_{resized_df.shape[0]}_{resized_df.shape[1]-1}'"
    except Exception as e:
        return e
