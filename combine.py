from werkzeug.middleware.dispatcher import DispatcherMiddleware
from current_weather import app as flask_app_10
from dynamic_discount import app as flask_app_11
from formation import app as flask_app_12
from player_search_response import app as flask_app_13
from team_search_response import app as flask_app_14
from turf_search_response import app as flask_app_15
from weather_prediction import app as flask_app_16
from wellcome import app as flask_app_17


application = DispatcherMiddleware(flask_app_17,{
    "/dynamic_discount": flask_app_11,
    "/current_weather":flask_app_10,
    "/formation":flask_app_12,
    "/player_search_response":flask_app_13,
    "/team_search_response":flask_app_14,
    "/turf_search_response":flask_app_15,
    "/weather_prediction":flask_app_16,
})