#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Computer Vision course. Usage: python3 make_computer_vision_course.py [out.json]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "cv"))
import cmk, cv_a, cv_b, make_apps  # noqa: E402
make_apps.main()
CHS = cv_a.CHS + cv_b.CHS
PRONOUNCE = {"OpenCV": "open C V", "Sobel": "so bul", "Canny": "can nee", "Hough": "huff", "Harris": "har iss", "SIFT": "sift", "ORB": "orb", "RANSAC": "ran sack", "Otsu": "oat sue",
    "HOG": "hog", "Haar": "har", "Viola": "vee oh luh", "Jones": "jones", "Dalal": "dah lahl", "Triggs": "triggs", "YOLO": "yo low", "SSD": "S S D", "U-Net": "you net", "ResNet": "res net",
    "AlexNet": "alex net", "ImageNet": "image net", "CLIP": "clip", "SAM": "sam", "DINO": "dye no", "LiDAR": "lie dar", "SLAM": "slam", "SVM": "S V M", "HSV": "H S V", "RGB": "R G B",
    "homography": "ho mog ruh fee", "epipolar": "epp ih po lar", "dilation": "dye lay shun", "morphology": "mor fol uh jee", "Gaussian": "gow see un", "Laplacian": "la plah see un",
    "mAP": "M A P", "IoU": "I O U", "NMS": "N M S", "ViT": "V I T", "kernel": "ker nul", "Lowe": "low", "Cooley": "koo lee"}
