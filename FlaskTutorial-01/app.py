import os
import html
from flask import Flask

# initialize Flask application
app = Flask(__name__)

# Using flask route decorators to creates routes
@app.route("/")
def home():
    return "<h1>Flask Demo 1</h1>\n<p>Baseline application is running.</p>"

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

# IMPORTANT below will allow for simple execution in development
# however in production WSGI servers like Passenger will treat 
# app.py as a python module. This familiar piece of code prevents
# flask from lauching when importing this file as a module.
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)