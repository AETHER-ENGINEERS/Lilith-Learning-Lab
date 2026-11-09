"""Mathematics for CS and AI, part 2: linear algebra II, calculus, optimization, probability."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

CHS = []

CHS.append(CH(
 "Linear algebra II: systems, determinants, eigenvalues and SVD",
 ("Eigen", [
  "Linear system | is | A x = b",
  "Elimination | solves | Systems",
  "Determinant | measures | Volume scaling",
  "Eigenvector | keeps | Its direction",
  "Eigenvalue | scales | An eigenvector",
  "SVD | factors | Any matrix",
  "PCA | uses | Eigenvectors of covariance"]),
 ["A linear system A x = b asks which input x the matrix A maps to b. Gaussian elimination solves it by row operations. The determinant tells how a matrix scales volume and whether it can be inverted.",
  "An eigenvector of A is a direction the matrix only stretches; the stretch factor is its eigenvalue. The singular value decomposition factors any matrix into rotations and a stretch, and powers principal component analysis and low-rank compression.",
  "The labs solve systems, compute determinants, find a dominant eigenvalue by power iteration and project data onto a direction."],
 [("Linear system", "Equations A x = b with unknown vector x."),
  ("Determinant", "A number det(A): the volume scale of the map; zero means not invertible."),
  ("Inverse", "A^-1 with A A^-1 = I; exists when det(A) is not zero."),
  ("Eigenvector", "A nonzero v with A v = lambda v."),
  ("SVD", "A = U S V^T with orthogonal U, V and a diagonal S of singular values."),
  ("PCA", "Find directions of greatest variance in data.")],
 ["Gaussian elimination solves A x = b in O(n^3) operations.",
  "det(AB) = det(A) det(B); det of a triangular matrix is the product of its diagonal.",
  "A v = lambda v; det(A - lambda I) = 0 gives the eigenvalues.",
  "Symmetric matrices have real eigenvalues and orthogonal eigenvectors.",
  "SVD: A = U S V^T; truncating small singular values gives the best low-rank approximation.",
  "PCA keeps the top eigenvectors of the covariance matrix."],
 [T("A system of linear equations such as two x plus y equals five and x minus y equals one is the question: which vector x does the matrix A send to the vector b? If A is invertible there is exactly one answer. Gaussian elimination finds it by adding multiples of one row to another until the matrix is triangular, then solving from the bottom up."),
  T("The determinant is a single number attached to a square matrix. For a two by two matrix it is a d minus b c. Geometrically it is the factor by which the map scales areas or volumes, with a sign for flipping. If it is zero the map squashes space onto something flatter and cannot be undone."),
  M(r"\det\begin{pmatrix}a&b\\c&d\end{pmatrix} = ad - bc, \qquad A v = \lambda v \iff \det(A - \lambda I) = 0"),
  T("Most vectors change direction when a matrix acts on them, but some do not: they are only stretched. These are eigenvectors, and the stretch factor is the eigenvalue. They reveal the natural axes of a map. Repeating the map many times makes any generic vector line up with the eigenvector of largest eigenvalue, which is the idea behind power iteration and Google's PageRank."),
  T("The singular value decomposition works for every matrix, not just square ones. It writes A as a rotation, a stretch along coordinate axes and another rotation. The stretches are the singular values. Keeping only the largest few gives the best possible low-rank approximation, used to compress images and to find latent factors in data."),
  M(r"A = U\,\Sigma\,V^{\top}, \qquad A_k = \sum_{i=1}^{k}\sigma_i\, u_i v_i^{\top}"),
  T("Principal component analysis applies this to data. Centre the data, compute its covariance matrix and take the eigenvectors with the largest eigenvalues. They are the directions of greatest spread, and projecting onto the first few gives a short summary of each point with minimal loss.")],
 [("What does det = 0 mean?", ["The map is not invertible", "The map is identity", "All entries zero", "Symmetric"], 0, "Space is flattened."),
  ("What is an eigenvector?", ["A direction only stretched by the matrix", "A zero vector", "A row", "A column sum"], 0, "A v = lambda v."),
  ("What does the SVD give?", ["A = U S V^T for any matrix", "Only square roots", "Only inverses", "Primes"], 0, "Rotation, stretch, rotation."),
  ("What does PCA find?", ["Directions of greatest variance", "The mean", "Outliers only", "Labels"], 0, "Top covariance eigenvectors.")],
 [("Det of 2x2?", "ad - bc."), ("Eigenvalue equation?", "det(A - lambda I) = 0."), ("Why truncate SVD?", "Best low-rank approximation."), ("Power iteration finds?", "The dominant eigenvector.")],
 [PL("Determinant 2x2", "Write det2(m): the determinant of a 2x2 matrix given as [[a, b], [c, d]].",
     "det2(m)", """
def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]
""", [[[[1, 2], [3, 4]]], [[[2, 0], [0, 3]]], [[[1, 2], [2, 4]]], [[[0, 1], [1, 0]]]], "ad - bc."),
  PL("Solve a 2x2 system", "Write solve2(m, b): solve m x = b for a 2x2 invertible matrix by Cramer's rule; return [x0, x1] rounded to 6 decimals.",
     "solve2(m, b)", """
