# Demo 1: Build the Local Foundation for a Production-Ready Flask App

### This demonstration is written for novices who need to build a Flask application that is safe for production, simple to maintain, ready to grow, and easy to test. The work is completed in stages so each step stays approachable while still reflecting habits used in real production projects.

### The application starts small and remains easy to inspect. During the demo, it uses one main code file so the full idea is visible in one place. It avoids extra platforms, outside APIs, and template files. Any HTML returned by the Flask app is written directly in the route response, which keeps the lesson focused on Flask basics instead of hiding behavior in other tools.

Each section strengthens the project in a practical way: improving reliability, making the code easier to manage, and preparing the application for future growth without adding unnecessary structure.

- Set up WSL for use with VS Code

    This creates a Linux-based workspace that more closely matches common server environments than a default desktop setup. It gives the project a cleaner path toward a reliable, production-ready Flask application.

- Create a virtual environment in VS Code

    This keeps project packages separate from the rest of the system. Dependencies stay controlled in one place, which makes the application easier to maintain.

- Build the base application with a simple home route

    This confirms the Flask app can start and respond to a basic request. It gives the project a small working foundation before more structure is added.

- Add a route that displays a filtered list of environment variables with python-dotenv

    This introduces configuration loading without hardcoding values into the app. It supports safer configuration management while keeping the demo in a single code file.

---

## Example: Connect VS Code to WSL for Flask Development

### In this section, WSL becomes the local Linux workspace for the Flask application. Working in an environment similar to many deployment targets helps reduce surprises when the app moves beyond a local machine.

---

Start by installing WSL on Windows and using Ubuntu as the working Linux environment. Open PowerShell as an administrator, then run the installation command.

```powershell
wsl --install
```

✔ **NOTE:** Remember to save your password during setup.

After the computer restarts, confirm that WSL is installed.

```powershell
wsl --list --verbose
```

---

Update Ubuntu packages so the local workspace is current, then install Python, package tools, virtual environment support, and Git.

```powershell
wsl
```

Update Linux packages.

```bash
sudo apt update && sudo apt upgrade -y
```

Install Python and basic tools.

```bash
sudo apt install python3 python3-pip python3-venv git -y
```

Confirm Python is available.

```bash
python3 --version
```

---

Prepare VS Code to work directly inside the WSL Linux environment by opening the Flask workspace through WSL instead of the default Windows environment.

```bash
mkdir -p ~/projects/flask-production-demo
cd ~/projects/flask-production-demo
code .
```

Search the VS Code extensions marketplace for WSL and install the Remote Development extension pack.

> **From VS Code, open the command palette.**<br>
> Ctrl + Shift + P <br>
> **Then select:**<br>
> WSL: Connect to WSL

✔ **NOTE:** Confirm VS Code shows `WSL: Ubuntu` in the lower-left corner.

By the end of this section, VS Code is connected to WSL and the Flask application can be built in a clean Linux-based workspace. This setup is closer to a real server environment, makes local issues easier to repeat and fix, and gives the project a stable place to run and grow.

---

## Example: Prepare a Clean Python Environment for the Flask App

### This part creates a virtual environment for the Flask project inside VS Code. The virtual environment keeps the app’s packages separate from the system Python setup, which makes updates safer and helps each engineer work from a consistent dependency list.

---

Configure VS Code and pip so the Flask environment is easier to build and maintain.

Install the recommended VS Code extensions:

- Python

    https://marketplace.visualstudio.com/items?itemName=ms-python.python

    Provides Python language support, debugging, and interpreter management.

- Markdown All in One

    https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one

    Improves Markdown editing, navigation, and formatting for documentation.

- autoDocstring

    https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring

    Automatically generates Python docstrings to support documentation discipline.

- Black Formatter

    https://black.readthedocs.io/en/stable/

    Black makes code review faster by producing smaller, more consistent diffs.

Open the WSL terminal in VS Code and upgrade pip.

> Press keys: **Ctrl + `**

```bash
python -m pip install --upgrade pip
```

---

Create a clean virtual environment so Flask dependencies stay separate from the system Python installation.

Create a virtual environment inside the project folder.

```bash
python3 -m venv .venv
```

Select the virtual environment in VS Code.

> Ctrl + Shift + P<br>
> Python: Select Interpreter<br>
> Choose:<br>
> `.venv/bin/python`

Activate the virtual environment.

```bash
source .venv/bin/activate
```

Confirm the virtual environment is active.

```bash
which python
python --version
```

---

Install the application framework and record the environment dependencies.

Install Flask.

```bash
python -m pip install Flask
```

Save installed packages.

```bash
python -m pip freeze > requirements.txt
```

At this point, the Flask app has its own isolated Python environment inside the project. Packages are separated from the system setup, the app can be rebuilt from `requirements.txt`, and future changes are easier to manage without adding extra application files.

---

## Example: Create a Working Flask App with a Home Route and Test Error Route

### This section creates the first working Flask application file with two simple routes. The home route confirms the app can respond successfully, while the test error route gives a safe way to observe failure behavior during development.

---

Create the first Flask application file with starter routes.

Create the application file.

```bash
touch app.py
```

Add the base Flask application code to `app.py`.

```python
from flask import Flask

