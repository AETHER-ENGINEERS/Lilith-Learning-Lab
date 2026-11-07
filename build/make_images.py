#!/usr/bin/env python3
"""Generate the tutorial's original SVG figures (no third-party artwork).
Usage: python3 make_images.py <output_dir>"""
import os, sys
from xml.sax.saxutils import escape

BG, PANEL, LINE = "#120d1c", "#1c1530", "#3d2f5c"
TX, DIM = "#efe9ff", "#a99dc7"
VIO, PINK, BLUE, GRN, AMB, RED = "#b26bff", "#e06aa8", "#4fa8ff", "#76b900", "#e3b341", "#ff6b6b"
FONT = "system-ui,-apple-system,Segoe UI,Roboto,sans-serif"


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h, self.t, self.d = w, h, title, desc
        self.o = []

    def add(self, s):
        self.o.append(s)

    def rect(self, x, y, w, h, fill=PANEL, stroke=LINE, r=10, sw=1.5, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, fill, stroke, sw, d))

    def text(self, x, y, s, size=13, fill=TX, anchor="middle", weight="400", style=""):
        self.add('<text x="%s" y="%s" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s" %s>%s</text>' % (x, y, size, fill, anchor, weight, style, escape(s)))

    def box(self, x, y, w, h, title, sub=None, color=VIO, fill=PANEL):
        self.rect(x, y, w, h, fill=fill, stroke=color)
        if sub:
            self.text(x + w / 2, y + h / 2 - 3, title, 13, TX, weight="600")
            self.text(x + w / 2, y + h / 2 + 14, sub, 10.5, DIM)
        else:
            self.text(x + w / 2, y + h / 2 + 5, title, 13, TX, weight="600")

    def arrow(self, x1, y1, x2, y2, color=DIM, dash=None, sw=1.8):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s marker-end="url(#ah)"/>' % (x1, y1, x2, y2, color, sw, d))

    def line(self, x1, y1, x2, y2, color=LINE, sw=1.5, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, color, sw, d))

    def render(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-labelledby="t d" font-family="%s">'
                '<title id="t">%s</title><desc id="d">%s</desc>'
                '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>'
                '<rect width="%d" height="%d" rx="14" fill="%s"/>') % (self.w, self.h, FONT, escape(self.t), escape(self.d), DIM, self.w, self.h, BG)
        return head + "".join(self.o) + "</svg>\n"


def save(d, name, s):
    with open(os.path.join(d, name), "w", encoding="utf-8") as f:
        f.write(s.render())


def soc_overview(d):
    s = Svg(640, 400, "Xavier SoC block diagram", "CPU, GPU, two DLAs, two PVAs, ISP, VIC and video engines all connect through a shared memory fabric to one LPDDR4x memory.")
    s.text(320, 26, "Xavier SoC: one chip, many processors", 15, VIO, weight="700")
    xs = [20, 175, 330, 485]
    s.box(xs[0], 44, 135, 70, "8x Carmel CPU", "Linux, Python, glue", BLUE)
    s.box(xs[1], 44, 135, 70, "Volta GPU", "512 CUDA + 64 Tensor", GRN)
    s.box(xs[2], 44, 135, 70, "DLA 0", "fixed-function NN", PINK)
    s.box(xs[3], 44, 135, 70, "DLA 1", "fixed-function NN", PINK)
    for x in xs:
        s.arrow(x + 67, 114, x + 67, 150, VIO)
    s.rect(20, 152, 600, 34, fill="#2a1f45", stroke=VIO)
    s.text(320, 174, "Shared memory fabric (every block competes for bandwidth)", 12.5, TX, weight="600")
    bx = [20, 155, 290, 425]
    s.box(bx[0], 214, 125, 66, "2x PVA", "classic vision (VPI)", AMB)
    s.box(bx[1], 214, 125, 66, "ISP", "camera raw to image", AMB)
    s.box(bx[2], 214, 125, 66, "VIC", "scale / convert", AMB)
    s.box(bx[3], 214, 125, 66, "NVENC / NVDEC", "video codec", AMB)
    for x in bx:
        s.arrow(x + 62, 186, x + 62, 214, VIO)
    s.line(586, 186, 586, 326, VIO, 2.2)
    s.arrow(586, 300, 586, 328, VIO)
    s.rect(20, 328, 600, 48, fill="#241a3c", stroke=PINK)
    s.text(320, 349, "LPDDR4x memory, 256-bit, about 136.5 GB/s", 13.5, TX, weight="700")
    s.text(320, 367, "16 / 32 / 64 GB, one pool for CPU, GPU and accelerators (no separate GPU memory)", 10.5, DIM)
    s.text(320, 303, "plus small helper cores for boot, power and safety (from memory)", 10.5, DIM)
    save(d, "soc-overview.svg", s)


