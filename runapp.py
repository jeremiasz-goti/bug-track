from bugtrack import app

"""

Main run file.

"""


# change debug to false in production
if __name__ == '__main__':
    app.run(debug=True)