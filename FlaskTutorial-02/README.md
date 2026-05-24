# Demo: Create a Maintainable Flask Configuration System

#### This demonstration introduces a controlled configuration layer for the Flask application so the app can run with clear, predictable settings across development, testing, and production. Instead of placing important values directly inside route logic, the application moves configuration into a central pattern that is easier to inspect, update, and extend as the project grows.

#### The configuration system supports production-ready behavior by requiring important environment values before the application starts. When a required setting is missing, the app stops immediately instead of continuing in an incomplete or unsafe state. This makes configuration problems easier to find early and prevents confusing runtime failures later.

#### The demo also supports maintainability by keeping configuration rules organized in one place while still using a single code file. Each environment can have its own behavior without introducing extra platforms, outside APIs, or template files. This keeps the demo simple while showing a pattern that can scale as more settings, routes, tests, and operational needs are added.

#### A safe runtime configuration route is included to show selected application settings without exposing secrets. This provides useful visibility into how the app is running while keeping sensitive values protected. The result is a cleaner Flask foundation that remains easy to understand, safer to change, and better prepared for future production-focused improvements.

#### For this demonstration of a `centralized configuration system` the examples presented are:
- Enforces required environment variables using a **fail-fast approach**
- Separates concerns across **development, testing, and production environments**
- Provides a clear and maintainable pattern for **scaling application configuration**
- Exposes a controlled route to **inspect runtime configuration safely**

---

## Validating Critical Flask Settings Before the App Runs

This example shows why the application should check required environment variables before it starts serving requests. A Flask app can appear to run correctly even when important settings are missing, but that creates hidden problems that may only appear later during testing, deployment, or normal use.<br>

A fail-fast approach makes the application stop immediately when a required value is not set. This turns a hidden configuration problem into a clear startup error that is easier to find and fix. It also supports production-ready behavior because the app does not continue running in an incomplete or unsafe state.<br>

This keeps the application easier to maintain because configuration rules are visible and predictable. It also prepares the app for future growth by creating a clear pattern for adding more required settings as the application expands.<br>

---

**Step 1:** Identify the required settings.

The application needs to know which values must exist before startup. In this demo, `SECRET_KEY` and `FLASK_ENV` are required because they control important application behavior. `SECRET_KEY` supports security-related Flask features, and `FLASK_ENV` decides which configuration class should be loaded.

```text id="pfn037"
SECRET_KEY
FLASK_ENV
```

**Step 2:** Confirm the accepted environment names.

The application should only allow known environment names. This prevents the app from starting with a misspelled or unsupported value such as `staging`, `local`, or `prod`.

```text id="zi32df"
development
testing
production
```

**Step 3:** Set the required values before running the app.

The environment values must be set before the application starts. This gives the Flask app the values it needs without hardcoding them directly into the route logic.

```bash id="f3fh01"
export SECRET_KEY="change-this-local-demo-value"
export FLASK_ENV="development"
```

**Step 4:** Add the base configuration class.

The base configuration class reads required values from the environment. If `SECRET_KEY` is missing, the app raises a clear error before startup continues.

```python id="cf75wc"
class Config:
    """Base configuration with minimal default settings with fast fail for missing critical settings."""
    APP_NAME = os.getenv("APP_NAME", "Flask Application")

    SECRET_KEY = os.getenv("SECRET_KEY")
    if SECRET_KEY is None:
        raise ValueError("SECRET_KEY is not set, exiting application.")
```

**Step 5:** Validate the selected Flask environment.

The application also checks `FLASK_ENV`. If the value is missing or not one of the approved names, the app stops immediately with a clear message.

```python id="k6xyu5"
    FLASK_ENV = os.getenv("FLASK_ENV")
    if FLASK_ENV == None:
        raise ValueError("FLASK_ENV is not set, exiting application.")
    if FLASK_ENV not in ("development", "production", "testing"):
        raise ValueError(f"Invalid FLASK_ENV: {FLASK_ENV}. Must be 'development', 'production', or 'testing', exiting application.")
```

**Step 6:** Load the selected configuration into the Flask app.

