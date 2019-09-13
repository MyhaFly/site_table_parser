from scripts.elibrary_parser import takeDataElibrary, saveRezult

# В каком виде вывести результат csv или json
rezult_type = "csv"
# Имя файла в который сохранить
save_path = "rezult"

# ID нужных страницы
page_id = [100,198]
# Вызов функции с парсингом
rezult = takeDataElibrary(page_id)

# Сохраняем результат
saveRezult(rezult, rezult_type, save_path)