def solve2(m, b):
    d = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    x0 = (b[0] * m[1][1] - m[0][1] * b[1]) / d
    x1 = (m[0][0] * b[1] - b[0] * m[1][0]) / d
    return [round(x0, 6), round(x1, 6)]
""", [[[[2, 1], [1, -1]], [5, 1]], [[[1, 0], [0, 1]], [3, 4]], [[[3, 2], [1, 4]], [7, 9]]], "Replace a column by b."),
  PL("Power iteration", "Write dominant(m, steps): start from [1, 1], repeat steps times: multiply by the 2x2 matrix m and divide by the largest absolute entry. Return the final scaling factor (largest absolute entry before dividing in the last step), rounded to 6 decimals. For a positive matrix this approaches the top eigenvalue.",
     "dominant(m, steps)", """
def dominant(m, steps):
    v = [1.0, 1.0]
    lam = 0.0
    for _ in range(steps):
        w = [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]
        lam = max(abs(w[0]), abs(w[1]))
        v = [w[0] / lam, w[1] / lam]
    return round(lam, 6)
""", [[[[2, 0], [0, 1]], 20], [[[2, 1], [1, 2]], 30], [[[1, 1], [1, 0]], 30]], "Multiply, normalise, repeat.", approx=1e-5),
  PL("Project onto a direction", "Write project(x, d): the projection of vector x onto direction d, as a list rounded to 6 decimals: (x.d / d.d) d.",
     "project(x, d)", """
def project(x, d):
    c = sum(a * b for a, b in zip(x, d)) / sum(b * b for b in d)
    return [round(c * b, 6) for b in d]
""", [[[3, 4], [1, 0]], [[1, 1], [1, 1]], [[2, 3, 4], [0, 0, 1]]], "Scale d by the shadow length."),
  ORDER("Gaussian elimination", "Order the steps.", ["Write the augmented matrix", "Use a pivot to clear entries below it", "Move to the next column", "Reach a triangular form", "Back-substitute from the last row"]),
  MATCH("Linear algebra II", "Match each term with its meaning.", [("Determinant", "Volume scale"), ("Eigenvector", "Only stretched"), ("SVD", "U S V^T"), ("PCA", "Top variance directions"), ("Inverse", "Undoes the map")]),
  FILL("Eigen", "An eigenvector satisfies A v = lambda v where lambda is the {{eigenvalue}}; a matrix with determinant {{0|zero}} has no inverse.")]))

CHS.append(CH(
 "Calculus: limits, derivatives and the chain rule",
 ("Calculus", [
  "Limit | describes | Behaviour near a point",
  "Derivative | is | Instantaneous rate of change",
  "Slope | is | Rise over run",
  "Chain rule | differentiates | Compositions",
  "Product rule | handles | Products",
  "Integral | accumulates | Area under a curve",
  "Taylor series | approximates | Smooth functions"]),
 ["Calculus is the mathematics of change. The derivative of a function measures how fast its output changes as its input changes: the slope of the curve at a point. The integral adds up small pieces to find total change or area.",
  "The chain rule differentiates a function of a function. It is the single most important rule for AI, because a neural network is a long composition of simple functions and backpropagation is the chain rule applied to it.",
  "The labs estimate derivatives numerically, apply the rules, integrate by the trapezoid rule and build a Taylor approximation."],
 [("Limit", "The value a function approaches as the input approaches a point."),
  ("Derivative", "f'(x) = lim (f(x+h) - f(x))/h."),
  ("Chain rule", "(f o g)'(x) = f'(g(x)) g'(x)."),
  ("Product rule", "(f g)' = f' g + f g'."),
  ("Integral", "The accumulated area under a curve."),
  ("Taylor series", "A polynomial approximation built from derivatives at a point.")],
 ["d/dx x^n = n x^(n-1); d/dx e^x = e^x; d/dx ln x = 1/x.",
  "Sum rule, product rule, quotient rule, chain rule.",
  "Derivative of sigmoid: s'(x) = s(x)(1 - s(x)).",
  "Fundamental theorem: the integral of f' from a to b equals f(b) - f(a).",
  "Taylor: f(x+h) ~ f(x) + f'(x) h + f''(x) h^2/2.",
  "At a minimum or maximum the derivative is zero."],
 [T("Imagine driving a car. Your position changes with time, and your speed is how fast. The derivative is exactly that: the instantaneous rate of change. To find it, take the change in output over a small change in input and let the input change shrink to zero. The result is the slope of the tangent line."),
  M(r"f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}, \qquad \frac{d}{dx}x^n = n x^{n-1}, \qquad \frac{d}{dx}e^{x}=e^{x}"),
  T("A handful of rules give the derivative of almost everything. Derivatives of sums add; the product rule handles products; the chain rule handles functions inside functions. If y depends on u and u depends on x, then the rate of change of y with x is the product of the two rates."),
  M(r"\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}, \qquad \sigma(x)=\frac{1}{1+e^{-x}},\quad \sigma'(x)=\sigma(x)\bigl(1-\sigma(x)\bigr)"),
  T("Why does this matter for AI? A network computes a chain: input, layer one, layer two, and finally a loss. To learn, we need the slope of the loss with respect to every weight. The chain rule lets us multiply local slopes along the chain, one layer at a time. That is backpropagation."),
  T("The integral goes the other way. It sums many thin slices to give the area under a curve, and the fundamental theorem says that this equals the change in an antiderivative. In probability, integrals add up the chance over a range of values. Finally, a Taylor series approximates a smooth function near a point by a polynomial, which explains why gradient methods work: near any point, a smooth function looks like a straight line.")],
 [("What does the derivative measure?", ["Instantaneous rate of change", "Total area", "The average", "The maximum"], 0, "The slope of the tangent."),
  ("Which rule differentiates f(g(x))?", ["Chain rule", "Product rule", "Sum rule", "Power rule"], 0, "Outer slope times inner slope."),
  ("What is the derivative of e^x?", ["e^x", "x e^x", "1", "ln x"], 0, "It is its own derivative."),
  ("What is backpropagation?", ["The chain rule applied to a network", "Random search", "Sorting", "Clustering"], 0, "Multiply local slopes.")],
 [("Derivative at a minimum?", "Zero."), ("Sigmoid derivative?", "s(1 - s)."), ("Integral measures?", "Accumulated area."), ("Taylor first order?", "A tangent line.")],
 [PL("Numerical derivative", "Write deriv(k, x): the central difference (f(x+h) - f(x-h)) / (2h) with h = 0.001 for f(x) = x^k, rounded to 3 decimals.",
     "deriv(k, x)", """
