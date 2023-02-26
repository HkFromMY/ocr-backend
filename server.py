from app.main import create_app
from app.main.controllers import routes

# create flask application
app = create_app()

# set up all the routes
routes.init_app(app)

if __name__ == "__main__":
    app.run()
