from flask import Flask
from flask import url_for

from flask_cors import CORS

from dt_endpoints.endpoint_home import home_page

application = Flask(__name__)
# CORS(application)


application.register_blueprint(home_page, url_prefix='')

# dtdb.init()


if __name__ == "__main__":
    application.run(host='0.0.0.0')
