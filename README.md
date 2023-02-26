# ocr-server
API for Image to Text backend

# Installation guide
1. Make sure Python > v3.10 is installed (best version is Python 3.10)
2. Run this command `pip install virtualenv` or `python -m pip install virtualenv` if the former doesn't work
3. Run `cd ocr-server` to navigate into the folder you have cloned
4. Run `virtualenv ENV` or `py -m virtualenv ENV` if the first one doesn't work
5. Run `.\ENV\Scripts\activate` if you're on Command Prompt or `source ./ENV/Scripts/activate` if you're on Bash terminal (Git Bash)
6. If your command prompt have `(ENV)` as the prefix then you're on the right track
7. After success, run `pip install -r requirements.txt` or `py -m pip install -r requirements.txt` if the first one doesn't work
8. After everything is installed, then run `flask --app server --debug run` to start the API server.
9. Enjoy developing!

### Note:
1. Can use `pip freeze > requirements.txt` to save all the dependencies installed.
