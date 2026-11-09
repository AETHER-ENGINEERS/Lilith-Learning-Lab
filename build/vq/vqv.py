"""VQ-VAE course."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

# 1
CHS.append(CH(
 "What is VQ-VAE?",
 ("The big picture", [
  "VQ-VAE | is | A discrete latent autoencoder",
  "Encoder | outputs | Continuous vectors",
  "Codebook | holds | K embedding vectors",
  "Quantizer | picks | Nearest codebook vector",
  "Decoder | reads | Quantized vectors",
  "Prior | models | Sequences of code indices",
  "VQ-VAE | introduced by | van den Oord et al."]),
 ["VQ-VAE, the Vector Quantised Variational AutoEncoder, is a generative model that learns discrete codes. It was introduced by Aaron van den Oord, Oriol Vinyals and Koray Kavukcuoglu in the 2017 paper Neural Discrete Representation Learning.",
  "An encoder turns the input into vectors. Each vector is replaced by the nearest entry of a learned codebook. A decoder rebuilds the input from the chosen entries. What remains between them is a grid of integer indices.",
  "A second model, an autoregressive prior such as PixelCNN, learns to generate those indices, and sampling from it plus decoding makes new data."],
 [("Autoencoder", "A network that compresses its input into a code and rebuilds the input from it."),
  ("Latent", "The hidden representation between encoder and decoder."),
  ("Codebook", "A table of K learned vectors; each is a possible discrete code."),
  ("Quantization", "Replacing a continuous vector by its nearest codebook vector."),
  ("Prior", "A model of how the codes are distributed, used to generate new samples."),
  ("Straight-through estimator", "A trick that copies gradients across the non-differentiable quantizer.")],
 ["Published at NeurIPS 2017 by van den Oord, Vinyals and Kavukcuoglu.",
  "Latents are discrete: each position holds an index into a codebook of K vectors.",
  "The quantizer is a nearest-neighbour lookup; gradients are copied across it.",
  "The loss has three parts: reconstruction, codebook and commitment.",
  "Generation needs a separate prior over the code indices, such as PixelCNN or WaveNet.",
  "The discrete bottleneck avoids the posterior collapse seen in many VAEs with powerful decoders."],
 [T("Many things we care about are naturally discrete. Language is a string of words. Speech is a sequence of phonemes. Even images can be described in words. A model whose hidden representation is discrete may therefore match the data better, and it can be handled by tools made for symbols, such as autoregressive sequence models."),
  T("The VQ-VAE paper, presented at NeurIPS 2017, builds a variational autoencoder whose latent codes are discrete. The abstract says it incorporates ideas from vector quantisation. It differs from ordinary VAEs in two ways: the encoder outputs discrete codes, not continuous ones, and the prior is learned instead of fixed."),
  T("Here is the whole pipeline. An input image goes through an encoder network and comes out as a grid of vectors, each of dimension D. A codebook holds K vectors of the same dimension. At each grid position the nearest codebook vector replaces the encoder's output. The decoder reads the grid of chosen vectors and produces a reconstruction. The thing the codebook indices form, a grid of integers between one and K, is the discrete representation."),
  M(r"x \;\xrightarrow{\ \text{encoder}\ }\; z_e(x) \;\xrightarrow{\ \text{nearest code}\ }\; z_q(x) \;\xrightarrow{\ \text{decoder}\ }\; \hat{x}"),
  T("There is one technical obstacle. Picking the nearest codebook vector is not differentiable, so gradients from the decoder cannot flow back into the encoder by the usual rule. The paper's solution is the straight-through estimator: in the backward pass, copy the gradient at the decoder input straight to the encoder output as if the quantizer were not there. Chapter 4 covers it."),
  T("Generation is separate from training. The autoencoder only learns to encode and decode. To make new samples, the paper trains an autoregressive prior over the grid of discrete codes after the autoencoder is done: PixelCNN for images and WaveNet for raw audio. Sample a grid of codes from the prior, look up the codebook vectors and decode."),
  T("A note on sources. This course follows the 2017 paper, and is supplemented by later descriptions of the method, for example the common implementations and the many tutorials. Numbers such as the commitment weight of 0.25 are the usual settings. Later work is labelled as background knowledge. The labs are tiny teaching examples in plain Python, with no neural network library.")],
 [("What does the quantizer do?", ["Replaces an encoder output by the nearest codebook vector", "Adds noise", "Trains the decoder", "Samples from a Gaussian"], 0, "A nearest-neighbour lookup."),
  ("Why is the prior learned after training?", ["Generation needs a model of the code indices", "To save memory", "The decoder needs it", "It is not learned"], 0, "PixelCNN or WaveNet."),
  ("What kind of latents does VQ-VAE use?", ["Discrete", "Gaussian", "Binary images", "None"], 0, "Indices into a codebook."),
  ("Who introduced VQ-VAE?", ["van den Oord, Vinyals and Kavukcuoglu", "Kingma and Welling", "Goodfellow", "Vaswani"], 0, "NeurIPS 2017.")],
 [("What are the three parts of VQ-VAE?", "Encoder, codebook with quantizer, decoder."), ("How big is the codebook?", "K vectors of dimension D."), ("What is generated by the prior?", "Grids of code indices."),
  ("Why discrete?", "It matches language and speech and allows sequence models.")],
 [ORDER("VQ-VAE pipeline", "Put the steps in order.", ["Encode the input into vectors", "Find the nearest codebook vector for each", "Replace the vectors by their codebook entries", "Decode the quantized grid", "Compare the output with the input"]),
  MATCH("Parts", "Match each part with its role.", [("Encoder", "Produces continuous vectors"), ("Codebook", "K learned embedding vectors"), ("Quantizer", "Nearest-neighbour lookup"), ("Decoder", "Rebuilds the input"), ("Prior", "Generates code grids")]),
  FILL("Basics", "VQ-VAE replaces each encoder output by its nearest {{codebook}} vector. Gradients are copied across the quantizer by the {{straight-through|straight through}} estimator.")]))

# 2
CHS.append(CH(
 "Autoencoders and bottlenecks",
 ("Autoencoders", [
  "Autoencoder | compresses | Input to a code",
  "Bottleneck | forces | Information loss",
  "Reconstruction loss | measures | Difference from input",
  "VAE | adds | A prior on latents",
  "Posterior collapse | ignores | The latent",
  "Discrete bottleneck | limits | Bits per position",
  "Rate | counts | Bits in the code"]),
 ["An autoencoder squeezes an input through a narrow code and tries to rebuild it. The narrowness, the bottleneck, forces the network to keep only what matters.",
  "A variational autoencoder, VAE, makes the code random and pushes it toward a simple prior. A known weakness is posterior collapse: a strong decoder learns to ignore the code. VQ-VAE avoids it, since the discrete code carries a fixed number of bits that the decoder must use.",
  "The size of the bottleneck is measurable. This chapter counts the bits and the compression."],
 [("Reconstruction loss", "A measure of how different the output is from the input, often mean squared error."),
  ("Bottleneck", "A layer much smaller than the input, limiting information."),
  ("VAE", "A variational autoencoder with a random latent and a prior."),
  ("Posterior collapse", "The decoder ignores the latent and the encoder outputs the prior."),
  ("Bit", "A unit of information: one yes-or-no choice."),
  ("Compression ratio", "Input size divided by code size.")],
 ["An autoencoder trains encoder and decoder together to minimize reconstruction error.",
  "A code with K possible values per position carries log2(K) bits per position.",
  "The compression ratio is input bits over code bits.",
  "VAEs with powerful decoders can suffer posterior collapse.",
  "A discrete code forces the decoder to use the bits it gets.",
  "In the paper, 128 by 128 ImageNet images were compressed to a 32 by 32 grid of discrete codes."],
 [T("The simplest autoencoder has two halves. The encoder takes an input, say an image, and produces a short vector. The decoder takes the vector and tries to produce the original image. Training reduces the difference between the output and the input, usually the mean squared error, averaged over all numbers."),
  M(r"L_{\mathrm{rec}} \;=\; \frac{1}{n}\sum_{i=1}^{n}\,(x_i - \hat{x}_i)^2"),
  T("If the code is as large as the input, the network can copy and learn nothing useful. The code must be small. That bottleneck is what forces the encoder to find structure: edges, shapes, parts. What it throws away is what the model considers unimportant."),
  T("A variational autoencoder adds probability. The encoder gives a distribution over codes, a sample is drawn, and a penalty keeps the distribution near a prior, usually a standard Gaussian. This gives a neat way to generate: draw from the prior and decode. A well-known difficulty is that if the decoder is powerful, such as an autoregressive model over the pixels, it can model the data without any help from the code. The code then carries almost nothing. This is posterior collapse."),
  T("The VQ-VAE paper notes that its model does not suffer from this problem. Its code is discrete, with a fixed set of values per position, and the decoder gets nothing about the input except the chosen codes. There is no sampling noise in the code and no penalty pushing it to the prior during training, so there is nothing to collapse into."),
  T("How much information is in a discrete code? A position that can take K values holds log base two of K bits, if all values are equally likely. A grid of positions holds that many bits for each. For the paper's ImageNet setting, a 128 by 128 colour image, with 24 bits per pixel, was encoded as a 32 by 32 grid with 512 possible values per position, which is 9 bits. The practice section computes the compression from these numbers. The grid sizes come from the paper's description and the result is my own arithmetic."),
  T("The labs in this chapter write the reconstruction error and count the bits and the compression ratio.")],
 [("What does a bottleneck force?", ["The network to keep only important information", "Larger images", "Random output", "Slower training"], 0, "Less capacity than the input."),
  ("How many bits does a position with 512 values hold at most?", ["9", "512", "5", "64"], 0, "log2(512) = 9."),
  ("What is posterior collapse?", ["The decoder ignores the latent", "The encoder crashes", "The loss is zero", "The prior is fixed"], 0, "Common with powerful decoders."),
  ("What does the compression ratio divide?", ["Input bits by code bits", "Code bits by input bits", "Pixels by colours", "Loss by steps"], 0, "A bigger ratio means more compression.")],
 [("What is MSE?", "The mean of squared differences."), ("What is a bit?", "One yes-or-no choice."), ("Why a small code?", "To force useful features."), ("What avoids posterior collapse here?", "The discrete code with no sampling noise.")],
 [PL("Reconstruction error", "Write mse(x, y): the mean of (x_i - y_i)^2 over two equal-length lists.",
     "mse(x, y)", """
