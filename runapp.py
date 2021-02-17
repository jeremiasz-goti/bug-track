from bugtrack import app


# change debug to false in production
if __name__ == '__main__':
    app.run(debug=True)