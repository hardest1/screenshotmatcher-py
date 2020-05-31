import pyscreenshot as ImageGrab
import time
import numpy as np
import logging

from cv2 import ( # pylint: disable=no-name-in-module
  perspectiveTransform,
  findHomography,
  RANSAC,
  FlannBasedMatcher,
  imread,
  imwrite,
  IMREAD_COLOR,
  IMREAD_GRAYSCALE,
  DescriptorMatcher_create,
  ORB_create,
)

from cv2.xfeatures2d import ( # pylint: disable=no-name-in-module,import-error
  SURF_create,
)


class Matcher():
  
  def __init__(self, match_uid, photo):

    logging.basicConfig(filename='./match.log',level=logging.DEBUG)

    self.match_uid = match_uid
    self.match_dir = './www/results/result-' + match_uid

    self.screenshot_file = 'screenshot.png'
    self.screenshot = ImageGrab.grab()
    self.screenshot.save(self.match_dir + '/' + self.screenshot_file)

    self.photo_file = photo

  def match(self, algorithm='SURF'):

    start_time = time.perf_counter()

    # Load pictures

    photo = imread( '{}/{}'.format(self.match_dir, self.photo_file), IMREAD_GRAYSCALE )
    screen = imread( '{}/{}'.format(self.match_dir, self.screenshot_file), IMREAD_GRAYSCALE )
    screen_colored = imread( '{}/{}'.format(self.match_dir, self.screenshot_file), IMREAD_COLOR )

    # Provisional switch statement
    if algorithm == 'SURF':
      match_result = self.algorithm_SURF(photo, screen, screen_colored)
    elif algorithm == 'ORB':
      match_result = self.algorithm_ORB(photo, screen, screen_colored)
    else:
      match_result = self.algorithm_SURF(photo, screen, screen_colored)


    logging.info('{}ms'.format(round( (time.perf_counter() - start_time) * 1000 )))

    return match_result

  def algorithm_SURF(self, photo, screen, screen_colored):

    # Init algorithm
    surf = SURF_create(400)
    surf.setUpright(True)

    # Detect and compute
    kp_photo, des_photo = surf.detectAndCompute(photo, None)
    kp_screen, des_screen = surf.detectAndCompute(screen, None)

    # Descriptor Matcher
    index_params = dict(algorithm = 0, trees = 5)
    search_params = dict(checks = 50)
    flann = FlannBasedMatcher(index_params, search_params)

    # Calc knn Matches
    matches = flann.knnMatch(des_photo, des_screen, k=2)

    logging.info('knn {}'.format(len(matches)))

    if not matches or len(matches) == 0:
      return False

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    logging.info('good {}'.format(len(good)))

    if not good or len(good) < 10:
      return False


    photo_pts = np.float32([ kp_photo[m.queryIdx].pt for m in good ]).reshape(-1,1,2) # pylint: disable=too-many-function-args
    screen_pts = np.float32([ kp_screen[m.trainIdx].pt for m in good ]).reshape(-1,1,2) # pylint: disable=too-many-function-args

    M, _ = findHomography(photo_pts, screen_pts, RANSAC, 5.0)

    if len(M) == 0:
      return False

    h, w = photo.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2) # pylint: disable=too-many-function-args
    dst = perspectiveTransform(pts, M)


    minX = dst[0][0][0]
    minY = dst[0][0][1]
    maxX = dst[0][0][0]
    maxY = dst[0][0][1]

    for i in range(4):
      if dst[i][0][0] < minX:
        minX = dst[i][0][0]
      if dst[i][0][0] > maxX:
        maxX = dst[i][0][0]
      if dst[i][0][1] < minY:
        minY = dst[i][0][1]
      if dst[i][0][1] > maxY:
        maxY = dst[i][0][1]

    minX = int(minX)
    minY = int(minY)
    maxX = int(maxX)
    maxY = int(maxY)

    if minX < 0:
      minX = 0
    if minY < 0:
      minY = 0

    logging.info('minY {}'.format(int(minY)))
    logging.info('minX {}'.format(int(minX)))
    logging.info('maxY {}'.format(int(maxY)))
    logging.info('maxX {}'.format(int(maxX)))

    if maxX - minX <= 0:
      return False
    if maxY - minY <= 0:
      return False

    imwrite(self.match_dir + '/result.png', screen_colored[ minY:maxY, minX:maxX])

    return True


  def algorithm_ORB(self, photo, screen, screen_colored):

    # Init algorithm
    orb = ORB_create(800)

    # Detect and compute
    kp_photo, des_photo = orb.detectAndCompute(photo, None)
    kp_screen, des_screen = orb.detectAndCompute(screen, None)

    # Descriptor Matcher
    descriptor_matcher = DescriptorMatcher_create('BruteForce-Hamming')

    # Calc knn Matches
    matches = descriptor_matcher.knnMatch(des_photo, des_screen, k=2)

    if not matches or len(matches) == 0:
      return False

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    if not good or len(good) < 20:
      return False

    photo_pts = np.float32([ kp_photo[m.queryIdx].pt for m in good ]).reshape(-1,1,2) # pylint: disable=too-many-function-args
    screen_pts = np.float32([ kp_screen[m.trainIdx].pt for m in good ]).reshape(-1,1,2) # pylint: disable=too-many-function-args

    M, _ = findHomography(photo_pts, screen_pts, RANSAC, 5.0)

    if len(M) == 0:
      return False

    h, w = photo.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2) # pylint: disable=too-many-function-args
    dst = perspectiveTransform(pts, M)


    minX = dst[0][0][0]
    minY = dst[0][0][1]
    maxX = dst[0][0][0]
    maxY = dst[0][0][1]

    for i in range(4):
      if dst[i][0][0] < minX:
        minX = dst[i][0][0]
      if dst[i][0][0] > maxX:
        maxX = dst[i][0][0]
      if dst[i][0][1] < minY:
        minY = dst[i][0][1]
      if dst[i][0][1] > maxY:
        maxY = dst[i][0][1]

    minX = int(minX)
    minY = int(minY)
    maxX = int(maxX)
    maxY = int(maxY)

    if minX < 0:
      minX = 0
    if minY < 0:
      minY = 0

    logging.info('minY {}'.format(int(minY)))
    logging.info('minX {}'.format(int(minX)))
    logging.info('maxY {}'.format(int(maxY)))
    logging.info('maxX {}'.format(int(maxX)))

    if maxX - minX <= 0:
      return False
    if maxY - minY <= 0:
      return False

    imwrite(self.match_dir + '/result.png', screen_colored[ int(minY):int(maxY), int(minX):int(maxX)])

    return True