def deriv(k, x):
    h = 0.001
    return round(((x + h) ** k - (x - h) ** k) / (2 * h), 3)
""", [[2, 3], [3, 2], [1, 5], [4, 1]], "Slope across a tiny interval.", approx=0.01),
  PL("Power rule", "Write power_deriv(k, x): the exact derivative k x^(k-1) of x^k.",
     "power_deriv(k, x)", """
def power_deriv(k, x):
    return k * x ** (k - 1)
""", [[2, 3], [3, 2], [5, 1], [1, 7]], "Bring down the exponent."),
  PL("Chain rule: sigmoid of a line", "Write sig_grad(w, x): the derivative with respect to w of sigmoid(w x), i.e. x s (1 - s) where s = sigmoid(w x). Round to 6 decimals. Use import math.",
     "sig_grad(w, x)", """
import math
def sig_grad(w, x):
    s = 1.0 / (1.0 + math.exp(-w * x))
    return round(x * s * (1 - s), 6)
""", [[0, 1], [1, 2], [-1, 3], [2, 0]], "Outer slope times inner slope.", approx=1e-6),
  PL("Trapezoid integral", "Write integrate(k, a, b, n): approximate the integral of x^k from a to b with the trapezoid rule using n slices, rounded to 4 decimals.",
     "integrate(k, a, b, n)", """
def integrate(k, a, b, n):
    h = (b - a) / n
    s = 0.5 * (a ** k + b ** k)
    for i in range(1, n):
        s += (a + i * h) ** k
    return round(s * h, 4)