The app reads `FLASK_ENV`, finds the matching class, and loads those settings into `app.config`. This keeps the startup process controlled and easier to extend later.

```python id="4z6q24"
flask_env = os.getenv("FLASK_ENV", "production").lower()
config_class = CONFIG_MAPPING.get(flask_env)
app.config.from_object(config_class)
```

**Step 7:** Start the application.

Now the app can be started. If the required settings are present and valid, the app continues running normally.

```bash id="5lo833"
python app.py
```

**Step 8:** Confirm the successful startup path.

Open the home route in the browser. This confirms the app loaded its configuration and is able to serve a normal response.

```text id="dsuwnn"
http://127.0.0.1:5000/
```

Expected browser output:

```text id="9o4m12"
<h1>Flask Demo 3</h1>
<p>Baseline application is running.</p>
```

**Step 9:** Test the missing `SECRET_KEY` failure.

Remove `SECRET_KEY` and start the app again. This confirms the application does not run when a required security value is missing.

```bash id="psoed5"
unset SECRET_KEY
python app.py
```

Expected terminal output:

```text id="7opp6m"
ValueError: SECRET_KEY is not set, exiting application.
```

**Step 10:** Test the missing `FLASK_ENV` failure.

Set `SECRET_KEY`, remove `FLASK_ENV`, and start the app again. This confirms the application does not guess which environment to use when the required environment name is missing.

```bash id="id1aj5"
export SECRET_KEY="change-this-local-demo-value"
unset FLASK_ENV
python app.py
```

Expected terminal output:

```text id="1xx5ai"
ValueError: FLASK_ENV is not set, exiting application.
```

**Step 11:** Test the invalid `FLASK_ENV` failure.

Set `FLASK_ENV` to an unsupported value and start the app again. This confirms the app rejects unknown environment names instead of loading the wrong configuration.

```bash id="7b7br0"
export SECRET_KEY="change-this-local-demo-value"
export FLASK_ENV="staging"
python app.py
```

Expected terminal output:

```text id="d5pdq8"
ValueError: Invalid FLASK_ENV: staging. Must be 'development', 'production', or 'testing', exiting application.
```

**Step 12:** Restore the valid local settings.

After testing the failure paths, restore valid settings so the application can run again for the rest of the demo.

```bash id="b3tt0y"
export SECRET_KEY="change-this-local-demo-value"
export FLASK_ENV="development"
python app.py
```

---

## Review Application Settings with a Protected Configuration View

This example shows why the Flask application needs a controlled way to inspect runtime configuration. As the application grows, it becomes important to confirm which settings were loaded without searching through the code or guessing from terminal output.<BR>

A protected configuration view gives useful visibility into how the application is running while keeping sensitive values controlled. The route should make configuration easier to review, but it should not become a place where secrets are casually exposed or copied into browser output.<BR>

This supports a production-ready and maintainable foundation because runtime behavior can be inspected in a clear and repeatable way. The application remains easier to troubleshoot, safer to review, and better prepared to grow while keeping configuration visibility separate from normal route logic.<BR>

**Step 1:** Add the configuration review route.

This route gives the application one clear place to inspect loaded Flask settings at runtime. It logs when the page is accessed, reads values from `app.config`, formats them as simple raw HTML, and returns the result to the browser without using templates or adding another file.

```python id="w1q6zp"
@app.route('/config')
def config():
    app.logger.info('Configuration page accessed')
    config_items = []
    for key, value in app.config.items():
        config_items.append(f'<b>{key}</b>: {value}')
    return f'<h2>Application Configuration:</h2><br>{"<br>".join(sorted(config_items))}'
```

**Step 2:** Start the application.

The application must be running before the configuration route can be inspected. The required environment values should already be set from the previous examples.

```bash id="z4b7yq"
python app.py
```

**Step 3:** Open the configuration route.

Open the route in the browser to review the loaded application settings.

```text id="u61l1z"
http://127.0.0.1:5000/config
```

Step 4: Confirm the expected browser output.

The browser should show a simple configuration page with loaded Flask settings. The exact values may differ based on the selected runtime and environment values.

