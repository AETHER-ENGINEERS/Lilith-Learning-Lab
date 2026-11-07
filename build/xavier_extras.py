"""Hand-written parts of the Jetson AGX Xavier course that the markdown does not carry:
per-chapter concept maps, quizzes, practice labs, extra glossary terms and the simulated terminal.
make_course.py merges these with docs/jetson_agx_xavier_tutorial.md to produce the course JSON."""

PRONOUNCE = {
    'VQ-VAE': 'V Q V A E', 'TensorRT': 'tensor R T', 'trtexec': 'T R T exec', 'JetPack': 'jet pack',
    'LPDDR4x': 'L P D D R four x', 'eMMC': 'e M M C', 'NVMe': 'N V M E', 'NVMM': 'N V M M',
    'NVENC': 'N V ENC', 'NVDEC': 'N V DEC', 'NVDLA': 'N V D L A', 'nvpmodel': 'N V P model',
    'jetson_clocks': 'jetson clocks', 'tegrastats': 'tegra stats', 'GStreamer': 'G Streamer',
    'cuDNN': 'cuda D N N', 'cuDLA': 'cuda D L A', 'CUDA': 'cooda', 'ONNX': 'onyx', 'Xavier': 'Zavier',
    'INT8': 'int eight', 'FP16': 'F P sixteen', 'FP32': 'F P thirty two', 'L4T': 'L four T',
    'SoC': 'system on chip', 'SoM': 'system on module', 'TOPS': 'tops', 'DLA': 'D L A', 'PVA': 'P V A',
    'ISP': 'I S P', 'VIC': 'V I C', 'VPI': 'V P I', 'VAE': 'V A E', 'PPO': 'P P O', 'PCIe': 'P C I e',
    'GPIO': 'G P I O', 'MIPI': 'mippy', 'CSI': 'C S I', 'LSTM': 'L S T M', 'GRU': 'G R U', 'EOL': 'end of life',
}

# ---------------------------------------------------------------- concept maps (one or more per chapter)
MAPS = {
    0: [('How to use this course', [
        'Read me first | splits into | Hardware, chapters 1 to 4 [ch1]',
        'Read me first | splits into | Get running, chapters 5 to 7 [ch5]',
        'Read me first | splits into | Compute, chapters 8 to 10 [ch8]',
        'Read me first | splits into | Design and pipelines, chapters 11 to 15 [ch11]',
        'Read me first | splits into | Tune and plan, chapters 16 to 19 [ch16]',
        'Hardware, chapters 1 to 4 | answers | What is inside the chip?',
        'Get running, chapters 5 to 7 | answers | How do I flash and watch it?',
        'Read me first | marks doubts with | (from memory) [ch21]'])],
    1: [('Module, carrier and kit', [
        'Jetson AGX Xavier | is a | System-on-module',
        'System-on-module | contains | Xavier SoC [ch2]',
        'System-on-module | contains | Memory and eMMC [ch3]',
        'System-on-module | plugs into | Carrier board [ch3]',
        'Carrier board | breaks out | USB, Ethernet, camera, PCIe',
        'Developer kit | is | Module plus carrier board',
        'Xavier SoC | delivers | 32 TOPS INT8',
        'Jetson AGX Xavier | is | End of life for new buyers [ch18]'])],
    2: [('The processors', [
        'Xavier SoC | has | Carmel CPU x8',
        'Xavier SoC | has | Volta GPU',
        'Xavier SoC | has | DLA x2 [ch10]',
        'Xavier SoC | has | PVA x2 [ch12]',
        'Xavier SoC | has | ISP, VIC, NVENC, NVDEC [ch13]',
        'Carmel CPU x8 | runs | Linux and your code',
        'Volta GPU | runs | CUDA and Tensor Cores [ch8]',
        'DLA x2 | runs | Fixed neural-net layers',
        'PVA x2 | runs | Classic vision with VPI'])],
    3: [('Shared memory and I/O', [
        'LPDDR4x memory | is shared by | CPU',
        'LPDDR4x memory | is shared by | GPU',
        'LPDDR4x memory | is shared by | DLA and PVA',
        'LPDDR4x memory | offers | About 136.5 GB/s',
        'Shared memory | enables | Zero-copy buffers',
        'Many engines at once | stress | Memory bandwidth',
        'Carrier board | provides | Cameras, PCIe, USB, Ethernet',
        'NVMe storage | beats | eMMC for models'])],
    4: [('Power, clocks and heat', [
        'nvpmodel | sets | Power mode',
        'Power mode | caps | CPU cores and clocks',
        'Power mode | caps | GPU and memory clocks',
        'jetson_clocks | locks | Clocks at the mode maximum',
        'Locked clocks | give | Stable benchmarks',
        'Weak power supply | causes | Brownouts',
        'High heat | triggers | Throttling [ch17]'])],
    5: [('The software stack', [
        'JetPack | bundles | Jetson Linux (L4T)',
        'JetPack | bundles | CUDA, cuDNN, TensorRT',
        'JetPack | bundles | VPI and multimedia APIs',
        'Jetson Linux (L4T) | provides | Kernel and drivers',
        'JetPack 5.1 | is the last line for | AGX Xavier',
        'JetPack 6 | targets | Orin only',
        'Fixed library versions | mean | Containers for newer tools [ch14]'])],
    6: [('Flashing the board', [
        'Host PC | runs | SDK Manager',
        'SDK Manager | flashes | Jetson over USB-C',
        'Recovery mode | is required for | Flashing',
        'Recovery mode | is confirmed by | lsusb on the host',
        'SDK Manager | installs | JetPack components',
        'First boot | needs | License, user, network',
        'NVMe boot | is | Faster than eMMC'])],
    7: [('Watching the system', [
        'tegrastats | reports | RAM and CPU load',
        'tegrastats | reports | GR3D_FREQ (GPU)',
        'tegrastats | reports | EMC_FREQ (memory)',
        'GR3D_FREQ | shows | GPU busy',
        'EMC_FREQ | hints | Bandwidth pressure',
        'jtop | shows | Engines and power pages',
        'nvidia-smi | is | Limited on Jetson'])],
    8: [('CUDA on the Xavier', [
        'Kernel launch | creates | Grid of blocks',
        'Block | holds | Threads',
        'Thread index | equals | blockIdx times blockDim plus threadIdx',
        'nvcc | compiles for | sm_72',
        'cudaDeviceSynchronize | waits for | Kernel results',
        'Tensor Cores | are used by | cuDNN, cuBLAS, TensorRT',
        'Volta GPU | has | 8 SMs, 512 CUDA cores'])],
    9: [('From model to engine', [
        'PyTorch model | exports to | ONNX',
        'ONNX | is built by | trtexec',
        'trtexec | produces | Engine',
        'Engine | runs on | GPU',
        'Engine | runs on | DLA [ch10]',
        'Engine | is tied to | One device and TensorRT version',
        '--fp16 | is | Best first precision',
        'INT8 | needs | Calibration'])],
    10: [('The DLA rules', [
        'DLA x2 | supports | FP16 and INT8 only',
        'DLA x2 | needs | Static shapes',
        'Unsupported layer | causes | GPU fallback',
        'GPU fallback | needs | --allowGPUFallback',
        'Many DLA and GPU switches | cost | Transfers and sync',
        'Softmax | is | Orin only',
        'ArgMax and TopK | are | Not supported',
        'DLA-friendly design | fixes | Fallbacks [ch11]'])],
    11: [('DLA-friendly models', [
        'VAE | deploys with | Mean mu only',
        'Mean mu only | removes | Sampling step',
        'Transposed conv | often falls back as | Deconv with padding',
        'Upsample plus conv | replaces | Transposed conv',
        'VQ-VAE search | becomes | 1x1 conv scores',
        '1x1 conv scores | run on | DLA',
        'Argmin and lookup | run on | CPU or GPU',
        'PPO | deploys as | Deterministic actor'])],
    12: [('PVA and VPI', [
        'VPI | has backend | PVA',
        'VPI | has backend | VIC',
        'VPI | has backend | CUDA and CPU',
        'PVA | runs | Filters, flow, tracking',
        'PVA | does not run | Neural networks',
        'Backend switches | cost | Conversions',
        'PVA | suits | Always-on preprocessing'])],
    13: [('Camera to inference', [
        'Camera sensor | feeds | ISP',
        'ISP | is read through | nvarguscamerasrc',
        'nvvidconv | uses | VIC',
        'VIC | resizes without | GPU cost',
        'NVMM caps | keep frames in | Hardware memory',
        'nvv4l2h265enc | encodes with | NVENC',
        'appsink | copies frames to | CPU (costly)',
        'DeepStream | builds on | These elements'])],
    14: [('Python and containers', [
        'PyTorch for Jetson | comes from | NVIDIA wheels',
        'pip default wheel | does not use | Jetson GPU',
        'Container tag | must match | L4T release',
        'docker run | needs | --runtime nvidia',
        'Production models | export to | ONNX then TensorRT',
        'Large builds | need | Swap on NVMe'])],
    15: [('The Sentry pipeline', [
        'Camera and ISP | feed | VIC resize',
        'VIC resize | feeds | DLA0 autoencoder',
        'DLA0 autoencoder | gives | Reconstruction error (CPU)',
        'High error | wakes | GPU detector',
        'Each engine | gets | Own stream or process',
        'Watchdog | guards against | Stalled engine',
        'Bandwidth budget | limits | Frames per second'])],
    16: [('Tuning checklist', [
        'FP16 | speeds up | Almost every model',
        'Fused layers | run as | One DLA unit',
        'Static shapes | keep | Engines simple',
        'Pre and post processing | stay on | Same device',
        'Warm-up | removes | Start-up noise',
        'Fewer partitions | mean | Faster DLA engines',
        'Throttling | slows | Sustained 30 W loads'])],
    17: [('Troubleshooting', [
        'Record versions | comes before | Any fix',
        'Out of memory | kills | Processes',
        'Out of memory | is fixed by | Swap or smaller batch',
        'Version change | breaks | Old engines',
        'Brownout | points to | Weak power supply',
        'Slow runs | check | Mode, clocks, throttling, fallbacks',
        'dmesg | shows | Kernel problems'])],
    18: [('Lifecycle', [
        'AGX Xavier | has | End-of-life notices',
        'AGX Xavier | stops at | JetPack 5.x',
        'Orin | offers | Newer DLA and Ampere GPU',
        'Xavier skills | carry over to | Orin',
        'Jetson Thor | has no | DLA',
        'New product | should plan | Orin-class module',
        'Reproducibility | needs | Saved image and versions'])],
    19: [('Cheat sheet map', [
        'Identify | uses | cat /etc/nv_tegra_release',
        'Power | uses | nvpmodel and jetson_clocks',
        'Monitor | uses | tegrastats and jtop',
        'Engines | use | trtexec',
        'trtexec | adds for DLA | --useDLACore --allowGPUFallback',
        'CUDA | compiles with | nvcc -arch=sm_72',
        'Camera | uses | nvarguscamerasrc and nvvidconv'])],
    20: [('Glossary families', [
        'Glossary | covers | Hardware terms',
        'Glossary | covers | Software terms',
        'Glossary | covers | Tools and commands',
        'Hardware terms | include | DLA, PVA, ISP, VIC',
        'Software terms | include | JetPack, TensorRT, ONNX',
        'Tools and commands | include | trtexec, tegrastats'])],
    21: [('Trusting the course', [
        'Checked claims | come from | NVIDIA and vendor pages',
        'Unchecked claims | are marked | (from memory)',
        'Docs for your release | beat | This course',
        'DLA limits | differ by | TensorRT version',
        'Double-check first | the | nvpmodel list and dev kit buttons'])],
}

