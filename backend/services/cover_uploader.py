import os
import shutil


def save_upload_cover(cover) -> str:
    upload_dir = os.path.join(os.getcwd(), 'uploads')

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(upload_dir, cover.filename)

    with open(dest, 'wb') as buffer:
        shutil.copyfileobj(cover.file, buffer)

    return dest