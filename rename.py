import os

import os

old_name='README_RUS.md'
new_name='README.md'
# Рекурсивный обход всех файлов и директорий в текущем каталоге
for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename==old_name:
            # print(f'{dirpath}/{filename} -> {dirpath}/{new_name}')
            os.renames(os.path.join(dirpath, filename), os.path.join(dirpath, new_name))