# ---------------------------------------------------------------- quizzes: (question, options, answer index, explanation)
QUIZ = {
    0: [("Which chapters help you get the board running?", ["Chapters 1 to 4", "Chapters 5 to 7", "Chapters 11 to 15", "Chapters 16 to 19"], 1, "Chapters 5 to 7 cover the software stack, flashing and first boot, and monitoring."),
        ("What does the marker (from memory) tell you?", ["The claim was checked against NVIDIA docs", "The claim was not re-checked and is listed in chapter 21", "The claim is wrong", "The claim only applies to Orin"], 1, "Unverified statements are marked and listed in the verification notes."),
        ("What is the one idea behind the Xavier having so many processors?", ["Marketing", "Each workload runs best on a specialized block that shares memory", "A single fast CPU is not possible", "They are spares in case one breaks"], 1, "Different workloads suit different blocks, and all of them share the same memory.")],
    1: [("What does the developer kit add to the module?", ["A faster SoC", "A carrier board, heatsink and power supply", "More cores", "JetPack 6"], 1, "The module is the compute board; the kit adds the carrier and accessories."),
        ("What is the 32 TOPS INT8 figure made of?", ["CPU plus GPU", "GPU plus the two DLAs", "Only the DLAs", "GPU plus PVA"], 1, "Roughly 22 TOPS from the GPU plus about 10 TOPS from the two DLAs."),
        ("How do you change the boot order on a Xavier?", ["BIOS setup menu", "You cannot; you flash images from a host PC", "Hold the power button", "Edit a jumper"], 1, "It is not a PC: there is no BIOS setup menu, you flash images from a host.")],
    2: [("Can you program the DLA with CUDA?", ["Yes, same as the GPU", "No, use TensorRT or cuDLA", "Only in INT8", "Only with VPI"], 1, "CUDA targets the GPU; the DLA is reached through TensorRT or cuDLA."),
        ("What is the PVA for?", ["Neural networks", "Classic vision such as filters and optical flow", "Video encoding", "Boot management"], 1, "The PVA runs classic computer vision through VPI, not neural networks."),
        ("What compute capability does the Xavier GPU have?", ["5.3", "6.2", "7.2", "8.7"], 2, "It is 7.2, built with -arch=sm_72."),
        ("Which block scales and converts frames without using the GPU?", ["ISP", "VIC", "NVENC", "PVA"], 1, "The VIC handles scaling, color conversion and cropping.")],
    3: [("Why can the CPU and GPU share a buffer with no copy?", ["They use separate memories linked by PCIe", "They are on the same SoC and use the same physical memory", "The driver compresses it", "It is not possible"], 1, "Unified memory means one physical pool."),
        ("What usually limits a Jetson running many models at once?", ["Disk space", "Shared memory bandwidth", "Fan speed", "Wi-Fi"], 1, "All engines compete for the same LPDDR4x bandwidth."),
        ("Where should you keep models for real work?", ["eMMC only", "NVMe", "A USB stick", "RAM disk"], 1, "NVMe is much faster and larger than the 32 GB eMMC.")],
    4: [("What does jetson_clocks do?", ["Sets the date", "Locks clocks at the maximum allowed by the current mode", "Switches the power mode", "Turns the fan off"], 1, "It pins CPU, GPU and memory clocks high within the current power mode."),
        ("Why benchmark with clocks locked?", ["It saves power", "Dynamic scaling makes timings vary between runs", "It is required by TensorRT", "It lowers temperature"], 1, "Fixed clocks give repeatable numbers."),
        ("Which command sets power mode 0?", ["nvpmodel -q 0", "sudo nvpmodel -m 0", "jetson_clocks -m 0", "tegrastats -m 0"], 1, "nvpmodel -m <id> sets the mode and needs sudo.")],
    5: [("Can you run JetPack 6 on an AGX Xavier?", ["Yes", "No, Xavier stops at JetPack 5.x", "Only with a patch", "Only on the 64 GB module"], 1, "JetPack 6 targets Orin."),
        ("Which library puts a model on the DLA?", ["cuBLAS", "TensorRT (or cuDLA)", "OpenCV", "VPI"], 1, "TensorRT builds DLA engines; cuDLA runs standalone loadables."),
        ("What does JetPack 5.1 ship for CUDA?", ["CUDA 10.2", "CUDA 11.4", "CUDA 12.2", "CUDA 9"], 1, "JetPack 5.1 has CUDA 11.4 and TensorRT 8.5.2.")],
    6: [("Which tool flashes the Jetson?", ["apt", "NVIDIA SDK Manager on a Linux host", "dd on the Jetson", "pip"], 1, "SDK Manager runs on an x86-64 Ubuntu host."),
        ("How do you confirm recovery mode?", ["The fan stops", "lsusb on the host lists an NVIDIA device", "The LED blinks red", "ping the Jetson"], 1, "In recovery mode the host sees an NVIDIA USB device."),
        ("Why keep a spare copy of customized images?", ["Re-flashing wipes the device storage", "JetPack deletes them nightly", "They expire", "SDK Manager needs them"], 0, "Flashing erases the target storage.")],
    7: [("Which tegrastats field tells you how busy the GPU is?", ["EMC_FREQ", "GR3D_FREQ", "RAM", "AO"], 1, "GR3D_FREQ shows GPU load and clock."),
        ("Which field hints at memory bandwidth pressure?", ["EMC_FREQ", "SWAP", "CPU", "GR3D_FREQ"], 0, "EMC is the memory controller."),
        ("Which tool replaces nvidia-smi on Jetson?", ["htop only", "tegrastats or jtop", "lspci", "dmesg"], 1, "nvidia-smi is limited on Jetson.")],
    8: [("How many blocks of 256 threads cover 1,000,000 elements?", ["3906", "3907", "3908", "4096"], 1, "ceil(1,000,000 / 256) = 3907."),
        ("Which -arch flag fits the Xavier GPU?", ["sm_53", "sm_62", "sm_72", "sm_87"], 2, "Compute capability 7.2 is sm_72."),
        ("What must you do before reading kernel results on the CPU?", ["Nothing", "cudaDeviceSynchronize()", "Reboot", "Lock clocks"], 1, "Kernel launches are asynchronous.")],
    9: [("Where should you build a TensorRT engine?", ["On any PC", "On the Jetson that will run it, same TensorRT version", "In the cloud", "It does not matter"], 1, "Engines are not portable across devices or TensorRT versions."),
        ("Which precision flag is the usual first step on Xavier?", ["--fp32", "--fp16", "--int4", "--bf16"], 1, "FP16 is usually the best first choice."),
        ("Why use --saveEngine?", ["Engines build in milliseconds", "Building can take minutes, so save and reload", "It enables the DLA", "It checks accuracy"], 1, "Load it later with --loadEngine.")],
    10: [("What precisions does the Xavier DLA support?", ["FP32 and FP16", "FP16 and INT8", "INT8 only", "Any"], 1, "No FP32 on the DLA."),
         ("What does --allowGPUFallback do?", ["Forces everything to GPU", "Lets unsupported layers run on the GPU instead of failing the build", "Adds INT8", "Disables the DLA"], 1, "Without it the build fails on an unsupported layer."),
         ("Why can heavy fallback slow a DLA engine?", ["The GPU is slow", "Each DLA/GPU boundary adds transfers and synchronization", "FP16 is lost", "The DLA turns off"], 1, "Boundaries cost data movement."),
         ("Which layer is NOT supported on the Xavier DLA?", ["Convolution", "ReLU", "Softmax", "Concat on channels"], 2, "Softmax is Orin only.")],
    11: [("Why can you drop ||a||^2 for the VQ-VAE argmin?", ["It is zero", "It is the same for every codebook entry", "It is negative", "It is slow"], 1, "A constant offset never changes which entry is smallest."),
         ("How do you express the codebook distance on a DLA?", ["Softmax", "A 1x1 convolution with weights -2*codebook and bias ||b||^2", "A transposed conv", "A LSTM"], 1, "The DLA computes all scores; argmin runs on CPU or GPU."),
         ("What do you do with a VAE's sigma at deployment?", ["Sample from it", "Ignore it and use the mean", "Double it", "Quantize it"], 1, "Use mu only and skip sampling.")],
    12: [("How do you program the PVA?", ["CUDA", "VPI with the PVA backend", "TensorRT", "GStreamer"], 1, "VPI selects the PVA backend."),
         ("Does the PVA run neural networks?", ["Yes", "No, use the DLA or GPU", "Only small ones", "Only INT8"], 1, "The PVA is for classic vision."),
         ("Why keep a pipeline stage on one VPI backend when you can?", ["Licensing", "Moving frames between backends costs conversions", "The PVA overheats", "VPI forbids it"], 1, "Each switch adds conversion work.")],
    13: [("Which GStreamer element reads MIPI cameras through the ISP?", ["v4l2src", "nvarguscamerasrc", "filesrc", "appsrc"], 1, "USB cameras use v4l2src instead."),
         ("Why scale before copying frames to the CPU?", ["It looks nicer", "The CPU copy is the expensive step, so fewer bytes help", "appsink requires it", "VIC cannot copy"], 1, "Resize with nvvidconv (VIC) first."),
         ("What does (memory:NVMM) in caps do?", ["Compresses frames", "Keeps frames in hardware memory", "Uses swap", "Enables audio"], 1, "It avoids copies to system memory.")],
    14: [("Why does pip install torch often not use the Jetson GPU?", ["It is banned", "The default wheel is not built for Jetson's Arm plus CUDA", "It needs Wi-Fi", "It needs root"], 1, "Use NVIDIA or Jetson-specific builds."),
         ("What must a container tag match?", ["Your Python version", "Your L4T release", "Your CPU temperature", "Your disk size"], 1, "Check with cat /etc/nv_tegra_release."),
         ("Which flag gives a container GPU access?", ["--gpus all only", "--runtime nvidia", "--privileged only", "--cuda"], 1, "Jetson uses the NVIDIA runtime.")],
    15: [("When does the GPU run in the Sentry pipeline?", ["Always", "Only when the DLA's reconstruction error is above the threshold", "Never", "Only at boot"], 1, "The DLA path is always on; the GPU wakes on events."),
         ("Why use separate streams or processes per engine?", ["Licensing", "So DLAs and GPU work at the same time", "To save RAM", "TensorRT requires it"], 1, "Otherwise they wait for each other."),
         ("What should the watchdog do if the DLA stalls?", ["Nothing", "Fall back to a simple CPU/GPU check", "Reboot", "Switch to JetPack 6"], 1, "Never fail silently.")],
    16: [("Why warm up before timing?", ["Early iterations include initialization and clock ramp-up", "It heats the room", "It is required by trtexec", "It reduces bandwidth"], 0, "Warm-up removes start-up noise."),
         ("What is the first check if a DLA engine is slower than expected?", ["The fan", "How many layers fell back and how many DLA subgraphs exist", "The Wi-Fi", "The disk"], 1, "Look at the build log."),
         ("What does fusing conv + batchnorm + ReLU achieve?", ["Smaller files", "They run as one unit on TensorRT and the DLA", "INT8", "Nothing"], 1, "Fewer, bigger units are faster.")],
    17: [("What do you do when an engine will not load after a JetPack update?", ["Copy it again", "Rebuild it on the device with the new TensorRT", "Downgrade the kernel", "Ignore"], 1, "Engines are version specific."),
         ("Which command shows recent kernel problems such as out-of-memory kills?", ["lsusb", "dmesg", "free", "uptime"], 1, "dmesg prints the kernel log."),
         ("Random reboots under load most likely mean...", ["A bad model", "A weak power supply", "Too much RAM", "Locked clocks"], 1, "Brownouts point to the supply.")],
    18: [("What is the last JetPack line that supports Xavier?", ["4.x", "5.x", "6.x", "7.x"], 1, "JetPack 6 does not support it."),
         ("Which generation of DLA does Xavier have?", ["First", "Second", "Third", "None"], 0, "Orin has the second generation."),
         ("What should a new product plan for today?", ["AGX Xavier", "An Orin-class module", "Nano 2GB", "A desktop PC"], 1, "Use Xavier for learning and existing designs.")],
    19: [("Which flags put a TensorRT build on DLA core 1 with fallback?", ["--dla=1", "--useDLACore=1 --allowGPUFallback", "--core=1", "--fallback"], 1, "Add --fp16 as well."),
         ("Which command locks clocks high?", ["sudo nvpmodel -q", "sudo jetson_clocks", "tegrastats", "jtop"], 1, "jetson_clocks pins the clocks."),
         ("Which file tells you the L4T release?", ["/etc/hosts", "/etc/nv_tegra_release", "/proc/cpuinfo", "/boot/config"], 1, "cat /etc/nv_tegra_release.")],
    20: [("What is a DLA?", ["Digital Logic Array", "Deep Learning Accelerator", "Direct Link Adapter", "Data Layer API"], 1, "NVDLA is NVIDIA's deep learning accelerator."),
         ("What does zero-copy mean?", ["Files with no content", "CPU and GPU access the same buffer without copying", "A free license", "No GPU"], 1, "Shared physical memory makes it possible."),
         ("Which term names the Jetson Linux release inside JetPack?", ["L4T", "VPI", "NVMM", "MAXN"], 0, "Linux for Tegra.")],
    21: [("How should you treat a claim marked (from memory)?", ["As verified", "As something to double-check first", "As false", "As Orin-only"], 1, "It was not re-checked."),
         ("If this course disagrees with the docs for your release...", ["Trust this course", "Trust the documentation", "Average them", "Ask the forum"], 1, "Limits differ between TensorRT versions."),
         ("Which claim should you double-check first?", ["The 32 TOPS figure", "The nvpmodel mode list and dev kit buttons", "That Xavier has 2 DLAs", "CUDA 11.4 in JetPack 5.1"], 1, "Those were not re-checked.")],
    22: [("What does a concept map show?", ["Only code", "How ideas connect through labeled links", "A schedule", "A circuit"], 1, "Nodes joined by relations like has, runs, causes."),
         ("What is a good habit with a map?", ["Skip it", "Cover the link words and say A <link> B aloud", "Print it", "Memorize colors"], 1, "Active recall of each link."),
         ("What does a pink node outline mean in the app?", ["Error", "It links to a chapter", "It is new", "It is optional"], 1, "Tap it to open that chapter.")],
}

