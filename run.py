from werkzeug.serving import run_simple
from combine import application

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True, use_evalex=True)