def which_processor(d):
    s = Svg(640, 392, "Which processor for which job", "Workloads on the left map to the processor and the software that drives it on the right.")
    s.text(320, 24, "Pick the cheapest processor that can do the job", 15, VIO, weight="700")
    rows = [("Python, JSON, networking", "CPU", "Linux", BLUE),
            ("Custom CUDA kernels, PyTorch", "GPU", "CUDA, cuDNN", GRN),
            ("Steady conv nets in FP16 / INT8", "DLA x2", "TensorRT, cuDLA", PINK),
            ("Blur, optical flow, tracking", "PVA", "VPI", AMB),
            ("Resize and color-convert frames", "VIC", "nvvidconv", AMB),
            ("Camera raw to RGB", "ISP", "Argus", AMB),
            ("Encode / decode video", "NVENC / NVDEC", "GStreamer", AMB)]
    for i, (a, b, api, c) in enumerate(rows):
        y = 42 + i * 48
        s.rect(20, y, 244, 38, PANEL, LINE)
        s.text(142, y + 24, a, 12)
        s.arrow(266, y + 24, 378, y + 24, c)
        s.text(322, y + 14, api, 9, DIM)
        s.rect(380, y, 240, 38, PANEL, c)
        s.text(500, y + 24, b, 13, TX, weight="700")
    save(d, "which-processor.svg", s)


def memory_unified(d):
    s = Svg(640, 300, "Unified memory on Jetson", "On a PC the CPU and GPU have separate memories joined by a copy over PCIe; on Jetson every processor uses the same LPDDR4x.")
    s.text(160, 26, "Desktop PC", 14, DIM, weight="700")
    s.box(20, 44, 120, 50, "CPU", None, BLUE)
    s.box(20, 170, 120, 50, "GPU", None, GRN)
    s.box(180, 44, 120, 50, "System RAM", None, BLUE)
    s.box(180, 170, 120, 50, "GPU VRAM", None, GRN)
    s.arrow(140, 69, 180, 69, DIM)
    s.arrow(140, 195, 180, 195, DIM)
    s.arrow(240, 94, 240, 170, RED, "5 4", 2.2)
    s.text(240, 138, "copy over PCIe", 10.5, RED)
    s.text(480, 26, "Jetson AGX Xavier", 14, VIO, weight="700")
    names = [("CPU", BLUE), ("GPU", GRN), ("DLA", PINK), ("PVA", AMB)]
    for i, (n, c) in enumerate(names):
        x = 350 + i * 68
        s.box(x, 44, 60, 44, n, None, c)
        s.arrow(x + 30, 88, x + 30, 150, VIO)
    s.rect(350, 152, 272, 54, "#241a3c", PINK)
    s.text(486, 176, "one LPDDR4x pool", 13.5, TX, weight="700")
    s.text(486, 194, "~136.5 GB/s shared", 11, DIM)
    s.text(486, 236, "No copies needed (zero-copy)", 12, GRN, weight="600")
    s.text(486, 254, "but everything competes for the same bandwidth", 11, DIM)
    s.line(320, 36, 320, 270, LINE, 1, "4 4")
    save(d, "memory-unified.svg", s)