def mse(x, y):
    total = 0.0
    for a, b in zip(x, y):
        total += (a - b) ** 2
    return total / len(x)
""", [[[1, 2, 3], [1, 2, 3]], [[0, 0], [1, 1]], [[1.0, 2.0], [2.0, 4.0]], [[5], [3]]], "Average the squared differences.", approx=1e-12),
  PL("Bits in a code", "Write bits_per_code(k): the number of bits needed to name one of k values, that is the smallest b with 2^b at least k.",
     "bits_per_code(k)", """
def bits_per_code(k):
    b = 0
    while 2 ** b < k:
        b += 1
    return b
""", [[2], [512], [3], [1], [1024]], "Count doublings until 2^b reaches k."),
  PL("Compression ratio", "An image has h by w pixels with c channels of bits_per_channel bits. It is encoded as a gh by gw grid of codes from a codebook of k entries (bits per code as in the previous lab, rounded up). Write compression(h, w, c, bits_per_channel, gh, gw, k): input bits divided by code bits.",
     "compression(h, w, c, bits_per_channel, gh, gw, k)", """
def compression(h, w, c, bits_per_channel, gh, gw, k):
    b = 0
    while 2 ** b < k:
        b += 1
    return (h * w * c * bits_per_channel) / (gh * gw * b)
""", [[128, 128, 3, 8, 32, 32, 512], [32, 32, 3, 8, 8, 8, 512], [28, 28, 1, 8, 7, 7, 64], [64, 64, 3, 8, 16, 16, 256]], "Input bits over latent grid bits.", approx=1e-9),
  ORDER("Autoencoder training", "Order one training step.", ["Feed an input to the encoder", "Pass the code to the decoder", "Compare the output with the input", "Compute the reconstruction loss", "Update the weights"]),
  MATCH("Terms", "Match each term with its meaning.", [("Bottleneck", "Narrow code"), ("Posterior collapse", "Latent ignored"), ("Bit", "Yes-or-no choice"), ("MSE", "Mean squared error"), ("Compression ratio", "Input bits over code bits")]),
  FILL("Autoencoders", "A narrow {{bottleneck}} forces the network to keep important information. A code with 512 values carries {{9}} bits per position.")]))

# 3
CHS.append(CH(
 "The codebook and nearest-neighbour quantization",
 ("Quantizer", [
  "Codebook | is | K by D table",
  "Quantizer | uses | Nearest neighbour",
  "Distance | is | Squared Euclidean",
  "Index | names | Codebook row",
  "Code usage | can be | Uneven",
  "Grid of indices | is | The latent",
  "Decoder | gets | Looked-up vectors"]),
 ["The codebook is a table e with K rows, each a vector of dimension D. At each position, the encoder's output vector z is compared with every row, and the closest one wins.",
  "The index of the winner is the discrete code. The looked-up row, not the original vector, goes to the decoder.",
  "How well the codebook is used matters. If only a few rows ever win, the capacity is wasted. The labs count the usage."],
 [("Codebook", "A table of K embedding vectors e_1 to e_K, each of dimension D."),
  ("Nearest neighbour", "The codebook entry with the smallest distance to the input."),
  ("Squared Euclidean distance", "The sum of squared differences between two vectors."),
  ("Index", "The position k of the chosen codebook row; the discrete code."),
  ("Latent grid", "The spatial arrangement of indices; 32 by 32 in the paper for ImageNet."),
  ("Code usage", "How often each codebook row is chosen.")],
 ["z_q(x) = e_k with k = argmin_j of the squared distance between z_e(x) and e_j.",
  "Ties go to the lowest index in the labs.",
  "The posterior is deterministic: one-hot on the nearest code.",
  "The latent for an image is a grid of indices; the decoder sees the vectors, not the indices.",
  "Codebook usage should be spread across many rows.",
  "The paper used a codebook of 512 vectors with dimension 64 in its image experiments, and mentions K and D as the main sizes."],
 [T("Think of the codebook as a dictionary of visual words. Each entry is a vector that the model can say. The encoder produces a vector at each position of a grid, a kind of rough, continuous word. The quantizer snaps that vector to the nearest dictionary entry, so each position holds exactly one of K words."),
  M(r"k \;=\; \arg\min_{j}\ \lVert z_e(x) - e_j \rVert_2^2, \qquad z_q(x) \;=\; e_k"),
  T("The nearest neighbour is measured with the ordinary Euclidean distance, usually squared since the square root does not change which is nearest. If two codebook entries are equally near, any rule will do; the labs take the lower index. The posterior is therefore deterministic: the probability is one for the closest entry and zero for every other."),
  T("The paper describes the shapes this way. The encoder output is a grid of vectors, each of dimension D. The codebook has K rows. Every position is quantized independently. For the image experiments the paper reduces a 128 by 128 image to a 32 by 32 grid. In many reimplementations the codebook has K of 512 and D of 64."),
  T("Because only the index matters for later models, the quantized latent is equivalent to a grid of integers. This is what makes the next step possible. A grid of integers can be modelled by any model for categorical sequences, which we use in chapter 8."),
  T("Code usage is the practical worry. At the start, the codebook vectors are random and the encoder outputs are somewhere else, and a few codebook rows may be nearest to all the outputs. Those rows win again and again and get trained, while the others never win and never get trained. Chapter 6 comes back to this. For now, count how often each row is used."),
  T("The labs find the nearest code, quantize a batch of vectors and count the usage of each row.")],
 [("How is the code chosen?", ["Nearest codebook vector", "Random", "Highest value", "Average"], 0, "argmin of the distance."),
  ("What does the decoder receive?", ["The codebook vector", "The index", "The input image", "Noise"], 0, "z_q, the looked-up row."),
  ("What is in a codebook row?", ["A vector of dimension D", "An image", "A word", "A probability"], 0, "K rows."),
  ("Why is the squared distance enough?", ["The square root does not change the nearest", "It is faster only", "Square roots fail", "It changes the answer"], 0, "Monotonic.")],
 [("What is the posterior?", "One-hot on the nearest code."), ("What shape is the latent grid for ImageNet in the paper?", "32 by 32."), ("What can go wrong with usage?", "A few rows win all the time."), ("What is K?", "The codebook size.")],
 [PL("Nearest code", "Write nearest_code(z, codebook): the index of the codebook row with the smallest squared distance to the vector z (ties go to the lowest index).",
     "nearest_code(z, codebook)", """
def nearest_code(z, codebook):
    best = None
    arg = 0
    for i in range(len(codebook)):
        d = 0.0
        for a, b in zip(z, codebook[i]):
            d += (a - b) ** 2
        if best is None or d < best - 1e-12:
            best = d
            arg = i
    return arg
""", [[[0.9, 1.1], [[0, 0], [1, 1], [2, 2]]], [[0, 0], [[1, 1], [-1, -1]]], [[5, 5], [[0, 0], [4, 6], [6, 4]]], [[0.5], [[0], [1]]], [[2.0, 0.0], [[0, 0], [4, 0], [2, 3]]]], "Compute the squared distance to each row and keep the smallest."),
  PL("Quantize a batch", "Write quantize(zs, codebook): for each vector in zs return [index, the chosen codebook vector] as two parallel lists: [list of indices, list of chosen vectors].",
     "quantize(zs, codebook)", """
def quantize(zs, codebook):
    idx = []
    chosen = []
    for z in zs:
        best = None
        arg = 0
        for i in range(len(codebook)):
            d = 0.0
            for a, b in zip(z, codebook[i]):
                d += (a - b) ** 2
            if best is None or d < best - 1e-12:
                best = d
                arg = i
        idx.append(arg)
        chosen.append(list(codebook[arg]))
    return [idx, chosen]
""", [[[[0.1, 0.1], [0.9, 1.0], [2.1, 1.9]], [[0, 0], [1, 1], [2, 2]]], [[[3, 3]], [[0, 0], [4, 4]]], [[[0.5, 0.5], [0.4, 0.6]], [[0, 1], [1, 0]]]], "Reuse the nearest-code search for every vector."),
  PL("Code usage", "Write code_counts(indices, k): a list of length k with the number of times each index appears.",
     "code_counts(indices, k)", """
def code_counts(indices, k):
    counts = [0] * k
    for i in indices:
        counts[i] += 1
    return counts
