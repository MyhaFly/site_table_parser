
import time

from flask import Flask
from flask import jsonify
from flask.globals import request

from utilitys.elibrary_parser import takeDataElibrary


app = Flask(__name__)
 
#http://127.0.0.1:5000/get_info?page_id=100,123,198
@app.route("/get_info")
def get_users_count():
    
    # ID нужных страницы
    page_id = request.args.get('page_id')
    # Перегоняем текст в числа
    page_id = page_id.split(",")
    page_id = [int(x) for x in page_id]
    
    # Вызов функции с парсингом
    rezult = takeDataElibrary(page_id)
    
    return jsonify(rezult)
  
if __name__ == "__main__":
    app.run()