def software_stack(d):
    s = Svg(640, 430, "Jetson software stack", "Layers from hardware up to your application, with the library that reaches each processor, and which JetPack lines support the Xavier.")
    s.text(320, 24, "The software stack (top to bottom)", 15, VIO, weight="700")
    layers = [("Your application (Python / C++)", BLUE), ("Frameworks: PyTorch, ONNX Runtime, DeepStream", BLUE),
              ("Libraries: TensorRT, cuDNN, CUDA, VPI, GStreamer, Argus", VIO), ("Jetson Linux (L4T): Ubuntu userland, kernel, drivers", PINK),
              ("Boot firmware, power and safety firmware", DIM), ("Hardware: CPU, GPU, 2x DLA, 2x PVA, ISP, VIC, NVENC/NVDEC", GRN)]
    for i, (t, c) in enumerate(layers):
        y = 40 + i * 44
        s.rect(20, y, 600, 36, PANEL, c)
        s.text(320, y + 23, t, 12.5)
    s.text(320, 316, "Who reaches which processor", 12.5, DIM, weight="700")
    chips = [("TensorRT", "GPU + DLA", PINK), ("CUDA / cuDNN", "GPU", GRN), ("VPI", "PVA, VIC, GPU", AMB), ("GStreamer", "NVENC, NVDEC, VIC", AMB), ("Argus", "ISP", AMB)]
    for i, (a, b, c) in enumerate(chips):
        x = 20 + i * 122
        s.rect(x, 326, 114, 40, PANEL, c)
        s.text(x + 57, 343, a, 11.5, TX, weight="700")
        s.text(x + 57, 358, b, 9.5, DIM)
    s.rect(20, 380, 190, 38, PANEL, AMB)
    s.text(115, 396, "JetPack 4.6.x", 11.5, TX, weight="700")
    s.text(115, 411, "Ubuntu 18.04 (end of life)", 9.5, DIM)
    s.rect(225, 380, 190, 38, PANEL, GRN)
    s.text(320, 396, "JetPack 5.1.x", 11.5, TX, weight="700")
    s.text(320, 411, "Ubuntu 20.04, CUDA 11.4, TRT 8.5", 9.5, DIM)
    s.rect(430, 380, 190, 38, PANEL, RED, dash="5 4")
    s.text(525, 396, "JetPack 6", 11.5, TX, weight="700")
    s.text(525, 411, "does not support Xavier", 9.5, RED)
    save(d, "software-stack.svg", s)


def flash_workflow(d):
    s = Svg(640, 250, "Flashing a Jetson", "Four steps: enter recovery mode, check USB, choose the JetPack version in SDK Manager, then flash and first boot.")
    s.text(320, 24, "Flashing from a host PC", 15, VIO, weight="700")
    steps = [("1", "Recovery mode", "power off, hold Force\nRecovery, press Power"), ("2", "Check USB", "host: lsusb lists an\nNVIDIA device"),
             ("3", "SDK Manager", "pick Jetson AGX Xavier\nand JetPack 5.1.x"), ("4", "Flash + boot", "first boot setup, then\napt install nvidia-jetpack")]
    for i, (n, t, sub) in enumerate(steps):
        x = 14 + i * 157
        s.rect(x, 48, 146, 150, PANEL, VIO)
        s.add('<circle cx="%d" cy="76" r="14" fill="%s"/>' % (x + 73, VIO))
        s.text(x + 73, 81, n, 14, "#12081f", weight="800")
        s.text(x + 73, 112, t, 13.5, TX, weight="700")
        for j, ln in enumerate(sub.split("\n")):
            s.text(x + 73, 138 + j * 16, ln, 10.5, DIM)
        if i < 3:
            s.arrow(x + 147, 123, x + 156, 123, VIO)
    s.text(320, 228, "Host: x86-64 Ubuntu PC + USB-C cable. Re-flashing erases the device storage.", 11.5, DIM)
    save(d, "flash-workflow.svg", s)