""", [[[0, 1, 1, 2, 1], 3], [[], 4], [[3, 3, 3], 4], [[0, 0, 1], 2]], "Add one for each index."),
  ORDER("Quantizing one vector", "Order the steps.", ["Take the encoder output vector", "Compute its distance to every codebook row", "Pick the row with the smallest distance", "Record its index", "Pass the row to the decoder"]),
  MATCH("Shapes", "Match each object with its shape.", [("Codebook", "K by D"), ("Encoder output", "Grid of D-vectors"), ("Latent indices", "Grid of integers"), ("Chosen row", "D-vector"), ("Counts", "Length K")]),
  FILL("Quantizer", "The quantizer picks the {{nearest}} codebook vector. The discrete code is its {{index}}. Unused rows waste {{capacity}}.")]))

# 4
CHS.append(CH(
 "The straight-through estimator",
 ("Gradients", [
  "Quantizer | has | Zero gradient almost everywhere",
  "Straight-through | copies | Decoder gradient to encoder",
  "Forward pass | uses | Quantized vector",
  "Backward pass | pretends | Identity",
  "Stop-gradient | blocks | Flow",
  "Encoder | learns | Through copied gradient",
  "Codebook | learns | Through its own loss"]),
 ["Training by gradient descent needs derivatives all the way back. The nearest-neighbour step is a staircase: its derivative is zero almost everywhere, and undefined at the jumps. Gradients from the decoder would never reach the encoder.",
  "The straight-through estimator ignores the staircase in the backward pass. The forward pass uses the quantized vector; the backward pass passes the gradient at z_q straight to z_e as if the quantizer were the identity.",
  "It is a biased approximation but works well in practice. The labs measure the true derivative and train a one-dimensional example with the trick."],
 [("Stop-gradient", "sg[x]: equals x in the forward pass and has zero gradient in the backward pass."),
  ("Straight-through estimator", "Copy the gradient of the quantized output to the unquantized input."),
  ("Staircase function", "A function that is flat between jumps; its derivative is zero almost everywhere."),
  ("Backpropagation", "Computing gradients backwards through the network."),
  ("Bias", "A systematic error of an estimate."),
  ("Identity", "The function f(x) = x with derivative 1.")],
 ["The quantizer's true derivative is zero almost everywhere.",
  "Straight-through: dL/dz_e is set equal to dL/dz_q.",
  "Common implementation: z_q_st = z_e + sg[z_q - z_e]; the value is z_q, the gradient is that of z_e.",
  "The decoder gradient moves the encoder output toward better codes.",
  "The codebook gets no gradient from reconstruction, so it needs its own loss.",
  "The estimate is biased but effective."],
 [T("Consider a one-dimensional codebook with entries at zero, one and two. The quantizer maps any number to the nearest of them. Plot it and you see a staircase: flat at 0 until one half, a jump to 1, flat until three halves, a jump to 2. The slope is zero on every flat part, and the jumps have infinite slope. For gradient descent, this is a disaster."),
  T("If we applied the chain rule honestly, the gradient of the loss with respect to the encoder output would be the decoder's gradient multiplied by the quantizer's slope, which is zero. The encoder would never learn. The paper observes this and proposes a simple fix. Since the encoder output z e and the decoder input z q have the same dimension, copy the gradient from one to the other."),
  M(r"\frac{\partial L}{\partial z_e} \;:=\; \frac{\partial L}{\partial z_q} \qquad\text{(straight-through)}"),
  T("In code the trick is a single line. Write z q st equal to z e plus the stop-gradient of z q minus z e. In the forward pass the two z e terms cancel and the result is exactly z q. In the backward pass the stop-gradient term contributes nothing, and the gradient flows into z e with slope one. Deep learning libraries provide stop-gradient as detach or stop_gradient."),
  T("What does the copied gradient mean? The decoder says: if z q moved in this direction, the reconstruction would be better. The encoder obliges by moving z e in the same direction. Eventually z e crosses a boundary and snaps to a different code. The decoder's wish is passed along to the encoder even though the quantizer is in the way."),
  T("The estimate is biased: it is not the gradient of any real function of the weights. It works because the encoder output and the chosen code are close, thanks to the commitment loss of chapter 5. If they were far apart, the gradient computed at z q would say little about the encoder's output."),
  T("The codebook itself gets no gradient from reconstruction. The decoder's input is a copy, and the straight-through path ends at the encoder. So the codebook learns from separate loss terms, the subject of the next chapter. The labs here measure the derivative of the staircase with a finite difference, copy a gradient and train a toy encoder with the trick.")],
 [("What is the quantizer's derivative almost everywhere?", ["Zero", "One", "Infinity", "Undefined"], 0, "It is a staircase."),
  ("What does the straight-through estimator do?", ["Copies the gradient from z_q to z_e", "Zeroes the gradient", "Doubles the gradient", "Blocks the encoder"], 0, "As if the quantizer were the identity."),
  ("What is stop-gradient?", ["Identity forward, zero gradient backward", "A stopping rule", "Early stopping", "A learning rate"], 0, "sg[x]."),
  ("Does reconstruction train the codebook?", ["No, it needs its own loss", "Yes, directly", "Only the first layer", "Always"], 0, "The gradient ends at the encoder.")],
 [("What is the forward value of z_e + sg[z_q - z_e]?", "z_q."), ("What is its gradient?", "That of z_e."), ("Is the estimator exact?", "No, it is biased."), ("Why is the commitment loss needed?", "To keep z_e near z_q so the copy is meaningful.")],
 [PL("Finite-difference derivative", "A 1-D quantizer maps z to the nearest entry of codebook (a list of numbers, ties to the lower index). Write fd_derivative(z, codebook, h): (q(z + h) - q(z)) / h.",
     "fd_derivative(z, codebook, h)", """
def fd_derivative(z, codebook, h):
    def q(v):
        best = None
        val = 0
        for e in codebook:
            d = (v - e) ** 2
            if best is None or d < best - 1e-12:
                best = d
                val = e
        return val
    return (q(z + h) - q(z)) / h
""", [[0.2, [0, 1, 2], 0.01], [0.49, [0, 1, 2], 0.01], [0.495, [0, 1, 2], 0.01], [1.2, [0, 1, 2], 0.1], [1.45, [0, 1, 2], 0.1]], "Evaluate the quantizer at z and z + h.", approx=1e-9),
  PL("Straight-through gradient", "Write ste_backward(grad_zq): the gradient passed to the encoder output. It is a copy of the list grad_zq.",
     "ste_backward(grad_zq)", """
def ste_backward(grad_zq):
    return list(grad_zq)
""", [[[0.5, -0.5]], [[1]], [[0, 0, 3]], [[]]], "Return the same numbers."),
  PL("Train a toy encoder", "A scalar encoder has z_e = w * x. The codebook is a list of numbers. The decoder is the identity: x_hat = z_q (the nearest codebook entry, ties to the lower index). The loss is (x - z_q)^2. With the straight-through estimator the gradient with respect to w is 2 * (z_q - x) * x. Write ste_train(w, x, codebook, lr, steps): run steps gradient steps and return [final w rounded to 6 decimals, final loss rounded to 6 decimals].",
     "ste_train(w, x, codebook, lr, steps)", """
def ste_train(w, x, codebook, lr, steps):
    def q(v):
        best = None
        val = 0
        for e in codebook:
            d = (v - e) ** 2
            if best is None or d < best - 1e-12:
                best = d
                val = e
        return val
    for t in range(steps):
        zq = q(w * x)
        w = w - lr * 2 * (zq - x) * x
    zq = q(w * x)
    return [round(w, 6), round((x - zq) ** 2, 6)]