""", [[2, 0, 3, 1000], [1, 0, 4, 10], [3, 1, 2, 1000]], "Add thin trapezoids.", approx=0.001),
  ORDER("Chain rule", "Order the steps to differentiate sin(x squared).", ["Name the inner function x squared", "Differentiate the outer: cos of the inner", "Differentiate the inner: 2x", "Multiply the two results", "Write 2x cos(x squared)"]),
  MATCH("Calculus", "Match each rule or idea with its use.", [("Derivative", "Slope"), ("Integral", "Area"), ("Chain rule", "Backpropagation"), ("Product rule", "(fg)' = f'g + fg'"), ("Taylor", "Local polynomial")]),
  FILL("Calculus", "The derivative is the {{slope}} of a curve; the {{chain}} rule drives backpropagation.")]))

CHS.append(CH(
 "Multivariate calculus: gradients, Jacobians and backpropagation",
 ("Multivariate", [
  "Partial derivative | holds | Other variables fixed",
  "Gradient | points | Uphill",
  "Jacobian | collects | All partials",
  "Hessian | measures | Curvature",
  "Chain rule | multiplies | Jacobians",
  "Backprop | runs | Chain rule backwards",
  "Loss | is | A scalar output"]),
 ["Functions in AI take many inputs, so we need derivatives in many dimensions. A partial derivative changes one variable and holds the others still. The gradient collects all partials into a vector pointing in the direction of steepest increase.",
  "The Jacobian is the matrix of partials of a vector-valued function, and the Hessian is the matrix of second derivatives, describing curvature. The multivariate chain rule multiplies Jacobians, and backpropagation does it efficiently from the loss backwards.",
  "The labs compute gradients, check them numerically, and run backpropagation through a tiny network."],
 [("Partial derivative", "df/dx_i: change in f when only x_i moves."),
  ("Gradient", "The vector of all partials; the direction of steepest ascent."),
  ("Jacobian", "Matrix J_ij = d f_i / d x_j of a vector function."),
  ("Hessian", "Matrix of second partial derivatives."),
  ("Backpropagation", "Chain rule applied from the output to the inputs."),
  ("Gradient check", "Compare analytic gradients with finite differences.")],
 ["grad f = (df/dx1, ..., df/dxn); it is orthogonal to level sets.",
  "Directional derivative = grad f . u for a unit vector u.",
  "Chain rule: J of (f o g) = J_f J_g.",
  "For a linear layer y = W x: dL/dW = (dL/dy) x^T and dL/dx = W^T (dL/dy).",
  "Hessian positive definite means a local minimum at a critical point.",
  "Reverse mode costs about the same as one forward pass for a scalar loss."],
 [T("Take a hill. At any point, you could walk north, east, or any direction in between. The slope depends on the direction. A partial derivative is the slope when you walk strictly along one axis. Put all the partials in a list and you have the gradient, which points straight uphill, and its length is how steep the hill is."),
  M(r"\nabla f = \Bigl(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_n}\Bigr), \qquad D_u f = \nabla f \cdot u"),
  T("For a function whose output is also a vector, we stack the gradients of each output into the Jacobian matrix. It is the best linear approximation of the function near a point. Linear algebra and calculus meet here: locally, every smooth function acts like a matrix."),
  T("The chain rule becomes a product of Jacobians. In a network, the loss depends on the last layer, which depends on the one before, and so on. Computing the product from the loss backwards means each step is a vector times a matrix, which is cheap. That is reverse-mode differentiation, or backpropagation. A single backward pass gives the gradient with respect to every weight."),
  M(r"y = Wx \;\Rightarrow\; \frac{\partial L}{\partial W} = \frac{\partial L}{\partial y}\,x^{\top}, \qquad \frac{\partial L}{\partial x} = W^{\top}\frac{\partial L}{\partial y}"),
  T("The Hessian matrix of second derivatives describes curvature. At a point where the gradient is zero, a Hessian with all positive eigenvalues means a valley bottom, a local minimum. Mixed signs mean a saddle, which is common in the high-dimensional landscapes of deep learning. A good habit is the gradient check: compare your formulas with small finite differences to catch bugs.")],
 [("What does the gradient point toward?", ["Steepest increase", "Steepest decrease", "A minimum", "Zero"], 0, "Uphill."),
  ("What is a Jacobian?", ["Matrix of first partials of a vector function", "A scalar", "Second derivatives", "A norm"], 0, "Best linear approximation."),
  ("What is dL/dx for y = W x?", ["W transpose times dL/dy", "W times dL/dy", "x", "Zero"], 0, "Backward through a linear layer."),
  ("What does a Hessian describe?", ["Curvature", "Slope", "Area", "Probability"], 0, "Second derivatives.")],
 [("Gradient of x^2 + y^2?", "(2x, 2y)."), ("Why reverse mode?", "One backward pass gives all weight gradients."), ("What is a saddle?", "Up in one direction, down in another."), ("Gradient check?", "Compare with finite differences.")],
 [PL("Gradient of a quadratic", "Write grad(x, y): the gradient of f(x, y) = 3x^2 + 2xy + y^2 as a list [df/dx, df/dy].",
     "grad(x, y)", """
def grad(x, y):
    return [6 * x + 2 * y, 2 * x + 2 * y]
""", [[1, 1], [0, 0], [2, -3], [-1, 4]], "Differentiate with the other variable fixed."),
  PL("Numerical gradient", "Write num_grad(x, y): central-difference gradient (h = 0.001) of f(x, y) = x^2 y + y^3, each entry rounded to 2 decimals.",
     "num_grad(x, y)", """
def num_grad(x, y):
    h = 0.001
    def f(a, b):
        return a * a * b + b ** 3
    gx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    gy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return [round(gx, 2), round(gy, 2)]
""", [[1, 2], [0, 1], [3, -1]], "Nudge each variable.", approx=0.02),
  PL("Backprop through y = w x + b", "Write linear_backprop(w, b, x, t): for y = w x + b and loss L = (y - t)^2, return [dL/dw, dL/db] rounded to 6 decimals.",
     "linear_backprop(w, b, x, t)", """
def linear_backprop(w, b, x, t):
    y = w * x + b
    dy = 2 * (y - t)
    return [round(dy * x, 6), round(dy, 6)]
""", [[1, 0, 2, 5], [0.5, 0.5, 1, 1], [-1, 2, 3, 0]], "Loss slope times local slope.", approx=1e-6),
  PL("One gradient descent step", "Write step(x, y, lr): one gradient descent step on f(x, y) = x^2 + 3 y^2; return [new_x, new_y] rounded to 6 decimals.",
     "step(x, y, lr)", """
def step(x, y, lr):
    return [round(x - lr * 2 * x, 6), round(y - lr * 6 * y, 6)]