# ---------------------------------------------------------------- extra glossary terms (chapters the markdown glossary did not cover)
EXTRA_GLOSSARY = {
    0: [('Concept map', 'A diagram of ideas joined by labeled links such as "has" or "runs".'), ('Jetson', 'NVIDIA\'s family of small computers for AI at the edge.'), ('(from memory)', 'A marker for a claim that was not re-checked against NVIDIA documentation.')],
    14: [('Container', 'A packaged, isolated environment that carries a program and its libraries; on Jetson it must match your L4T release.'), ('Wheel', 'A prebuilt Python package file; Jetson needs wheels built for Arm and your JetPack.'), ('NVIDIA runtime', 'The Docker runtime (--runtime nvidia) that gives a container access to the GPU.')],
    15: [('CUDA stream', 'An ordered queue of GPU work; separate streams let work overlap.'), ('Watchdog', 'A check that notices a stalled engine and switches to a fallback.'), ('Bandwidth budget', 'Bytes per frame times frames per second times how often each tensor moves.')],
    16: [('Warm-up', 'Running an engine a few times before timing, to skip initialization and clock ramp-up.'), ('Layer fusion', 'Merging layers such as conv, batchnorm and ReLU into one unit.'), ('Pinned memory', 'Memory that stays in place so transfers are faster.')],
    17: [('dmesg', 'A command that prints the kernel log, where out-of-memory kills and USB or thermal messages show up.'), ('Brownout', 'A short voltage drop, often from a weak power supply, that causes throttling or reboots.'), ('Out of memory (OOM)', 'The kernel kills a process because CPU and GPU together used all the shared RAM.')],
    18: [('End of life (EOL)', 'A vendor notice that a product will no longer be sold, with a last-time-buy date.'), ('Orin', 'The newer Jetson generation with second-generation DLAs and an Ampere GPU.'), ('Sustaining release', 'A software update that fixes problems but adds no new features.')],
    19: [('nv_tegra_release', 'The file /etc/nv_tegra_release; it names your L4T release.'), ('jtop', 'A monitoring app from the jetson-stats package.'), ('nvarguscamerasrc', 'The GStreamer element that reads MIPI cameras through the ISP.')],
    21: [('Verification note', 'A record of which claims were checked against sources and which were not.'), ('Source', 'A document or page that supports a claim.')],
    22: [('Node', 'A box in a concept map holding one idea.'), ('Link', 'A labeled line between two nodes, read as "A link B".')],
}
# markdown glossary term -> chapter (overrides the automatic placement)
GLOSSARY_CH = {
    'DLA / NVDLA': 10, 'FP16 / INT8': 9, 'NVDEC / NVENC': 13, 'SoC / SoM': 1, 'VAE / VQ-VAE': 11, 'AGX Xavier': 1, 'TOPS': 1,
    'Carmel': 2, 'Tensor Core': 2, 'Volta': 2, 'BPMP': 2, 'cuDLA': 10, 'PPO': 11, 'TensorRT': 9, 'DeepStream': 13, 'Carrier board': 3,
    'eMMC': 3, 'Fallback (GPU fallback)': 10,
}

