"""
This script defines a WSGI file that runs our flask application 
"""

from application import app as application
if __name__ == "__main__":
    application.run(debug=True)