""", [[0.1, 1.0, [0, 1, 2], 0.2, 20], [0.5, 2.0, [0, 1, 2], 0.1, 10], [3.0, 1.0, [0, 1, 2], 0.2, 10], [0.0, 1.5, [0, 1, 2, 3], 0.1, 10]], "Quantize w * x, compute the copied gradient, update w."),
  ORDER("Straight-through step", "Order the steps.", ["Forward: encode and quantize", "Decode the quantized vector", "Compute the loss", "Backward: gradient at z_q", "Copy that gradient to z_e"]),
  MATCH("Gradients", "Match each item with its behaviour.", [("Quantizer derivative", "Zero almost everywhere"), ("sg[x]", "Value x, gradient zero"), ("z_e + sg[z_q - z_e]", "Value z_q, gradient of z_e"), ("Codebook", "Needs its own loss"), ("Commitment loss", "Keeps z_e near z_q")]),
  FILL("Trick", "The quantizer has a {{zero}} derivative almost everywhere, so the {{straight-through|straight through}} estimator copies the gradient from z_q to z_e.")]))

# 5
CHS.append(CH(
 "The VQ-VAE loss",
 ("Three terms", [
  "Reconstruction loss | trains | Encoder and decoder",
  "Codebook loss | moves | Codebook toward encoder",
  "Commitment loss | keeps | Encoder near codebook",
  "Stop-gradient | separates | The two roles",
  "Beta | weights | Commitment loss",
  "Beta | set to | 0.25",
  "Total | sums | Three terms"]),
 ["The VQ-VAE loss has three terms. The reconstruction term trains the encoder and decoder; its gradient reaches the encoder by the straight-through path. The codebook term pulls the chosen codebook vector toward the encoder's output. The commitment term pulls the encoder's output toward the chosen vector.",
  "The stop-gradient operator keeps the two pulls apart, so that each only moves one side. A weight beta, 0.25 in the paper's experiments, scales the commitment term; the authors report the results are robust to its value.",
  "The labs compute each term and the gradients that result."],
 [("Codebook loss", "||sg[z_e] - e||^2: moves the codebook vector toward the encoder output."),
  ("Commitment loss", "beta ||z_e - sg[e]||^2: keeps the encoder output close to its codebook vector."),
  ("beta", "The weight of the commitment loss; 0.25 in the paper."),
  ("Stop-gradient", "sg[.]: a constant in the backward pass."),
  ("Embedding space", "The space in which the codebook vectors live."),
  ("Volume growth", "The encoder outputs can grow without bound if not committed.")],
 ["L = ||x - D(z_q)||^2 + ||sg[z_e] - e||^2 + beta ||z_e - sg[e]||^2.",
  "Only the decoder and encoder see the first term (encoder via straight-through).",
  "Only the codebook sees the second term.",
  "Only the encoder sees the third term.",
  "beta was 0.25 in the paper, which found results robust for values from about 0.1 to 2.",
  "The paper's first experiments used the squared error for images and a categorical output for audio."],
 [T("Here is the loss as given in the paper. It has three terms, and each trains a different group of parameters."),
  M(r"L \;=\; \log p\bigl(x \mid z_q(x)\bigr) \;+\; \bigl\lVert \mathrm{sg}[z_e(x)] - e \bigr\rVert_2^2 \;+\; \beta\,\bigl\lVert z_e(x) - \mathrm{sg}[e] \bigr\rVert_2^2"),
  T("The first term is the reconstruction. In the paper's formula it is a log likelihood that, for a Gaussian output, is the squared error between the input and the decoder output, up to constants. It trains the decoder directly. It reaches the encoder only through the straight-through copy. It does not touch the codebook."),
  T("The second term is the codebook loss, also called the vector quantisation objective. It measures the distance between the encoder output and the chosen codebook vector, with a stop-gradient on the encoder output. Only the codebook vector e moves. It moves toward the encoder output. It is the same as one step of k-means: the centre moves to the data point."),
  T("The third term is the commitment loss. It has the same distance but with the stop-gradient on the codebook vector instead, so only the encoder moves, toward its chosen vector. Why is it needed? The codebook vectors only move as fast as their loss allows. Without a constraint the encoder outputs could grow in magnitude and jump between codes without ever settling. The commitment loss makes the encoder stay close."),
  T("The paper gives the weight beta of this term as robust: it reports that results did not change much for beta between 0.1 and 2.0, and used 0.25 in all experiments. The squared distance between the encoder output and the code is exactly the quantization error."),
  T("Be careful with a detail. Many implementations use means over elements rather than sums, so the numbers differ by a constant factor, and some swap which term carries beta. The labs use the mean squared error for each of the three, matching common code. Next you compute them and the matching gradients.")],
 [("Which term moves the codebook?", ["The codebook loss", "The commitment loss", "The reconstruction loss", "None"], 0, "||sg[z_e] - e||^2."),
  ("What does the commitment loss do?", ["Keeps the encoder output near its code", "Trains the decoder", "Sets K", "Adds noise"], 0, "It moves only the encoder."),
  ("What value of beta did the paper use?", ["0.25", "10", "0", "100"], 0, "Robust between about 0.1 and 2."),
  ("What does stop-gradient do in the loss?", ["Selects which side moves", "Stops training", "Rounds numbers", "Doubles loss"], 0, "It separates the roles.")],
 [("What reaches the encoder?", "Reconstruction (via straight-through) and commitment."), ("What reaches the codebook?", "Only the codebook loss."), ("Why commit?", "To stop encoder outputs growing and flipping."), ("What is the second term like?", "A k-means update.")],
 [PL("Loss terms", "Write vq_losses(x, xhat, ze, e, beta): return [recon, codebook, commit, total] where recon is the mean squared error between x and xhat, codebook is the mean squared difference between ze and e (the value of ||sg[ze] - e||^2 averaged over elements), commit is beta times the same mean, and total is their sum. Round each to 6 decimals.",
     "vq_losses(x, xhat, ze, e, beta)", """
def vq_losses(x, xhat, ze, e, beta):
    recon = sum((a - b) ** 2 for a, b in zip(x, xhat)) / len(x)
    cb = sum((a - b) ** 2 for a, b in zip(ze, e)) / len(ze)
    commit = beta * cb
    total = recon + cb + commit
    return [round(recon, 6), round(cb, 6), round(commit, 6), round(total, 6)]
""", [[[1, 2], [1, 2], [0.5, 0.5], [0.5, 0.5], 0.25], [[1, 0], [0, 0], [1, 1], [0, 0], 0.25], [[0.5], [0.0], [2.0], [1.0], 1.0], [[1, 1, 1], [0, 1, 2], [0, 0], [3, 4], 0.25]], "Three means; the commitment loss is beta times the codebook distance."),
  PL("Codebook gradient", "The codebook loss is the sum over elements of (ze - e)^2 with ze held constant. Write codebook_grad(ze, e): the gradient with respect to e, that is 2 * (e_i - ze_i) for each element.",
     "codebook_grad(ze, e)", """
def codebook_grad(ze, e):
    return [2 * (b - a) for a, b in zip(ze, e)]
""", [[[1, 2], [0, 0]], [[0.5, 0.5], [0.5, 0.5]], [[3], [1]], [[0, -1, 2], [1, 1, 1]]], "Differentiate (ze - e)^2 with respect to e."),
  PL("Commitment gradient", "The commitment loss is beta times the sum over elements of (ze - e)^2 with e held constant. Write commit_grad(ze, e, beta): the gradient with respect to ze, 2 * beta * (ze_i - e_i).",
     "commit_grad(ze, e, beta)", """
def commit_grad(ze, e, beta):
    return [2 * beta * (a - b) for a, b in zip(ze, e)]
""", [[[1, 2], [0, 0], 0.25], [[0.5], [0.5], 0.25], [[3, 3], [1, 5], 1.0]], "Differentiate with respect to ze this time.", approx=1e-12),
  PL("Move the code", "A single SGD step on the codebook loss moves e toward ze. Write codebook_step(ze, e, lr): return the new e (rounded to 6 decimals each), e - lr * 2 * (e - ze) for each element.",
     "codebook_step(ze, e, lr)", """
def codebook_step(ze, e, lr):
    return [round(b - lr * 2 * (b - a), 6) for a, b in zip(ze, e)]
""", [[[1.0, 1.0], [0.0, 0.0], 0.25], [[1.0], [0.0], 0.5], [[2.0, -2.0], [0.0, 0.0], 0.1]], "Subtract the gradient times the learning rate."),
  ORDER("The three pulls", "Order the story of one step.", ["Decoder error moves the decoder and, through the copy, the encoder", "The codebook vector moves toward the encoder output", "The encoder output moves toward its code", "Both sides get closer", "The next batch starts"]),
  MATCH("Terms", "Match each term with who moves.", [("Reconstruction", "Decoder and encoder"), ("Codebook loss", "Codebook vector"), ("Commitment loss", "Encoder"), ("beta", "Weight of commitment"), ("sg", "Blocks one side's gradient")]),
  FILL("Loss", "The {{codebook}} loss moves the code toward the encoder output; the {{commitment}} loss moves the encoder toward the code. The paper used beta equal to {{0.25}}.")]))

# 6
CHS.append(CH(
 "Learning the codebook: k-means, EMA and dead codes",
 ("Codebook learning", [
  "Codebook update | resembles | K-means",
  "EMA | smooths | Cluster statistics",
  "Dead code | is | Never chosen",
  "Reinitialisation | revives | Dead codes",
  "Decay | sets | Memory of EMA",
  "Counts | track | Code usage",
  "Laplace smoothing | avoids | Division by zero"]),
 ["Updating the codebook entry toward the vectors assigned to it is the k-means algorithm. The VQ-VAE codebook loss does this by gradient descent. The paper's appendix describes an alternative with exponential moving averages: keep a running count and sum for each code and set the code to their ratio.",
  "A frequent failure is the dead code: an entry that is never nearest to anything, so it never moves. Typical repairs replace dead entries with encoder outputs from the batch.",
  "The labs write a k-means step, an EMA update and a dead-code repair."],
 [("K-means", "Alternate assigning points to the nearest centre and moving each centre to the mean of its points."),
  ("EMA", "Exponential moving average: new = decay * old + (1 - decay) * observation."),
  ("Dead code", "A codebook entry that no encoder output is nearest to."),
  ("Reinitialisation", "Replacing a dead code by a vector from the data."),
  ("Decay", "The EMA memory, for example 0.99."),
  ("Cluster size", "The running count of vectors assigned to a code.")],
 ["The codebook loss is a gradient-descent form of k-means.",
  "EMA update: N_i = g N_i + (1 - g) n_i; m_i = g m_i + (1 - g) sum of assigned z; e_i = m_i / N_i.",
  "The paper's appendix suggests decay 0.99 for the EMA variant.",
  "Dead codes never receive updates and waste capacity.",
  "Fixes: reinitialise from data, lower codebook dimension, or normalise.",
  "The EMA variant needs no codebook gradient and is often steadier."],
 [T("Look again at the codebook loss. For one code, summed over the vectors assigned to it, it is a sum of squared distances. Minimizing it by moving the code gives the average of the assigned vectors. That is exactly the update of k-means, an old and well-understood clustering method: assign every point to the nearest centre, then move each centre to the mean of its points."),
  T("So the VQ-VAE codebook is a set of k-means centres in the encoder's output space, with the twist that the encoder is also moving. The assignments change as the encoder learns, and the centres chase them."),
  T("The paper's appendix suggests replacing gradient descent on the codebook by an exponential moving average. Keep for each code two running quantities: a count of the vectors assigned to it, and the sum of those vectors. After each batch, multiply the old values by a decay close to one and add the batch's contributions with the remaining weight. The code is the running sum divided by the running count."),
  M(r"N_i \leftarrow \gamma N_i + (1-\gamma)\, n_i, \qquad m_i \leftarrow \gamma m_i + (1-\gamma) \sum_j z_{i,j}, \qquad e_i \leftarrow \frac{m_i}{N_i}"),
  T("Here n i is the number of encoder outputs in this batch assigned to code i, the z i j are those outputs, and gamma is the decay. Gamma of 0.99 is the value suggested in the paper. This version has no learning rate for the codebook, and removes the codebook loss from the objective, leaving reconstruction and commitment."),
  T("The failure mode is the dead code. A code that is not the nearest to any output gets no updates. With the EMA, its count decays toward zero, and it never recovers. The more codes die, the fewer values the grid can really use, and the reconstruction suffers. Repairs include periodically replacing codes whose usage is under a threshold with vectors taken from the current batch, a trick used by later work."),
  T("In the practice section you write a k-means step, the EMA step on two-dimensional vectors, a dead-code detector and a repair that copies batch vectors.")],
 [("What does a k-means step do?", ["Assigns points then moves centres to the means", "Adds noise", "Trains a decoder", "Halves K"], 0, "Two alternating steps."),
  ("What is a dead code?", ["Never the nearest to any output", "Too large", "A duplicate", "A zero vector"], 0, "It never gets updated."),
  ("What does the EMA decay control?", ["How long the memory is", "The codebook size", "The loss weight", "The batch size"], 0, "gamma close to 1 remembers more."),
  ("What does the codebook loss resemble?", ["K-means", "Dropout", "Attention", "Softmax"], 0, "Centres move to the data.")],
 [("What is e_i in EMA?", "Running sum divided by running count."), ("What decay did the paper suggest?", "0.99."), ("How to fix dead codes?", "Reinitialise from data."), ("Why no codebook loss in EMA?", "The codebook is updated directly.")],
 [PL("K-means step", "Write kmeans_step(points, centers): assign each point (list of numbers) to the nearest centre (squared distance, ties to the lower index) and return the new centres, each the mean of its assigned points, rounded to 6 decimals (a centre with no points stays unchanged).",
     "kmeans_step(points, centers)", """