def trt_workflow(d):
    s = Svg(640, 250, "From model to TensorRT engine", "Train a model, export ONNX with fixed shapes, build an engine with trtexec on the Jetson, then run it.")
    s.text(320, 24, "Model to engine", 15, VIO, weight="700")
    items = [("PyTorch / TF", "train anywhere", BLUE), ("ONNX", "fixed shapes", VIO), ("trtexec", "on the Jetson", GRN), ("Engine", "device + version\nspecific", PINK), ("Run", "Python / C++ /\nDeepStream", AMB)]
    for i, (a, b, c) in enumerate(items):
        x = 14 + i * 125
        s.rect(x, 54, 112, 84, PANEL, c)
        s.text(x + 56, 84, a, 13.5, TX, weight="700")
        for j, ln in enumerate(b.split("\n")):
            s.text(x + 56, 104 + j * 14, ln, 10.5, DIM)
        if i < 4:
            s.arrow(x + 113, 96, x + 124, 96, c)
    s.rect(14, 160, 612, 62, "#241a3c", LINE)
    s.text(320, 184, "trtexec --onnx=model.onnx --fp16 [--useDLACore=0 --allowGPUFallback] --saveEngine=m.engine", 11, TX, style='font-family="ui-monospace,Menlo,monospace"')
    s.text(320, 206, "Build on the device that will run it; engines do not carry across TensorRT versions.", 11, DIM)
    save(d, "trt-workflow.svg", s)


def dla_partition(d):
    s = Svg(640, 330, "DLA subgraphs and fallbacks", "A good model keeps layers on the DLA and puts non-DLA layers at the end; a bad one bounces between DLA and GPU.")
    s.text(320, 24, "Keep the DLA part in one piece", 15, VIO, weight="700")

    def row(y, label, seq, color_note):
        s.text(20, y - 8, label, 12, color_note, anchor="start", weight="700")
        x = 14
        prev = None
        for name, dev in seq:
            w = 20 + 7.2 * len(name)
            c = GRN if dev == "D" else AMB
            if prev is not None and prev != dev:
                s.text(x - 3, y + 50, "copy+sync", 8.5, RED)
            s.rect(x, y, w, 34, "#16241a" if dev == "D" else "#2d2410", c, 8)
            s.text(x + w / 2, y + 21, name, 11.5, TX)
            x += w + 6
            prev = dev
    row(66, "Good: 1 DLA subgraph, GPU only for the tail",
        [("conv", "D"), ("relu", "D"), ("conv", "D"), ("relu", "D"), ("resize x2", "D"), ("conv", "D"), ("softmax", "G"), ("argmax", "G")], GRN)
    row(176, "Bad: many DLA/GPU switches",
        [("conv", "D"), ("gelu", "G"), ("conv", "D"), ("softmax", "G"), ("deconv p1", "G"), ("relu", "D")], RED)
    s.rect(14, 266, 14, 14, "#16241a", GRN, 3)
    s.text(34, 278, "runs on DLA", 11, DIM, anchor="start")
    s.rect(130, 266, 14, 14, "#2d2410", AMB, 3)
    s.text(150, 278, "falls back to GPU", 11, DIM, anchor="start")
    s.text(320, 312, "Each switch adds data copies and synchronization. Check the --verbose build log.", 11, DIM)
    save(d, "dla-partition.svg", s)


def vq_pipeline(d):
    s = Svg(640, 300, "VQ-VAE on the DLA", "Encoder and codebook scores run on the DLA, argmin and lookup on CPU or GPU, then the decoder runs on the DLA.")
    s.text(320, 24, "VQ-VAE split: tensors on the DLA, the choice on the CPU", 15, VIO, weight="700")
    top = [("Camera frame", "256x256", BLUE), ("Encoder", "conv stack (DLA)", PINK), ("Scores", "1x1 conv (DLA)", PINK)]
    bot = [("Reconstruction", "image out", BLUE), ("Decoder", "resize + conv (DLA)", PINK), ("Lookup", "codebook[idx] (CPU/GPU)", AMB)]
    for i, (a, b, c) in enumerate(top):
        x = 20 + i * 205
        s.box(x, 50, 180, 62, a, b, c)
        if i < 2:
            s.arrow(x + 182, 81, x + 203, 81, c)
    s.rect(20, 136, 600, 40, "#241a3c", AMB)
    s.text(320, 154, "argmin over the score channels: score_k = ||b_k||^2 - 2 a.b_k   (CPU or GPU)", 11.5, TX, weight="600")
    s.text(320, 169, "||a||^2 is the same for every k, so it is dropped", 10, DIM)
    s.arrow(525, 112, 525, 136, AMB)
    s.arrow(525, 176, 525, 200, AMB)
    for i, (a, b, c) in enumerate(bot):
        x = 435 - i * 205
        s.box(x, 200, 180, 62, a, b, c)
        if i < 2:
            s.arrow(x - 2, 231, x - 23, 231, c)
    s.text(320, 288, "Two hand-offs between DLA and CPU per frame: measure them.", 11, DIM)
    save(d, "vq-dla-pipeline.svg", s)


