import os
import shutil


def save_upload_cover(contents, filename: str, username: str) -> str:
    upload_dir = os.path.join(os.getcwd(), f'uploads/{username}')
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
        os.makedirs(upload_dir)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    with open(f'{upload_dir}/{filename}', 'wb') as f:
        f.write(contents)

    return upload_dir