def kmeans_step(points, centers):
    k = len(centers)
    d = len(centers[0])
    sums = [[0.0] * d for i in range(k)]
    cnt = [0] * k
    for p in points:
        best = None
        arg = 0
        for i in range(k):
            dist = sum((a - b) ** 2 for a, b in zip(p, centers[i]))
            if best is None or dist < best - 1e-12:
                best = dist
                arg = i
        cnt[arg] += 1
        for j in range(d):
            sums[arg][j] += p[j]
    out = []
    for i in range(k):
        if cnt[i] == 0:
            out.append(list(centers[i]))
        else:
            out.append([round(s / cnt[i], 6) for s in sums[i]])
    return out
""", [[[[0, 0], [0, 2], [10, 10], [10, 12]], [[0, 0], [10, 10]]], [[[1], [2], [3]], [[0], [100]]], [[[0, 0], [1, 1]], [[0, 0], [1, 1], [5, 5]]], [[[2, 2], [4, 4]], [[3, 3]]]], "Accumulate sums and counts per centre, then divide."),
  PL("EMA update", "Write ema_step(N, m, zs, idx, gamma): N is the list of running counts, m the list of running sums (each a 2-vector), zs the batch of 2-vectors, idx their assigned codes. Return the new codebook (each e_i = m_i / N_i, rounded to 6 decimals) after updating N_i = gamma N_i + (1 - gamma) n_i and m_i = gamma m_i + (1 - gamma) sum of its assigned z.",
     "ema_step(N, m, zs, idx, gamma)", """
def ema_step(N, m, zs, idx, gamma):
    k = len(N)
    n = [0] * k
    s = [[0.0, 0.0] for i in range(k)]
    for z, i in zip(zs, idx):
        n[i] += 1
        s[i][0] += z[0]
        s[i][1] += z[1]
    book = []
    for i in range(k):
        Ni = gamma * N[i] + (1 - gamma) * n[i]
        mi = [gamma * m[i][0] + (1 - gamma) * s[i][0], gamma * m[i][1] + (1 - gamma) * s[i][1]]
        book.append([round(mi[0] / Ni, 6), round(mi[1] / Ni, 6)])
    return book
""", [[[1.0, 1.0], [[0.0, 0.0], [5.0, 5.0]], [[1, 1], [6, 4]], [0, 1], 0.9], [[1.0, 1.0], [[1.0, 1.0], [2.0, 2.0]], [[3, 3]], [0], 0.5], [[2.0], [[2.0, 4.0]], [[1, 1], [3, 3]], [0, 0], 0.99]], "Update the counts and sums, then divide."),
  PL("Find dead codes", "Write dead_codes(counts, threshold): the indices of codes whose count is at most the threshold.",
     "dead_codes(counts, threshold)", """
def dead_codes(counts, threshold):
    return [i for i in range(len(counts)) if counts[i] <= threshold]
""", [[[5, 0, 3, 0], 0], [[5, 1, 3, 0], 1], [[9, 9], 0], [[], 0]], "Compare each count with the threshold."),
  PL("Revive them", "Write revive(codebook, dead, batch): replace the dead codes in order by the batch vectors in order (the first dead code gets batch[0], the next batch[1], wrapping around if there are more dead codes than batch vectors). Return the new codebook.",
     "revive(codebook, dead, batch)", """
def revive(codebook, dead, batch):
    new = [list(c) for c in codebook]
    for j in range(len(dead)):
        new[dead[j]] = list(batch[j % len(batch)])
    return new
""", [[[[0, 0], [1, 1], [2, 2]], [1], [[9, 9]]], [[[0, 0], [1, 1], [2, 2]], [0, 2], [[7, 7], [8, 8]]], [[[0, 0], [1, 1]], [], [[5, 5]]], [[[0], [1], [2]], [0, 1, 2], [[4], [5]]]], "Copy the codebook and overwrite the dead rows."),
  ORDER("EMA codebook update", "Order the steps.", ["Assign each encoder output to its nearest code", "Count the outputs per code", "Sum the outputs per code", "Update running counts and sums with the decay", "Set each code to the sum divided by the count"]),
  MATCH("Ideas", "Match each idea with its effect.", [("K-means", "Centres move to means"), ("EMA", "Running averages of statistics"), ("Dead code", "Never used"), ("Revive", "Copy a batch vector"), ("gamma", "Decay of the EMA")]),
  FILL("Codebook", "The codebook loss is like {{k-means|kmeans|k means}}. An {{EMA|exponential moving average}} update uses a decay such as {{0.99}}.")]))

# 7
CHS.append(CH(
 "Information: rate, perplexity and usage",
 ("Measuring codes", [
  "Entropy | measures | Information per code",
  "Perplexity | is | Exponential of entropy",
  "Perplexity | counts | Effective codes in use",
  "Rate | is | Bits per latent",
  "Uniform usage | maximizes | Perplexity",
  "Low perplexity | signals | Collapse",
  "Bits | bound | Compression"]),
 ["How many of the K codes does a trained model really use? Entropy and perplexity give the answer. Entropy measures the average information per code in bits. Perplexity, two to the power of the entropy, is the effective number of equally likely codes.",
  "If all K codes are used equally, perplexity is K. If one code takes everything, it is 1. Perplexity is tracked in many VQ-VAE implementations as a health check on the codebook.",
  "The labs compute entropy, perplexity and the fraction of the codebook in use."],
 [("Entropy", "The average information of a distribution: minus the sum of p log p."),
  ("Perplexity", "2 to the entropy in bits (or e to the entropy in nats); the effective number of codes."),
  ("Rate", "The number of bits needed to send the code."),
  ("Distribution of usage", "The fraction of positions assigned to each code."),
  ("Effective codebook size", "The perplexity of the usage distribution."),
  ("Codebook utilisation", "The fraction of codes ever used.")],
 ["H = -sum p_i log2 p_i bits; perplexity = 2^H.",
  "Uniform usage over K codes: H = log2 K and perplexity = K.",
  "One code used: H = 0 and perplexity = 1.",
  "A model with perplexity far below K is wasting its codebook.",
  "The fraction of unused codes is another simple diagnostic.",
  "Rate is bounded by log2 K per position; the prior can code the indices in fewer bits."],
 [T("Imagine two codebooks of 512 entries. In the first, every entry is used about equally often. In the second, ten entries are used all the time and the rest almost never. Both can be called codebooks of 512, but the second behaves like a codebook of ten. A single number should tell them apart."),
  T("Take the usage distribution: the fraction p i of grid positions assigned to code i over a large sample. The entropy of this distribution is the average number of bits needed to name a code if you design the best possible binary code for it. Perplexity is two to that power."),
  M(r"H \;=\; -\sum_{i} p_i \log_2 p_i, \qquad \mathrm{PPL} \;=\; 2^{H}"),
  T("For a uniform distribution over K codes the entropy is log base two of K and the perplexity is K. For a distribution concentrated on one code, the entropy is zero and the perplexity is one. In between, perplexity reads as the number of equally popular codes that would give the same entropy. Implementations often use natural logarithms; the perplexity is the same."),
  T("This gives a health check. During training, log the perplexity of the codes used in each batch. If it rises toward K, the codebook is in good use. If it sinks toward a small number, codes are dying out. Many public implementations print exactly this number during training."),
  T("There is a link to compression. The raw rate of the grid is log base two of K bits per position. If the usage is uneven, the entropy is lower than that, so an entropy coder or a good prior could encode the grid in fewer bits. A prior that models the dependence between neighbouring positions can go lower still, which is how chapter 8 uses the grid."),
  T("The labs compute entropy and perplexity from counts, the utilisation fraction, and the rate in bits for a whole grid.")],
 [("What is perplexity here?", ["2 to the entropy of code usage", "The loss", "The codebook size", "The number of epochs"], 0, "The effective number of codes."),
  ("What is perplexity for uniform usage of K codes?", ["K", "1", "log K", "0"], 0, "Entropy is log2 K."),
  ("What does low perplexity signal?", ["Wasted codebook", "A good model", "Fast training", "A big decoder"], 0, "Few codes in use."),
  ("What is the entropy of one code used always?", ["0", "1", "K", "Undefined"], 0, "No uncertainty.")],
 [("How are probabilities found?", "Counts divided by their total."), ("Is perplexity at most K?", "Yes."), ("Why monitor it?", "It reveals codebook collapse."), ("What is the rate of the grid?", "Positions times log2 K bits.")],
 [PL("Entropy in bits", "Write entropy_bits(counts): the entropy in bits of the distribution given by the counts (ignore zero counts). Use import math.",
     "entropy_bits(counts)", """
