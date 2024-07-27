# Get Slices from DB Images API

This FastAPI application allows users to interact with image data stored in a database. The API provides endpoints to upload image data, retrieve a list of available images, and get slices of images based on specified depth parameters.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [GET `/`](#get-)
  - [GET `/api/available_images`](#get-apiavailable_images)
  - [POST `/api/get_slice`](#post-apigetslice)
  - [POST `/api/upload_image`](#post-apiupload_image)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/aesedeu/iloveai.git
    cd yourrepository
    ```
2. **Start the application**
    ```sh
    docker-compose up -d
    ```

    Two containers will be created (api-container + postgres-container)

## Usage

Once the application is running, you can interact with the API using tools like `curl`, `httpie`, or Postman. Below are the details of the available endpoints.

## API Endpoints

### GET `/`

Returns basic information about the API.

- **Response**:
    ```json
    {
        "Api_Name": "Get slices"
    }
    ```

### GET `/api/available_images`

Retrieves a list of available images in the database.

- **Response**:
    ```json
    {
        "list_available_images": [
            "example_image_5460_150",
            "open_innovation_image_42_42"
        ]
    }
    ```

### POST `/api/get_slice`

Retrieves a slice of the specified image from the database based on depth parameters.

- **Request Body**:
    ```json
    {
        "min_depth": 9100.2,
        "max_depth": 9130.5,
        "image_name":"example_image_5460_150"
    }
    ```

- **Response**:
    - On success: Returns the image slice as a PNG file.
    - On error: Returns an error message.
    ```json
    {
        "Error": "Requested image 'example_image_5460_150' not found. Please check available images using '/api/available_images'"
    }
    ```


# Additional info for the reviwer(s)

1. autopep8 and pylint were used to check code quality
2. Minimal tests I wrote just to check api endpoints
3. In the task nothing were said regarding CI/CD pipelines so it's haven't been done
4. Docstrings written not very detailed. Just for example (but I write them everytime detailed as much as possible)