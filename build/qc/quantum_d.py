# -*- coding: utf-8 -*-
"""Quantum computing for beginners: the Bloch sphere chapter."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

BLOCH = []
BLOCH.append(CH(
 "The Bloch sphere: a globe for one qubit",
 ("Bloch sphere", [
  "Qubit | lives on | A sphere",
  "North pole | is | Plain 0",
  "South pole | is | Plain 1",
  "Equator | is | 50 50 blends",
  "Longitude | is | Phase",
  "Gates | are | Turns"]),
 ["A single qubit can always be drawn as an arrow from the centre of a ball to its surface. This ball is called the Bloch sphere. It turns the two hidden numbers of a qubit into a picture you can hold in your head.",
  "The north pole is a plain 0 and the south pole is a plain 1. The equator holds the fair blends. How far east you are on the globe is the phase. Every gate is just a turn of the globe.",
  "The sphere only works for one qubit at a time. When a qubit is entangled, its arrow shrinks and sits inside the ball, and that shrinking is a way to see entanglement."],
 [("Bloch sphere", "A ball whose surface holds every state of one qubit."),
  ("Pole", "The top and bottom of the sphere: plain 0 and plain 1."),
  ("Equator", "The middle ring: equal chances of 0 and 1."),
  ("Longitude", "The angle around the vertical axis. It is the phase."),
  ("Latitude", "How far from the poles. It sets the chances."),
  ("Axis", "A line to turn around: x, y or z."),
  ("Theta", "The angle measured down from the north pole.")],
 ["The north pole is 0 and the south pole is 1.",
  "Height on the sphere sets the chance: chance of 1 = (1 minus z) / 2.",
  "Longitude (turning around the vertical axis) is the phase.",
  "X, Y and Z are half turns about the x, y and z axes.",
  "H is a half turn about the line between x and z.",
  "S and T are quarter and eighth turns about the vertical axis.",
  "An entangled qubit has a shorter arrow, inside the ball."],
 [T("Think of a globe. A plain 0 sits on the north pole and a plain 1 sits on the south pole. A qubit is a pin stuck from the centre of the globe through one spot on the surface. That one arrow tells you everything about the qubit."),
  T("Height is chance. At the north pole you always measure 0. At the south pole you always measure 1. On the equator, halfway, you get 0 half the time and 1 half the time. The nearer the arrow is to the south, the more likely a 1."),
  T("Why do the two poles stand for states that are so different, yet sit only half a world apart? Because the sphere uses half angles. The angle you see on the sphere is double the angle between the amplitudes. Opposite poles on the globe are 180 degrees apart, while the states 0 and 1 are as different as two states can be."),
  M("|ψ⟩ = cos(θ/2) |0⟩ + e^(iφ) sin(θ/2) |1⟩"),
  T("Here θ (theta) is how far down from the north pole the arrow points, and φ (phi) is how far around the vertical axis. The chance of a 1 is sin(θ/2) squared. This is the same formula you met with H, phase, H."),
  T("Next, the phase. Two arrows at the same height have the same chances, but they can point to different longitudes. The four marked points on the equator are |+⟩ (towards you at 0 degrees), |+i⟩ (90 degrees), |−⟩ (180 degrees) and |−i⟩ (270 degrees). They all give 50/50 when measured, but they are different states, which is why H then Z then H works."),
  T("Now the best part: gates are turns. Imagine pushing a skewer through the globe along an axis and spinning it. X is a half turn about the x axis, so it swaps the poles. Z is a half turn about the vertical axis, so it keeps the poles but turns the equator halfway round, flipping the phase. Y is a half turn about the y axis."),
  T("The H gate is a half turn about a slanted skewer that runs between x and z. It sends the north pole to the +x point on the equator, which is the fair blend |+⟩. Do it twice and you are back at the pole: two half turns make a full turn. S is a quarter turn about the vertical axis, and T is an eighth. RX, RY and RZ are turns by any angle you choose."),
  C("# where does H take the north pole? Chance of 1 from the height z\nz = 0.0          # on the equator\np1 = (1 - z) / 2\nprint('chance of 1:', p1)", "python"),
  T("Open the lab and the Bloch tab, then press H. The arrow glides from the north pole down to +x. Drag the sphere to look from any side, or press Top view to see the phase around the circle. The readout below tells you the exact x, y, z numbers."),
  T("A last idea. Put two qubits into a Bell pair and look at each one on its own sphere. Each arrow shrinks to nothing, right in the middle of the ball. Neither qubit alone has a direction, because all the information lives in the link between them. A shorter arrow means entanglement."),
  T("What the sphere cannot do: it draws one qubit at a time. For two qubits you need the amplitude table, as in Inspect. Still, almost every one-qubit gate you will ever meet is a turn of this globe, and thinking of it that way makes circuits much easier to guess.")],
 [("Where is a plain 0 on the Bloch sphere?", ["North pole", "South pole", "Equator", "Centre"], 0, "Top of the globe."),
  ("Where does a 50/50 qubit sit?", ["On the equator", "At a pole", "At the centre", "Nowhere"], 0, "Halfway up."),
  ("What does X do on the sphere?", ["A half turn about x, swapping the poles", "Nothing", "A quarter turn", "Shrinks the arrow"], 0, "0 becomes 1."),
  ("What does the longitude of the arrow mean?", ["The phase", "The chance of 1", "The number of shots", "The noise"], 0, "Turning around the vertical axis."),
  ("What does Z do to a qubit at the north pole?", ["Nothing you can see", "Moves it to the south", "Moves it to the equator", "Removes it"], 0, "The pole lies on the axis."),
  ("What does a short arrow inside the ball mean?", ["The qubit is entangled", "The qubit is lost", "The chance is 0", "The qubit is plain 0"], 0, "Information is shared."),
  ("H then H on a plain 0 gives:", ["Plain 0 again", "Plain 1", "A 50/50 blend", "Noise"], 0, "Two half turns make a full turn.")],
 [("North pole", "Plain 0"), ("South pole", "Plain 1"), ("Equator", "Fair 50/50 blends"), ("Longitude", "Phase"), ("Short arrow", "Entangled qubit")],
 [MATCH("Match the gate to the turn", "Pair each gate with what it does on the sphere.", [("X", "half turn about the x axis"), ("Z", "half turn about the vertical axis"), ("S", "quarter turn about the vertical axis"), ("T", "eighth turn about the vertical axis")]),
  MATCH("Match the point", "Pair each state with where it sits.", [("|0⟩", "north pole"), ("|1⟩", "south pole"), ("|+⟩", "equator, towards you"), ("|−⟩", "equator, opposite |+⟩")]),
  FILL("The globe", "The north pole is plain {{0}}. The south pole is plain {{1}}. The equator holds {{fair}} blends. The angle around the vertical axis is the {{phase}}. A qubit entangled with another has a {{shorter}} arrow."),
  PL("Chance from the angle", "Write chance_one(theta): the arrow is theta degrees down from the north pole. The chance of 1 is sin of half the angle, squared. Use import math. Round to 4 decimals.", "chance_one(theta)", '''
import math
def chance_one(theta):
    return round(math.sin(math.radians(theta) / 2) ** 2, 4)
''', [[0], [90], [180], [60]], "Half the angle."),
  ORDER("Order the turns", "Put the steps in order to take the north pole to the +i point on the equator.", ["Start at the north pole (plain 0)", "Apply H to reach +x on the equator", "Apply S, a quarter turn about the vertical axis", "The arrow now points at +i"])]))