import math
def entropy_bits(counts):
    total = sum(counts)
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log(p, 2)
    return h
""", [[[1, 1]], [[4, 0, 0, 0]], [[1, 1, 1, 1]], [[3, 1]], [[10, 10, 10, 10, 10, 10, 10, 10]]], "Use p log2 p and skip zero counts.", approx=1e-9),
  PL("Perplexity", "Write perplexity(counts): 2 raised to the entropy in bits of the counts. Use import math.",
     "perplexity(counts)", """
import math
def perplexity(counts):
    total = sum(counts)
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log(p, 2)
    return 2 ** h
""", [[[1, 1]], [[5, 0, 0]], [[1, 1, 1, 1]], [[9, 1]], [[100, 100, 100]]], "Compute entropy then exponentiate.", approx=1e-9),
  PL("Utilisation", "Write utilisation(counts): the fraction of codes with a count above zero.",
     "utilisation(counts)", """
def utilisation(counts):
    used = 0
    for c in counts:
        if c > 0:
            used += 1
    return used / len(counts)
""", [[[3, 0, 1, 0]], [[1, 1]], [[0, 0, 5]], [[7]]], "Count the used entries.", approx=1e-12),
  PL("Raw rate of a grid", "Write grid_bits(gh, gw, k): the raw number of bits in a gh by gw grid of codes from k choices, with bits per code rounded up to a whole number.",
     "grid_bits(gh, gw, k)", """
def grid_bits(gh, gw, k):
    b = 0
    while 2 ** b < k:
        b += 1
    return gh * gw * b
""", [[32, 32, 512], [8, 8, 64], [1, 1, 2], [16, 16, 1000]], "Positions times bits per code."),
  ORDER("Reading usage", "Order the steps to compute perplexity.", ["Count how often each code is used", "Divide by the total to get probabilities", "Compute the entropy", "Exponentiate in base 2", "Compare the result with K"]),
  MATCH("Numbers", "Match each case with its perplexity.", [("Uniform over 8 codes", "8"), ("One code only", "1"), ("Two codes equally", "2"), ("Four codes equally", "4"), ("Uniform over 512", "512")]),
  FILL("Usage", "Perplexity is two to the {{entropy}} of the code usage. A low perplexity signals a wasted {{codebook}}.")]))

# 8
CHS.append(CH(
 "The prior: generating with PixelCNN",
 ("Generation", [
  "Prior | models | Distribution of codes",
  "Autoregressive prior | factorizes | Joint into conditionals",
  "PixelCNN | models | Image code grids",
  "WaveNet | models | Audio codes",
  "Raster order | flattens | The grid",
  "Sampling | draws | One code at a time",
  "Decoder | turns | Codes into data"]),
 ["Training the autoencoder gives codes but not new data. To generate we need a model of which grids of codes are likely: a prior. The VQ-VAE paper trains an autoregressive prior after the autoencoder is fixed.",
  "An autoregressive model predicts each code from the ones before it in a fixed order, such as raster order for an image grid. Sampling goes one code at a time, then the decoder turns the grid into an image. For audio the paper uses a WaveNet.",
  "The labs build a tiny autoregressive prior, a bigram model on code sequences, with training, scoring and sampling."],
 [("Prior", "A model of the probability of code grids."),
  ("Autoregressive", "Predicting each element given the earlier ones."),
  ("Raster order", "Reading a grid row by row, left to right."),
  ("PixelCNN", "An autoregressive convolutional network for images."),
  ("WaveNet", "An autoregressive convolutional network for audio."),
  ("Negative log likelihood", "Minus the log probability of the data; the training loss of a prior.")],
 ["p(z) = product of p(z_t | z_1 ... z_(t-1)) over the codes in raster order.",
  "The paper used PixelCNN for images and WaveNet for audio.",
  "In training the prior, the autoencoder is frozen.",
  "Sampling: draw a code, append, repeat; then decode.",
  "The paper's ImageNet latents are 32 by 32 grids; the prior models these 1,024 positions.",
  "Because the prior is over a small grid, it is far cheaper than a PixelCNN on pixels."],
 [T("After training, a VQ-VAE can compress and reconstruct. To make new images we also need to know which code grids are plausible. The autoencoder says nothing about that. The paper therefore separates the work into two stages: first train the encoder, codebook and decoder; then, with them frozen, train a prior over the grids of indices."),
  M(r"p(z) \;=\; \prod_{t=1}^{T} p\bigl(z_t \mid z_1, \dots, z_{t-1}\bigr)"),
  T("An autoregressive model chooses an order for the positions and predicts each from the earlier ones. For an image grid, the natural order is raster scan: left to right in each row, rows from top to bottom. The paper uses PixelCNN, a convolutional network with masks so that each position sees only the earlier ones, for images, and WaveNet for audio."),
  T("Why is this a good division of labour? A PixelCNN on raw pixels must spend its capacity on fine detail. The VQ-VAE already took care of detail, compressing a 128 by 128 image to a 32 by 32 grid. The prior has to model only 1,024 positions each with 512 choices, and focuses on the large-scale structure of the picture. The paper reports that this gives samples of good quality at a lower cost."),
  T("Sampling goes step by step. Ask the prior for the distribution over the first code, draw one, then ask for the second given the first, draw, and so on to the end of the grid. Then look up each index in the codebook and run the decoder. The only randomness is in the draws."),
  T("In the practice section we use the simplest possible autoregressive model, a bigram model in which each code depends only on the previous one. It is far weaker than PixelCNN, yet everything else is the same: a conditional table, a likelihood to score sequences and a sampling loop."),
  T("The labs flatten a grid in raster order, estimate a smoothed bigram table, score a sequence and sample from the table with given random numbers.")],
 [("What does the prior model?", ["Distributions over code grids", "Pixels directly", "The decoder weights", "The loss"], 0, "It makes generation possible."),
  ("Which order is used for an image grid?", ["Raster order", "Random", "Diagonal only", "Spiral"], 0, "Row by row."),
  ("Why train the prior on codes rather than pixels?", ["The grid is much smaller", "Pixels are discrete", "Codes are colours", "It is required by law"], 0, "A 32 by 32 grid instead of 128 by 128 pixels."),
  ("What does sampling need?", ["Random draws one code at a time", "A single draw for the whole image", "No randomness", "The input image"], 0, "Then decode.")],
 [("Which networks did the paper use?", "PixelCNN for images and WaveNet for audio."), ("Is the autoencoder frozen?", "Yes, during prior training."), ("What is a bigram model?", "Each element depends on the previous one."), ("What is NLL?", "Minus log likelihood.")],
 [PL("Raster order", "Write raster(grid): the list of the entries of the grid (a list of rows) read row by row from top to bottom.",
     "raster(grid)", """
def raster(grid):
    out = []
    for row in grid:
        for v in row:
            out.append(v)
    return out
""", [[[[1, 2], [3, 4]]], [[[5]]], [[[0, 1, 2], [3, 4, 5]]], [[]]], "Nested loops."),
  PL("Bigram prior", "Write train_bigram(seqs, k, alpha): estimate a k by k table T where T[a][b] is the smoothed probability that code b follows code a: (count(a then b) + alpha) / (count(a followed by anything) + alpha * k). Count all adjacent pairs in all the sequences. Round each entry to 6 decimals.",
     "train_bigram(seqs, k, alpha)", """