SANDBOX = cmk.terminal("Vision cheat sheet", "cv>", "A scripted lookup. Try: gray, conv, sobel, canny, hough, harris, ransac, otsu, iou, nms, resnet, vit, clip", [
    ("gray", ["gray = 0.299 R + 0.587 G + 0.114 B."]),
    ("conv", ["out[r][c] = sum k[i][j] img[r+i][c+j]. Blur kernels sum to 1, edge kernels sum to 0."]),
    ("sobel", ["Gx = [[-1,0,1],[-2,0,2],[-1,0,1]], Gy is its transpose. Magnitude = sqrt(Gx^2 + Gy^2)."]),
    ("canny", ["Blur, gradient, non-maximum suppression, two thresholds with linking."]),
    ("hough", ["Each edge pixel votes for rho = x cos t + y sin t."]),
    ("harris", ["R = det(M) - k trace(M)^2, large at corners."]),
    ("ransac", ["Sample minimal set, fit, count inliers, repeat, keep the best."]),
    ("otsu", ["Pick the threshold that maximises between-class variance."]),
    ("iou", ["Intersection over union of two boxes. Match if IoU >= 0.5."]),
    ("nms", ["Sort by score, keep the best, drop boxes with IoU above the threshold."]),
    ("resnet", ["y = F(x) + x. Skip connections let very deep networks train."]),
    ("vit", ["Cut the image into patches, treat them as tokens, apply self-attention."]),
    ("clip", ["Image and text embeddings in one space; zero-shot by cosine similarity."]),
])
EXAM = [
 ("What is a pixel?", ["One element of an image grid", "A kind of filter", "A camera lens", "A colour space"], 0, "A number or three."),
 ("What does a colour image's shape look like?", ["(height, width, 3)", "(3, 3)", "(width, 1)", "(1, 1)"], 0, "Channels last."),
 ("Why weight green most in gray conversion?", ["The eye is most sensitive to green", "It is brightest", "It is cheapest", "Sensors need it"], 0, "Perception."),
 ("What should a blur kernel sum to?", ["1", "0", "-1", "255"], 0, "Keep brightness."),
 ("Which filter removes salt-and-pepper noise?", ["Median", "Box blur", "Sobel", "Sharpen"], 0, "Nonlinear."),
 ("What does the Sobel operator estimate?", ["Image derivatives", "Colour", "Depth", "Noise"], 0, "Gradients."),
 ("What does Canny's non-maximum suppression do?", ["Thins edges", "Blurs", "Sharpens", "Resizes"], 0, "One pixel wide."),
 ("How does the Hough transform detect lines?", ["Pixels vote in parameter space", "By colour", "By blurring", "By sorting"], 0, "Voting."),
 ("What makes a good keypoint?", ["The image changes in all directions around it", "It is bright", "It is in the centre", "It is gray"], 0, "Corner."),
 ("What does RANSAC do?", ["Fits a model robustly to noisy matches", "Detects edges", "Blurs", "Resizes"], 0, "Inliers."),
 ("How many point pairs define a homography?", ["Four", "Two", "One", "Eight"], 0, "Four correspondences."),
 ("What does Otsu's method choose?", ["A threshold maximising between-class variance", "A kernel", "A colour", "A filter size"], 0, "Automatic."),
 ("What does erosion do?", ["Shrinks foreground shapes", "Grows them", "Blurs", "Sharpens"], 0, "Removes specks."),
 ("In the pinhole model, image position is:", ["f X / Z", "X + Z", "f Z / X", "X / f"], 0, "Farther is smaller."),
 ("Stereo depth is:", ["f B / d", "d / (f B)", "f + B", "B d"], 0, "Disparity inverse."),
 ("How many lookups give a rectangle sum in an integral image?", ["Four", "One", "Area", "Eight"], 0, "Corners."),
 ("What does HOG describe?", ["Shape by gradient directions", "Colour", "Depth", "Noise"], 0, "Cells of histograms."),
 ("What does a convolutional layer share across positions?", ["Kernel weights", "Outputs", "Inputs", "Biases only"], 0, "Weight sharing."),
 ("What did ResNet introduce?", ["Skip connections", "Pooling", "ReLU", "Kernels"], 0, "y = F(x) + x."),
 ("Why use transfer learning?", ["It needs little data", "It is slower", "It avoids labels", "It avoids GPUs"], 0, "Reuse features."),
 ("What does IoU measure?", ["Overlap of two boxes", "Brightness", "Box colour", "Speed"], 0, "Intersection over union."),
 ("What does NMS do?", ["Removes duplicate overlapping boxes", "Adds boxes", "Blurs", "Rotates"], 0, "Keep the best."),
 ("What does U-Net output?", ["A label per pixel", "One class", "A single box", "A caption"], 0, "Semantic segmentation."),
 ("What does ViT feed the transformer?", ["Image patches as tokens", "Single pixels", "Histograms", "Edges"], 0, "16x16 patches."),
 ("What is CLIP trained on?", ["Images paired with captions", "Only labels", "Only text", "Depth maps"], 0, "Shared space."),
 ("What is zero-shot classification?", ["Classifying with text descriptions of classes", "Using no model", "Training from scratch", "Using zero data"], 0, "Compare with prompts."),
]
CFG = dict(id="computer-vision", title="Computer Vision",
    subtitle="From pixels and filters to CNNs, detectors and vision transformers, classical and modern, with Python labs and playgrounds",
    description="A hands-on course in computer vision covering both classical and modern techniques: images as data and colour spaces; convolution, blurring and the median filter; Sobel, Canny and Hough; keypoints, descriptors, RANSAC and homographies; thresholding, morphology and connected components; camera geometry, calibration and stereo depth; HOG, Haar cascades, bags of visual words and SVMs; convolutional networks, ResNet and transfer learning; detection with IoU and non-maximum suppression, YOLO and Mask R-CNN, and segmentation with U-Net; and vision transformers, CLIP, SAM and diffusion with a look at bias and responsible use. Every chapter has Python labs verified in the built-in interpreter, plus a convolution playground and an IoU and NMS lab.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="cv", apps={"__KERNEL__": "kernel.html", "__BOXES__": "boxes.html"})
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "computer-vision.course.json")
    cmk.main(CFG, CHS, [sys.argv[0], out])