# ---------------------------------------------------------------- simulated Xavier terminal
POWER = [(0, 'MAXN', 8, 2265, 1377, 2133), (1, 'MODE_10W', 2, 1200, 520, 1331), (2, 'MODE_15W', 4, 1200, 670, 1331), (3, 'MODE_30W_ALL', 8, 1200, 900, 1600),
         (4, 'MODE_30W_6CORE', 6, 1450, 900, 1600), (5, 'MODE_30W_4CORE', 4, 1780, 900, 1600), (6, 'MODE_30W_2CORE', 2, 2100, 900, 1600), (7, 'MODE_15W_DESKTOP', 4, 1500, 670, 1331)]


def trt(model, need=(), forbid=()):
    r = r'^(/usr/src/tensorrt/bin/)?trtexec(?=.*\s--onnx=' + model.replace('.', r'\.') + r')'
    for f in need:
        r += r'(?=.*\s' + f + r'(\s|=|$))'
    for f in forbid:
        r += r'(?!.*\s' + f + r')'
    return r + '.*$'


def terminal_commands():
    C = []
    add = lambda re, out, **kw: C.append(dict(re=re, out=out, **kw))
    add(r'^cat /etc/nv_tegra_release$', ['# R35 (release), REVISION: 2.1, BOARD: t186ref, EABI: aarch64   (simulated)', '# Jetson Linux 35.2.1 is the L4T release inside JetPack 5.1'], cls='')
    add(r'^(sudo )?nvpmodel -q --verbose$', ['NVPM VERB: Config file: /etc/nvpmodel.conf'] + ['  MODE %d: %s  (cpus online: %d, GPU max %d MHz)  [illustrative]' % (i, n, c, g) for i, n, c, cm, g, e in POWER] + ['NV Power Mode: {{modeName}}', '{{mode}}'])
    add(r'^(sudo )?nvpmodel -q$', ['NV Power Mode: {{modeName}}', '{{mode}}'])
    for i, n, c, cm, g, e in POWER:
        add(r'^sudo nvpmodel -m %d$' % i, ['NVPM WARN: clocks reset by the new power mode; run sudo jetson_clocks to lock them again.', 'Power mode set: ' + n], set=dict(mode=str(i), modeName=n, cpus=str(c), cpuMhz=str(cm), gpuMhz=str(g), emc=str(e), locked='no'))
    add(r'^nvpmodel -m', ['NVPM ERROR: Run this command as root (use sudo).'], cls='err')
    add(r'^sudo nvpmodel -m', ['NVPM ERROR: Invalid mode id. Use "sudo nvpmodel -q --verbose" to list modes.'], cls='err')
    add(r'^sudo jetson_clocks --show$', ['SOC family:tegra194  Machine:Jetson AGX Xavier', 'Online CPUs: 0-{{cpus}}', 'GPU MinFreq=114750000 MaxFreq={{gpuMhz}}000000   locked: {{locked}}'])
    add(r'^sudo jetson_clocks --fan$', ['fan set to maximum'])
    add(r'^sudo jetson_clocks$', ['clocks locked at the maximum of {{modeName}}'], set=dict(locked='yes'), cls='ok')
    add(r'^jetson_clocks', ['jetson_clocks must be run as root (use sudo).'], cls='err')
    add(r'^(sudo )?tegrastats$', ['RAM 2951/31920MB (lfb 7078x4MB) SWAP 0/15960MB CPU [12%@{{cpuMhz}},9%@{{cpuMhz}},8%@{{cpuMhz}},7%@{{cpuMhz}}] EMC_FREQ 5%@{{emc}} GR3D_FREQ 0%@{{gpuMhz}} AO@38C GPU@39C',
                                    'RAM 2953/31920MB (lfb 7078x4MB) SWAP 0/15960MB CPU [11%@{{cpuMhz}},10%@{{cpuMhz}},8%@{{cpuMhz}},6%@{{cpuMhz}}] EMC_FREQ 5%@{{emc}} GR3D_FREQ 0%@{{gpuMhz}} AO@38C GPU@39C',
                                    '(clocks locked, so GR3D_FREQ shows the mode maximum; simulated, real lines have more fields)'], when=dict(locked='yes'))
    add(r'^(sudo )?tegrastats$', ['RAM 2951/31920MB (lfb 7078x4MB) SWAP 0/15960MB CPU [12%@{{cpuMhz}},9%@{{cpuMhz}},8%@{{cpuMhz}},7%@{{cpuMhz}}] EMC_FREQ 5%@{{emc}} GR3D_FREQ 0%@114 AO@38C GPU@39C',
                                    'RAM 2953/31920MB (lfb 7078x4MB) SWAP 0/15960MB CPU [11%@{{cpuMhz}},10%@{{cpuMhz}},8%@{{cpuMhz}},6%@{{cpuMhz}}] EMC_FREQ 5%@{{emc}} GR3D_FREQ 0%@114 AO@38C GPU@39C',
                                    '(idle: the GPU clock sits at 114 MHz until it is busy or clocks are locked; simulated)'])
    add(r'^ls$', ['model.onnx  decoder.onnx  vqscore.onnx  vector_add.cu  export.py{{engines}}'])
    add(r'^cat model\.onnx$', ['model.onnx: demo network: conv-relu-conv-relu-resize-conv-softmax', '  conv1 (conv)  relu1  conv2 (conv, stride 2)  relu2  up1 (resize nearest x2)  conv3  softmax'])
    add(r'^cat decoder\.onnx$', ['decoder.onnx: VAE-style decoder using transposed convolutions with padding 1', '  dec_conv1  dec_relu1  deconv1 (padding 1)  dec_relu2  deconv2 (padding 1)  out (sigmoid)'])
    add(r'^cat vqscore\.onnx$', ['vqscore.onnx: VQ-VAE codebook scores as a 1x1 conv, followed by argmin', '  score_conv (conv)  argmin (argmax)'])
    add(r'^cat vector_add\.cu$', ['// vector_add.cu', '__global__ void add(const float* a, const float* b, float* c, int n) {', '  int i = blockIdx.x * blockDim.x + threadIdx.x;', '  if (i < n) c[i] = a[i] + b[i];', '}', '// main(): n = 1<<20, 256 threads/block, blocks = (n+255)/256'])
    # --- trtexec on model.onnx
    head = '&&&& RUNNING TensorRT.trtexec [TensorRT v8502] # {{0}}'
    tail_ok = '&&&& PASSED TensorRT.trtexec'
    add(trt('model.onnx', ['--fp16', '--saveEngine=gpu\\.engine'], ['--useDLACore', '--int8']), ['[I] Parsing ONNX model model.onnx (7 layers)', '[I] Building engine (FP16, GPU) ... done in 25.3 s', '[I] Saved engine to gpu.engine', '[I] Running 10 iterations on GPU, power mode {{modeName}}, clocks locked', '[I] Latency: min = 2.05 ms, max = 2.20 ms, mean = 2.11 ms', '[I] Throughput: 474.0 qps (batch 1)', tail_ok], when=dict(locked='yes'), set=dict(engines='  gpu.engine*', gpuEngine='yes'))
    add(trt('model.onnx', ['--fp16', '--saveEngine=gpu\\.engine'], ['--useDLACore', '--int8']), ['[I] Parsing ONNX model model.onnx (7 layers)', '[I] Building engine (FP16, GPU) ... done in 25.3 s', '[I] Saved engine to gpu.engine', '[I] Running 10 iterations on GPU, power mode {{modeName}}, clocks NOT locked', '[I] Latency: min = 2.31 ms, max = 2.95 ms, mean = 2.48 ms   (varies: lock the clocks for steady numbers)', '[I] Throughput: 403.2 qps (batch 1)', tail_ok], set=dict(engines='  gpu.engine*', gpuEngine='yes'))
    add(trt('model.onnx', ['--fp16'], ['--useDLACore', '--int8']), ['[I] Parsing ONNX model model.onnx (7 layers)', '[I] Building engine (FP16, GPU) ... done in 25.3 s', '[I] Latency: mean = 2.2 ms', tail_ok])
    add(trt('model.onnx', ['--int8'], ['--useDLACore']), ['[W] No calibration data given: INT8 scales are placeholders. Use this run for timing only.', '[I] Latency: mean = 1.4 ms', tail_ok], cls='warn')
    add(trt('model.onnx', [], ['--useDLACore', '--fp16', '--int8']), ['[I] Building engine (FP32, GPU) ...', '[I] Latency: mean = 4.8 ms   (FP32 is the slowest option; try --fp16)', tail_ok])
    add(trt('model.onnx', ['--useDLACore=[01]'], ['--fp16', '--int8']), ['[E] DLA supports only FP16 and INT8. Add --fp16 (or --int8).', '&&&& FAILED TensorRT.trtexec'], cls='err')
    add(trt('model.onnx', ['--fp16', '--useDLACore=[01]'], ['--allowGPUFallback']), ['[E] Layer softmax (softmax) cannot run on DLA: Softmax is not supported on Xavier DLA (Orin only). Add --allowGPUFallback to run it on the GPU.', '[E] Engine build failed.', '&&&& FAILED TensorRT.trtexec'], cls='err')
    add(trt('model.onnx', ['--fp16', '--useDLACore=[01]', '--allowGPUFallback', '--verbose']), ['[I] Parsing ONNX model model.onnx (7 layers)', '[V] conv1 (conv) -> DLA', '[V] relu1 (relu) -> DLA', '[V] conv2 (conv) -> DLA', '[V] relu2 (relu) -> DLA', '[V] up1 (resize) -> DLA', '[V] conv3 (conv) -> DLA', '[V] softmax (softmax) -> GPU  [fallback: Softmax is not supported on Xavier DLA (Orin only)]', '[I] DLA subgraphs: 1, DLA/GPU transitions: 1', '[I] Building engine (FP16, DLA) ... done in 42.0 s', '[I] Latency: mean = 6.4 ms (DLA, +GPU for 1 layer)', tail_ok], set=dict(dlaDone='yes'))
    add(trt('model.onnx', ['--fp16', '--useDLACore=[01]', '--allowGPUFallback']), ['[W] 1 layer(s) will run on the GPU. Add --verbose to see which.', '[I] DLA subgraphs: 1, DLA/GPU transitions: 1', '[I] Building engine (FP16, DLA) ... done in 42.0 s', '[I] Latency: mean = 6.4 ms', tail_ok], set=dict(dlaDone='yes'))
    add(trt('decoder.onnx', ['--fp16', '--useDLACore=[01]'], ['--allowGPUFallback']), ['[E] Layer deconv1 (deconv) cannot run on DLA: deconvolution padding must be 0 (recent TensorRT docs). Add --allowGPUFallback to run it on the GPU.', '[E] Engine build failed.', '&&&& FAILED TensorRT.trtexec'], cls='err')
    add(trt('decoder.onnx', ['--fp16', '--useDLACore=[01]', '--allowGPUFallback', '--verbose']), ['[V] dec_conv1 (conv) -> DLA', '[V] dec_relu1 (relu) -> DLA', '[V] deconv1 (deconv) -> GPU  [fallback: padding must be 0]', '[V] dec_relu2 (relu) -> DLA', '[V] deconv2 (deconv) -> GPU  [fallback: padding must be 0]', '[V] out (sigmoid) -> DLA', '[I] DLA subgraphs: 3, DLA/GPU transitions: 4  (many transitions add overhead)', '[I] Latency: mean = 8.1 ms   (slower: every boundary costs a transfer)', tail_ok], cls='warn', set=dict(dlaDone='yes'))
    add(trt('decoder.onnx', ['--fp16', '--useDLACore=[01]', '--allowGPUFallback']), ['[W] 2 layer(s) will run on the GPU. Add --verbose to see which.', '[I] DLA subgraphs: 3, DLA/GPU transitions: 4  (many transitions add overhead)', '[I] Latency: mean = 8.1 ms', tail_ok], cls='warn', set=dict(dlaDone='yes'))
    add(trt('vqscore.onnx', ['--fp16', '--useDLACore=[01]', '--allowGPUFallback']), ['[I] score_conv (conv) -> DLA', '[I] argmin (argmax) -> GPU  [fallback: ArgMax/TopK are not supported on DLA]', '[I] DLA subgraphs: 1, DLA/GPU transitions: 1', tail_ok], set=dict(dlaDone='yes'))
    add(r'^(/usr/src/tensorrt/bin/)?trtexec(?=.*\s--loadEngine=gpu\.engine)', ['[I] Loaded engine gpu.engine (FP16, GPU, model.onnx)', '[I] Latency: mean = 2.1 ms', tail_ok], when=dict(gpuEngine='yes'))
    add(r'^(/usr/src/tensorrt/bin/)?trtexec(?=.*\s--loadEngine=)', ['[E] Engine file not found (build one first with --saveEngine)', '&&&& FAILED TensorRT.trtexec'], cls='err')
    add(r'^(/usr/src/tensorrt/bin/)?trtexec', ['Usage: trtexec --onnx=model.onnx [--fp16|--int8] [--useDLACore=0|1 --allowGPUFallback] [--saveEngine=x.engine] [--verbose]', '       trtexec --loadEngine=x.engine [--iterations=N]'])
    # --- CUDA
    add(r'^export PATH=/usr/local/cuda/bin:\$PATH$', [], set=dict(cuda='yes'))
    add(r'^nvcc', ['bash: nvcc: command not found', 'hint: export PATH=/usr/local/cuda/bin:$PATH'], cls='err', when=dict(cuda='no'))
    add(r'^nvcc --version$', ['nvcc: NVIDIA (R) Cuda compiler driver', 'Cuda compilation tools, release 11.4, V11.4.315'])
    add(r'^nvcc(?=.*vector_add\.cu)(?=.*-arch=sm_72)(?=.*-o vector_add)', ['compiled vector_add.cu -> vector_add for sm_72'], cls='ok', set=dict(built='ok'))
    add(r'^nvcc(?=.*vector_add\.cu)(?=.*-arch=sm_\d+)(?=.*-o vector_add)', ['compiled vector_add.cu -> vector_add (wrong architecture: the Xavier is sm_72)'], cls='warn', set=dict(built='wrong'))
    add(r'^nvcc(?=.*vector_add\.cu)(?=.*-o vector_add)', ['note: no -arch given; for the Xavier GPU use -arch=sm_72', 'compiled vector_add.cu -> vector_add'], cls='warn', set=dict(built='ok'))
    add(r'^nvcc', ['nvcc fatal   : No input files specified. Try: nvcc -arch=sm_72 vector_add.cu -o vector_add'], cls='err')
    add(r'^\./vector_add$', ['c[0] = 3.000000 (expected 3.0)'], cls='ok', when=dict(built='ok'), set=dict(ran='yes'))
    add(r'^\./vector_add$', ['CUDA error: no kernel image is available for execution on the device (built for the wrong arch; Xavier is sm_72)'], cls='err', when=dict(built='wrong'))
    add(r'^\./vector_add$', ['bash: ./vector_add: No such file or directory'], cls='err')
    # --- misc
    add(r'^whoami$', ['nvidia']); add(r'^pwd$', ['/home/nvidia']); add(r'^nproc$', ['{{cpus}}'])
    add(r'^uname( -a)?$', ['Linux jetson-xavier 5.10.104-tegra #1 SMP PREEMPT aarch64 aarch64 aarch64 GNU/Linux  (simulated)'])
    add(r'^free( -h)?$', ['              total        used        free      shared  buff/cache   available', 'Mem:           31Gi       2.9Gi        26Gi       0.4Gi       2.3Gi        28Gi', 'Swap:          15Gi          0B        15Gi'])
    add(r'^df( -h)?$', ['Filesystem      Size  Used Avail Use% Mounted on', '/dev/mmcblk0p1   28G   17G  9.3G  65% /'])
    add(r'^lscpu$', ['Architecture:        aarch64', 'CPU(s):              {{cpus}} online (of 8)', 'Model name:          ARMv8 Processor rev 0 (v8l)   [Carmel]', 'Vendor ID:           Nvidia'])
    add(r'^lsusb$', ['Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub', '(on the host PC in recovery mode you would see an "NVIDIA Corp." device instead)'])
    add(r'^apt-cache show nvidia-jetpack$', ['Package: nvidia-jetpack', 'Version: 5.1-b147', '(simulated; run on your device for the real value)'])
    add(r'^dpkg -l', ['ii  tensorrt  8.5.2.2-1+cuda11.4  arm64  Meta package for TensorRT', 'ii  libcudnn8  8.6.0.166-1+cuda11.4  arm64  cuDNN runtime', 'ii  libnvvpi2  2.2.7  arm64  VPI runtime'])
    add(r'^python3 -c .*tensorrt', ['8.5.2.2'])
    add(r'^python3 -c .*torch', ['1.13.0a0+d0d6b1f2.nv22.09 True   (a Jetson-specific wheel; a pip default wheel would print False)'])
    add(r'^jtop$', ['jtop is a full-screen app: pages CPU, GPU, MEM, ENG (engines), PWR, CTRL. Install with: sudo pip3 install -U jetson-stats'])
    add(r'^dmesg', ['[  812.114] nvgpu: gpu power on', '[ 1203.552] tegra-pmc: power mode changed', '[ 2290.010] (look here for "Out of memory", USB and thermal messages)'])
    add(r'^gst-launch-1\.0 .*nvarguscamerasrc', ['Setting pipeline to PAUSED ...', 'GST_ARGUS: Creating output stream', '(simulated: camera -> ISP -> VIC -> display; on hardware the frames stay in NVMM memory)'])
    add(r'^gst-launch-1\.0', ['Setting pipeline to PLAYING ...', '(simulated)'])
    return C