""", [[1, 1, 0.1], [2, -1, 0.05], [0, 5, 0.1]], "Move against the gradient."),
  ORDER("Backpropagation", "Order the steps.", ["Run the forward pass and store activations", "Compute the loss", "Differentiate the loss with respect to the output", "Pass gradients back through each layer", "Read the gradient for every weight"]),
  MATCH("Multivariate", "Match each object with its meaning.", [("Gradient", "Steepest ascent"), ("Jacobian", "Matrix of first partials"), ("Hessian", "Curvature"), ("Partial derivative", "One variable moves"), ("Backprop", "Reverse chain rule")]),
  FILL("Gradient", "The {{gradient}} points toward steepest increase, so gradient descent moves {{against|opposite}} it.")]))

CHS.append(CH(
 "Optimization: gradient descent, convexity and Lagrange multipliers",
 ("Optimization", [
  "Objective | is | Minimised",
  "Gradient descent | steps | Downhill",
  "Learning rate | sets | Step size",
  "Convex | has | One valley",
  "Momentum | smooths | Updates",
  "Lagrange multiplier | handles | Constraints",
  "Stochastic gradient | samples | Data"]),
 ["Training a model means minimising a loss. Gradient descent repeats a simple step: move a little against the gradient. The learning rate is the step size, and too large a step overshoots while too small a step crawls.",
  "A convex function has a single valley, so descent finds the global minimum. Deep networks are not convex, yet descent works well in practice. Momentum, stochastic mini-batches and adaptive methods improve it. Lagrange multipliers handle constraints.",
  "The labs run gradient descent, show how the step size matters, implement momentum and solve a constrained problem."],
 [("Objective", "The function to minimise, such as a loss."),
  ("Gradient descent", "x <- x - lr * grad f(x)."),
  ("Learning rate", "The step size in gradient descent."),
  ("Convex function", "A function lying below its chords; every local minimum is global."),
  ("Momentum", "Keep a running average of past gradients."),
  ("Lagrange multiplier", "Turns a constrained problem into an unconstrained one.")],
 ["Update: x_{t+1} = x_t - eta * grad f(x_t).",
  "For f = a x^2, descent converges when 0 < eta < 1/a.",
  "Convex: f(tx + (1-t)y) <= t f(x) + (1-t) f(y).",
  "Momentum: v <- beta v + grad; x <- x - eta v.",
  "Constrained optimum: grad f = lambda grad g with g(x) = 0.",
  "SGD uses a random mini-batch to estimate the gradient."],
 [T("Picture standing on a foggy hillside, wanting the lowest point. You cannot see far, but you can feel the slope under your feet. So you step downhill, feel again, and repeat. That is gradient descent. Each step moves against the gradient by an amount set by the learning rate."),
  M(r"x_{t+1} \;=\; x_t - \eta\,\nabla f(x_t)"),
  T("The learning rate matters a lot. For the simple bowl f equals a times x squared, steps smaller than one over a converge smoothly, steps near that size bounce, and larger steps blow up. In practice you tune it, or let methods such as Adam adapt it."),
  T("Convexity makes things easy. A convex function is shaped like a bowl: any line between two points on its graph lies above the graph. Every local minimum is then a global minimum, and descent cannot get trapped. Linear and logistic regression are convex. Deep networks are not, but descent still finds good solutions."),
  T("Momentum adds memory: the update follows a running average of recent gradients, like a heavy ball rolling downhill, which smooths noise and speeds travel along narrow valleys. Stochastic gradient descent uses a small random batch of data at each step. It is noisy but cheap, and the noise can even help escape poor spots."),
  M(r"\min f(x)\ \text{ s.t. } g(x)=0 \;\Rightarrow\; \nabla f(x) = \lambda\,\nabla g(x)"),
  T("Sometimes the answer must satisfy a rule. Lagrange multipliers handle equality constraints: at the best point, the gradient of the objective is parallel to the gradient of the constraint, so the objective cannot be improved without breaking the rule. The multiplier says how much the optimum would change if the constraint were loosened.")],
 [("What does gradient descent do?", ["Steps against the gradient", "Steps along the gradient", "Picks randomly", "Sorts"], 0, "Downhill."),
  ("What if the learning rate is too big?", ["It can diverge", "It converges faster always", "Nothing", "It stops"], 0, "Overshoot."),
  ("What is special about convex functions?", ["Local minimum is global", "No minimum", "Two valleys", "Zero gradient"], 0, "One valley."),
  ("What does momentum do?", ["Averages past gradients", "Randomises", "Stops updates", "Doubles the loss"], 0, "A rolling ball.")],
 [("SGD uses?", "A random mini-batch."), ("Lagrange condition?", "Gradients parallel."), ("Why tune the learning rate?", "Too big diverges, too small crawls."), ("Convex examples?", "Linear and logistic regression.")],
 [PL("Gradient descent on a bowl", "Write descend(x0, lr, steps): minimise f(x) = (x - 3)^2 by gradient descent from x0; return x rounded to 6 decimals.",
     "descend(x0, lr, steps)", """
def descend(x0, lr, steps):
    x = x0
    for _ in range(steps):
        x = x - lr * 2 * (x - 3)
    return round(x, 6)
""", [[0, 0.1, 50], [10, 0.5, 5], [0, 0.01, 10], [3, 0.1, 10]], "Gradient is 2(x - 3).", approx=1e-5),
  PL("Does it diverge?", "Write diverges(a, lr): 1 if gradient descent on f(x) = a x^2 (a > 0) with step lr diverges (the factor |1 - 2 a lr| is above 1), else 0.",
     "diverges(a, lr)", """
