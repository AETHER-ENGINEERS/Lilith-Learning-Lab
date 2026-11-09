#!/usr/bin/env python3
"""Build the VQ-VAE course. Usage: python3 make_vqvae_course.py <out.json>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "vq"))
import cmk, vqv  # noqa: E402

PRONOUNCE = {
    "VQ-VAE-2": "V Q V A E two", "VQ-VAE": "V Q V A E", "VQGAN": "V Q gan", "VAE": "V A E", "VAEs": "V A Es",
    "PixelCNN": "pixel C N N", "WaveNet": "wave net", "SoundStream": "sound stream", "Jukebox": "juke box",
    "Kavukcuoglu": "kah voo koo loo", "Razavi": "rah zah vee", "van den Oord": "van den ord", "Vinyals": "vin yalls",
    "NeurIPS": "neur ips", "ImageNet": "image net", "EMA": "E M A", "MSE": "M S E", "GAN": "gan", "NLL": "N L L",
    "k-means": "k means", "K-means": "K means", "argmin": "arg min", "sg": "stop gradient", "Gaussian": "gaussian",
    "bigram": "bi gram", "Bigram": "Bi gram", "PPL": "perplexity",
}

SANDBOX = cmk.terminal("VQ-VAE lookup", "vq>", "A scripted lookup, not a real model. Try: loss, sizes, ste, ema", [
    ("loss", ["L = ||x - D(z_q)||^2 + ||sg[z_e] - e||^2 + beta ||z_e - sg[e]||^2", "beta = 0.25"]),
    ("sizes", ["codebook K=512, dimension D=64", "ImageNet 128x128 -> 32x32 grid of indices"]),
    ("ste", ["z_q_st = z_e + sg[z_q - z_e]", "forward value z_q, backward gradient of z_e"]),
    ("ema", ["N = g N + (1-g) n", "m = g m + (1-g) sum z", "e = m / N, decay g = 0.99"]),
    ("prior", ["PixelCNN for images, WaveNet for audio, trained on frozen codes"]),
])

EXAM = [
 ("What does the VQ-VAE quantizer do?", ["Replaces each encoder output by the nearest codebook vector", "Adds Gaussian noise", "Trains the prior", "Normalizes the batch"], 0, "A nearest-neighbour lookup."),
 ("Who introduced VQ-VAE?", ["van den Oord, Vinyals and Kavukcuoglu", "Kingma and Welling", "Vaswani et al.", "Goodfellow et al."], 0, "NeurIPS 2017."),
 ("What are the latents of a VQ-VAE?", ["Discrete indices into a codebook", "Gaussian vectors", "Binary images", "Words"], 0, "One index per grid position."),
 ("Why is a straight-through estimator needed?", ["The quantizer has zero gradient almost everywhere", "The decoder is discrete", "Adam fails", "The data is binary"], 0, "A staircase function."),
 ("What does the straight-through estimator do?", ["Copies the gradient from z_q to z_e", "Zeroes gradients", "Scales gradients by K", "Adds noise to gradients"], 0, "As if the quantizer were the identity."),
 ("What is the forward value of z_e + sg[z_q - z_e]?", ["z_q", "z_e", "0", "z_q - z_e"], 0, "The z_e terms cancel."),
 ("Which loss term moves the codebook vector toward the encoder output?", ["The codebook loss", "The commitment loss", "Reconstruction", "None"], 0, "||sg[z_e] - e||^2."),
 ("What does the commitment loss do?", ["Keeps the encoder output near its chosen code", "Moves the codebook", "Trains the decoder", "Samples codes"], 0, "Only the encoder moves."),
 ("What value of beta did the paper use?", ["0.25", "0", "10", "100"], 0, "The paper reports robustness to beta."),
 ("Does the reconstruction loss train the codebook directly?", ["No", "Yes", "Only in the first step", "Only with EMA"], 0, "The gradient ends at the encoder."),
 ("How many bits does one code from 512 entries hold at most?", ["9", "512", "5", "64"], 0, "log2 512."),
 ("The codebook loss resembles which algorithm?", ["K-means", "Dropout", "Attention", "Beam search"], 0, "Centres move toward their points."),
 ("What decay does the paper suggest for EMA updates?", ["0.99", "0.5", "0.1", "1.5"], 0, "The appendix suggests gamma 0.99."),
 ("What is a dead code?", ["A code never nearest to any output", "A code with big norm", "A repeated code", "The first code"], 0, "It never gets updated."),
 ("How can dead codes be repaired?", ["Reinitialise them from batch vectors", "Lower beta to 0", "Remove the decoder", "Train longer without change"], 0, "A common trick."),
 ("What is the perplexity of uniform usage over K codes?", ["K", "1", "log K", "0"], 0, "2 to the log2 K."),
 ("What does low perplexity signal?", ["Codebook collapse", "A strong decoder", "Fast training", "A good prior"], 0, "Few codes in use."),
 ("What is the entropy of a code that is always the same?", ["0", "1", "K", "Infinite"], 0, "No uncertainty."),
 ("Which prior did the paper use for images?", ["PixelCNN", "WaveNet", "LSTM only", "None"], 0, "WaveNet was used for audio."),
 ("Which prior did the paper use for audio?", ["WaveNet", "PixelCNN", "GAN", "Transformer"], 0, "A convolutional autoregressive model."),
 ("When is the prior trained?", ["After the autoencoder, which is frozen", "Jointly from step 0", "Before the encoder", "Never"], 0, "Two-stage training."),
 ("In what order is an image code grid usually modelled?", ["Raster order", "Random order", "Reverse order only", "Diagonal only"], 0, "Row by row."),
 ("Why model codes rather than pixels with PixelCNN?", ["The grid is far smaller", "Codes are colours", "Pixels are discrete", "It is required"], 0, "32 by 32 instead of 128 by 128."),
 ("How are latents of a 128 by 128 ImageNet image shaped in the paper?", ["32 by 32 grid", "1 by 1", "128 by 128", "8 by 8"], 0, "A 4 times reduction per side."),
 ("What does posterior collapse mean?", ["The decoder ignores the latent", "The loss reaches zero", "The prior diverges", "The codebook doubles"], 0, "Seen in VAEs with strong decoders."),
 ("What does residual quantization do?", ["Quantizes what the previous codebook left over", "Quantizes parts separately", "Removes codes", "Averages codebooks"], 0, "Background knowledge, later work."),
 ("What does product quantization do?", ["Splits the vector and quantizes each part separately", "Multiplies codes", "Prunes the book", "Trains a prior"], 0, "Parts are independent."),
 ("How many combinations do m codebooks of K entries give?", ["K^m", "K*m", "m^K", "K+m"], 0, "Tuples of indices."),
 ("Who wrote VQ-VAE-2?", ["Razavi, van den Oord and Vinyals", "Vaswani", "Kingma", "Radford"], 0, "2019, hierarchical codes."),
 ("What is the main training failure of VQ-VAE?", ["Codebook collapse", "Vanishing prior", "Over-large beta", "Missing decoder"], 0, "Few codes win everything."),
 ("Why is the straight-through gradient called biased?", ["It is not the true derivative", "It uses noise", "It is random", "It is exact"], 0, "It is a copy."),
 ("Why does the commitment loss matter for straight-through?", ["It keeps z_e near z_q so the copied gradient is meaningful", "It trains the decoder", "It increases K", "It is optional with no effect"], 0, "Otherwise the gradient says little."),
 ("What can sharpen blurry VQ-VAE reconstructions in later work?", ["Adversarial and perceptual losses", "Fewer codes", "Smaller images", "Larger beta"], 0, "Background knowledge."),
 ("Which is a nearest code with ties?", ["The lowest index in the labs", "A random one", "The highest index", "Both"], 0, "A convention for determinism."),
 ("What do the labs use instead of a deep-learning library?", ["Plain Python on toy examples", "TensorFlow", "PyTorch", "JAX"], 0, "Teaching examples."),
 ("What does an autoencoder bottleneck force?", ["Keeping only the important information", "More pixels", "Random output", "A bigger decoder"], 0, "Less capacity than the input."),
 ("What does the second term of the loss equal in a k-means view?", ["Moving a centre toward its points", "Reassigning points", "Splitting clusters", "Nothing"], 0, "Same objective."),
]

CFG = dict(id="vq-vae", title="VQ-VAE: Discrete Latents", subtitle="Codebooks, straight-through gradients and priors, with Python labs",
    description="Neural Discrete Representation Learning (van den Oord, Vinyals, Kavukcuoglu, 2017): the codebook and nearest-neighbour quantizer, the straight-through estimator, the three-part loss, EMA and dead codes, perplexity, autoregressive priors, and extensions. Theory plus Python labs.",
    pronounce=PRONOUNCE, sandbox=SANDBOX, exam=EXAM, appdir="vq", apps={})

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "courses", "vq-vae.course.json")
    cmk.main(CFG, vqv.CHS, [sys.argv[0], out])