CHIPS = ['cat /etc/nv_tegra_release', 'sudo nvpmodel -q', 'sudo nvpmodel -m 0', 'sudo jetson_clocks', 'tegrastats', 'ls',
         'trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine', 'trtexec --onnx=model.onnx --fp16 --useDLACore=0 --allowGPUFallback --verbose',
         'trtexec --onnx=decoder.onnx --fp16 --useDLACore=0', 'export PATH=/usr/local/cuda/bin:$PATH', 'nvcc -arch=sm_72 vector_add.cu -o vector_add', './vector_add']
VARS = dict(mode='0', modeName='MAXN', cpus='8', cpuMhz='2265', gpuMhz='1377', emc='2133', locked='no', cuda='no', built='no', engines='', gpuEngine='no', dlaDone='no')
INTRO = 'Simulated Jetson AGX Xavier shell. Try: cat /etc/nv_tegra_release, sudo nvpmodel -q, sudo jetson_clocks, tegrastats, trtexec ..., nvcc ... Pipes to grep/head/tail work. Numbers are illustrative.'


def terminal(title, intro, tasks, id_=None):
    return dict(type='terminal', id=id_ or title.lower().replace(' ', '-'), title=title, intro=intro, prompt='nvidia@xavier:~$', banner='Simulated Jetson AGX Xavier. Type help, or tap a chip. Nothing here touches a real device.',
                vars=VARS, commands=terminal_commands(), chips=CHIPS, tasks=[dict(text=t, cmd=c) for t, c in tasks], notFound='{{0}}: command not found. Type help.')


