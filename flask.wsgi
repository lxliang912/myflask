import sys

sys.path.insert(0, 'e:/Workspaces/myflask')

from app.app import create_app

#Initialize WSGI app object
application = create_app()