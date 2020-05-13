import os
import uuid
import json
from flask import Flask, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

from common.config import (
    APP_NAME, 
    ICON_PATH,
    HOST,
    PORT,
    SERVICE_URL
)

from matching.matcher import Matcher
from common.utils import allowed_file


class Server():
  def __init__(self):

    self.app = Flask(__name__, static_url_path='/', static_folder='../../www')

    self.results_dir = '../www/results'

    self.app.add_url_rule('/', 'index', self.index_route)
    self.app.add_url_rule('/heartbeat', 'heartbeat', self.heartbeat_route)
    self.app.add_url_rule('/get-url', 'get-url', self.get_url_route)
    
    self.app.add_url_rule('/match', 'match', self.match_route, methods=['POST'])


  def start(self):
    self.app.run(host=HOST, port=PORT, threaded=True)

  def stop(self):
    _shutdown = request.environ.get('werkzeug.server.shutdown')
    if _shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    _shutdown()


  # Routes

  def index_route(self):
    return redirect("/index.html", code=301)

  def heartbeat_route(self):
    return "ok"

  def get_url_route(self):
    return SERVICE_URL

  def match_route(self):

    # Check if there is an image in the request
    if 'image_file.jpg' not in request.files:
      return 'No file part'

    # Get uploaded file
    uploaded_file = request.files['image_file.jpg']

    # Check if file has data
    if not uploaded_file or uploaded_file.filename == '':
      return 'No selected file'

    # Check if filetype is allowed
    if not allowed_file(uploaded_file.filename):
      return 'Invalid filetype'
    
    # Create match uid
    uid = uuid.uuid4().hex

    # Create Match dir
    match_dir = self.results_dir + '/result-' + uid
    os.mkdir(match_dir)

    # Save uploaded image to match dir
    photo_extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
    filename = 'photo.' + photo_extension
    uploaded_file.save( match_dir + '/' + filename )
    
    # Start matcher
    matcher = Matcher(uid, filename)

    match_result = matcher.match(algorithm='ORB')

    response = {'uid': uid}

    if not match_result:
      response['hasResult'] = False
      return Response( json.dumps(response), mimetype='application/json' )
    else:
      response['hasResult'] = True
      response['filename'] = '/results/result-' + uid + '/result.png'
      return Response( json.dumps(response), mimetype='application/json' )