def sandbox():
    t = terminal('Xavier shell', INTRO, [('Identify your software: cat /etc/nv_tegra_release', r'^cat /etc/nv_tegra_release$'), ('Query the power mode: sudo nvpmodel -q', r'^(sudo )?nvpmodel -q'), ('Set MAXN: sudo nvpmodel -m 0', r'^sudo nvpmodel -m 0$'),
                                       ('Lock clocks: sudo jetson_clocks', r'^sudo jetson_clocks$'), ('Build a GPU FP16 engine with trtexec', r'trtexec.*--onnx=model\.onnx.*--fp16.*--saveEngine=gpu\.engine'),
                                       ('Build for DLA with fallback and --verbose', r'trtexec.*--useDLACore=\d.*--allowGPUFallback.*--verbose'), ('Compile and run vector_add for sm_72', r'^\./vector_add$'), ('Watch the system: tegrastats', r'^(sudo )?tegrastats$')], 'sandbox')
    return t


# ---------------------------------------------------------------- practice labs
DLA_CHECK = r"""
var layers = result;
if (!Array.isArray(layers)) return { pass: false, msgs: ['FAIL the code must return an array of layers'] };
function dev(l) {
  var t = String(l.type || '').toLowerCase();
  if (['conv','fc','batchnorm','scale','eltwise','lrn','shuffle','relu','sigmoid','tanh','leakyrelu','clippedrelu','pool','concat'].indexOf(t) >= 0) return null;
  if (t === 'deconv') return (l.padding || 0) !== 0 ? 'deconvolution padding must be 0' : null;
  if (t === 'resize') { if (!Number.isInteger(l.scale)) return 'resize needs an integer scale'; return l.scale > (l.mode === 'bilinear' ? 4 : 32) ? 'resize scale too large' : null; }
  if (t === 'softmax') return 'Softmax is not supported on Xavier DLA (Orin only)';
  if (t === 'argmax' || t === 'topk') return 'ArgMax/TopK are not supported on DLA';
  return 'layer type ' + t + ' is not supported on DLA';
}
var msgs = [], gpu = 0, sub = 0, prev = null;
layers.forEach(function (l) {
  var why = dev(l), d = why ? 'GPU' : 'DLA';
  if (why) gpu++;
  if (d === 'DLA' && prev !== 'DLA') sub++;
  prev = d;
  msgs.push('  ' + d + ' ' + (l.name || l.type) + ' (' + l.type + ')' + (why ? '  -> ' + why : ''));
});
var last = layers[layers.length - 1];
var checks = [
  [layers.length >= 5, 'at least 5 layers'],
  [layers.some(function (l) { return l.type === 'conv'; }), 'contains a conv'],
  [sub === 1, 'exactly 1 DLA subgraph (found ' + sub + ')'],
  [gpu <= 1, 'at most 1 GPU layer (found ' + gpu + ')'],
  [gpu === 0 || (last && last.type === 'argmax'), 'any GPU layer is the final argmax']
];
var pass = true;
checks.forEach(function (c) { pass = pass && c[0]; msgs.push((c[0] ? 'PASS ' : 'FAIL ') + c[1]); });
return { pass: pass, msgs: msgs };
"""