def diverges(a, lr):
    return 1 if abs(1 - 2 * a * lr) > 1 else 0
""", [[1, 0.1], [1, 1.5], [2, 0.4], [0.5, 2.5]], "Each step multiplies x by 1 - 2 a lr."),
  PL("Momentum", "Write momentum(x0, lr, beta, steps): minimise f(x) = x^2 using v = beta v + 2x, then x = x - lr v, starting with v = 0; return x rounded to 6 decimals.",
     "momentum(x0, lr, beta, steps)", """
def momentum(x0, lr, beta, steps):
    x = x0
    v = 0.0
    for _ in range(steps):
        v = beta * v + 2 * x
        x = x - lr * v
    return round(x, 6)
""", [[5, 0.1, 0.9, 30], [1, 0.1, 0.0, 10], [2, 0.05, 0.5, 20]], "Keep a running velocity.", approx=1e-5),
  PL("Lagrange: best point on a line", "Minimise x^2 + y^2 subject to x + y = s. The Lagrange condition gives x = y = s/2. Write constrained(s): the minimum value, rounded to 6 decimals.",
     "constrained(s)", """
def constrained(s):
    x = s / 2.0
    return round(2 * x * x, 6)
""", [[2], [4], [0], [-6]], "Parallel gradients mean x equals y."),
  ORDER("Training loop", "Order the steps of gradient-descent training.", ["Initialise the parameters", "Compute the loss on a batch", "Compute the gradient", "Update parameters against the gradient", "Repeat until the loss stops falling"]),
  MATCH("Optimization", "Match each item with its role.", [("Learning rate", "Step size"), ("Convexity", "One valley"), ("Momentum", "Running average"), ("Lagrange multiplier", "Constraint handling"), ("SGD", "Mini-batch gradient")]),
  FILL("Optimization", "Gradient descent subtracts the gradient times the {{learning rate|step size}}; in a {{convex}} problem every local minimum is global.")]))

CHS.append(CH(
 "Probability: axioms, conditional probability and Bayes' rule",
 ("Probability", [
  "Sample space | lists | Outcomes",
  "Event | is | A set of outcomes",
  "Probability | measures | Chance",
  "Conditional | restricts to | What is known",
  "Independence | means | No information shared",
  "Bayes rule | reverses | Conditioning",
  "Random variable | maps | Outcomes to numbers"]),
 ["Probability measures uncertainty. A sample space lists all outcomes, an event is a set of them, and probability assigns a number between zero and one. The axioms make these numbers behave consistently.",
  "Conditional probability asks: given that this happened, how likely is that? Independence means one event tells you nothing about the other. Bayes' rule reverses a conditional and is the engine of learning from evidence.",
  "The labs compute conditional probabilities, apply Bayes to a medical test, check independence and simulate with a counting argument."],
 [("Sample space", "The set of all possible outcomes."),
  ("Event", "A subset of the sample space."),
  ("Conditional probability", "P(A | B) = P(A and B)/P(B)."),
  ("Independence", "P(A and B) = P(A) P(B)."),
  ("Bayes' rule", "P(A | B) = P(B | A) P(A) / P(B)."),
  ("Random variable", "A number attached to each outcome.")],
 ["Axioms: P(event) >= 0; P(whole space) = 1; probabilities of disjoint events add.",
  "P(not A) = 1 - P(A); P(A or B) = P(A) + P(B) - P(A and B).",
  "Law of total probability: P(B) = sum over i of P(B | A_i) P(A_i).",
  "Bayes: posterior is proportional to likelihood times prior.",
  "Independent events: P(A | B) = P(A).",
  "Base-rate neglect: ignoring P(A) when reading a test result."],
 [T("Roll a die. The sample space is the six faces. An event such as even is a set of faces, and its probability is the favourable outcomes over all outcomes when they are equally likely. The axioms say that probabilities are never negative, the whole space has probability one, and disjoint events add."),
  M(r"P(A\mid B) = \frac{P(A\cap B)}{P(B)}, \qquad P(A\cap B)=P(A)P(B)\ \text{if independent}"),
  T("Conditioning changes the sample space. Knowing a die is even leaves three faces, so the chance of a six becomes one third. Two events are independent if knowing one does not change the chance of the other, such as two separate coin flips."),
  T("Bayes' rule turns a conditional around. We often know how likely a symptom is given a disease, but want to know how likely the disease is given the symptom. The rule combines the likelihood, the prior and a normaliser."),
  M(r"P(H\mid E) = \frac{P(E\mid H)\,P(H)}{P(E)}, \qquad P(E)=\sum_i P(E\mid H_i)P(H_i)"),
  T("Imagine a disease that affects one person in a thousand, and a test that is ninety-nine percent accurate. A positive result does not mean a ninety-nine percent chance of illness. Among a thousand people, one is ill and nearly always tests positive, but about ten of the healthy ones also test positive. So the chance is only about one in eleven. Forgetting the base rate is one of the most common reasoning errors."),
  T("A random variable assigns a number to each outcome, such as the sum of two dice. Almost all of machine learning treats data and predictions as random variables, and training as inference about them.")],
 [("What is P(not A)?", ["1 - P(A)", "P(A)", "0", "P(A)^2"], 0, "Complement."),
  ("What does independence mean?", ["P(A and B) = P(A) P(B)", "P(A) = P(B)", "A implies B", "Disjoint"], 0, "No shared information."),
  ("What does Bayes' rule give?", ["P(H | E) from P(E | H)", "The mean", "Variance", "A sum"], 0, "Reverses the conditional."),
  ("What is base-rate neglect?", ["Ignoring the prior", "Ignoring the test", "Counting twice", "Rounding"], 0, "Rare things stay rare.")],
 [("Total probability?", "Sum over cases of P(B|A) P(A)."), ("Disjoint events?", "Probabilities add."), ("Posterior?", "Likelihood times prior, normalised."), ("Why is a positive test often wrong?", "Low base rate.")],
 [PL("Conditional probability", "Write cond(joint, b): P(A | B) = joint / b, rounded to 6 decimals.",
     "cond(joint, b)", """
