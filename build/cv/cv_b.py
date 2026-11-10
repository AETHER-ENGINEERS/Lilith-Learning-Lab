# -*- coding: utf-8 -*-
"""Computer vision course, part 2: cameras, classical recognition, CNNs, detection, transformers."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


CHS.append(CH(
 "Cameras, geometry and depth",
 ("Geometry", [
  "Pinhole camera | projects | 3D to 2D",
  "Focal length | scales | The image",
  "Intrinsics | describe | The camera",
  "Extrinsics | describe | Its pose",
  "Distortion | bends | Straight lines",
  "Stereo | gives | Depth",
  "Disparity | is | Pixel shift"]),
 ["The pinhole model projects a 3D point (X, Y, Z) to the image at (f X / Z, f Y / Z): farther things appear smaller. Intrinsic parameters (focal length, principal point) describe the camera; extrinsics give its position and rotation.",
  "Real lenses distort straight lines; calibration with a checkerboard estimates the parameters so we can undo it.",
  "Two cameras a baseline B apart see the same point shifted by a disparity d; depth is Z = f B / d. Closer objects have larger disparity."],
 [("Pinhole camera model", "An idealised camera in which light passes through a single point, projecting 3D points to the image plane."),
  ("Focal length", "The distance from the pinhole to the image plane, here in pixels, setting the field of view."),
  ("Camera calibration", "Estimating a camera's intrinsic parameters and lens distortion, often from images of a checkerboard."),
  ("Disparity", "The horizontal shift of a point between the left and right images of a stereo pair."),
  ("Epipolar geometry", "The geometry relating two views: a point in one image lies on a known line in the other.")],
 ["u = f X / Z + cx; v = f Y / Z + cy.",
  "Depth Z = f B / d.",
  "Field of view = 2 atan(W / (2 f)).",
  "Calibrate with a checkerboard.",
  "Homogeneous coordinates make projection a matrix product."],
 [T("Hold a coin at arm's length and it covers a mountain. Distant things look small; the camera loses the third dimension and keeps a perspective view. The pinhole model captures this simply: a point at depth Z, X sideways, lands on the image at f times X over Z, where f is the focal length. Double the distance and the image halves."),
  T("To use the model in practice we need the camera's numbers. Intrinsic parameters are the focal length in pixels and the principal point, where the optical axis meets the sensor. Extrinsic parameters say where the camera is and which way it points. Together they form the camera matrix. Lenses also bend straight lines, so calibration images of a checkerboard let software estimate the distortion and correct it."),
  C("ok, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)\nundistorted = cv2.undistort(img, K, dist)\n\nstereo = cv2.StereoSGBM_create(minDisparity=0, numDisparities=64, blockSize=7)\ndisp = stereo.compute(left_gray, right_gray).astype('float32') / 16.0\ndepth = f * baseline / np.maximum(disp, 0.1)", "python"),
  T("Depth comes from two views. Hold a finger in front of you and close one eye then the other: the finger jumps against the background. That jump, the disparity, is large for close things and small for far ones. With two cameras a baseline B apart and focal length f, a point with disparity d lies at depth Z equal to f B over d. Finding the matching pixel in the other image, stereo matching, is a search along one row after rectification."),
  T("Modern systems also estimate depth from a single image with learned models, or measure it directly with LiDAR and time-of-flight sensors. Structure from motion and SLAM combine many views, solving for camera poses and 3D points together, which is how phones and robots build maps. The labs project points, triangulate depth and apply transforms.")],
 [("What does the pinhole model say?", ["Image position is f X / Z", "Image position is X + Z", "Depth is f X", "Light bends"], 0, "Farther is smaller."),
  ("What is disparity?", ["The pixel shift between stereo views", "A colour difference", "A kernel", "A threshold"], 0, "Left-right offset."),
  ("What is depth from disparity?", ["f B / d", "d / (f B)", "f + B + d", "B / f"], 0, "Larger disparity, closer."),
  ("What does calibration estimate?", ["Camera parameters and distortion", "Object classes", "Edges", "Colours"], 0, "Checkerboard."),
  ("What are extrinsics?", ["The camera's pose", "The focal length", "The lens", "The sensor size"], 0, "Rotation and translation."),
  ("What does SLAM do?", ["Maps and localises together", "Blurs images", "Detects faces", "Classifies colours"], 0, "Robots.")],
 [("Z = f B / d", "stereo depth"), ("u = f X / Z", "perspective projection"), ("cv2.undistort", "remove lens distortion")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Intrinsics", "focal length and principal point"), ("Extrinsics", "camera pose"), ("Disparity", "stereo pixel shift"), ("Calibration", "estimate camera parameters"), ("Homography", "plane-to-plane map")]),
  PL("Project a point", "Write project(X, Y, Z, f, cx, cy): the pixel [u, v] = [f X / Z + cx, f Y / Z + cy], rounded to 2 decimals.", "project(X, Y, Z, f, cx, cy)", '''
def project(X, Y, Z, f, cx, cy):
    return [round(f * X / Z + cx, 2), round(f * Y / Z + cy, 2)]
''', [[1, 2, 10, 500, 320, 240], [0, 0, 5, 800, 400, 300], [-2, 1, 4, 100, 50, 50]], "Divide by depth."),
  PL("Stereo depth", "Write depth(f, baseline, disparity): f x baseline / disparity rounded to 3 decimals; return None if disparity is not positive.", "depth(f, baseline, disparity)", '''
def depth(f, baseline, disparity):
    if disparity <= 0:
        return None
    return round(f * baseline / float(disparity), 3)
''', [[700, 0.12, 10], [700, 0.12, 40], [500, 0.5, 0], [800, 0.1, 5]], "Larger disparity means closer.", approx=0.002),
  PL("Field of view", "Write fov(width_px, f): the horizontal field of view in degrees, 2 atan(width / (2 f)), rounded to 1 decimal.", "fov(width_px, f)", '''
import math
def fov(width_px, f):
    return round(math.degrees(2 * math.atan(width_px / (2.0 * f))), 1)
''', [[640, 500], [1920, 1000], [100, 50]], "Use atan.", approx=0.1),
  PL("Rotate a point", "Write rotate(x, y, angle_deg): rotate (x, y) anticlockwise about the origin and return [x', y'] rounded to 3 decimals.", "rotate(x, y, angle_deg)", '''
import math
def rotate(x, y, angle_deg):
    a = math.radians(angle_deg)
    return [round(x * math.cos(a) - y * math.sin(a), 3), round(x * math.sin(a) + y * math.cos(a), 3)]
''', [[1, 0, 90], [1, 1, 45], [2, 3, 180], [0, 5, 0]], "Standard rotation matrix.", approx=0.002),
  PL("Affine transform", "Write affine(points, A): apply the 2x3 affine matrix A = [[a, b, tx], [c, d, ty]] to each [x, y]: [a x + b y + tx, c x + d y + ty].", "affine(points, A)", '''
def affine(points, A):
    return [[A[0][0] * p[0] + A[0][1] * p[1] + A[0][2], A[1][0] * p[0] + A[1][1] * p[1] + A[1][2]] for p in points]
''', [[[[0, 0], [1, 1]], [[1, 0, 5], [0, 1, 3]]], [[[1, 0]], [[0, -1, 0], [1, 0, 0]]], [[[2, 2]], [[2, 0, 0], [0, 2, 0]]]], "Matrix times vector plus translation."),
  PL("Radial distortion", "Write distort(x, y, k1): the barrel distortion of normalised coordinates, [x (1 + k1 r^2), y (1 + k1 r^2)] with r^2 = x^2 + y^2, rounded to 4 decimals.", "distort(x, y, k1)", '''
def distort(x, y, k1):
    r2 = x * x + y * y
    s = 1 + k1 * r2
    return [round(x * s, 4), round(y * s, 4)]
''', [[0.5, 0.5, -0.2], [0, 0, 0.3], [1, 0, 0.1]], "Scale by 1 + k1 r squared.", approx=0.0002)]
))

CHS.append(CH(
 "Classical recognition: HOG, Haar and bags of features",
 ("Recognition", [
  "HOG | describes | Shape by gradients",
  "Haar feature | compares | Rectangles",
  "Integral image | speeds | Rectangle sums",
  "Viola-Jones | detects | Faces fast",
  "Bag of words | counts | Visual words",
  "SVM | separates | With a margin",
  "Sliding window | scans | Positions"]),
 ["Before deep learning, recognition was a pipeline: extract hand-designed features, then train a classifier. HOG (histogram of oriented gradients) describes shape by local gradient directions and, with a linear SVM, detected pedestrians.",
  "Viola and Jones detected faces in real time using Haar features (differences of rectangle sums) computed instantly from an integral image, and a cascade that rejects most windows early.",
  "Bag of visual words clusters local descriptors into a vocabulary and describes an image by the histogram of words, then classifies the histogram."],
 [("HOG", "Histogram of oriented gradients: a descriptor built from gradient-direction histograms in cells."),
  ("Integral image", "An image where each entry holds the sum of all pixels above and to the left, allowing any rectangle sum in four lookups."),
  ("Haar-like feature", "The difference between the sums of pixels in adjacent rectangles."),
  ("Cascade", "A sequence of classifiers in which early cheap stages reject most non-objects."),
  ("Support vector machine", "A classifier that finds the separating boundary with the widest margin.")],
 ["Rectangle sum = I(D) - I(B) - I(C) + I(A).",
  "HOG: cells of 8x8, 9 orientation bins.",
  "Sliding window x image pyramid = detector.",
  "SVM: sign(w.x + b).",
  "Bag of words: histogram of cluster ids."],
 [T("Early face detectors seemed impossible in real time. Paul Viola and Michael Jones solved it in 2001 with three ideas. First, simple features: Haar-like rectangles, such as a dark band across the eyes above a lighter band on the cheeks. Second, the integral image, which lets you add up any rectangle with just four array lookups. Third, a cascade of classifiers, so that most windows are rejected by the first cheap tests."),
  T("The integral image is a lovely trick. Make a table where each entry is the sum of all pixels above and to the left of it. The sum over any rectangle is then the bottom-right entry, minus the entries to the left and above, plus the corner that was subtracted twice. Constant time, whatever the size. The feature value is a difference of two or three such sums."),
  T("Another classic, HOG by Navneet Dalal and Bill Triggs, describes an object by its edges. Divide the window into cells of 8 by 8 pixels. In each cell, build a histogram of gradient directions weighted by gradient strength. Normalise over blocks of cells for lighting invariance. A linear support vector machine trained on these long vectors detects pedestrians well, and the whole pipeline slides across the image at many scales."),
  C("from skimage.feature import hog\nfrom sklearn.svm import LinearSVC\n\nfeat = hog(gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2))\nclf = LinearSVC(C=0.01).fit(train_features, train_labels)\n\nface = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')\nboxes = face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)", "python"),
  T("For whole-image categories such as 'beach' or 'forest', the bag of visual words treats local descriptors like words in a document. Cluster thousands of SIFT descriptors with k-means; each centre is a visual word. Describe an image by the histogram of words it contains and train an SVM on histograms. These pipelines dominated until 2012, when learned features overtook them, but their ideas, sliding windows, multiscale pyramids and normalisation, live on in modern detectors.")],
 [("How many lookups give a rectangle sum in an integral image?", ["Four", "One", "Rectangle area", "Eight"], 0, "Corners."),
  ("What does Viola-Jones use to be fast?", ["Integral image and a cascade", "A huge network", "Colour only", "Random guesses"], 0, "Reject early."),
  ("What does HOG describe?", ["Shape through gradient directions", "Colour", "Depth", "Texture only"], 0, "Cells of histograms."),
  ("What is a visual word?", ["A cluster centre of local descriptors", "A letter", "A label", "A pixel"], 0, "k-means."),
  ("What does an SVM maximise?", ["The margin", "The error", "The number of features", "The image size"], 0, "Widest gap."),
  ("Why a sliding window?", ["To search every position", "To blur", "To save memory", "To rotate"], 0, "Detect anywhere.")],
 [("hog(img)", "HOG features"), ("CascadeClassifier", "Viola-Jones in OpenCV"), ("sign(w.x + b)", "linear SVM decision")],
 [MATCH("Match the term", "Pair each classical idea with its job.", [("Integral image", "fast rectangle sums"), ("Haar feature", "difference of rectangles"), ("Cascade", "reject non-faces early"), ("HOG", "gradient-direction histograms"), ("Bag of words", "histogram of visual words")]),
  PL("Integral image", "Write integral(img): the integral image I where I[r][c] is the sum of img[0..r][0..c].", "integral(img)", '''
def integral(img):
    h = len(img)
    w = len(img[0])
    I = [[0] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            s = img[r][c]
            if r > 0:
                s = s + I[r - 1][c]
            if c > 0:
                s = s + I[r][c - 1]
            if r > 0 and c > 0:
                s = s - I[r - 1][c - 1]
            I[r][c] = s
    return I
''', [[[[1, 2], [3, 4]]], [[[1, 1, 1], [1, 1, 1]]], [[[5]]]], "Add above and left, subtract the overlap."),
  PL("Rectangle sum", "Write rect_sum(I, r0, c0, r1, c1): the sum of the original image over rows r0..r1 and columns c0..c1 (inclusive) using the integral image I.", "rect_sum(I, r0, c0, r1, c1)", '''
def rect_sum(I, r0, c0, r1, c1):
    s = I[r1][c1]
    if r0 > 0:
        s = s - I[r0 - 1][c1]
    if c0 > 0:
        s = s - I[r1][c0 - 1]
    if r0 > 0 and c0 > 0:
        s = s + I[r0 - 1][c0 - 1]
    return s
''', [[[[1, 3, 6], [5, 12, 21], [12, 27, 45]], 1, 1, 2, 2], [[[1, 3], [4, 10]], 0, 0, 1, 1], [[[1, 3], [4, 10]], 1, 0, 1, 1]], "Four lookups."),
  PL("Haar feature", "Write haar_two(img, r, c, h, w): the value of a two-rectangle Haar feature: the sum of the left h x w rectangle minus the sum of the right h x w rectangle next to it, with the top-left corner at (r, c). Use plain sums.", "haar_two(img, r, c, h, w)", '''
def haar_two(img, r, c, h, w):
    left = 0
    right = 0
    for i in range(h):
        for j in range(w):
            left = left + img[r + i][c + j]
            right = right + img[r + i][c + w + j]
    return left - right
''', [[[[9, 9, 1, 1], [9, 9, 1, 1]], 0, 0, 2, 2], [[[1, 2, 3, 4]], 0, 0, 1, 2], [[[5, 5], [5, 5]], 0, 0, 2, 1]], "Two adjacent rectangles."),
  PL("HOG cell histogram", "Write hog_cell(gx, gy, bins): for equal-length lists of gradient components of a cell, build an unsigned-orientation histogram: orientation = atan2(gy, gx) in degrees folded into [0, 180), bin width 180 / bins, each pixel adds its magnitude sqrt(gx^2 + gy^2) to its bin. Return the histogram rounded to 2 decimals.", "hog_cell(gx, gy, bins)", '''
import math
def hog_cell(gx, gy, bins):
    hist = [0.0] * bins
    w = 180.0 / bins
    for i in range(len(gx)):
        ang = math.degrees(math.atan2(gy[i], gx[i])) % 180.0
        mag = math.sqrt(gx[i] ** 2 + gy[i] ** 2)
        b = int(ang // w)
        if b >= bins:
            b = bins - 1
        hist[b] = hist[b] + mag
    return [round(v, 2) for v in hist]
''', [[[1, 0, 3], [0, 1, 4], 4], [[2, 2], [2, -2], 2], [[0], [0], 3]], "Magnitude into the orientation bin.", approx=None),
  PL("Visual word histogram", "Write bow(descriptors, words): assign each descriptor (list of numbers) to the nearest word (squared distance, lowest index on ties) and return the histogram of counts over the words.", "bow(descriptors, words)", '''
def bow(descriptors, words):
    hist = [0] * len(words)
    for d in descriptors:
        best = 0
        bd = None
        for i in range(len(words)):
            s = 0
            for j in range(len(d)):
                s = s + (d[j] - words[i][j]) ** 2
            if bd is None or s < bd:
                bd = s
                best = i
        hist[best] = hist[best] + 1
    return hist
''', [[[[0, 0], [1, 1], [9, 9], [8, 8], [9, 8]], [[0, 0], [9, 9]]], [[[5]], [[0], [10]]], [[], [[1]]]], "Count assignments."),
  PL("Linear SVM", "Write svm_predict(w, b, X): for each feature vector return 1 if w.x + b >= 0 else -1.", "svm_predict(w, b, X)", '''
def svm_predict(w, b, X):
    out = []
    for x in X:
        s = b
        for j in range(len(w)):
            s = s + w[j] * x[j]
        out.append(1 if s >= 0 else -1)
    return out
''', [[[1, 1], -3, [[1, 1], [2, 2], [3, 0]]], [[-1], 0, [[1], [-1], [0]]], [[0.5, -0.5], 0, [[2, 1], [1, 2]]]], "Sign of the linear score.")]
))

CHS.append(CH(
 "Convolutional neural networks",
 ("CNNs", [
  "CNN | learns | Its own filters",
  "Convolution layer | detects | Local patterns",
  "Pooling | shrinks | Feature maps",
  "ReLU | adds | Non-linearity",
  "Receptive field | grows | With depth",
  "ResNet | adds | Skip connections",
  "Transfer learning | reuses | Pretrained features"]),
 ["A convolutional neural network stacks learned convolution layers with non-linearities and pooling. Early layers learn edges, middle layers textures and parts, late layers whole objects.",
  "AlexNet's win in the 2012 ImageNet contest started the deep learning era. VGG, Inception and ResNet followed; ResNet's skip connections made very deep networks trainable.",
  "Instead of training from scratch, you usually start from a network pretrained on ImageNet and fine-tune it on your own data: transfer learning."],
 [("Convolutional layer", "A layer applying many learned small kernels across the image, sharing weights across positions."),
  ("Pooling", "Downsampling feature maps, for example by taking the maximum of each 2x2 block."),
  ("Receptive field", "The region of the input image that influences a given unit."),
  ("Skip connection", "A shortcut that adds a layer's input to its output, as in ResNet."),
  ("Transfer learning", "Starting from a model trained on a large dataset and adapting it to a new task.")],
 ["Output size = (W - K + 2P) / S + 1.",
  "Params per conv layer = K*K*Cin*Cout + Cout.",
  "Max pool 2x2 halves width and height.",
  "ResNet: y = F(x) + x.",
  "Fine-tune: freeze early layers, train the head."],
 [T("In classical vision, experts designed the filters. A convolutional network lets the data decide. It stacks layers in which many small kernels slide over the image, exactly the convolution of Chapter 2, but with the numbers in each kernel learned by gradient descent. Sharing each kernel across all positions makes the network efficient and gives it translation equivariance: a cat is a cat wherever it sits."),
  T("A typical block is convolution, a non-linearity such as ReLU, and pooling. Pooling shrinks the maps, say taking the biggest value in each 2 by 2 block, so deeper layers see wider regions of the image: the receptive field grows. Peering inside trained networks shows early layers responding to edges and colours, middle layers to textures and parts like eyes and wheels, and the last layers to whole objects."),
  C("from tensorflow import keras\nfrom tensorflow.keras import layers\n\nmodel = keras.Sequential([\n    layers.Input((64, 64, 3)),\n    layers.Conv2D(32, 3, activation='relu'), layers.MaxPooling2D(),\n    layers.Conv2D(64, 3, activation='relu'), layers.MaxPooling2D(),\n    layers.Flatten(), layers.Dense(64, activation='relu'),\n    layers.Dense(10, activation='softmax'),\n])\nbase = keras.applications.ResNet50(weights='imagenet', include_top=False)\nbase.trainable = False   # transfer learning: train only a new head", "python"),
  T("The ImageNet contest asked programs to classify a million photographs into a thousand categories. In 2012, AlexNet, a deep CNN trained on graphics cards, cut the error from twenty-six to sixteen percent, and the field changed. Deeper networks followed, but stacking layers eventually made training harder. ResNet's fix in 2015 was the skip connection: each block learns a residual, a correction added to its input, so the signal and gradient pass straight through. Networks with over a hundred layers trained well."),
  T("Training a large CNN from scratch needs millions of images. Transfer learning avoids that. Take a network pretrained on ImageNet, replace its last layer with one for your classes, and train just that layer, or fine-tune the whole network gently. A few hundred examples can be enough. Data augmentation, random flips, crops and colour changes, stretches small datasets further. Count the sizes and parameters in the labs; it shows why convolution is so economical.")],
 [("What does a conv layer share across positions?", ["Its kernel weights", "Its output", "Its input", "Its bias only"], 0, "Weight sharing."),
  ("What does max pooling do?", ["Downsamples by taking the maximum", "Adds colour", "Rotates", "Sharpens"], 0, "Shrinks maps."),
  ("What did ResNet introduce?", ["Skip connections", "Pooling", "ReLU", "Kernels"], 0, "y = F(x) + x."),
  ("Why use transfer learning?", ["Little data is needed", "It is slower", "It avoids GPUs", "It removes labels"], 0, "Reuse features."),
  ("What do early CNN layers detect?", ["Edges and colours", "Whole objects", "Faces only", "Text"], 0, "Low-level."),
  ("What started the deep learning era in vision?", ["AlexNet in 2012", "Canny in 1986", "SIFT in 1999", "HOG in 2005"], 0, "ImageNet.")],
 [("(W - K + 2P)/S + 1", "conv output size"), ("K*K*Cin*Cout", "conv weights"), ("y = F(x) + x", "residual block")],
 [MATCH("Match the term", "Pair each CNN idea with its meaning.", [("Convolution layer", "learned sliding kernels"), ("Pooling", "downsample"), ("Receptive field", "input region seen by a unit"), ("Skip connection", "add input to output"), ("Fine-tuning", "adapt a pretrained network")]),
  PL("Output size", "Write conv_out(w, k, p, s): the output width (W - K + 2P) // S + 1 of a convolution.", "conv_out(w, k, p, s)", '''
def conv_out(w, k, p, s):
    return (w - k + 2 * p) // s + 1
''', [[28, 3, 0, 1], [28, 3, 1, 1], [224, 7, 3, 2], [32, 5, 0, 2]], "Integer arithmetic."),
  PL("Parameter count", "Write conv_params(k, cin, cout): the number of weights plus biases in a conv layer, k x k x cin x cout + cout.", "conv_params(k, cin, cout)", '''
def conv_params(k, cin, cout):
    return k * k * cin * cout + cout
''', [[3, 3, 32], [3, 32, 64], [1, 64, 128], [7, 3, 64]], "Weights per filter times filters, plus biases."),
  PL("Max pool", "Write max_pool(img, size): non-overlapping size x size max pooling (stride = size); incomplete blocks at the edges are ignored.", "max_pool(img, size)", '''
def max_pool(img, size):
    h = len(img) // size
    w = len(img[0]) // size
    out = []
    for r in range(h):
        row = []
        for c in range(w):
            m = img[r * size][c * size]
            for i in range(size):
                for j in range(size):
                    if img[r * size + i][c * size + j] > m:
                        m = img[r * size + i][c * size + j]
            row.append(m)
        out.append(row)
    return out
''', [[[[1, 3, 2, 1], [4, 2, 0, 5], [1, 1, 9, 8], [0, 2, 7, 6]], 2], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2], [[[5]], 1]], "Maximum of each block."),
  PL("Strided convolution", "Write conv_stride(img, k, stride, pad): zero-pad the image by pad on all sides, then slide the kernel k with the given stride (no flip) and return the output image.", "conv_stride(img, k, stride, pad)", '''
def conv_stride(img, k, stride, pad):
    h = len(img)
    w = len(img[0])
    P = [[0] * (w + 2 * pad) for _ in range(h + 2 * pad)]
    for r in range(h):
        for c in range(w):
            P[r + pad][c + pad] = img[r][c]
    kh = len(k)
    kw = len(k[0])
    out = []
    r = 0
    while r + kh <= len(P):
        row = []
        c = 0
        while c + kw <= len(P[0]):
            s = 0
            for i in range(kh):
                for j in range(kw):
                    s = s + k[i][j] * P[r + i][c + j]
            row.append(s)
            c = c + stride
        out.append(row)
        r = r + stride
    return out
''', [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, 1]], 1, 0], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1, 1], [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], [[1, 1], [1, 1]], 2, 0]], "Pad, then step by the stride."),
  PL("Receptive field", "Write receptive_field(layers): layers is a list of [kernel, stride]; return the receptive field of one unit in the last layer using rf = 1, jump = 1; for each layer rf += (k - 1) x jump, jump *= stride.", "receptive_field(layers)", '''
def receptive_field(layers):
    rf = 1
    jump = 1
    for k, s in layers:
        rf = rf + (k - 1) * jump
        jump = jump * s
    return rf
''', [[[[3, 1], [3, 1], [3, 1]]], [[[3, 1], [2, 2], [3, 1], [2, 2]]], [[[7, 2]]]], "Track the jump."),
  PL("Residual block", "Write residual(x, f_out): the elementwise sum x + f_out of the input vector and the layer's output (equal lengths); then return the ReLU of the sum.", "residual(x, f_out)", '''
def residual(x, f_out):
    return [max(0, x[i] + f_out[i]) for i in range(len(x))]
''', [[[1, -2, 3], [0, 1, -5]], [[0, 0], [1, -1]], [[5], [-3]]], "Add the shortcut, then ReLU.")]
))

CHS.append(CH(
 "Detection, segmentation and tracking",
 ("Detection", [
  "Detection | finds | Objects and boxes",
  "IoU | measures | Box overlap",
  "NMS | removes | Duplicates",
  "Anchor | seeds | Box proposals",
  "YOLO | detects | In one pass",
  "Segmentation | labels | Every pixel",
  "U-Net | restores | Resolution"]),
 ["Detection finds what and where: a box and a class for every object. Intersection over union (IoU) measures how well two boxes overlap, and non-maximum suppression removes duplicate detections of the same object.",
  "R-CNN families propose regions then classify them; YOLO and SSD predict boxes in a single pass and run in real time. Mask R-CNN adds a mask per object (instance segmentation).",
  "Semantic segmentation labels every pixel; encoder-decoder networks such as U-Net downsample to understand and upsample to localise."],
 [("Bounding box", "A rectangle that encloses an object, given by its corners or by centre, width and height."),
  ("Intersection over union (IoU)", "The area of overlap of two boxes divided by the area of their union."),
  ("Non-maximum suppression", "Discarding boxes that overlap a higher-scoring box of the same class too much."),
  ("Instance segmentation", "Finding each object and giving it a pixel mask."),
  ("Mean average precision (mAP)", "A standard detection score averaging precision over recall levels and classes.")],
 ["IoU = intersection / (A + B - intersection).",
  "NMS: sort by score, keep, drop IoU > threshold.",
  "Match if IoU >= 0.5.",
  "YOLO: grid cells predict boxes.",
  "U-Net: encoder, decoder, skip links."],
 [T("Classifying a photograph as 'street' is one thing; finding every car, pedestrian and traffic light in it, with boxes, is detection, and self-driving cars depend on it. A detector outputs, for each object, a box, a class and a confidence score."),
  T("To judge a box we need a measure of overlap. Intersection over union divides the area the predicted and true boxes share by the area they cover together. One is a perfect match, zero is no overlap, and a detection is usually counted correct if its IoU with a true box is at least one half. Detectors often fire many overlapping boxes on one object, so non-maximum suppression sorts boxes by score, keeps the best, and deletes any other box that overlaps it too much."),
  C("from ultralytics import YOLO\nmodel = YOLO('yolov8n.pt')\nresults = model('street.jpg')\nfor box in results[0].boxes:\n    print(box.cls, box.conf, box.xyxy)\n\nimport torchvision\nmask_rcnn = torchvision.models.detection.maskrcnn_resnet50_fpn(weights='DEFAULT').eval()", "python"),
  T("Two families of detector dominate. The R-CNN family first proposes regions that might contain objects, then classifies and refines each; Faster R-CNN made proposals part of the network. YOLO, short for you only look once, and SSD divide the image into a grid and predict boxes and classes for every cell in one forward pass, fast enough for video. Mask R-CNN extends Faster R-CNN with a mask for each detected object."),
  T("Sometimes boxes are not enough and we need a label for every pixel: road, sky, person. That is semantic segmentation. U-Net, shaped like the letter U, downsamples through convolutions to capture context and then upsamples back to full size, with skip connections carrying fine detail across. It became the standard for medical images. Add tracking across video frames, linking boxes by IoU and appearance, and you have the core of modern perception systems. The playground lets you drag boxes and see IoU and suppression.")],
 [("What does IoU measure?", ["Overlap of two boxes", "Image brightness", "Box colour", "Speed"], 0, "Intersection over union."),
  ("What is IoU of identical boxes?", ["1", "0", "0.5", "2"], 0, "Perfect overlap."),
  ("What does NMS do?", ["Removes overlapping duplicates", "Adds boxes", "Blurs", "Resizes"], 0, "Keep the best."),
  ("What does YOLO stand for?", ["You only look once", "Your object looks odd", "Yet another layer of objects", "You obtain labels often"], 0, "Single pass."),
  ("What does U-Net output?", ["A label per pixel", "One class", "A box", "A caption"], 0, "Semantic segmentation."),
  ("What does Mask R-CNN add to Faster R-CNN?", ["A mask per object", "Colour", "Depth", "Sound"], 0, "Instance masks.")],
 [("IoU = inter / union", "box overlap"), ("model(img)", "run a detector"), ("mAP@0.5", "detection score")],
 [APP("BOXES", "Boxes, IoU and NMS", "Drag the two boxes to see IoU, then add a few candidate detections and move the NMS threshold to see which boxes survive. Try the NMS demo at three different thresholds to complete the lab.", 820),
  MATCH("Match the term", "Pair each detection idea with its meaning.", [("IoU", "box overlap score"), ("NMS", "drop duplicate boxes"), ("YOLO", "single-pass detector"), ("Mask R-CNN", "instance segmentation"), ("U-Net", "encoder-decoder for pixels")]),
  PL("IoU", "Write iou(a, b): the IoU of two boxes [x1, y1, x2, y2] (x1 < x2, y1 < y2), rounded to 4 decimals; 0 if they do not overlap.", "iou(a, b)", '''
def iou(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    w = x2 - x1
    h = y2 - y1
    if w <= 0 or h <= 0:
        return 0
    inter = w * h
    ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return round(inter / float(ua), 4)
''', [[[0, 0, 2, 2], [1, 1, 3, 3]], [[0, 0, 2, 2], [0, 0, 2, 2]], [[0, 0, 1, 1], [2, 2, 3, 3]], [[0, 0, 4, 4], [1, 1, 3, 3]]], "Overlap over union.", approx=0.0002),
  PL("Non-maximum suppression", "Write nms(boxes, scores, thr): sort boxes by score descending (stable), keep a box if its IoU with every already kept box is at most thr; return the list of kept indexes in the order kept.", "nms(boxes, scores, thr)", '''
def nms(boxes, scores, thr):
    def iou(a, b):
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        w = x2 - x1
        h = y2 - y1
        if w <= 0 or h <= 0:
            return 0
        inter = w * h
        ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
        return inter / float(ua)
    order = sorted(range(len(boxes)), key=lambda i: -scores[i])
    keep = []
    for i in order:
        ok = True
        for j in keep:
            if iou(boxes[i], boxes[j]) > thr:
                ok = False
        if ok:
            keep.append(i)
    return keep
''', [[[[0, 0, 10, 10], [1, 1, 11, 11], [50, 50, 60, 60]], [0.9, 0.8, 0.7], 0.5], [[[0, 0, 10, 10], [0, 0, 10, 10]], [0.5, 0.9], 0.5], [[[0, 0, 4, 4], [2, 2, 6, 6]], [0.6, 0.7], 0.9]], "Greedy keep-the-best."),
  PL("Precision and recall of detections", "Write det_pr(pred_boxes, true_boxes, thr): match each predicted box (in the given order) to an unmatched true box with IoU >= thr (take the first matching true box); return [true positives, false positives, false negatives].", "det_pr(pred_boxes, true_boxes, thr)", '''
def det_pr(pred_boxes, true_boxes, thr):
    def iou(a, b):
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        w = x2 - x1
        h = y2 - y1
        if w <= 0 or h <= 0:
            return 0
        inter = w * h
        ua = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
        return inter / float(ua)
    used = [False] * len(true_boxes)
    tp = 0
    fp = 0
    for p in pred_boxes:
        hit = False
        for j in range(len(true_boxes)):
            if not used[j] and iou(p, true_boxes[j]) >= thr:
                used[j] = True
                hit = True
                break
        if hit:
            tp = tp + 1
        else:
            fp = fp + 1
    return [tp, fp, len(true_boxes) - tp]
''', [[[[0, 0, 10, 10], [50, 50, 60, 60]], [[1, 1, 10, 10], [100, 100, 110, 110]], 0.5], [[], [[0, 0, 1, 1]], 0.5], [[[0, 0, 2, 2]], [[0, 0, 2, 2]], 0.5]], "Match greedily."),
  PL("Dice coefficient", "Write dice(a, b): the Dice score 2 |A and B| / (|A| + |B|) of two binary masks (lists of rows of 0/1), rounded to 4 decimals; 1.0 if both are empty.", "dice(a, b)", '''
def dice(a, b):
    inter = 0
    sa = 0
    sb = 0
    for r in range(len(a)):
        for c in range(len(a[0])):
            inter = inter + a[r][c] * b[r][c]
            sa = sa + a[r][c]
            sb = sb + b[r][c]
    if sa + sb == 0:
        return 1.0
    return round(2.0 * inter / (sa + sb), 4)
''', [[[[1, 1], [0, 0]], [[1, 0], [0, 0]]], [[[0, 0]], [[0, 0]]], [[[1, 1, 1]], [[1, 1, 1]]]], "Overlap relative to sizes.", approx=0.0002),
  PL("Upsample", "Write upsample(img, factor): nearest-neighbour upsampling in which each pixel is repeated factor times in both directions (as in a U-Net decoder).", "upsample(img, factor)", '''
def upsample(img, factor):
    out = []
    for row in img:
        wide = []
        for v in row:
            wide = wide + [v] * factor
        for i in range(factor):
            out.append(list(wide))
    return out
''', [[[[1, 2], [3, 4]], 2], [[[5]], 3], [[[1, 2]], 1]], "Repeat across and down."),
  PL("Box encoding", "Write encode(box, anchor): the regression targets used by detectors for a box and an anchor, both [cx, cy, w, h]: [(cx - acx) / aw, (cy - acy) / ah, ln(w / aw), ln(h / ah)], rounded to 4 decimals.", "encode(box, anchor)", '''
import math
def encode(box, anchor):
    return [round((box[0] - anchor[0]) / anchor[2], 4), round((box[1] - anchor[1]) / anchor[3], 4),
            round(math.log(box[2] / anchor[2]), 4), round(math.log(box[3] / anchor[3]), 4)]
''', [[[12, 10, 20, 20], [10, 10, 10, 10]], [[5, 5, 5, 5], [5, 5, 5, 5]], [[0, 0, 2, 8], [1, 2, 4, 4]]], "Offsets scaled by anchor size.", approx=0.0002)]
))

CHS.append(CH(
 "Vision transformers, foundation models and responsible vision",
 ("Modern vision", [
  "Patches | become | Tokens",
  "ViT | applies | Transformers to images",
  "Attention | relates | All patches",
  "CLIP | links | Images and text",
  "SAM | segments | Anything",
  "Diffusion | generates | Images",
  "Bias | needs | Auditing"]),
 ["The Vision Transformer (ViT) cuts an image into patches, treats each as a token, adds position information and applies self-attention so every patch can relate to every other. With enough data it matches or beats CNNs.",
  "Foundation models are trained on huge data and reused for many tasks. CLIP learns to match images with captions, enabling zero-shot classification by comparing an image with text prompts. SAM segments any object from a click or a box.",
  "Diffusion models generate images by learning to remove noise step by step. These powerful tools also raise issues of bias, privacy, surveillance and misinformation."],
 [("Vision Transformer", "A model that splits an image into patches and processes them as a sequence with a transformer."),
  ("Self-attention", "A mechanism in which each token computes a weighted average of all tokens' values, with weights from query-key similarity."),
  ("CLIP", "A model trained to place images and their captions near each other in a shared embedding space."),
  ("Zero-shot classification", "Classifying into categories never trained on, by comparing the image with text descriptions of the classes."),
  ("Diffusion model", "A generative model that learns to reverse a gradual noising process.")],
 ["Patches: (H/P) x (W/P) tokens.",
  "Attention = softmax(Q K^T / sqrt(d)) V.",
  "CLIP: cosine similarity of image and text embeddings.",
  "Diffusion: x_t = sqrt(a) x_0 + sqrt(1 - a) noise.",
  "Audit performance across groups."],
 [T("For a decade convolutional networks ruled vision. Then in 2020 researchers at Google showed that a plain transformer, the architecture behind language models, could classify images just as well. The trick is to chop the image into patches, say 16 by 16 pixels, flatten each into a vector and treat the patches as the words of a sentence. A 224 by 224 image becomes 196 tokens."),
  T("The transformer's key operation is self-attention. Every patch asks a question, a query, and every patch offers a key; the match between a query and a key decides how much that patch's value contributes to the answer. The result is that any patch can directly draw on any other, even far away, while a convolution only sees its small neighbourhood. Positional embeddings tell the model where each patch sat."),
  C("from transformers import CLIPModel, CLIPProcessor\nfrom PIL import Image\n\nmodel = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')\nproc = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')\nimage = Image.open('photo.jpg')\ntexts = ['a photo of a dog', 'a photo of a cat', 'a photo of a bicycle']\ninputs = proc(text=texts, images=image, return_tensors='pt', padding=True)\nprobs = model(**inputs).logits_per_image.softmax(dim=1)\nprint(probs)", "python"),
  T("Large pretrained 'foundation' models changed practice. CLIP was trained on hundreds of millions of image and caption pairs to place matching pairs close together. To classify with no extra training, you write a sentence for each class, embed them, and pick the one nearest the image: zero-shot classification. The Segment Anything Model segments any object you point at. DINO-style self-supervised models learn useful features from images alone."),
  T("Generation, too, is learned. Diffusion models gradually add noise to training images until nothing remains, and train a network to undo one step of that noise. To create a picture, begin with pure noise and repeatedly denoise, optionally guided by a text prompt. The same power raises serious questions: face recognition and surveillance, bias when training data under-represents groups, deepfakes and consent. Audit models across groups, document their limits, and ask whether a system should be built at all.")],
 [("What does ViT feed into the transformer?", ["Image patches as tokens", "Whole pixels one at a time", "Colour histograms", "Edges only"], 0, "16x16 patches."),
  ("How many tokens for a 224 image with 16 patches?", ["196", "224", "16", "49"], 0, "14 x 14."),
  ("What is CLIP trained on?", ["Images paired with captions", "Only labels", "Only text", "Depth maps"], 0, "Contrastive."),
  ("What is zero-shot classification?", ["Classifying new classes using text descriptions", "Classifying with no model", "Training from scratch", "Using zero images"], 0, "Compare with prompts."),
  ("How does diffusion generate images?", ["By repeatedly removing noise", "By copying a photo", "By drawing edges", "By thresholding"], 0, "Reverse process."),
  ("Why audit vision systems by group?", ["Errors may differ across groups", "To speed up", "To reduce size", "To save data"], 0, "Fairness.")],
 [("(H/P) x (W/P)", "number of patches"), ("softmax(QK^T/sqrt d) V", "attention"), ("cos(image, text)", "CLIP similarity")],
 [MATCH("Match the term", "Pair each modern vision idea with its meaning.", [("ViT", "transformer on patches"), ("CLIP", "image and text in one space"), ("SAM", "segment anything from prompts"), ("Diffusion", "generate by denoising"), ("Foundation model", "large pretrained model reused widely")]),
  PL("Patchify", "Write patchify(img, p): cut a square gray image (list of rows, size divisible by p) into p x p patches in row-major order, each flattened row by row into a list. Return the list of patches.", "patchify(img, p)", '''
def patchify(img, p):
    h = len(img)
    w = len(img[0])
    out = []
    for r in range(0, h, p):
        for c in range(0, w, p):
            patch = []
            for i in range(p):
                for j in range(p):
                    patch.append(img[r + i][c + j])
            out.append(patch)
    return out
''', [[[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 2], [[[1, 2], [3, 4]], 1], [[[1, 2], [3, 4]], 2]], "Walk the grid in steps of p."),
  PL("Number of tokens", "Write num_tokens(h, w, p): how many patches an h x w image gives with patch size p, assuming divisibility.", "num_tokens(h, w, p)", '''
def num_tokens(h, w, p):
    return (h // p) * (w // p)
''', [[224, 224, 16], [384, 384, 16], [32, 64, 8]], "Count patches per row and column."),
  PL("Attention weights", "Write attention(q, keys): the softmax over keys of the scaled dot product q.k / sqrt(d), where d is the length of q. Return the weights rounded to 4 decimals.", "attention(q, keys)", '''
import math
def attention(q, keys):
    d = len(q)
    scores = []
    for k in keys:
        s = 0.0
        for j in range(d):
            s = s + q[j] * k[j]
        scores.append(s / math.sqrt(d))
    m = max(scores)
    e = [math.exp(s - m) for s in scores]
    t = sum(e)
    return [round(v / t, 4) for v in e]
''', [[[1, 0], [[1, 0], [0, 1], [1, 1]]], [[0, 0], [[1, 2], [3, 4]]], [[2, 2, 2, 2], [[1, 1, 1, 1], [0, 0, 0, 0]]]], "Softmax of scaled scores.", approx=None),
  PL("Cosine similarity", "Write cosine(a, b): the cosine similarity of two vectors, rounded to 4 decimals.", "cosine(a, b)", '''
import math
def cosine(a, b):
    dot = sum([a[i] * b[i] for i in range(len(a))])
    na = math.sqrt(sum([v * v for v in a]))
    nb = math.sqrt(sum([v * v for v in b]))
    return round(dot / (na * nb), 4)
''', [[[1, 0], [0, 1]], [[1, 2, 3], [2, 4, 6]], [[1, 1], [-1, -1]]], "Dot product over the norms.", approx=0.0002),
  PL("Zero-shot classify", "Write zero_shot(image_vec, text_vecs, names): return the name whose text embedding has the highest cosine similarity with the image embedding (first on ties).", "zero_shot(image_vec, text_vecs, names)", '''
import math
def zero_shot(image_vec, text_vecs, names):
    def cos(a, b):
        dot = sum([a[i] * b[i] for i in range(len(a))])
        return dot / (math.sqrt(sum([v * v for v in a])) * math.sqrt(sum([v * v for v in b])))
    best = 0
    bv = None
    for i in range(len(text_vecs)):
        v = cos(image_vec, text_vecs[i])
        if bv is None or v > bv + 1e-12:
            bv = v
            best = i
    return names[best]
''', [[[1, 0.1], [[1, 0], [0, 1]], ['dog', 'cat']], [[0, 1], [[1, 0], [0, 1], [1, 1]], ['a', 'b', 'c']], [[1, 1], [[1, 0], [0, 1], [1, 1]], ['a', 'b', 'c']]], "Pick the closest text."),
  PL("Forward diffusion step", "Write noisy(x0, noise, alpha_bar): the noised sample x_t = sqrt(alpha_bar) x x0 + sqrt(1 - alpha_bar) x noise, elementwise on equal-length lists, rounded to 4 decimals.", "noisy(x0, noise, alpha_bar)", '''
import math
def noisy(x0, noise, alpha_bar):
    a = math.sqrt(alpha_bar)
    b = math.sqrt(1 - alpha_bar)
    return [round(a * x0[i] + b * noise[i], 4) for i in range(len(x0))]
''', [[[1, 0.5], [0, 1], 1.0], [[1, 0.5], [0.2, -0.3], 0.5], [[2], [1], 0.0]], "Blend signal and noise.", approx=None),
  PL("Accuracy by group", "Write group_accuracy(groups, y_true, y_pred): the accuracy per group as a list of [group, accuracy] sorted by group, rounded to 3 decimals.", "group_accuracy(groups, y_true, y_pred)", '''
def group_accuracy(groups, y_true, y_pred):
    tot = {}
    ok = {}
    for i in range(len(groups)):
        g = groups[i]
        tot[g] = tot.get(g, 0) + 1
        if y_true[i] == y_pred[i]:
            ok[g] = ok.get(g, 0) + 1
    return [[g, round(ok.get(g, 0) / float(tot[g]), 3)] for g in sorted(tot.keys())]
''', [[['a', 'a', 'b', 'b'], [1, 0, 1, 1], [1, 0, 0, 0]], [['x'], [1], [1]], [['p', 'q'], [0, 0], [1, 0]]], "Compare per group.", approx=None)]
))