app = Flask(__name__)

# Using flask route decorators to creates routes
@app.route("/")
def home():
    return "<h1>Flask Demo 1</h1>\n<p>Baseline application is running.</p>"

@app.route("/fail")
def fail():
    raise RuntimeError("Intentional failure for testing")

if __name__ == "__main__":
    app.run(debug=True)
```

---

Test the working home route and the intentional error route.

Run the Flask application for the first time.

```bash
python app.py
```

> **NOTE:**<br>
> We use `python app.py` because it starts the app directly from the single code file. This makes it easy to see where the Flask app is created, where the routes are defined, and where the local server starts.<br><br>
> The behavior is different from `flask run`. With `python app.py`, the file runs first, then `app.run()` starts Flask. With `flask run`, Flask looks for the app and starts it without using the `if __name__ == "__main__"` block.<br><br>
> For this demo, `python app.py` is useful because it is simple to repeat and keeps startup behavior clear. It also reinforces that the Flask debug server is for local testing, not for running the app in production.<br><br>

Open the home route in a browser to test the home page.

> **Navigate to:** http://127.0.0.1:5000/

Open the error test route in a browser to observe the failure behavior.

> **Navigate to:** http://127.0.0.1:5000/error

> **NOTE:** You can also see logging in the WSL console while the application is running. Logging will be discussed more in future demonstrations.

This starter app is easy to run, read, and test. The home route proves that the app responds correctly, and the error route gives a controlled way to check failure behavior. Keeping both routes in one file makes the first version easier to understand while still preparing the project for stronger testing and cleaner growth later.

---

## Example: Display Selected Environment Settings with python-dotenv

### This portion shows how the Flask app can read configuration values from a local `.env` file and display only selected settings in the browser. It helps junior engineers understand how to keep settings outside the code while avoiding the risk of exposing secrets.

---

Separate app settings from the Python file while keeping project dependencies documented.

Install python-dotenv in the terminal.

```bash
pip install python-dotenv
```

Save the updated package list.

```bash
pip freeze > requirements.txt
```

Create a local `.env` file.

```bash
touch .env
```

Add safe demo values to the `.env` file.

```text
FLASK_ENV_NAME=local
APP_DISPLAY_NAME=Production Ready Flask Demo
APP_VERSION=1.0.0
LOG_LEVEL=INFO
SECRET_KEY=do-not-display-this-value
```

---

Now load configuration from the environment while keeping browser output simple, controlled, and safer for development.

Update `app.py` to load environment values and display only approved keys.

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

Run the Flask application.

```bash
python app.py
```

Open the environment route in a browser to see the selected settings.

> **Navigate to:** http://127.0.0.1:5000/env

This route moves app settings out of the Python code and into a local environment file. Only approved values appear in the browser, which helps junior engineers practice configuration management without exposing sensitive data. The app stays simple, but it now has a stronger pattern for managing settings across environments.

---

### Conclusion

> In this demonstration, you built the local foundation for a Flask application using production-friendly habits without making the first version harder than necessary. You prepared a Linux-based workspace with WSL and VS Code, then created a dedicated Python environment so the project can manage its own packages independently of the system setup.<br><br>
> You also created a single-file Flask application with a working home route, a controlled error route, and an environment route that reads selected values from a `.env` file. The result is a small but useful application that can be run, tested, and understood before additional structure is introduced.<br><br>
> The main lesson is to make the app clear, repeatable, and safe to change. A production-ready application does not start with complexity. It starts with a clean setup, controlled dependencies, visible behavior, and configuration that is not hardcoded into the application logic.<br><br>
> This demo remains easy to maintain because each step has a clear purpose. It also supports future growth because the app already separates setup, dependencies, routes, and configuration habits while still using one Flask code file, raw HTML output, and no extra platforms.<br><br>

---

### Useful References

- **[Microsoft Learn — Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)**  
   Supports installing WSL with `wsl --install` and checking installed Linux distributions with `wsl --list --verbose`.

- **[Microsoft Learn — Set up a WSL development environment](https://learn.microsoft.com/en-us/windows/wsl/setup/environment)**  
   Supports using WSL as a local development environment and connecting it with VS Code.

- **[Microsoft Learn — Get started using VS Code with WSL](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)**  
   Supports authoring and debugging code in VS Code through Windows Subsystem for Linux.

- **[VS Code Documentation — Developing in WSL](https://code.visualstudio.com/docs/remote/wsl)**  
   Supports using the VS Code WSL extension to develop in a Linux-based environment from Windows.

- **[Flask Documentation — Installation](https://flask.palletsprojects.com/en/stable/installation/)**  
   Supports creating an environment and installing Flask with `pip install Flask`.

- **[Flask Documentation — Quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)**  
   Supports the basic Flask app pattern, route creation, and running a minimal Flask application.

- **[Python Documentation — `venv`](https://docs.python.org/3/library/venv.html)**  
   Supports creating isolated Python virtual environments for project-specific packages.

- **[Python Tutorial — Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)**  
   Supports using a `.venv` folder and managing project packages in an isolated environment.

- **[python-dotenv on PyPI](https://pypi.org/project/python-dotenv/)**  
   Supports installing `python-dotenv` and loading environment values from a `.env` file.
