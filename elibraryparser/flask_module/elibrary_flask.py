
import time

from flask import Flask
from flask import jsonify

from utilitys.elibrary_parser import takeDataElibrary


app = Flask(__name__)
 
#http://127.0.0.1:5000/get_users_count
@app.route("/get_organization_info")
def get_users_count():
    
    page_id = [100, 123, 198]
    rezult = takeDataElibrary(page_id)
    
    return jsonify(rezult)
  
if __name__ == "__main__":
    app.run()