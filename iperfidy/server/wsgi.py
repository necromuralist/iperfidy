"""the server WSGI thing"""
import connexion


application = connexion.FlaskApp(__name__)
application.add_api("swagger.yaml")

if __name__ == "__main__":
    application.run()
