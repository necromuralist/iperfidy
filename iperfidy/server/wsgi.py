"""the server WSGI thing"""
# this project
from iperfidy.server.api import application

if __name__ == "__main__":
    application.run()