def train_bigram(seqs, k, alpha):
    c = [[0] * k for i in range(k)]
    for s in seqs:
        for a, b in zip(s[:-1], s[1:]):
            c[a][b] += 1
    T = []
    for a in range(k):
        tot = sum(c[a]) + alpha * k
        T.append([round((c[a][b] + alpha) / tot, 6) for b in range(k)])
    return T
""", [[[[0, 1, 0, 1]], 2, 1.0], [[[0, 0, 1], [1, 1, 0]], 2, 0.5], [[[2, 1, 0, 2]], 3, 1.0], [[[0]], 2, 1.0]], "Count pairs, then add alpha and normalize each row."),
  PL("Score a sequence", "Write sequence_nll(seq, T): the negative natural log likelihood of the code sequence, taking the first code to have probability 1/k and each next code the table probability T[prev][cur]. Use import math.",
     "sequence_nll(seq, T)", """
import math
def sequence_nll(seq, T):
    k = len(T)
    total = -math.log(1.0 / k)
    for a, b in zip(seq[:-1], seq[1:]):
        total -= math.log(T[a][b])
    return total
""", [[[0, 1, 0, 1], [[0.25, 0.75], [0.75, 0.25]]], [[0, 0, 0], [[0.9, 0.1], [0.5, 0.5]]], [[1], [[0.5, 0.5], [0.5, 0.5]]], [[0, 1, 2], [[0.2, 0.5, 0.3], [0.1, 0.1, 0.8], [0.3, 0.3, 0.4]]]], "Add up -log of each factor.", approx=1e-9),
  PL("Sample from the prior", "Write generate(T, first, us): start with the code first, and for each uniform number u in us choose the next code from the row of the current code by the cumulative rule (the first code whose cumulative probability exceeds u, the last code otherwise). Return the whole list of codes.",
     "generate(T, first, us)", """
def generate(T, first, us):
    out = [first]
    for u in us:
        row = T[out[-1]]
        total = 0.0
        pick = len(row) - 1
        for j in range(len(row)):
            total += row[j]
            if total > u:
                pick = j
                break
        out.append(pick)
    return out
""", [[[[0.9, 0.1], [0.2, 0.8]], 0, [0.5, 0.95, 0.1]], [[[0.5, 0.5], [0.5, 0.5]], 1, [0.3, 0.7]], [[[0.1, 0.2, 0.7], [0.3, 0.3, 0.4], [0.0, 1.0, 0.0]], 0, [0.9, 0.5, 0.99, 0.2]], [[[1.0]], 0, [0.5, 0.5]]], "Walk along the cumulative sum of the current row."),
  ORDER("Generation", "Order the steps.", ["Train the autoencoder", "Freeze it and encode the data to code grids", "Train the autoregressive prior on the grids", "Sample a new grid from the prior", "Look up the codes and decode"]),
  MATCH("Models", "Match each model with its job.", [("PixelCNN", "Prior over image code grids"), ("WaveNet", "Prior over audio codes"), ("Encoder", "Produces continuous vectors"), ("Decoder", "Turns codes into data"), ("Bigram", "Each code depends on the previous one")]),
  FILL("Prior", "An {{autoregressive}} prior predicts each code from the earlier ones in {{raster}} order. The autoencoder is {{frozen}} during prior training.")]))

# 9
CHS.append(CH(
 "Extensions: hierarchies, residual and product codes",
 ("Beyond the basics", [
  "VQ-VAE-2 | uses | Hierarchy of codes",
  "Residual quantization | stacks | Quantizers",
  "Product quantization | splits | Vector into parts",
  "Larger capacity | needs | More codes or levels",
  "Applications | include | Images, audio, speech",
  "Prior | works on | Compressed codes",
  "Discrete tokens | feed | Transformers"]),
 ["The VQ-VAE idea has been extended in many directions. VQ-VAE-2 uses a hierarchy: a coarse top-level code grid for global structure and finer codes conditioned on it. Residual quantization uses several codebooks in a row, each coding what the previous ones missed. Product quantization splits a vector into parts and quantizes each part with its own small codebook.",
  "All of these raise the capacity of the code: with several levels or parts, the number of distinct combinations multiplies, while each codebook stays small.",
  "These extensions are background knowledge in this course, beyond the original paper. The labs implement residual and product quantization."],
 [("VQ-VAE-2", "A 2019 hierarchical extension by Razavi, van den Oord and Vinyals."),
  ("Hierarchical codes", "Several grids of codes at different resolutions."),
  ("Residual quantization", "Quantize, subtract the result, then quantize the remainder with the next codebook."),
  ("Product quantization", "Split a vector into pieces and quantize each piece separately."),
  ("Capacity", "How many distinct vectors the code can represent."),
  ("Token", "A discrete symbol fed to a sequence model.")],
 ["Capacity of m codebooks of K entries each is K^m with residual or product quantization.",
  "Residual: z_q = e1[k1] + e2[k2] + ..., where each k is chosen on the remainder.",
  "Product: split z into parts and quantize each part with its own codebook.",
  "VQ-VAE-2 (Razavi et al., 2019) used a top and bottom level of codes with PixelCNN priors.",
  "Later systems for images (such as VQGAN), music (Jukebox) and audio codecs (such as SoundStream) build on discrete codes; this is background, not from the 2017 paper.",
  "Discrete tokens let Transformers do generation over images and audio."],
 [T("The original model uses one grid of one codebook. That works, but images contain details at many scales: global layout, objects, textures. A single coarse grid has to hold everything. A natural extension is to use more than one level of codes."),
  T("VQ-VAE-2, by Ali Razavi, Aaron van den Oord and Oriol Vinyals in 2019, uses a hierarchy. A top level of codes on a small grid captures global structure. A bottom level on a larger grid captures the details left over, conditioned on the top. Separate autoregressive priors are trained for each level. This detail is background knowledge: it is outside the 2017 paper that this course follows."),
  T("Another route to more capacity is residual quantization. Quantize the vector with the first codebook, subtract the chosen entry, and quantize the remainder with the second codebook, and so on. The final approximation is the sum of the chosen entries. With m codebooks of K entries, you can express K to the m different vectors while storing only m times K entries. Audio codecs such as SoundStream use this idea, again as background knowledge."),
  M(r"z \;\approx\; e^{(1)}_{k_1} + e^{(2)}_{k_2} + \dots + e^{(m)}_{k_m}, \qquad r_1 = z - e^{(1)}_{k_1},\ \ k_2 = \mathrm{nearest}\bigl(r_1\bigr),\ \dots"),
  T("A third route is product quantization. Cut the vector into m pieces. Quantize each piece independently with its own small codebook. The code is the tuple of m indices. The capacity is again K to the m. Unlike residual quantization, the pieces are quantized independently, so the search is parallel."),
  T("Why does this matter? Discrete codes turn images and audio into token sequences, the kind of data that Transformers handle well. Systems such as VQGAN for images and Jukebox for music use VQ-VAE-like tokenizers followed by autoregressive models. These are later developments I mention for orientation."),
  T("The labs implement residual quantization and product quantization on small vectors, and count capacity.")],
 [("What does residual quantization quantize in stage 2?", ["The remainder after stage 1", "The original vector again", "The codebook", "Noise"], 0, "Subtract and repeat."),
  ("How many vectors can m codebooks of K entries express?", ["K^m", "K*m", "m^K", "K+m"], 0, "Tuples of indices."),
  ("What does product quantization do?", ["Quantizes parts separately", "Multiplies vectors", "Prunes the codebook", "Trains a prior"], 0, "Split, then quantize each piece."),
  ("Who wrote VQ-VAE-2?", ["Razavi, van den Oord and Vinyals", "Vaswani", "Kingma", "Goodfellow"], 0, "2019.")],
 [("What does the top level of VQ-VAE-2 hold?", "Global structure."), ("What do residual levels hold?", "What earlier levels missed."), ("Why discrete tokens?", "They suit sequence models."), ("Is this in the 2017 paper?", "No, it is later work.")],
 [PL("Residual quantization", "Write residual_quantize(z, books): books is a list of codebooks (each a list of vectors). For each in order, pick the nearest entry to the current remainder (ties to the lower index), record its index and subtract it. Return [list of indices, final remainder rounded to 6 decimals].",
     "residual_quantize(z, books)", """
def residual_quantize(z, books):
    r = list(z)
    idx = []
    for book in books:
        best = None
        arg = 0
        for i in range(len(book)):
            d = sum((a - b) ** 2 for a, b in zip(r, book[i]))
            if best is None or d < best - 1e-12:
                best = d
                arg = i
        idx.append(arg)
        r = [a - b for a, b in zip(r, book[arg])]
    return [idx, [round(x, 6) for x in r]]
""", [[[1.5, 1.5], [[[0, 0], [1, 1], [2, 2]], [[0, 0], [0.5, 0.5]]]], [[3.0], [[[0], [2]], [[0], [1]]]], [[0.2, 0.2], [[[0, 0]], [[0, 0]]]], [[2.2, -1.1], [[[2, -1], [0, 0]], [[0.2, -0.1], [0, 0]]]]], "Subtract the chosen entry before moving to the next book."),
  PL("Product quantization", "Write product_quantize(z, books): z is split into len(books) equal parts; part j is quantized with books[j] (a list of vectors of the part length; nearest by squared distance, ties to the lower index). Return the list of indices.",
     "product_quantize(z, books)", """
