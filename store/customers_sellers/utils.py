import os
from django.conf import settings


def remove_previous_image(media_path):
    """Функция удаления файла (Изображения) и и папки, в которой файл хранится (если он пустой)"""

    try:
        path = settings.BASE_DIR.joinpath('media', media_path)
        os.remove(path)
    except:
        pass
    else:
        parent_path = path.parent
        try:
            os.rmdir(parent_path)
        except OSError as e:
            print(f'Ошибка удаления: {e}')