DLA_START = 'return [\n  { type: "conv", name: "enc1" },\n  { type: "gelu", name: "act1" },\n  { type: "conv", name: "enc2", stride: 2 },\n  { type: "softmax", name: "attn_norm" },\n  { type: "deconv", name: "up1", padding: 1 },\n  { type: "relu", name: "act2" },\n  { type: "resize", name: "up2", mode: "bilinear", scale: 2.5 },\n  { type: "conv", name: "out" },\n  { type: "argmax", name: "pick" }\n];'
DLA_SOL = 'return [\n  { type: "conv", name: "enc1" },\n  { type: "relu", name: "act1" },\n  { type: "conv", name: "enc2", stride: 2 },\n  { type: "resize", name: "up1", mode: "nearest", scale: 2 },\n  { type: "conv", name: "up1_conv" },\n  { type: "relu", name: "act2" },\n  { type: "resize", name: "up2", mode: "nearest", scale: 2 },\n  { type: "conv", name: "out" },\n  { type: "argmax", name: "pick" }\n];'


def vq_tests():
    import random
    r = random.Random(42); tests = []
    for _ in range(8):
        D, K = 4, 6
        cb = [[round(r.uniform(-2, 2), 2) for _ in range(D)] for _ in range(K)]
        a = [round(r.uniform(-2, 2), 2) for _ in range(D)]
        best = min(range(K), key=lambda k: sum((a[i] - cb[k][i]) ** 2 for i in range(D)))
        tests.append(dict(args=[a, cb], expect=best, label='nearest(a, codebook of %d)' % K))
    return tests