def product_quantize(z, books):
    m = len(books)
    n = len(z) // m
    idx = []
    for j in range(m):
        part = z[j * n:(j + 1) * n]
        best = None
        arg = 0
        for i in range(len(books[j])):
            d = sum((a - b) ** 2 for a, b in zip(part, books[j][i]))
            if best is None or d < best - 1e-12:
                best = d
                arg = i
        idx.append(arg)
    return idx
""", [[[0.1, 0.9, 2.0, 0.0], [[[0, 0], [0, 1]], [[2, 0], [0, 2]]]], [[1, 1], [[[0], [1]], [[0], [2]]]], [[5, 5, 5, 5, 5, 5], [[[5, 5]], [[5, 5], [0, 0]], [[0, 0], [5, 5]]]]], "Slice z into equal pieces and search each book."),
  PL("Capacity", "Write capacity(k, m): the number of distinct code combinations of m codebooks with k entries each.",
     "capacity(k, m)", """
def capacity(k, m):
    return k ** m
""", [[512, 1], [512, 2], [16, 4], [2, 10]], "k to the m."),
  ORDER("Residual quantization", "Order the steps.", ["Quantize the vector with codebook 1", "Subtract the chosen entry", "Quantize the remainder with codebook 2", "Repeat for each codebook", "Sum the chosen entries for the approximation"]),
  MATCH("Extensions", "Match each method with its idea.", [("VQ-VAE-2", "Top and bottom code grids"), ("Residual quantization", "Quantize what is left"), ("Product quantization", "Quantize parts separately"), ("Prior", "Models the code grid"), ("Tokens", "Input for sequence models")]),
  FILL("Capacity", "Residual quantization quantizes the {{remainder|residual}}. With m codebooks of K entries the capacity is K to the {{m}}.")]))

# 10
CHS.append(CH(
 "Problems, comparisons and where it stands",
 ("Critique", [
  "Codebook collapse | wastes | Capacity",
  "Straight-through | is | Biased",
  "VAE | uses | Continuous latents",
  "GAN | needs | No encoder",
  "Prior | is | Trained separately",
  "Reconstruction | can be | Blurry",
  "Later tokenizers | improve | Codebook use"]),
 ["VQ-VAE solved posterior collapse and gave a clean way to learn discrete representations, but it has its own weak points. Codebook collapse leaves most codes unused. The straight-through gradient is a biased approximation. The two-stage training means the prior never influences the codes.",
  "Compared with a standard VAE, the latent is discrete and the prior is learned. Compared with a GAN, VQ-VAE has an explicit encoder and likelihood-based training, but its reconstructions can be blurry, a reason later work added adversarial and perceptual losses.",
  "The labs finish with diagnostic tools: a collapse report and a quantization error summary."],
 [("Codebook collapse", "Only a small part of the codebook is ever used."),
  ("Bias", "The straight-through gradient is not the true gradient."),
  ("Two-stage training", "First the autoencoder, then the prior."),
  ("Blurry reconstruction", "Squared error alone tends to average away fine detail."),
  ("Perceptual loss", "A loss based on features of a pretrained network, used to sharpen results."),
  ("Quantization error", "The distance between the encoder output and its code.")],
 ["Codebook collapse is the main training failure; diagnose it with usage and perplexity.",
  "The straight-through gradient is biased but works if the commitment loss keeps z_e close to z_q.",
  "The prior is trained after the autoencoder, so generation quality depends on both stages.",
  "Squared error tends to give blurry reconstructions; later work adds adversarial and perceptual losses (background).",
  "Alternatives: EMA codebooks, reinitialisation, lower-dimensional codes, residual codes.",
  "The core idea, discrete learned tokens, now underpins many generative systems."],
 [T("What goes wrong in practice? The most common problem is codebook collapse. Early in training, a few codes win most assignments and get trained, while the rest are left behind. Over time the model uses a fraction of the codebook and the reconstructions are worse than a full codebook would give. The diagnostics of chapter 7, usage and perplexity, show it. The repairs of chapter 6, EMA updates and reinitialisation, reduce it."),
  T("A second problem is the straight-through estimator. It is biased, as chapter 4 showed. Its quality depends on the encoder output being near the chosen code, which is why the commitment loss matters. If the two are far apart, the gradient at the code says little about where the encoder output should go. Some later methods replace the hard assignment with a softened one or add extra losses."),
  T("A third issue is that the two stages are separate. The encoder and the codebook are trained without regard to how easily a prior can model the codes. A code that reconstructs well but is a chaotic jumble of symbols is hard for the prior. Some later models train both together."),
  T("Compare with the alternatives. A standard VAE has continuous latents with a fixed Gaussian prior, and tends to give blurry samples, and can suffer posterior collapse. A GAN generates images without an encoder, with sharp results but unstable training and no explicit likelihood. VQ-VAE with a PixelCNN prior is likelihood-based, covers the data well and is stable to train. Its reconstructions from squared error can still be soft, and later systems add adversarial and perceptual losses to sharpen them. That is background knowledge."),
  T("What is its legacy? The idea of learning a discrete vocabulary for continuous data, then modelling sequences of those tokens, is now widespread. Image generators, music generators and audio codecs use variants of it. The VQ-VAE paper itself showed images, audio and video frames, and reported speech samples with recognisable words when a WaveNet prior was used on the codes."),
  T("The course ends with diagnostic labs: a collapse report, the average quantization error, and the choice of the best codebook size under a budget."),
  T("Where to go next: read the 2017 paper itself, then VQ-VAE-2, then the work on residual and finite scalar quantization. Implement a small VQ-VAE on a toy image set in your favourite deep-learning library and plot the perplexity during training.")],
 [("What is codebook collapse?", ["Most codes are never used", "The decoder fails", "The loss is zero", "The prior diverges"], 0, "Detected with usage and perplexity."),
  ("Why is the straight-through gradient biased?", ["It ignores the quantizer's real derivative", "It is exact", "It uses noise", "It is random"], 0, "It is a copy, not a derivative."),
  ("What can sharpen blurry reconstructions?", ["Adversarial and perceptual losses", "Smaller codebooks", "Fewer layers", "Lower resolution only"], 0, "Later work, background."),
  ("Why train the prior separately?", ["The autoencoder is fixed first", "It is faster only", "It is mandatory by the loss", "It avoids data"], 0, "Two-stage training.")],
 [("What is the main failure?", "Codebook collapse."), ("What helps?", "EMA, reinitialisation and monitoring."), ("Is VQ-VAE likelihood based?", "With the prior, yes."), ("What was the legacy?", "Discrete tokens for continuous data.")],
 [PL("Collapse report", "Write collapse_report(counts): return [number of used codes, number of dead codes, 1 if fewer than a quarter of the codes are used else 0].",
     "collapse_report(counts)", """
def collapse_report(counts):
    used = 0
    for c in counts:
        if c > 0:
            used += 1
    dead = len(counts) - used
    flag = 0
    if used * 4 < len(counts):
        flag = 1
    return [used, dead, flag]
""", [[[5, 0, 0, 0, 0, 0, 0, 0]], [[1, 1, 1, 1]], [[3, 3, 0, 0]], [[0, 0, 0, 9]]], "Count the used entries and compare with a quarter."),
  PL("Average quantization error", "Write quant_error(zs, quantized): the mean over the vectors of the squared distance between each vector and its quantized version (sum over elements, mean over vectors), rounded to 6 decimals.",
     "quant_error(zs, quantized)", """
def quant_error(zs, quantized):
    total = 0.0
    for z, q in zip(zs, quantized):
        total += sum((a - b) ** 2 for a, b in zip(z, q))
    return round(total / len(zs), 6)
""", [[[[0, 0], [1, 1]], [[0, 0], [1, 0]]], [[[1.0]], [[0.5]]], [[[2, 2], [0, 0]], [[2, 2], [0, 0]]]], "Sum squared differences and average over vectors."),
  PL("Pick a codebook size", "Candidates are lists [k, error, bits_per_position]. Write choose_k(cands, max_bits): among the candidates with bits_per_position at most max_bits, return the k with the smallest error (ties go to the smaller k); return 0 if none fits.",
     "choose_k(cands, max_bits)", """
def choose_k(cands, max_bits):
    best = None
    arg = 0
    for k, err, bits in cands:
        if bits <= max_bits:
            if best is None or err < best - 1e-12 or (abs(err - best) <= 1e-12 and k < arg):
                best = err
                arg = k
    return arg
""", [[[[64, 0.5, 6], [512, 0.2, 9], [1024, 0.15, 10]], 9], [[[64, 0.5, 6], [512, 0.2, 9]], 5], [[[32, 0.3, 5], [64, 0.3, 6]], 6], [[[8, 1.0, 3]], 4]], "Filter by bits, then minimize the error."),
  ORDER("Fixing collapse", "Order a sensible response.", ["Log perplexity and usage during training", "Notice that usage is low", "Revive dead codes from batch vectors", "Consider EMA updates", "Check that perplexity recovers"]),
  MATCH("Problems and fixes", "Match each problem with a remedy.", [("Codebook collapse", "Reinitialise or EMA"), ("Blurry output", "Perceptual or adversarial loss (later work)"), ("Biased gradient", "Commitment loss"), ("Poor generation", "Stronger prior"), ("Low capacity", "Residual or product codes")]),
  FILL("Problems", "Codebook {{collapse}} wastes capacity. The straight-through gradient is {{biased|an approximation}}. Training happens in {{two}} stages.")]))