def camera_pipeline(d):
    s = Svg(640, 220, "Camera to inference pipeline", "Camera frames pass through the ISP and VIC in hardware, then inference on DLA or GPU, with the CPU only handling control and small tensors.")
    s.text(320, 24, "Keep frames in hardware memory", 15, VIO, weight="700")
    items = [("Camera", "MIPI CSI-2", BLUE), ("ISP", "Argus", AMB), ("VIC", "resize + color", AMB), ("DLA / GPU", "TensorRT", PINK), ("CPU", "control, small tensors", GRN)]
    for i, (a, b, c) in enumerate(items):
        x = 12 + i * 126
        s.box(x, 48, 114, 70, a, b, c)
        if i < 4:
            s.arrow(x + 115, 83, x + 125, 83, c)
    s.arrow(296, 118, 296, 158, AMB)
    s.box(222, 160, 148, 44, "NVENC", "H.264 / H.265 file", AMB)
    s.text(500, 150, "NVMM memory: frames stay in", 11, DIM)
    s.text(500, 166, "hardware buffers between stages", 11, DIM)
    s.text(500, 190, "Scale before the CPU copy.", 11, GRN, weight="600")
    save(d, "camera-pipeline.svg", s)


def sentry_pipeline(d):
    s = Svg(640, 320, "Always-on perception loop", "The DLA reconstructs the scene all the time; the CPU compares it with the frame; the GPU detector wakes only when the error is high.")
    s.text(320, 24, "The Sentry loop: sleep cheap, wake smart", 15, VIO, weight="700")
    s.box(14, 50, 118, 62, "Camera", "ISP + VIC 256x256", BLUE)
    s.box(158, 50, 138, 62, "DLA 0", "encoder (mu) + decoder", PINK)
    s.box(322, 50, 138, 62, "CPU", "error = |x - recon|", GRN)
    s.arrow(133, 81, 157, 81, BLUE)
    s.arrow(297, 81, 321, 81, PINK)
    s.add('<polygon points="545,48 625,81 545,114 465,81" fill="%s" stroke="%s" stroke-width="1.5"/>' % (PANEL, AMB))
    s.text(545, 78, "error >", 11.5, TX, weight="700")
    s.text(545, 93, "threshold?", 11.5, TX, weight="700")
    s.arrow(461, 81, 466, 81, GRN)
    s.rect(30, 190, 250, 62, "#16241a", GRN)
    s.text(155, 214, "No: GPU stays idle", 13.5, TX, weight="700")
    s.text(155, 234, "keep looping at low power", 10.5, DIM)
    s.rect(360, 190, 250, 62, "#2d1830", PINK)
    s.text(485, 214, "Yes: wake the GPU", 13.5, TX, weight="700")
    s.text(485, 234, "full-frame detector, then handle events", 10.5, DIM)
    s.arrow(520, 108, 485, 190, PINK)
    s.arrow(520, 108, 200, 190, GRN, "4 4")
    s.text(320, 290, "Add a watchdog: if the DLA engine stalls, fall back to a simple CPU or GPU check.", 11, DIM)
    save(d, "sentry-pipeline.svg", s)


NAMES = ["soc-overview", "which-processor", "memory-unified", "software-stack", "flash-workflow", "trt-workflow", "dla-partition", "vq-dla-pipeline", "camera-pipeline", "sentry-pipeline"]

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "images"
    os.makedirs(out, exist_ok=True)
    for fn in (soc_overview, which_processor, memory_unified, software_stack, flash_workflow, trt_workflow, dla_partition, vq_pipeline, camera_pipeline, sentry_pipeline):
        fn(out)
    print("wrote", len(os.listdir(out)), "svgs to", out)
