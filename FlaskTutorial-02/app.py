import os
import html
from flask import Flask

# create Configuration classes for different environments 
# and set the appropriate setting from the environment variables or default values
class Config:
    """Base configuration with minimal default settings with fast fail for missing critical settings."""
    APP_NAME = os.getenv("APP_NAME", "Flask Application")

    SECRET_KEY = os.getenv("SECRET_KEY")
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set, exiting application.")

    FLASK_ENV = os.getenv("FLASK_ENV")
    if FLASK_ENV == None:
        raise ValueError("FLASK_ENV is not set, exiting application.")
    if FLASK_ENV not in ("development", "production", "testing"):
        raise ValueError(f"Invalid FLASK_ENV: {FLASK_ENV}. Must be 'development', 'production', or 'testing', exiting application.")

# Each environment can have its own specific settings, but they will all inherit from the base Config class.
# This allows us to have a common set of settings and then override or add specific settings for each environment as needed.
# In development we might want to enable debug mode and set a different log level, while in production we would want to enable 
# debug mode and set a higher log level.
class DevelopmentConfig(Config):
    """Development configuration with debug settings."""
    DEBUG = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")

# In testing we might want to use a different database URI, and set testing to True 
# to enable testing mode in Flask.
class TestingConfig(Config):
    """Testing configuration with testing settings."""
    TESTING = os.getenv("FLASK_TESTING", "1") in ("1", "true", "True")

    # Additional testing-specific settings can be added here
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

# In production we want to set a higher log level, disable debug mode, and 
# ensure that we have secure settings for cookies and database URI.
class ProductionConfig(Config):
    """Production configuration with production settings."""
    DEBUG = False

    # Additional production-specific settings can be added here
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

CONFIG_MAPPING = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}

# initialize Flask application
app = Flask(__name__)

# load configuration based on FLASK_ENV environment variable
# remember to set FLASK_ENV in your environment or app will fail to start.
flask_env = os.getenv("FLASK_ENV", "production").lower()
config_class = CONFIG_MAPPING.get(flask_env)
app.config.from_object(config_class)

# Using flask route decorators to creates routes
@app.route("/")
def home():
    return "<h1>Flask Demo 3</h1>\n<p>Baseline application is running.</p>"

@app.route("/fail")
def fail():
    raise RuntimeError("Intentional failure for testing")

@app.route("/env")
def env():
    # allowed list of environment variables.
    allowed_env_vars = [
        "HOSTNAME", "PWD",
        "USER", "HOME",
        "PATH", "LANG",
        "APP_DISPLAY_NAME", "APP_VERSION", 
        "LOG_LEVEL", "SECRET_KEY", 
        "FLASK_ENV_NAME", "FLASK_DEBUG"
    ]

    # create dictionary of allowed environment key / value pairs.
    env_data = {
        k: v for k, v in os.environ.items()
        if k in allowed_env_vars
    }

    # add environmental pairs into a list of html represention
    # of the pairs.
    rows = "\n".join(
        f"<b>{html.escape(k)}:</b>{html.escape(v)}<br>"
        for k, v in sorted(env_data.items())
    )

    # return simple html output to browser as response.
    return f"<h1>Runtime Environment (Filtered)</h1>\n{rows}"

# route for visualizing flask application configuration
@app.route('/config')
def config():
    config_items = []
    for key, value in app.config.items():
        config_items.append(f'<b>{key}</b>: {value}')
    return f'<h2>Application Configuration:</h2><br>{"<br>".join(sorted(config_items))}'

# IMPORTANT below will allow for simple execution in development
# however in production WSGI servers like Passenger will treat 
# app.py as a python module. This familiar piece of code prevents
# flask from lauching when importing this file as a module.
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)