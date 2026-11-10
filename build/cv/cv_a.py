# -*- coding: utf-8 -*-
"""Computer vision course, part 1: pixels, filtering, edges, features, segmentation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []


def APP(key, title, intro, h=700):
    return {"type": "webxdc", "title": title, "intro": intro, "height": h, "html": "__%s__" % key}


IMG = "[[0, 0, 0, 0], [0, 9, 9, 0], [0, 9, 9, 0], [0, 0, 0, 0]]"

CHS.append(CH(
 "Images as data",
 ("Images", [
  "Image | is | A grid of pixels",
  "Pixel | holds | Intensity or colour",
  "Channel | is | One colour plane",
  "Grayscale | has | One channel",
  "Histogram | counts | Intensities",
  "Colour space | organises | Colour",
  "Resolution | is | Width by height"]),
 ["A digital image is a grid of pixels. A grayscale pixel is one number, usually 0 to 255; a colour pixel has three channels, red, green and blue. In code, an image is an array with a shape such as height by width by 3.",
  "Computer vision asks a machine to extract meaning from such arrays: what is in the picture, where, how far, how it moves. It splits into classical methods, built from hand-designed filters and geometry, and modern methods that learn their filters from data.",
  "Simple operations already do useful work: converting to gray, adjusting brightness, flipping, resizing and counting intensities in a histogram."],
 [("Pixel", "One element of an image: a number for gray, or several for colour."),
  ("Channel", "One plane of an image, such as the red channel."),
  ("Histogram", "A count of how many pixels have each intensity."),
  ("HSV", "A colour space with hue, saturation and value, closer to how people describe colour."),
  ("Resolution", "The number of pixels in the image, width by height.")],
 ["Image = array of shape (H, W) or (H, W, 3).",
  "Gray = 0.299 R + 0.587 G + 0.114 B.",
  "Histogram: count per intensity.",
  "Brightness: add and clip to 0..255.",
  "Index as img[row][col]."],
 [T("A camera sensor counts light at millions of little sites. Each site becomes a pixel, a number. Lay them in rows and columns and you have an image. To a program, a photograph is nothing but a big table of numbers, and every vision algorithm is a calculation on that table."),
  T("A grayscale image has one number per pixel, from zero for black to 255 for white. A colour image has three, one each for red, green and blue. We write its shape as height, width, channels. Rows come first, so pixel (r, c) is at row r down and column c across."),
  C("import numpy as np\nimport cv2                     # OpenCV\n\nimg = cv2.imread('cat.jpg')     # BGR order in OpenCV!\ngray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\nprint(img.shape, gray.shape)    # (480, 640, 3) (480, 640)\nhist = cv2.calcHist([gray], [0], None, [256], [0, 256])\nbright = np.clip(gray.astype(int) + 40, 0, 255).astype('uint8')", "python"),
  T("To turn colour into gray you average the channels, but not equally: the eye is most sensitive to green, so the standard weights are about 0.299 red, 0.587 green and 0.114 blue. Other colour spaces help other tasks. HSV separates the hue, the actual colour, from how pale and how bright it is, which makes tasks like finding red objects easier."),
  T("A histogram counts how many pixels have each brightness. A dark, low-contrast photo has all its counts bunched at the left. Stretching the histogram, or equalising it, spreads the values and boosts contrast. Brightness adjustment is addition with clipping to the range 0 to 255, so values do not wrap around."),
  T("This course follows the history of the field. First the classical toolkit of filters, edges, corners, segmentation and geometry, which still powers phones, factories and robots. Then convolutional networks, detection and segmentation, vision transformers and foundation models. The labs build the main ideas in plain Python on small images, so you see every step.")],
 [("What is a pixel?", ["One element of an image grid", "A kind of camera", "A file type", "A filter"], 0, "A number or three."),
  ("What is the shape of a colour image?", ["(height, width, 3)", "(3, 3)", "(width, height)", "(1, 1)"], 0, "Rows first."),
  ("Why weight green most in gray conversion?", ["The eye is most sensitive to green", "Green is brightest on screens", "It is easiest", "Cameras prefer green"], 0, "Perception."),
  ("What does a histogram count?", ["Pixels at each intensity", "Edges", "Faces", "Channels"], 0, "Intensity distribution."),
  ("Why clip after adding brightness?", ["To stay within 0..255", "To blur", "To sharpen", "To rotate"], 0, "Avoid overflow."),
  ("What does HSV separate?", ["Hue from saturation and brightness", "Rows from columns", "Gray from colour", "Noise from signal"], 0, "Colour space.")],
 [("img[r][c]", "pixel at row r, column c"), ("gray = .299R + .587G + .114B", "luminance"), ("np.clip(x, 0, 255)", "keep valid range")],
 [APP("KERNEL", "Convolution playground", "Pick a small test image and a 3x3 kernel (blur, sharpen, edge, emboss or your own numbers) and see the result. Try at least four different kernels to complete this lab.", 800),
  MATCH("Match the term", "Pair each term with its meaning.", [("Pixel", "one image element"), ("Channel", "one colour plane"), ("Histogram", "count per intensity"), ("HSV", "hue, saturation, value"), ("Grayscale", "one number per pixel")]),
  PL("RGB to gray", "Write to_gray(img): img is a list of rows of [r, g, b] pixels. Return a list of rows with the gray value round(0.299 r + 0.587 g + 0.114 b) as an integer.", "to_gray(img)", '''
def to_gray(img):
    out = []
    for row in img:
        out.append([int(round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2])) for p in row])
    return out
''', [[[[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]]], [[[[10, 20, 30]]]], [[[[100, 100, 100], [0, 0, 0]]]]], "Apply the weights to each pixel."),
  PL("Intensity histogram", "Write histogram(img, bins): the counts of pixel values 0..255 falling into bins equal-width bins (width 256 / bins) for a gray image (list of rows).", "histogram(img, bins)", '''
def histogram(img, bins):
    counts = [0] * bins
    w = 256 // bins
    for row in img:
        for v in row:
            i = v // w
            if i >= bins:
                i = bins - 1
            counts[i] = counts[i] + 1
    return counts
''', [[[[0, 10, 200], [255, 128, 64]], 4], [[[0, 0, 0]], 2], [[[100, 150], [200, 250]], 8]], "Integer divide by the bin width."),
  PL("Brightness", "Write brighten(img, delta): add delta to every pixel of a gray image and clip each result to 0..255.", "brighten(img, delta)", '''
def brighten(img, delta):
    return [[max(0, min(255, v + delta)) for v in row] for row in img]
''', [[[[0, 100, 250]], 20], [[[0, 100, 250]], -50], [[[10], [20]], 0]], "Clip with min and max."),
  PL("Flip and rotate", "Write rot90(img): rotate a gray image (list of rows) 90 degrees clockwise.", "rot90(img)", '''
def rot90(img):
    h = len(img)
    w = len(img[0])
    out = []
    for c in range(w):
        out.append([img[h - 1 - r][c] for r in range(h)])
    return out
''', [[[[1, 2, 3], [4, 5, 6]]], [[[1, 2], [3, 4]]], [[[7]]]], "Column c of the result is column c read bottom to top."),
  PL("Resize (nearest neighbour)", "Write resize(img, new_h, new_w): nearest-neighbour resize: output pixel (r, c) takes img[r * h // new_h][c * w // new_w] where h, w are the original sizes.", "resize(img, new_h, new_w)", '''
def resize(img, new_h, new_w):
    h = len(img)
    w = len(img[0])
    return [[img[r * h // new_h][c * w // new_w] for c in range(new_w)] for r in range(new_h)]
''', [[[[1, 2], [3, 4]], 4, 4], [[[1, 2, 3, 4], [5, 6, 7, 8]], 1, 2], [[[9]], 2, 3]], "Map each output pixel back to the source."),
  PL("Value channel (HSV)", "Write rgb_to_hsv(r, g, b) for 0..255 channels: return [hue in degrees 0..360 rounded to 1 decimal, saturation 0..1 rounded to 3, value 0..1 rounded to 3]. Hue is 0 when max equals min.", "rgb_to_hsv(r, g, b)", '''
def rgb_to_hsv(r, g, b):
    r1 = r / 255.0
    g1 = g / 255.0
    b1 = b / 255.0
    mx = max(r1, g1, b1)
    mn = min(r1, g1, b1)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r1:
        h = 60.0 * (((g1 - b1) / d) % 6)
    elif mx == g1:
        h = 60.0 * ((b1 - r1) / d + 2)
    else:
        h = 60.0 * ((r1 - g1) / d + 4)
    s = 0.0 if mx == 0 else d / mx
    return [round(h, 1), round(s, 3), round(mx, 3)]
''', [[255, 0, 0], [0, 255, 0], [0, 0, 255], [128, 128, 128], [255, 255, 0]], "Use the max channel to pick the hue branch.", approx=None)]
))

CHS.append(CH(
 "Filtering and convolution",
 ("Filtering", [
  "Kernel | is | A small weight grid",
  "Convolution | slides | The kernel",
  "Box blur | averages | Neighbours",
  "Gaussian | blurs | Smoothly",
  "Sharpen | boosts | Detail",
  "Median filter | removes | Salt and pepper",
  "Separable | splits | Into two 1D passes"]),
 ["A filter replaces each pixel by a weighted sum of its neighbours. The weights form a small grid called a kernel, and sliding it over the image is convolution (or its twin, correlation).",
  "A box blur averages; a Gaussian blur weights nearer pixels more and blurs without blocky artefacts; sharpening subtracts a blur from the original to boost detail. A median filter, which is not linear, removes isolated speckles without smearing edges.",
  "Many kernels are separable: a 2D Gaussian is the product of two 1D ones, which cuts the work from k squared to 2k per pixel."],
 [("Kernel", "A small grid of weights applied around each pixel."),
  ("Convolution", "Sliding a (flipped) kernel over an image and summing products at each position."),
  ("Gaussian blur", "A smoothing filter whose weights follow a bell curve."),
  ("Median filter", "Replaces each pixel with the median of its neighbourhood."),
  ("Separable filter", "A 2D kernel that is the outer product of two 1D kernels.")],
 ["out[r][c] = sum k[i][j] img[r+i][c+j].",
  "Blur kernels sum to 1.",
  "Edge kernels sum to 0.",
  "Gaussian sigma sets the blur size.",
  "Median removes salt and pepper noise."],
 [T("To blur a photo, replace each pixel by the average of itself and its eight neighbours. To sharpen it, push each pixel away from the average of its neighbours. Both are the same operation with different numbers. The numbers form a kernel, a little 3 by 3 table, and the operation is called convolution."),
  T("Strictly, convolution flips the kernel before sliding, while correlation does not. Deep learning libraries actually compute correlation and call it convolution. For symmetric kernels, such as blurs, there is no difference. The output is a new image, smaller by the kernel's border unless the edges are padded with zeros or copies."),
  C("import cv2, numpy as np\nblur = cv2.GaussianBlur(img, (5, 5), sigmaX=1.2)\nk = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)\nsharp = cv2.filter2D(img, -1, k)\nclean = cv2.medianBlur(noisy, 3)", "python"),
  T("The Gaussian kernel is the natural blur. Its weights fall off like a bell curve with distance, with a parameter sigma that sets how wide it is. A larger sigma gives a stronger blur. Because the 2D Gaussian equals a product of two 1D bell curves, you can blur rows then columns, which is much cheaper for big kernels."),
  T("Noise comes in kinds. Gaussian noise is small random variation everywhere, and blurring reduces it, at the cost of detail. Salt-and-pepper noise is isolated white and black dots. Blurring merely smears them, but a median filter, taking the middle value of the neighbourhood, removes them cleanly and keeps edges sharp. The playground lets you try kernels on a test image.")],
 [("What is a kernel?", ["A small grid of weights", "A kind of image", "A colour", "An operating system"], 0, "Filter weights."),
  ("What should a blur kernel sum to?", ["1", "0", "-1", "255"], 0, "Preserve brightness."),
  ("Which filter removes salt-and-pepper noise?", ["Median", "Box blur", "Sharpen", "Sobel"], 0, "Not linear."),
  ("Why are separable kernels useful?", ["Cheaper to compute", "They sharpen", "They remove colour", "They rotate"], 0, "Two 1D passes."),
  ("What does sigma control in a Gaussian?", ["The width of the blur", "The colour", "The rotation", "The size of the image"], 0, "Bell width."),
  ("What do deep learning libraries really compute?", ["Correlation", "Fourier transforms", "Medians", "Histograms"], 0, "No kernel flip.")],
 [("cv2.GaussianBlur", "smooth with a Gaussian"), ("cv2.filter2D", "apply any kernel"), ("cv2.medianBlur", "median filter")],
 [MATCH("Match the filter", "Pair each filter with its effect.", [("Box blur", "average of neighbours"), ("Gaussian", "smooth bell-shaped blur"), ("Sharpen", "boost detail"), ("Median", "remove speckle"), ("Edge kernel", "responds to changes")]),
  PL("Valid convolution (correlation)", "Write conv2d(img, k): slide the kernel k over img without padding (no flip). Output size (H - kh + 1) by (W - kw + 1); each value is the sum of kernel times covered pixels.", "conv2d(img, k)", '''
def conv2d(img, k):
    h = len(img)
    w = len(img[0])
    kh = len(k)
    kw = len(k[0])
    out = []
    for r in range(h - kh + 1):
        row = []
        for c in range(w - kw + 1):
            s = 0
            for i in range(kh):
                for j in range(kw):
                    s = s + k[i][j] * img[r + i][c + j]
            row.append(s)
        out.append(row)
    return out
''', [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0, 1], [1, 0]]], [[[0, 0, 0, 0], [0, 9, 9, 0], [0, 9, 9, 0], [0, 0, 0, 0]], [[1, 1], [1, 1]]], [[[1, 2, 3, 4]], [[1, -1]]]], "Four nested loops."),
  PL("Pad with zeros", "Write pad(img, p): surround the image with p rows and columns of zeros on every side.", "pad(img, p)", '''
def pad(img, p):
    w = len(img[0])
    out = []
    for i in range(p):
        out.append([0] * (w + 2 * p))
    for row in img:
        out.append([0] * p + list(row) + [0] * p)
    for i in range(p):
        out.append([0] * (w + 2 * p))
    return out
''', [[[[1, 2], [3, 4]], 1], [[[5]], 2], [[[1, 2, 3]], 0]], "Add zeros around."),
  PL("Box blur", "Write box_blur(img): the 3x3 mean filter over the valid region, each value rounded to 2 decimals.", "box_blur(img)", '''
def box_blur(img):
    h = len(img)
    w = len(img[0])
    out = []
    for r in range(h - 2):
        row = []
        for c in range(w - 2):
            s = 0
            for i in range(3):
                for j in range(3):
                    s = s + img[r + i][c + j]
            row.append(round(s / 9.0, 2))
        out.append(row)
    return out
''', [[[[0, 0, 0, 0], [0, 9, 9, 0], [0, 9, 9, 0], [0, 0, 0, 0]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[9, 9, 9], [9, 9, 9], [9, 9, 9]]]], "Average nine values.", approx=None),
  PL("Gaussian kernel", "Write gaussian_kernel(size, sigma): a size x size kernel (size odd) with weights exp(-(x^2 + y^2) / (2 sigma^2)) where x, y are offsets from the centre, normalised to sum to 1, rounded to 4 decimals.", "gaussian_kernel(size, sigma)", '''
import math
def gaussian_kernel(size, sigma):
    c = size // 2
    k = []
    total = 0.0
    for i in range(size):
        row = []
        for j in range(size):
            v = math.exp(-((i - c) ** 2 + (j - c) ** 2) / (2.0 * sigma * sigma))
            row.append(v)
            total = total + v
        k.append(row)
    return [[round(v / total, 4) for v in row] for row in k]
''', [[3, 1.0], [3, 0.5], [5, 1.0]], "Compute then normalise.", approx=None),
  PL("Median filter", "Write median3x3(img): the 3x3 median filter over the valid region.", "median3x3(img)", '''
def median3x3(img):
    h = len(img)
    w = len(img[0])
    out = []
    for r in range(h - 2):
        row = []
        for c in range(w - 2):
            vals = []
            for i in range(3):
                for j in range(3):
                    vals.append(img[r + i][c + j])
            vals.sort()
            row.append(vals[4])
        out.append(row)
    return out
''', [[[[1, 1, 1, 1], [1, 99, 1, 1], [1, 1, 1, 1]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[0, 0, 0], [0, 255, 0], [0, 0, 0]]]], "Sort nine values and take the fifth."),
  PL("Is it separable?", "Write outer(a, b): the 2D kernel that is the outer product of 1D vectors a (column) and b (row): result[i][j] = a[i] x b[j].", "outer(a, b)", '''
def outer(a, b):
    return [[x * y for y in b] for x in a]
''', [[[1, 2, 1], [1, 2, 1]], [[1, 0, -1], [1, 1, 1]], [[2], [3, 4]]], "Multiply every pair.")]
))

CHS.append(CH(
 "Edges, gradients and lines",
 ("Edges", [
  "Edge | is | Sharp change",
  "Gradient | points | Uphill",
  "Sobel | estimates | Gradient",
  "Magnitude | gives | Edge strength",
  "Canny | thins | And links edges",
  "Hough | votes for | Lines",
  "Noise | confuses | Derivatives"]),
 ["An edge is a place where brightness changes quickly. The gradient of an image points in the direction of fastest increase and its length measures how fast; edges are where the gradient magnitude is large.",
  "The Sobel kernels estimate the horizontal and vertical derivatives. The Canny detector smooths, finds the gradient, thins edges to one pixel by non-maximum suppression and links them with two thresholds.",
  "The Hough transform finds lines by letting every edge pixel vote for all the lines that could pass through it; real lines collect many votes."],
 [("Gradient", "A vector of partial derivatives (dI/dx, dI/dy) pointing to the steepest increase."),
  ("Sobel operator", "A pair of 3x3 kernels that approximate the x and y derivatives with some smoothing."),
  ("Non-maximum suppression", "Keeping only pixels that are local maxima along the gradient direction, to thin edges."),
  ("Hysteresis thresholding", "Keeping strong edges and weak edges only if connected to strong ones."),
  ("Hough transform", "A voting method that detects shapes, such as lines, in a parameter space.")],
 ["Magnitude = sqrt(Gx^2 + Gy^2).",
  "Direction = atan2(Gy, Gx).",
  "Canny: blur, gradient, thin, threshold.",
  "Line: rho = x cos(theta) + y sin(theta).",
  "Smooth first or noise explodes."],
 [T("Where does one object end and another begin? Often at an edge: a sudden jump in brightness. In calculus a jump is a large derivative, so edge detection is derivative estimation. For an image we have two derivatives, left to right and top to bottom, and together they make the gradient."),
  T("A derivative is a difference between neighbours. The Sobel kernels do this over a 3 by 3 patch and also smooth a little, which tames noise. One kernel responds to vertical edges, the other to horizontal. Combine their outputs as the square root of the sum of squares to get the strength of the edge in any direction, and take the arctangent to get its orientation."),
  C("gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)\ngy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)\nmag = np.hypot(gx, gy)\nedges = cv2.Canny(gray, 100, 200)\nlines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,\n                        minLineLength=50, maxLineGap=10)", "python"),
  T("A thick band of strong gradient is not yet an edge map. John Canny's 1986 detector adds three ideas. Blur first to resist noise. Thin the band to a single pixel line by keeping only local maxima across the edge. Then use two thresholds: strong pixels are certainly edges, weak ones count only if they connect to a strong one. This gives clean continuous contours and the method is still widely used."),
  T("Edges are fragments; we often want lines, circles or other shapes. The Hough transform turns detection into voting. A line through the origin at angle theta is described by its distance rho. Each edge pixel votes for every pair of values rho and theta consistent with a line through it. Votes pile up for the true lines. The method tolerates gaps and noise, and the lab runs it on a handful of points.")],
 [("What is an edge?", ["A place of rapid brightness change", "A border of the file", "A colour", "A filter"], 0, "Large gradient."),
  ("What does the gradient magnitude measure?", ["Edge strength", "Colour", "Image size", "Noise only"], 0, "sqrt(Gx^2 + Gy^2)."),
  ("What does Canny's non-maximum suppression do?", ["Thins edges to one pixel", "Blurs", "Adds colour", "Resizes"], 0, "Local maxima."),
  ("What is hysteresis thresholding?", ["Weak edges kept if linked to strong", "Using one threshold", "Blurring twice", "Sorting"], 0, "Two thresholds."),
  ("How does the Hough transform find lines?", ["Edge pixels vote in parameter space", "By blurring", "By sorting pixels", "By colour"], 0, "Voting."),
  ("Why smooth before differentiating?", ["Derivatives amplify noise", "To brighten", "To resize", "To invert"], 0, "Noise explodes.")],
 [("cv2.Canny(img, lo, hi)", "edge detector"), ("rho = x cos t + y sin t", "line parameters"), ("atan2(gy, gx)", "edge direction")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Gradient", "direction of steepest increase"), ("Sobel", "derivative kernels"), ("NMS", "thin edges"), ("Hysteresis", "two-threshold linking"), ("Hough", "voting for lines")]),
  PL("Sobel gradients", "Write sobel(img): for the valid 3x3 positions return [Gx, Gy] where Gx is the sum of the kernel [[-1,0,1],[-2,0,2],[-1,0,1]] times the patch and Gy the same with the transposed kernel [[-1,-2,-1],[0,0,0],[1,2,1]]. Return two images (lists of rows): [Gx_image, Gy_image].", "sobel(img)", '''
def sobel(img):
    kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    h = len(img)
    w = len(img[0])
    gx = []
    gy = []
    for r in range(h - 2):
        rx = []
        ry = []
        for c in range(w - 2):
            sx = 0
            sy = 0
            for i in range(3):
                for j in range(3):
                    sx = sx + kx[i][j] * img[r + i][c + j]
                    sy = sy + ky[i][j] * img[r + i][c + j]
            rx.append(sx)
            ry.append(sy)
        gx.append(rx)
        gy.append(ry)
    return [gx, gy]
''', [[[[0, 0, 9, 9], [0, 0, 9, 9], [0, 0, 9, 9]]], [[[0, 0, 0], [0, 0, 0], [9, 9, 9]]], [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]], "Two kernels, one patch."),
  PL("Gradient magnitude", "Write magnitude(gx, gy): the element-wise sqrt(gx^2 + gy^2) of two equal-sized images, each rounded to 2 decimals.", "magnitude(gx, gy)", '''
import math
def magnitude(gx, gy):
    out = []
    for r in range(len(gx)):
        out.append([round(math.sqrt(gx[r][c] ** 2 + gy[r][c] ** 2), 2) for c in range(len(gx[0]))])
    return out
''', [[[[3, 0]], [[4, 5]]], [[[0]], [[0]]], [[[6, -8]], [[8, 6]]]], "Pythagoras per pixel.", approx=None),
  PL("Edge direction", "Write direction(gx, gy): the gradient angle atan2(gy, gx) in degrees rounded to the nearest integer.", "direction(gx, gy)", '''
import math
def direction(gx, gy):
    return int(round(math.degrees(math.atan2(gy, gx))))
''', [[1, 0], [0, 1], [-1, 0], [1, 1], [0, -1]], "Use atan2."),
  PL("Threshold edges", "Write edge_map(mag, t): a binary image with 1 where mag >= t, else 0.", "edge_map(mag, t)", '''
def edge_map(mag, t):
    return [[1 if v >= t else 0 for v in row] for row in mag]
''', [[[[1, 5, 9], [3, 7, 2]], 5], [[[0, 0]], 1], [[[4]], 4]], "Compare each value."),
  PL("Hysteresis", "Write hysteresis(mag, lo, hi): a row of strengths is processed in one dimension: a value >= hi is an edge; a value >= lo is an edge only if an adjacent value (left or right) is an edge after propagation. Take a 1D list mag and return the 0/1 list. Propagate repeatedly until nothing changes.", "hysteresis(mag, lo, hi)", '''
def hysteresis(mag, lo, hi):
    n = len(mag)
    e = [1 if v >= hi else 0 for v in mag]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if e[i] == 0 and mag[i] >= lo:
                if (i > 0 and e[i - 1] == 1) or (i < n - 1 and e[i + 1] == 1):
                    e[i] = 1
                    changed = True
    return e
''', [[[1, 5, 9, 5, 1], 4, 8], [[5, 5, 5, 9], 4, 8], [[5, 1, 5], 4, 8], [[9, 5, 5, 5, 1], 4, 8]], "Grow from strong edges."),
  PL("Hough accumulator", "Write hough(points, thetas): points is a list of [x, y]; thetas a list of angles in degrees. For each point and angle compute rho = round(x cos(theta) + y sin(theta)) and count votes. Return [theta, rho, votes] for the cell with the most votes (ties: smallest theta, then smallest rho).", "hough(points, thetas)", '''
import math
def hough(points, thetas):
    votes = {}
    for p in points:
        for t in thetas:
            a = math.radians(t)
            rho = int(round(p[0] * math.cos(a) + p[1] * math.sin(a)))
            key = (t, rho)
            votes[key] = votes.get(key, 0) + 1
    best = None
    for key in sorted(votes.keys()):
        if best is None or votes[key] > votes[best]:
            best = key
    return [best[0], best[1], votes[best]]
''', [[[[0, 3], [1, 3], [2, 3], [5, 3]], [0, 45, 90, 135]], [[[2, 0], [2, 1], [2, 4]], [0, 90]], [[[0, 0], [1, 1], [2, 2], [3, 3]], [0, 45, 90, 135]]], "Each point votes once per angle.")]
))

CHS.append(CH(
 "Features, matching and geometry of images",
 ("Features", [
  "Corner | is | Distinct feature",
  "Keypoint | is | A stable location",
  "Descriptor | summarises | A patch",
  "SIFT ORB | are | Feature methods",
  "Matching | compares | Descriptors",
  "RANSAC | rejects | Outliers",
  "Homography | maps | Plane views"]),
 ["To recognise a place or stitch photos we need points that can be found again from another view. Corners are good: the image changes in every direction around them. The Harris detector scores this with the structure tensor.",
  "A descriptor summarises the patch around a keypoint as a vector. SIFT uses gradient histograms; ORB uses a binary string compared with Hamming distance. Matching finds nearest descriptors and a ratio test removes ambiguous ones.",
  "RANSAC fits a model, such as a homography, to many noisy matches by repeatedly fitting to random minimal sets and keeping the model with the most inliers."],
 [("Keypoint", "A distinctive, repeatable image location such as a corner."),
  ("Descriptor", "A vector describing the appearance around a keypoint, used for matching."),
  ("Ratio test", "Accepting a match only if the best distance is much smaller than the second-best."),
  ("RANSAC", "Random sample consensus: fit models to random subsets and keep the one agreeing with most data."),
  ("Homography", "A 3x3 matrix mapping points between two views of a plane.")],
 ["Harris: R = det(M) - k trace(M)^2.",
  "ORB descriptor: bits; compare with Hamming distance.",
  "Ratio test: d1 < 0.75 d2.",
  "RANSAC: sample, fit, count inliers, repeat.",
  "Homography: (x, y, 1) -> H (x, y, 1)."],
 [T("Stand in front of a blank wall and you cannot tell where you are looking. Stand in front of a window frame and you can. Corners and blobs are distinctive: shift a small window around them and the picture changes in every direction. The Harris detector measures exactly that. From the image gradients in a window it forms a small 2 by 2 matrix; a corner makes both of its eigenvalues large, an edge only one, and a flat patch none."),
  T("Finding a keypoint is half the job. To match it in another photo we describe its neighbourhood with a vector that survives changes in rotation, scale and lighting. SIFT, from David Lowe, builds histograms of gradient directions. ORB makes a string of brightness comparisons between pixel pairs, a binary descriptor that can be compared with the Hamming distance, the count of differing bits, extremely fast."),
  C("orb = cv2.ORB_create(1000)\nk1, d1 = orb.detectAndCompute(img1, None)\nk2, d2 = orb.detectAndCompute(img2, None)\nbf = cv2.BFMatcher(cv2.NORM_HAMMING)\nmatches = bf.knnMatch(d1, d2, k=2)\ngood = [m for m, n in matches if m.distance < 0.75 * n.distance]\npts1 = np.float32([k1[m.queryIdx].pt for m in good])\npts2 = np.float32([k2[m.trainIdx].pt for m in good])\nH, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)", "python"),
  T("Matching is never perfect: repeated windows and textures create ambiguous matches. Lowe's ratio test keeps a match only when the best candidate is clearly closer than the second best. Some wrong matches still remain, and a method that fits a line or homography by least squares would be dragged away by them. RANSAC is the cure."),
  T("RANSAC picks the minimum number of matches needed for the model, two for a line, four for a homography, fits it, and counts how many other matches agree within a tolerance, the inliers. After many random trials, it keeps the model with the most inliers and refits on them. A homography is the 3 by 3 matrix describing how a flat surface looks from two viewpoints, which is the basis of panorama stitching, document scanning and augmented reality.")],
 [("What makes a good keypoint?", ["The image changes in every direction around it", "It is in the centre", "It is bright", "It is gray"], 0, "Corner."),
  ("What does ORB compare with?", ["Hamming distance", "Euclidean only", "Edit distance", "Colour"], 0, "Binary string."),
  ("What does the ratio test do?", ["Removes ambiguous matches", "Blurs", "Detects corners", "Scales"], 0, "Best vs second best."),
  ("What does RANSAC do?", ["Fits a model robustly to noisy data", "Detects edges", "Sorts pixels", "Reduces colour"], 0, "Inliers."),
  ("How many matches does a homography need?", ["Four", "Two", "One", "Eight"], 0, "Four point pairs."),
  ("What is a homography used for?", ["Mapping between views of a plane", "Blurring", "Counting pixels", "Compressing"], 0, "Panoramas.")],
 [("R = det(M) - k tr(M)^2", "Harris response"), ("cv2.findHomography", "estimate homography"), ("d1 < 0.75 d2", "ratio test")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Harris", "corner detector"), ("ORB", "binary descriptor"), ("Hamming distance", "count of different bits"), ("RANSAC", "robust model fitting"), ("Homography", "plane-to-plane mapping")]),
  PL("Harris response", "Write harris(sxx, syy, sxy, k): the Harris corner response det(M) - k trace(M)^2 for M = [[sxx, sxy], [sxy, syy]], rounded to 3 decimals.", "harris(sxx, syy, sxy, k)", '''
def harris(sxx, syy, sxy, k):
    det = sxx * syy - sxy * sxy
    tr = sxx + syy
    return round(det - k * tr * tr, 3)
''', [[10, 10, 0, 0.04], [10, 0, 0, 0.04], [0, 0, 0, 0.04], [5, 8, 2, 0.05]], "Determinant minus k trace squared.", approx=0.002),
  PL("Hamming distance", "Write hamming(a, b): the number of differing bits between two integers.", "hamming(a, b)", '''
def hamming(a, b):
    x = a ^ b
    n = 0
    while x:
        n = n + (x & 1)
        x = x >> 1
    return n
''', [[0, 0], [5, 3], [255, 0], [170, 85], [12, 12]], "XOR then count ones."),
  PL("Nearest descriptor", "Write match(desc, candidates): the index of the candidate (list of numbers) with the smallest squared Euclidean distance to the descriptor desc (lowest index on ties).", "match(desc, candidates)", '''
def match(desc, candidates):
    best = 0
    bd = None
    for i in range(len(candidates)):
        d = 0
        for j in range(len(desc)):
            d = d + (desc[j] - candidates[i][j]) ** 2
        if bd is None or d < bd:
            bd = d
            best = i
    return best
''', [[[1, 1], [[5, 5], [1, 2], [0, 0]]], [[0, 0, 0], [[1, 1, 1], [1, 1, 1]]], [[9], [[1], [8], [10]]]], "Compare distances."),
  PL("Ratio test", "Write ratio_test(dists, ratio): given the distances to a keypoint's candidates, return True if the smallest distance is below ratio times the second smallest (False if fewer than two candidates).", "ratio_test(dists, ratio)", '''
def ratio_test(dists, ratio):
    if len(dists) < 2:
        return False
    s = sorted(dists)
    return s[0] < ratio * s[1]
''', [[[1, 10, 20], 0.75], [[5, 6], 0.75], [[3], 0.75], [[2, 2.5, 9], 0.8]], "Compare best with second best."),
  PL("Apply a homography", "Write apply_h(H, x, y): map the point (x, y) by the 3x3 matrix H using homogeneous coordinates: (u, v, w) = H (x, y, 1); return [u / w, v / w] rounded to 3 decimals.", "apply_h(H, x, y)", '''
def apply_h(H, x, y):
    u = H[0][0] * x + H[0][1] * y + H[0][2]
    v = H[1][0] * x + H[1][1] * y + H[1][2]
    w = H[2][0] * x + H[2][1] * y + H[2][2]
    return [round(u / w, 3), round(v / w, 3)]
''', [[[[1, 0, 5], [0, 1, 3], [0, 0, 1]], 2, 2], [[[2, 0, 0], [0, 2, 0], [0, 0, 1]], 1, 1], [[[1, 0, 0], [0, 1, 0], [0.1, 0, 1]], 10, 5]], "Divide by w at the end.", approx=0.002),
  PL("RANSAC inliers", "Write inliers(points, a, b, c, tol): count the [x, y] points whose distance to the line a x + b y + c = 0 is at most tol (distance |a x + b y + c| / sqrt(a^2 + b^2)).", "inliers(points, a, b, c, tol)", '''
import math
def inliers(points, a, b, c, tol):
    n = 0
    d = math.sqrt(a * a + b * b)
    for p in points:
        if abs(a * p[0] + b * p[1] + c) / d <= tol:
            n = n + 1
    return n
''', [[[[0, 0], [1, 1], [2, 2], [3, 10]], 1, -1, 0, 0.1], [[[0, 1], [5, 1], [9, 3]], 0, 1, -1, 0.5], [[[1, 1]], 1, 1, 0, 0.5]], "Count points close to the line.")]
))

CHS.append(CH(
 "Segmentation, morphology and regions",
 ("Segmentation", [
  "Segmentation | splits | Image into regions",
  "Threshold | separates | Light from dark",
  "Otsu | picks | Best threshold",
  "Morphology | reshapes | Binary masks",
  "Connected components | label | Blobs",
  "Watershed | floods | From markers",
  "Clustering | groups | Pixel colours"]),
 ["Segmentation divides an image into meaningful regions. The simplest method is thresholding: pixels above a value are foreground. Otsu's method picks the threshold that best separates the two groups of the histogram.",
  "Morphological operations clean up binary masks: erosion shrinks shapes and removes specks, dilation grows them and fills holes, and opening and closing combine the two.",
  "Connected component labelling counts and measures blobs. Clustering colours with k-means and the watershed algorithm are other classical ways to segment."],
 [("Thresholding", "Splitting pixels into two classes by comparing intensity with a value."),
  ("Otsu's method", "A way to choose a threshold by maximising the variance between the two resulting classes."),
  ("Erosion", "Shrinking foreground shapes: a pixel stays only if all its neighbours are foreground."),
  ("Dilation", "Growing foreground shapes: a pixel turns on if any neighbour is foreground."),
  ("Connected components", "Maximal sets of foreground pixels connected to each other.")],
 ["mask = img > t.",
  "Opening = erode then dilate (removes specks).",
  "Closing = dilate then erode (fills holes).",
  "Connectivity: 4 or 8 neighbours.",
  "Otsu: maximise between-class variance."],
 [T("Count the coins on a table, find the tumour in a scan, cut a person out of a photo. All start with segmentation: deciding which pixels belong together. The simplest idea is a threshold. If coins are bright and the table is dark, mark every pixel above some value as coin."),
  T("But which value? Look at the histogram. If there are two humps, one for the dark background and one for the bright objects, the best threshold sits in the valley. Otsu's method finds it automatically by trying every threshold and keeping the one that makes the two groups most different from each other, measured by the variance between the classes."),
  C("_, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\nkernel = np.ones((3, 3), np.uint8)\nclean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)\nn, labels, stats, centroids = cv2.connectedComponentsWithStats(clean)\nprint('objects:', n - 1)", "python"),
  T("Thresholding leaves noisy masks: stray dots and little holes. Morphological operations use a small shape, the structuring element, to tidy up. Erosion keeps a pixel only if the whole neighbourhood is foreground, so it removes specks and shrinks shapes. Dilation turns a pixel on if any neighbour is on, so it grows shapes and closes gaps. Erosion followed by dilation, called opening, removes specks without changing big shapes."),
  T("Then label the blobs. Connected component analysis scans the mask and gives each group of touching foreground pixels its own number, by flood filling from each unvisited pixel. The count gives the number of coins and the statistics give each one's area and centre. Touching coins merge into one blob, which is where the watershed algorithm, treating the image as a landscape to flood from markers, can split them.")],
 [("What does thresholding do?", ["Splits pixels into two classes by intensity", "Blurs", "Rotates", "Adds colour"], 0, "Foreground and background."),
  ("What does Otsu's method choose?", ["The threshold that best separates two classes", "The brightest pixel", "The kernel", "The colour"], 0, "Between-class variance."),
  ("What does erosion do?", ["Shrinks foreground shapes", "Grows shapes", "Blurs", "Sharpens"], 0, "Removes specks."),
  ("What is opening?", ["Erosion then dilation", "Dilation then erosion", "Two dilations", "A threshold"], 0, "Cleans noise."),
  ("What do connected components give?", ["Labelled blobs", "Edges", "Corners", "Histograms"], 0, "Count objects."),
  ("What is watershed useful for?", ["Splitting touching objects", "Blurring", "Colour correcting", "Resizing"], 0, "Flooding.")],
 [("cv2.THRESH_OTSU", "automatic threshold"), ("cv2.morphologyEx", "morphological ops"), ("connectedComponents", "label blobs")],
 [MATCH("Match the term", "Pair each term with its meaning.", [("Threshold", "split by intensity"), ("Erosion", "shrink shapes"), ("Dilation", "grow shapes"), ("Opening", "remove specks"), ("Connected component", "touching foreground group")]),
  PL("Threshold", "Write threshold(img, t): 1 where the pixel is greater than t, else 0.", "threshold(img, t)", '''
def threshold(img, t):
    return [[1 if v > t else 0 for v in row] for row in img]
''', [[[[10, 200], [90, 130]], 100], [[[0, 0]], 0], [[[5]], 4]], "Compare each pixel."),
  PL("Otsu threshold", "Write otsu(hist): for a histogram (list of counts per intensity level, at least 2 levels), return the threshold t (levels 0..t are background) that maximises the between-class variance w0 w1 (m0 - m1)^2. The first t wins ties.", "otsu(hist)", '''
def otsu(hist):
    total = float(sum(hist))
    best = 0
    bv = -1.0
    for t in range(len(hist) - 1):
        w0 = sum(hist[:t + 1]) / total
        w1 = 1 - w0
        if w0 == 0 or w1 == 0:
            continue
        m0 = sum([i * hist[i] for i in range(t + 1)]) / (w0 * total)
        m1 = sum([i * hist[i] for i in range(t + 1, len(hist))]) / (w1 * total)
        v = w0 * w1 * (m0 - m1) ** 2
        if v > bv + 1e-9:
            bv = v
            best = t
    return best
''', [[[5, 10, 2, 0, 0, 3, 9, 6]], [[10, 0, 0, 10]], [[1, 8, 1, 0, 0, 1, 8, 1]]], "Try every threshold.", approx=None),
  PL("Erode", "Write erode(mask): a pixel stays 1 only if it and all of its 4-neighbours (up, down, left, right) are 1 and inside the image; otherwise 0.", "erode(mask)", '''
def erode(mask):
    h = len(mask)
    w = len(mask[0])
    out = []
    for r in range(h):
        row = []
        for c in range(w):
            ok = mask[r][c] == 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr = r + dr
                cc = c + dc
                if rr < 0 or rr >= h or cc < 0 or cc >= w or mask[rr][cc] != 1:
                    ok = False
            row.append(1 if ok else 0)
        out.append(row)
    return out
''', [[[[1, 1, 1], [1, 1, 1], [1, 1, 1]]], [[[0, 1, 0], [1, 1, 1], [0, 1, 0]]], [[[1, 0], [0, 0]]]], "Check the four neighbours."),
  PL("Dilate", "Write dilate(mask): a pixel becomes 1 if it or any of its 4-neighbours is 1.", "dilate(mask)", '''
def dilate(mask):
    h = len(mask)
    w = len(mask[0])
    out = []
    for r in range(h):
        row = []
        for c in range(w):
            on = mask[r][c] == 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                rr = r + dr
                cc = c + dc
                if 0 <= rr < h and 0 <= cc < w and mask[rr][cc] == 1:
                    on = True
            row.append(1 if on else 0)
        out.append(row)
    return out
''', [[[[0, 0, 0], [0, 1, 0], [0, 0, 0]]], [[[1, 0], [0, 0]]], [[[0, 0], [0, 0]]]], "Any neighbour on."),
  PL("Count blobs", "Write count_blobs(mask): the number of 4-connected components of 1s.", "count_blobs(mask)", '''
def count_blobs(mask):
    h = len(mask)
    w = len(mask[0])
    seen = [[False] * w for _ in range(h)]
    n = 0
    for r in range(h):
        for c in range(w):
            if mask[r][c] == 1 and not seen[r][c]:
                n = n + 1
                stack = [(r, c)]
                seen[r][c] = True
                while stack:
                    y, x = stack.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        yy = y + dy
                        xx = x + dx
                        if 0 <= yy < h and 0 <= xx < w and mask[yy][xx] == 1 and not seen[yy][xx]:
                            seen[yy][xx] = True
                            stack.append((yy, xx))
    return n
''', [[[[1, 0, 1], [0, 0, 0], [1, 1, 1]]], [[[1, 1], [1, 1]]], [[[1, 0], [0, 1]]], [[[0, 0]]]], "Flood fill from each unseen 1."),
  PL("Blob areas", "Write blob_areas(mask): the sorted list of areas (pixel counts) of the 4-connected components.", "blob_areas(mask)", '''
def blob_areas(mask):
    h = len(mask)
    w = len(mask[0])
    seen = [[False] * w for _ in range(h)]
    areas = []
    for r in range(h):
        for c in range(w):
            if mask[r][c] == 1 and not seen[r][c]:
                a = 0
                stack = [(r, c)]
                seen[r][c] = True
                while stack:
                    y, x = stack.pop()
                    a = a + 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        yy = y + dy
                        xx = x + dx
                        if 0 <= yy < h and 0 <= xx < w and mask[yy][xx] == 1 and not seen[yy][xx]:
                            seen[yy][xx] = True
                            stack.append((yy, xx))
                areas.append(a)
    return sorted(areas)
''', [[[[1, 0, 1], [0, 0, 0], [1, 1, 1]]], [[[1, 1, 0], [1, 0, 1]]], [[[0]]]], "Count pixels while flooding.")]
))
