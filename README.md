# Production-First Flask Demonstration Guide

A production-first Flask application does not begin with extra layers, hidden behavior, or a large folder tree. It begins with a small app that is easy to run, easy to read, and safe to change. The supplied Demo 1 README shows this clearly by starting inside VS Code and WSL, using a clean Python environment, creating one visible Flask file, returning raw HTML directly from route functions, and adding only the pieces needed to prove that the application can run, fail in a controlled way, and show selected runtime settings.

The core goals are production ready, easily maintainable, built for scalability, and guided by a security first mindset. In this approach, production ready means the app is shaped for real deployment habits from the start, even while it remains small. Easily maintainable means a future change can be made without guessing where behavior is hidden. Built for scalability means the first version does not block later growth. Security first means the app avoids careless exposure of settings and keeps output controlled.

The Demo 1 README represents these goals through restraint. It uses WSL because a Linux-based local workspace is closer to common server environments than a default desktop setup. It uses VS Code connected to WSL so the editor, terminal, and Python tools operate in the same place. It creates a virtual environment so dependencies belong to the project instead of the machine. It records dependencies so the environment can be rebuilt. It creates a small Flask app in one file so the entry point, routes, and local run behavior remain visible.

This guide keeps the same limits. It uses only pure Flask features. It assumes WSGI deployment is the standard production path. It keeps the application in a single code file for these demonstrations. It does not use templates, so HTML is returned as raw strings from route functions. That choice keeps the lesson focused on Flask behavior and avoids hiding output in a second file before the application needs that structure.

## Example: Demo 1 as the Local Foundation

Demo 1 begins by placing development inside WSL and opening the project through VS Code. That is a production-aligned choice because it reduces the gap between local work and server behavior. The commands in the demo create a clean workspace, install Python tools, and open the folder from the Linux side.

```bash
mkdir -p ~/projects/flask-production-demo
cd ~/projects/flask-production-demo
code .
```

The important lesson is not the folder name. The lesson is that the project should live in a place that can be repeated, inspected, and rebuilt. A stable workspace makes the application easier to support because the editor, terminal, and Python interpreter all point at the same project.

The next production-first move is the virtual environment. A Flask app should not depend on whatever packages happen to be installed on the system. The environment should be created inside the project and selected in VS Code so the app, terminal, and editor agree on the Python interpreter.

```bash
python3 -m venv .venv
source .venv/bin/activate
which python
python --version
```

After Flask is installed, the dependency list is saved. This is a small habit, but it is one of the clearest maintainability wins in the demo because the project can be rebuilt from a known package list.

```bash
python -m pip install Flask
python -m pip freeze > requirements.txt
```

The first Flask code stays small on purpose. The home route proves the app can respond. The failure route proves that failure behavior can be triggered on demand during development. Both routes return raw strings, which follows the demonstration rule to avoid templating.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Flask Demo 1</h1>\n<p>Baseline application is running.</p>"

@app.route("/fail")
def fail():
    raise RuntimeError("Intentional failure for testing")

if __name__ == "__main__":
    app.run(debug=True)
```

This starter code should be treated as a stepping stone, not as the final production shape. The `debug=True` setting is useful for local learning, but it should not be carried into a WSGI deployment. The final pattern in the supplied material improves this by keeping local execution inside the `if __name__ == "__main__"` guard while leaving the `app` object available for a WSGI server to import.

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

That guard matters. In production, a WSGI server imports the Python file as a module and looks for the Flask application object. The guard prevents the development server from starting just because the file was imported. This is a simple example of production-first thinking: the local path remains easy, but the deployment path is not blocked.

Configuration is introduced through environment values. The demo’s `/env` route does not print every setting it can find. It builds an allowed list, filters the environment, escapes the output, and then renders only the approved values. That pattern supports a security first mindset because the application controls what it reveals.

```python
import os
import html
from flask import Flask

app = Flask(__name__)

@app.route("/env")
def env():
    allowed_env_vars = [
        "HOSTNAME", "PWD",
        "USER", "HOME",
        "PATH", "LANG",
        "APP_DISPLAY_NAME", "APP_VERSION",
        "LOG_LEVEL", "SECRET_KEY",
        "FLASK_ENV_NAME", "FLASK_DEBUG"
    ]

    env_data = {
        k: v for k, v in os.environ.items()
        if k in allowed_env_vars
    }

    rows = "\n".join(
        f"<b>{html.escape(k)}:</b>{html.escape(v)}<br>"
        for k, v in sorted(env_data.items())
    )

    return f"<h1>Runtime Environment (Filtered)</h1>\n{rows}"
```

The escaping is just as important as the filter. Raw HTML output is allowed in this demonstration, but raw user-controlled or environment-controlled text should not be trusted. The `html.escape` call keeps values from being treated as HTML by the browser. That is the kind of small, steady security choice that belongs in the first version rather than being added after the app grows.

The final single-file version from the supplied material brings these ideas together. It keeps the app importable for WSGI, keeps the routes visible, keeps HTML raw, and keeps environment output filtered and escaped.

```python
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
```

The production lesson in this file is that simplicity is not the same as carelessness. A single file can still have clear startup behavior, controlled configuration display, escaped output, and a route that helps test failure behavior. Those choices make the app easier to maintain because each behavior is visible and named.

The logging goal should continue from the same foundation. Demo 1 already points attention to console output when the app is running and includes a controlled failure route. A production-first logging demonstration should use that route to show how failures are recorded, how log level is controlled through configuration, and how noisy local output can be separated from useful application messages. Because the supplied README does not include a completed logging implementation, this guide does not add a logging example that was not present in the demo.

The scalability goal should also build from the same foundation. Demo 1 keeps the app in one file so the behavior is visible before more shape is added. A later refactor can introduce blueprints and Python modules when the app has enough routes to justify that move. That refactor should not change the user-facing behavior first. It should move working behavior into clearer places while keeping the app importable for WSGI and testable from the outside. Because the supplied README keeps the demonstration in one code file, this guide treats that single-file design as the current demonstration boundary.

The testing goal follows naturally from the home route, the failure route, and the environment route. A production-first test demonstration should confirm that the home route returns a successful response, that the environment route only shows allowed settings, and that failure behavior is predictable. Since the supplied README does not include unit test files or test commands, this guide does not add a test example beyond explaining how the existing routes prepare the app for testing.

The strongest habit in Demo 1 is controlled growth. The project starts with a real development environment, a clean dependency boundary, a visible Flask app, and safe configuration display. It avoids templates, avoids extra platforms, and avoids adding structure before there is a reason for it. That is the production-first approach: build a small version that can be trusted, then expand only when the next demonstration needs the extra shape.