LABS = {
    0: [dict(type='order', title='A path through the course', intro='Put the parts of the course in the order you will read them.', items=['Hardware (chapters 1 to 4)', 'Get the board running (chapters 5 to 7)', 'Compute: CUDA, TensorRT, the DLA (chapters 8 to 10)', 'Design and pipelines (chapters 11 to 15)', 'Tune, troubleshoot and plan ahead (chapters 16 to 19)'], hint='Hardware first, then software, then compute, then design.')],
    1: [dict(type='match', title='Name the part', intro='Match each Jetson term to what it is.', pairs=[['Module', 'Xavier SoC plus memory, eMMC and power circuitry'], ['Carrier board', 'Breaks out USB, Ethernet, display, camera and PCIe'], ['Developer kit', 'A module on a carrier with heatsink and power supply'], ['32 TOPS INT8', 'GPU plus the two DLAs combined']]),
        dict(type='fill', title='Not a PC', intro='Complete the sentence.', text='The Xavier is not a PC: there is no {{BIOS}} setup menu, so you {{flash|flash images}} images onto it from a host PC.')],
    2: [dict(type='match', title='Which processor?', intro='Match each block to its job.', pairs=[['CPU', 'Runs Linux, Python and orchestration'], ['GPU', 'CUDA and fast FP16/INT8 deep learning'], ['DLA', 'Fixed neural-network layers at low power'], ['PVA', 'Classic vision: filters, optical flow, tracking'], ['ISP', 'Turns raw sensor data into images'], ['VIC', 'Scaling and color conversion with no GPU cost']]),
        dict(type='fill', title='GPU facts', text='The Xavier GPU has compute capability {{7.2}}, so you compile with -arch={{sm_72}}.')],
    3: [dict(type='fill', title='Memory facts', text='Memory is 256-bit {{LPDDR4x}} at about {{136.5}} GB/s, and it is {{shared}} by every processor.', hint='One pool for CPU, GPU, DLAs, PVAs and media blocks.')],
    4: [terminal('Power and clocks', 'Practice the power commands.', [('Query the power mode: sudo nvpmodel -q', r'^(sudo )?nvpmodel -q'), ('Set MAXN: sudo nvpmodel -m 0', r'^sudo nvpmodel -m 0$'), ('Lock the clocks: sudo jetson_clocks', r'^sudo jetson_clocks$')], 'power')],
    5: [dict(type='match', title='Library to processor', intro='Which software reaches which processor?', pairs=[['CUDA, cuDNN, TensorRT', 'GPU'], ['TensorRT or cuDLA', 'DLA'], ['VPI', 'PVA and VIC'], ['Argus', 'ISP'], ['GStreamer or Multimedia API', 'NVENC and NVDEC']]),
        dict(type='order', title='The software stack', intro='Order the layers from the bottom up.', items=['Hardware', 'Bootloader and firmware', 'Linux kernel and drivers (L4T)', 'CUDA, cuDNN, TensorRT, VPI, multimedia libraries', 'Frameworks and your application'])],
    6: [dict(type='order', title='Flash the board', intro='Put the flashing steps in order.', items=['Connect the host to the flashing USB-C port', 'Put the Jetson in recovery mode', 'Check that lsusb on the host lists an NVIDIA device', 'Choose product and JetPack in SDK Manager', 'Flash and install components', 'First boot: license, user, network'])],
    7: [dict(type='code', title='Parse tegrastats', intro='Write parseGr3d(line): return {load, mhz} from the GR3D_FREQ field of a tegrastats line (some releases print the clock in brackets). Return null if the field is missing.', fn='parseGr3d',
             starter='function parseGr3d(line) {\n  // return { load: <number>, mhz: <number> }\n}',
             tests=[dict(args=['RAM 2951/31920MB CPU [12%@2265,off] EMC_FREQ 5%@2133 GR3D_FREQ 37%@1377 AO@38C'], expect=dict(load=37, mhz=1377)), dict(args=['GR3D_FREQ 0%@114 thermal@41C'], expect=dict(load=0, mhz=114)), dict(args=['EMC_FREQ 9%@2133 GR3D_FREQ 88%@[1377] GPU@50C'], expect=dict(load=88, mhz=1377)), dict(args=['no gpu field here'], expect=None)],
             hint='Use a regular expression such as /GR3D_FREQ\\s+(\\d+)%@\\[?(\\d+)\\]?/ and convert the groups with Number().',
             solution='function parseGr3d(line) {\n  var m = /GR3D_FREQ\\s+(\\d+)%@\\[?(\\d+)\\]?/.exec(line);\n  if (!m) return null;\n  return { load: Number(m[1]), mhz: Number(m[2]) };\n}'),
        terminal('Watch the system', 'Read tegrastats.', [('Run tegrastats', r'^(sudo )?tegrastats$')], 'watch')],
    8: [dict(type='code', title='CUDA grid size', intro='Write gridSize(n, block): the number of blocks so that blocks * block >= n (ceiling division).', fn='gridSize', starter='function gridSize(n, block) {\n  // return the number of blocks\n}',
             tests=[dict(args=[1000000, 256], expect=3907), dict(args=[256, 256], expect=1), dict(args=[257, 256], expect=2), dict(args=[1, 128], expect=1), dict(args=[0, 256], expect=0)],
             hint='Add (block - 1) to n before the integer division, then truncate.', solution='function gridSize(n, block) {\n  return Math.floor((n + block - 1) / block);\n}'),
        dict(type='write', title='Compile for the Xavier', prompt='Write the nvcc command that compiles vector_add.cu into an executable called vector_add for the Xavier GPU.', checks=[dict(re=r'^\s*nvcc\b', msg='uses nvcc'), dict(re=r'-arch=sm_72', msg='targets sm_72'), dict(re=r'vector_add\.cu', msg='compiles vector_add.cu'), dict(re=r'-o\s+vector_add\b', msg='outputs vector_add')], hint='nvcc -arch=sm_72 file.cu -o name', solution='nvcc -arch=sm_72 -O2 vector_add.cu -o vector_add')],
    9: [dict(type='write', title='Build an FP16 engine', prompt='Write the trtexec command that builds an FP16 engine from model.onnx and saves it as gpu.engine.', checks=[dict(re=r'trtexec', msg='uses trtexec'), dict(re=r'--onnx=model\.onnx', msg='reads model.onnx'), dict(re=r'--fp16', msg='uses --fp16'), dict(re=r'--saveEngine=gpu\.engine', msg='saves gpu.engine'), dict(re=r'--useDLACore', msg='does not target the DLA', **{'not': True})], hint='trtexec --onnx=... --fp16 --saveEngine=...', solution='trtexec --onnx=model.onnx --fp16 --saveEngine=gpu.engine'),
        terminal('Build engines', 'Build a GPU engine, then load it back.', [('Build the FP16 GPU engine', r'trtexec.*--saveEngine=gpu\.engine'), ('Load it again', r'trtexec.*--loadEngine=gpu\.engine')], 'engines')],
    10: [dict(type='code', title='Make the model DLA-friendly', intro='Edit the layer list so it runs as ONE DLA subgraph, with at most one GPU layer, and that layer must be the final argmax. Keep at least 5 layers and one conv. Use the Xavier DLA rules from this chapter. The code must return the layer array.', isBody=True,
              starter=DLA_START, checkJs=DLA_CHECK, hint='GELU -> relu. Softmax is not on Xavier DLA: remove it. Deconv with padding 1 -> resize nearest scale 2 then a conv. Bilinear scale 2.5 -> an integer scale.', solution=DLA_SOL),
         terminal('See the fallbacks', 'Build for the DLA and read the placement.', [('Build model.onnx for DLA with fallback and --verbose', r'trtexec.*--onnx=model\.onnx.*--useDLACore=\d.*--allowGPUFallback.*--verbose'), ('Try decoder.onnx and read why layers fall back', r'trtexec.*--onnx=decoder\.onnx.*--allowGPUFallback')], 'fallbacks')],
    11: [dict(type='code', title='VQ-VAE nearest entry', intro='Write nearest(a, codebook): return the index of the closest codebook vector using the score ||b||^2 - 2 a.b (do not compute ||a - b||^2). This is the math you would put in a 1x1 convolution on the DLA.', fn='nearest',
              starter='// a: array of D numbers; codebook: array of K arrays of D numbers\nfunction nearest(a, codebook) {\n  // your code\n}', tests=vq_tests(),
              hint='For each k: score = sum(b_i^2) - 2*sum(a_i*b_i). Return the index with the smallest score.',
              solution='function nearest(a, codebook) {\n  var best = 0, bs = Infinity;\n  for (var k = 0; k < codebook.length; k++) {\n    var b = codebook[k], nb = 0, dot = 0;\n    for (var i = 0; i < a.length; i++) { nb += b[i] * b[i]; dot += a[i] * b[i]; }\n    var score = nb - 2 * dot;\n    if (score < bs) { bs = score; best = k; }\n  }\n  return best;\n}'),
         dict(type='fill', title='VAE at deployment', text='At deployment a VAE ignores the variance and passes the {{mean|mu}} to the decoder, so there is no {{sampling|sample|noise}} step.')],
    12: [dict(type='fill', title='PVA and VPI', text='The PVA is programmed through {{VPI}} by choosing the {{PVA}} backend. It does not run {{neural networks|neural network}}.')],
    13: [dict(type='order', title='Camera to inference', intro='Order the stages of the capture-to-model path.', items=['Camera sensor', 'ISP (nvarguscamerasrc)', 'VIC resize (nvvidconv)', 'DLA or GPU inference', 'CPU handles control and small tensors'], hint='The CPU only sees small results at the end.'),
         dict(type='fill', title='GStreamer', text='MIPI cameras use {{nvarguscamerasrc}}, USB cameras use {{v4l2src}}, and (memory:{{NVMM}}) keeps frames in hardware memory.')],
    14: [dict(type='fill', title='Containers', text='Run containers with --runtime {{nvidia}}; the image tag must match your {{L4T}} release.')],
    15: [dict(type='code', title='Bandwidth budget', intro='Write mbPerSecond(width, height, channels, bytesPerValue, moves, fps): megabytes per second (1 MB = 1,000,000 bytes) when each frame is moved "moves" times.', fn='mbPerSecond',
              starter='function mbPerSecond(width, height, channels, bytesPerValue, moves, fps) {\n  // your code\n}',
              tests=[dict(args=[256, 256, 3, 2, 4, 30], expect=47.18592, approx=0.01), dict(args=[3840, 2160, 3, 1, 10, 30], expect=7464.96, approx=0.01), dict(args=[1, 1, 1, 1, 1, 1], expect=0.000001, approx=0.0001)],
              hint='bytes per frame = width*height*channels*bytesPerValue; multiply by moves and fps; divide by 1e6.', solution='function mbPerSecond(width, height, channels, bytesPerValue, moves, fps) {\n  return width * height * channels * bytesPerValue * moves * fps / 1e6;\n}')],
    16: [dict(type='match', title='Symptom to first check', intro='Match the symptom to the first thing to check.', pairs=[['Timings vary from run to run', 'Lock clocks with jetson_clocks'], ['DLA engine slower than expected', 'Count GPU fallbacks and DLA subgraphs'], ['First iterations look slow', 'Warm up the engine before timing'], ['Slowdown under sustained 30 W', 'Thermal throttling']])],
    17: [dict(type='match', title='Problem to cause', intro='Match each problem to its likely cause or fix.', pairs=[['Engine will not load after an update', 'Rebuild it with the new TensorRT'], ['import tensorrt fails in a venv', 'Create it with --system-site-packages'], ['Random reboots under load', 'A weak power supply'], ['A process gets killed', 'Out of memory: shared RAM ran out']])],
    18: [dict(type='fill', title='What comes next', text='JetPack {{5}}.x is the last line for the Xavier. Orin has a {{second|2nd}}-generation DLA, and Jetson Thor has {{no}} DLA.')],
    19: [dict(type='write', title='Lock the clocks', prompt='Write the command that locks the clocks at the maximum of the current power mode.', checks=[dict(re=r'sudo\s+jetson_clocks\s*$', msg='sudo jetson_clocks')], hint='It needs root.', solution='sudo jetson_clocks'),
         dict(type='write', title='Build for DLA core 1', prompt='Write the trtexec flags (after --onnx=model.onnx) that build an FP16 engine for DLA core 1 with GPU fallback.', checks=[dict(re=r'--fp16', msg='--fp16'), dict(re=r'--useDLACore=1', msg='--useDLACore=1'), dict(re=r'--allowGPUFallback', msg='--allowGPUFallback')], solution='--fp16 --useDLACore=1 --allowGPUFallback')],
    20: [dict(type='match', title='Glossary check', intro='Match each term to its meaning.', pairs=[['DLA', 'Deep Learning Accelerator'], ['zero-copy', 'CPU and GPU use the same buffer without copying'], ['L4T', 'Jetson Linux release inside JetPack'], ['NVMM', 'Hardware-managed memory for frames'], ['ONNX', 'Open format for exchanging neural networks']])],
    21: [dict(type='fill', title='Trust but verify', text='Claims marked {{(from memory)|from memory}} were not re-checked. Where this course disagrees with the {{documentation|docs}} for your release, trust that.')],
    22: [dict(type='match', title='Which map?', intro='Match each map to what it explains.', pairs=[['The Xavier at a glance', 'What it is made of and why shared memory matters'], ['Software that reaches each processor', 'Which library drives which block'], ['From a model to the DLA', 'The path from a trained model and what causes fallbacks'], ['Power, speed and heat', 'How modes, clocks, heat and bandwidth affect speed']])],
}
