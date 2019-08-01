from app import App
#from app import api
from app.api_restfull_extension import sockectio
##

if __name__ == '__main__':
    sockectio.run(App)      # use gunicorn to start the server