```text id="yezn96"
<h2>Application Configuration:</h2><br>
<b>APP_NAME</b>: Flask Application
<b>DEBUG</b>: True
<b>SECRET_KEY</b>: change-this-local-demo-value
```

---

## Keeping Environment-Specific Settings Clear and Controlled

This example shows why a Flask application should separate settings based on how and where the application is running. Different runtime situations often need different behavior, so the configuration should make those differences clear instead of mixing them into route logic or scattering them throughout the code.<BR>

A local setup may need more visibility for troubleshooting, an automated check may need safer test behavior, and a public-facing runtime may need stricter settings. Keeping these concerns separated helps prevent one runtime from accidentally using values or behavior meant for another.<BR>

This supports a production-ready and maintainable foundation because configuration decisions stay organized, predictable, and easier to review. The application remains simple in a single code file while still showing a pattern that can grow as more runtime settings are added.<BR>

---

**Step 1:** Start with a shared base configuration.

The base configuration holds settings that apply across all runtime situations. This keeps common values in one place and prevents repeated configuration rules from being copied into each environment-specific class.

```python id="2kxuyo"
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
```

**Step 2:** Add a configuration class for local troubleshooting behavior.

This class inherits from the shared base configuration and adds behavior that is useful while working locally. The debug setting is controlled by an environment value so it can be changed without editing route code.

```python id="qq4qly"
class DevelopmentConfig(Config):
    """Development configuration with debug settings."""
    DEBUG = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")

    # Additional development-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
```

**Step 3:** Add a configuration class for automated check behavior.

This class keeps test-focused settings separate from normal runtime behavior. It enables testing mode and uses cookie settings that are practical for controlled checks without mixing those settings into the rest of the application.

```python id="hmz6ox"
class TestingConfig(Config):
    """Testing configuration with testing settings."""
    TESTING = os.getenv("FLASK_TESTING", "1") in ("1", "true", "True")

    # Additional testing-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

**Step 4:** Add a configuration class for stricter public-facing behavior.

This class defines safer runtime behavior for a public-facing environment. Debug mode is disabled, logging is stricter by default, and cookie behavior is more secure.

```python id="iuv5j8"
class ProductionConfig(Config):
    """Production configuration with production settings."""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
    DEBUG = False

    # Additional production-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
```

**Step 5:** Create a configuration mapping.

The mapping gives the application one controlled place to connect a runtime name to the correct configuration class. This keeps the selection logic simple and easier to extend later.

```python id="ksg0f7"
CONFIG_MAPPING = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
```

**Step 6:** Read the selected runtime setting.

The application reads the selected runtime value from the environment. This allows the same code file to load different behavior without changing the Python source each time.

```python id="888l5i"
flask_env = os.getenv("FLASK_ENV", "production").lower()
```

**Step 7:** Select the matching configuration class.

The selected runtime value is used to find the matching configuration class. Since the base configuration already validates supported values, the app can load the correct class from the mapping.

```python id="4sbgzb"
config_class = CONFIG_MAPPING.get(flask_env)
```

**Step 8:** Load the selected configuration into Flask.

The selected class is loaded into `app.config`. This makes the chosen settings available to Flask and keeps configuration behavior separate from route behavior.

```python id="e1iryc"
app.config.from_object(config_class)
```

**Step 9:** Start the application with one selected runtime.

Set the required values and choose the runtime behavior before starting the app. This confirms the same code file can behave differently based on controlled configuration.

```bash id="alnlky"
export SECRET_KEY="change-this-local-demo-value"
export FLASK_ENV="development"
python app.py
```

**Step 10:** Confirm the selected configuration through the controlled route.

Open the configuration route in the browser to inspect the loaded settings. This helps confirm which behavior was loaded without changing the application code.

```text id="6x7gjs"
http://127.0.0.1:5000/config
```

Expected browser output will include selected Flask configuration values similar to this.

```text id="yp531l"
<h2>Application Configuration:</h2><br>
...
<b>DEBUG</b>: True
...
```

**Step 11:** Switch to another runtime behavior.

Change the runtime value and restart the application. This shows that the application can load a different configuration class through environment control instead of source code changes.

```bash id="7m89ly"
export SECRET_KEY="change-this-local-demo-value"
export FLASK_ENV="production"
python app.py
```

**Step 12:** Confirm the new runtime behavior.

Open the configuration route again and confirm the loaded setting changed. This shows the configuration classes are separated and controlled by the selected runtime value.

```text id="54p940"
http://127.0.0.1:5000/config
```

Expected browser output will include selected Flask configuration values similar to this.

```text id="kj4ss9"
<h2>Application Configuration:</h2><br>
...
<b>DEBUG</b>: False
...
```

---

## Flask Application

---

```python
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

    # Additional development-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)