def cond(joint, b):
    return round(joint / b, 6)
""", [[0.2, 0.5], [0.1, 0.1], [0.0, 0.3], [0.15, 0.6]], "Divide by what is known.", approx=1e-6),
  PL("Bayes: medical test", "Write posterior(prior, sens, spec): the probability of disease given a positive test, with prior P(D), sensitivity P(+|D) and specificity P(-|not D). Round to 6 decimals.",
     "posterior(prior, sens, spec)", """
def posterior(prior, sens, spec):
    pos = sens * prior + (1 - spec) * (1 - prior)
    return round(sens * prior / pos, 6)
""", [[0.001, 0.99, 0.99], [0.5, 0.9, 0.9], [0.01, 0.95, 0.9], [0.2, 0.8, 0.95]], "Likelihood times prior over the total.", approx=1e-6),
  PL("Are they independent?", "Write independent(pa, pb, pab): 1 if pab equals pa * pb to within 1e-9, else 0.",
     "independent(pa, pb, pab)", """
def independent(pa, pb, pab):
    return 1 if abs(pab - pa * pb) < 1e-9 else 0
""", [[0.5, 0.5, 0.25], [0.5, 0.5, 0.3], [0.2, 0.3, 0.06], [0.4, 0.5, 0.4]], "Compare the product."),
  PL("Two dice", "Write dice_prob(total): the probability that two fair dice sum to total, counted over the 36 outcomes, rounded to 6 decimals.",
     "dice_prob(total)", """
def dice_prob(total):
    c = 0
    for a in range(1, 7):
        for b in range(1, 7):
            if a + b == total:
                c += 1
    return round(c / 36, 6)
