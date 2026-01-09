import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image

# Base directory for storing uploads (you can adjust this)
UPLOAD_DIR = "images"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile, subfolder: str = "") -> str:
    """
    Save an uploaded image to a specified folder.
    
    Args:
        file (UploadFile): The uploaded image file.
        subfolder (str): Optional subfolder inside uploads/images.

    Returns:
        str: The saved image path.
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, JPG, and PNG allowed.")

    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"

    # Determine save path
    folder_path = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, unique_name)

    # Save file to disk
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Validate image
    try:
        Image.open(file_path).verify()
    except Exception:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    return file_path


def delete_image(file_path: str) -> bool:
    """
    Delete an image file if it exists.

    Args:
        file_path (str): Path to the image file.

    Returns:
        bool: True if deleted, False if not found.
    """
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