# In testing we might want to use a different database URI, and set testing to True 
# to enable testing mode in Flask.
class TestingConfig(Config):
    """Testing configuration with testing settings."""
    TESTING = os.getenv("FLASK_TESTING", "1") in ("1", "true", "True")

    # Additional testing-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

# In production we want to set a higher log level, disable debug mode, and 
# ensure that we have secure settings for cookies and database URI.
class ProductionConfig(Config):
    """Production configuration with production settings."""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
    DEBUG = False

    # Additional production-specific settings can be added here
    FLASK_SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_SQLALCHEMY_DATABASE_URI", None)
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
```

---

## Conclusion

For this demonstration, you created a maintainable configuration system that supports production-ready behavior while keeping the Flask application simple enough to inspect in a single code file. The application now has a clear pattern for loading settings, validating required values, separating runtime behavior, and reviewing selected configuration details through a controlled route.<BR>

The main production lesson is that an application should not start when critical settings are missing or invalid. By enforcing required environment variables with a fail-fast approach, configuration problems are found at startup instead of becoming harder-to-trace failures later. This makes the application safer to run and easier to troubleshoot.<BR>

The maintainability lesson is that configuration should have one predictable home. Instead of scattering settings through route logic, the app uses configuration classes and a mapping pattern to keep runtime-specific behavior organized. This makes the code easier to read, easier to adjust, and easier to extend as more settings are added.<BR>

The scalability lesson is that a small application can still be designed with future growth in mind. The demo does not introduce extra platforms, outside APIs, or template files, but it still creates a structure that can support more routes nad more settings later.<BR>

The controlled configuration route adds useful visibility into how the application is running. It gives a direct way to inspect loaded settings during the demo while reinforcing an important rule: runtime visibility should be intentional, limited, and reviewed carefully so sensitive values are not exposed unnecessarily.<BR>

This demonstration keeps the application aligned with the core goals by staying production ready, easy to maintain, built for scalability, and contained in a single code file. The result is a clearer Flask foundation that can grow without losing control of how the application is configured.<BR>

---

### Demonstration References
## References

1. **[Flask Documentation — Configuration Handling](https://flask.palletsprojects.com/en/stable/config/)**  
   Supports using `app.config`, loading configuration values into Flask, managing built-in configuration values, and organizing application configuration.

2. **[Flask Documentation — Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)**  
   Supports the basic Flask application pattern, route decorators, returning browser responses from routes, and running a simple Flask app.

3. **[Flask Documentation — API: Flask.config](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.config)**  
   Supports the use of the Flask application configuration object through `app.config`.

4. **[Python Documentation — os](https://docs.python.org/3/library/os.html)**  
   Supports using `os.getenv()` and `os.environ` to read environment values used by the Flask configuration classes and runtime inspection route.

5. **[Python Documentation — Exceptions](https://docs.python.org/3/library/exceptions.html)**  
   Supports raising `ValueError` when required configuration values are missing or invalid.

6. **[Python Documentation — html](https://docs.python.org/3/library/html.html)**  
   Supports using `html.escape()` to safely escape values before displaying selected environment data in raw HTML output.

7. **[Flask Documentation — Debug Mode](https://flask.palletsprojects.com/en/stable/debugging/)**  
   Supports the idea that debug behavior should be controlled carefully and should not be treated the same as a public-facing runtime setting.