""", [[7], [2], [12], [1]], "Count favourable pairs.", approx=1e-6),
  ORDER("Bayesian update", "Order the steps.", ["Choose a prior for the hypothesis", "Observe the evidence", "Compute the likelihood of the evidence under each hypothesis", "Multiply likelihood by prior", "Normalise to get the posterior"]),
  MATCH("Probability", "Match each term with its meaning.", [("Prior", "Belief before evidence"), ("Likelihood", "P(evidence | hypothesis)"), ("Posterior", "Belief after evidence"), ("Independence", "Product rule holds"), ("Base rate", "How common the thing is")]),
  FILL("Bayes", "Bayes' rule multiplies the {{likelihood}} by the prior; ignoring the {{base rate|prior}} causes bad medical-test reasoning.")]))

CHS.append(CH(
 "Random variables, distributions and expectation",
 ("Distributions", [
  "Random variable | has | A distribution",
  "Expectation | is | The average",
  "Variance | measures | Spread",
  "Gaussian | models | Bell-shaped noise",
  "Bernoulli | models | Yes or no",
  "Law of large numbers | says | Averages settle",
  "Central limit theorem | explains | Why bells appear"]),
 ["A random variable has a distribution: how likely each value is. The expectation is the average value, the variance measures spread and the standard deviation is its square root. Common distributions include Bernoulli, binomial, uniform and Gaussian.",
  "Two theorems explain why statistics works. The law of large numbers says averages settle on the expectation. The central limit theorem says sums of many small independent effects look Gaussian.",
  "The labs compute expectations and variances, evaluate the Gaussian density, compute binomial probabilities and simulate averages."],
 [("Expectation", "E[X] = sum x P(x): the probability-weighted average."),
  ("Variance", "Var(X) = E[(X - mean)^2]."),
  ("Bernoulli", "A single yes or no trial with success probability p."),
  ("Binomial", "The count of successes in n independent Bernoulli trials."),
  ("Gaussian", "The bell curve with mean mu and standard deviation sigma."),
  ("Central limit theorem", "Averages of many independent samples become Gaussian.")],
 ["E[a X + b Y] = a E[X] + b E[Y] always (linearity).",
  "Var(X) = E[X^2] - (E[X])^2; Var(aX) = a^2 Var(X).",
  "Binomial: P(k) = C(n, k) p^k (1-p)^(n-k); mean np, variance np(1-p).",
  "Gaussian density: exp(-(x-mu)^2/(2 sigma^2)) / (sigma sqrt(2 pi)).",
  "Law of large numbers: the sample mean tends to E[X].",
  "CLT: the mean of n samples has standard deviation sigma/sqrt(n)."],
 [T("A random variable is a number whose value depends on chance. Its distribution lists how likely each value is. For a fair die, each of one to six has probability one sixth. The expectation is the long-run average, found by weighting each value by its probability."),
  M(r"E[X] = \sum_x x\,P(x), \qquad \mathrm{Var}(X) = E\bigl[(X-E[X])^2\bigr] = E[X^2]-(E[X])^2"),
  T("Expectation is linear: the expectation of a sum is the sum of expectations, even when the variables depend on each other. This simple fact solves many puzzles. Variance measures how far values typically stray from the mean; it adds for independent variables."),
  T("A Bernoulli variable is a single coin flip with chance p of success. The sum of n independent flips is binomial, with mean n p and variance n p times one minus p. The Gaussian, or normal, distribution is the bell curve described by a mean and a standard deviation. Most of its mass lies within two standard deviations of the mean."),
  M(r"p(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\!\Bigl(-\frac{(x-\mu)^2}{2\sigma^2}\Bigr)"),
  T("Why do bell curves appear everywhere? The central limit theorem says that the average of many independent random effects is approximately Gaussian, whatever the individual distributions. The law of large numbers says that average settles toward the expectation as the sample grows, with spread shrinking like one over the square root of the sample size. This is why polls of a thousand people can be accurate, and why Gaussian noise is the default model in machine learning.")],
 [("What is E[X] for a fair die?", ["3.5", "3", "4", "6"], 0, "Average of one to six."),
  ("What is the variance of a sum of independent variables?", ["The sum of variances", "The product", "Zero", "The mean"], 0, "Variances add."),
  ("What does the CLT say?", ["Averages become Gaussian", "Averages vanish", "Sums are uniform", "Variance is zero"], 0, "Many small effects."),
  ("How does the sample-mean spread shrink?", ["Like 1/sqrt(n)", "Like 1/n squared", "Not at all", "Like n"], 0, "Four times the data halves it.")],
 [("Linearity of expectation?", "E[X+Y] = E[X] + E[Y]."), ("Binomial mean?", "n p."), ("Why Gaussian noise?", "The CLT."), ("Standard deviation?", "Square root of variance.")],
 [PL("Expectation and variance", "Write ev(values, probs): return [mean, variance] of a discrete distribution, each rounded to 6 decimals.",
     "ev(values, probs)", """
def ev(values, probs):
    m = sum(v * p for v, p in zip(values, probs))
    var = sum(p * (v - m) ** 2 for v, p in zip(values, probs))
    return [round(m, 6), round(var, 6)]
""", [[[1, 2, 3, 4, 5, 6], [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]], [[0, 1], [0.5, 0.5]], [[10, 20], [0.9, 0.1]]], "Weight by probability.", approx=1e-6),
  PL("Binomial probability", "Write binom(n, k, p): P(exactly k successes in n trials), rounded to 6 decimals.",
     "binom(n, k, p)", """
def binom(n, k, p):
    c = 1
    for i in range(1, k + 1):
        c = c * (n - k + i) // i
    return round(c * p ** k * (1 - p) ** (n - k), 6)
""", [[10, 5, 0.5], [5, 0, 0.1], [4, 4, 0.9], [20, 3, 0.2]], "C(n,k) p^k (1-p)^(n-k).", approx=1e-6),
  PL("Gaussian density", "Write gauss(x, mu, sigma): the Gaussian density at x, rounded to 6 decimals. Use import math.",
     "gauss(x, mu, sigma)", """
import math
def gauss(x, mu, sigma):
    z = (x - mu) / sigma
    return round(math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi)), 6)
""", [[0, 0, 1], [1, 0, 1], [3, 2, 0.5], [0, 1, 2]], "The bell formula.", approx=1e-6),
  PL("Shrinking standard error", "Write std_err(sigma, n): the standard deviation of the mean of n independent samples, sigma/sqrt(n), rounded to 6 decimals. Use import math.",
     "std_err(sigma, n)", """
import math
def std_err(sigma, n):
    return round(sigma / math.sqrt(n), 6)
""", [[1, 100], [2, 4], [10, 25], [3, 1]], "Divide by the root of n.", approx=1e-6),
  ORDER("Sampling", "Order the steps to estimate an average by simulation.", ["Decide the quantity to average", "Draw many random samples", "Compute the value for each", "Average the values", "Report the average with its standard error"]),
  MATCH("Distributions", "Match each distribution with its description.", [("Bernoulli", "One yes or no trial"), ("Binomial", "Successes in n trials"), ("Gaussian", "Bell curve"), ("Uniform", "All values equally likely"), ("CLT", "Why averages look normal")]),
  FILL("Expectation", "The expectation is the probability-{{weighted}} average; the sample mean's spread shrinks like one over the {{square root|sqrt}} of n.")]))
