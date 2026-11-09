"""The Devil's Trill: decoding an image. Chapters 1-8."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cd"))
from clib import *

A = []

A.append(CH(
 "Reading the image",
 ("The image", [
  "Hebrew title | names | The evil eye", "Greek line | quotes | Revelation 20:7", "RGB circles | show | Additive colour", "Eye in triangle | is | The Eye of Providence",
  "Le Trille du Diable | is | A violin sonata", "Formulas | define | Universal intelligence", "Collage | mixes | Many traditions"]),
 ["This course starts from one collage and treats each part as a doorway into a subject. At the top is the Hebrew phrase ayin hara, the evil eye. Below it is a Greek line from Revelation.",
  "In the centre, three coloured circles surround an eye in a triangle. Near the bottom is the title of a violin sonata. Around the edges are formulas about universal intelligence.",
  "The pieces do not explain each other. The goal is to learn what each really is, then decide what the arrangement means."],
 [("Collage", "An artwork made by placing different pieces together."), ("Symbol", "A sign that stands for an idea."), ("Iconography", "The study of the meaning of images and their traditions."),
  ("Context", "The history and setting that give a sign its meaning."), ("Allusion", "An indirect reference to something else."), ("Apophenia", "Seeing connections in unrelated things.")],
 ["Identify each element before interpreting the whole.", "Every element has a source with its own history.", "Putting symbols side by side suggests a link without proving one.",
  "The Hebrew reads ayin hara, the evil eye.", "The Greek is Revelation 20:7.", "The formulas are from Legg and Hutter's definition of machine intelligence."],
 [T("Start by simply listing what is there. Top: the Hebrew words ayin hara, written in large block letters. Under them, two lines of Greek."),
  T("In the middle, a triangle with an eye over three circles of red, green and blue. Under that, the French title Le Trille du Diable, with the English words Devil's Trill in brackets. "),
  T("At the bottom, a line of musical notation signed with the composer's name, G. Tartini. Around the border, formulas using the Greek letters upsilon, mu, xi, pi and the summation sign."),
  T("Next, ask what kind of thing each one is. The Hebrew is a phrase from Jewish folk belief. The Greek is a biblical verse. The coloured circles are a diagram from colour science. The eye in the triangle is an old religious and later political symbol. The title and music belong to a famous violin piece. The formulas belong to computer science."),
  T("Only then ask about the whole. A creator who puts these together is making a statement about fear, the unseen, music, mathematics and perhaps the idea of a created mind. We cannot read the creator's intention from the picture alone, so we study each part carefully and leave the final reading open."),
  T("A good habit for any layered image is to separate three questions. What is it? What does it mean in its own tradition? And what does it suggest in this arrangement? The first two have answers you can check. The third is interpretation, and different viewers will reach different views.")],
 [("What is the first step in reading a collage?", ["Identify each element on its own terms", "Decide what it all means", "Ignore the text", "Look only at colours"], 0, "Facts first, interpretation after."),
  ("Which words does the Hebrew say?", ["Ayin hara, the evil eye", "Shalom aleichem", "Shema Yisrael", "Hag sameach"], 0, "Ayin hara."),
  ("What is placing symbols side by side an example of?", ["Suggestion without proof", "A mathematical proof", "A scientific law", "A translation"], 0, "It invites a link.")],
 [("What is iconography?", "The study of what images mean in their traditions."), ("What is apophenia?", "Seeing connections where none exist."), ("What is an allusion?", "An indirect reference."), ("What are the three questions?", "What is it, what does it mean there, what does it suggest here.")],
 [MATCH("Parts of the image", "Match each part of the collage with its source.", [("Hebrew phrase", "Jewish folk belief about the evil eye"), ("Greek sentence", "The Book of Revelation"), ("Three coloured circles", "Additive colour mixing"), ("Eye in a triangle", "The Eye of Providence"), ("Sheet music", "Tartini's Devil's Trill sonata"), ("Formulas", "Universal intelligence")]),
  ORDER("Reading an image", "Put the steps in order.", ["List every element you can see", "Find out what each element is", "Learn what each means in its own tradition", "Consider what the arrangement suggests", "Say clearly which parts are fact and which are interpretation"]),
  PL("Count the elements", "Write count_kinds(items): items is a list of strings naming the kind of each element (for example 'text', 'symbol', 'formula'). Return a list of [kind, count] pairs sorted by kind.",
     "count_kinds(items)", """
def count_kinds(items):
    d = {}
    for k in items:
        d[k] = d.get(k, 0) + 1
    return [[k, d[k]] for k in sorted(d)]
""", [[["text", "symbol", "text", "formula", "symbol", "text"]], [["formula"]], [[]]], "Count each kind.", approx=None)]))

A.append(CH(
 "The evil eye (ayin hara)",
 ("Evil eye", [
  "Ayin hara | means | Evil eye", "Envy | is | The root of the belief", "Hamsa | is | A protective hand", "Red thread | is | A common charm",
  "Bli ayin hara | is | A spoken protection", "Gematria | adds | Letter values", "Many cultures | share | The belief"]),
 ["The evil eye is the belief that a harmful glance, usually from envy or admiration, can bring bad luck to the person or thing looked at. In Hebrew the phrase is ayin hara. The belief is very old and found across the Mediterranean, the Middle East, South Asia and beyond.",
  "In Jewish tradition the phrase appears in the Mishnah and Talmud, and customs developed to guard against it: not boasting about good fortune, a red string, the hamsa hand, and the spoken phrase bli ayin hara, without an evil eye, said after mentioning something good.",
  "The lab adds up the numerical values of the Hebrew letters, a traditional practice called gematria."],
 [("Ayin hara", "Hebrew for evil eye, literally bad eye."), ("Mati", "The Greek name for the evil eye and its blue charm."), ("Hamsa", "A hand-shaped charm used for protection."),
  ("Amulet", "An object believed to protect."), ("Gematria", "Giving letters numbers and adding them up."), ("Kinehora", "A Yiddish form of 'no evil eye'.")],
 ["The belief links harm to a glance, especially an envious one.", "It is found in many cultures with different names and charms.", "Jewish sources mention the evil eye, for example in the Mishnah (Pirkei Avot) and the Talmud.",
  "Common protections: blue beads, the hamsa, red thread, spitting symbolically, spoken phrases.", "The Hebrew letters also stand for numbers.", "Folk belief is studied by anthropologists as a way societies talk about envy and luck."],
 [T("Why would people fear a look? In small communities, good fortune can stir envy, and envy can spoil relationships. The evil eye gives a name to that worry and gives people simple things to do about it. Anthropologists see it as a way a society manages the tension between sharing luck and keeping it."),
  T("The idea is very old. Ancient Greek and Roman writers describe it, and it appears in Mesopotamian and Egyptian sources. In Hebrew the phrase ayin hara is used in classical Jewish texts, where it can mean a grudging or envious attitude as well as a harmful glance, and it is mentioned in the Talmud as something to guard against."),
  T("Protection takes many forms. The hamsa is a hand shape, found in Jewish and Muslim communities. A blue glass eye, the mati, is common in Greece and Turkey. A red thread is worn on the wrist. People may also say a phrase after a compliment, such as bli ayin hara or the Yiddish kinehora, to turn away jealousy."),
  T("In the image the Hebrew words ayin hara are written in big letters at the top, so the viewer meets the idea of a harmful watching eye before seeing the watching eye in the triangle. Whether that link is intended or only suggested is for the viewer to judge."),
  T("Hebrew letters also have number values, and gematria is the tradition of adding them. Ayin is 70, yod is 10 and final nun is 50, so the word ayin adds to 130. Hey is 5, resh is 200 and ayin is 70, so hara adds to 275. Gematria is a traditional word-play, not a proof of anything, and the lab below only practises the arithmetic.")],
 [("What does ayin hara literally mean?", ["Bad eye", "Holy hand", "Blue bead", "Red thread"], 0, "Ayin means eye."),
  ("What does the hamsa represent?", ["A protective hand", "A musical note", "A colour", "A verse"], 0, "A charm against the evil eye."),
  ("What is gematria?", ["Giving letters number values and adding them", "A type of charm", "A prayer", "A calendar"], 0, "A traditional practice.")],
 [("What is the Greek name for the evil eye?", "Mati."), ("What does bli ayin hara mean?", "Without an evil eye."), ("Is the belief only Jewish?", "No, it is found in many cultures."), ("What does the red thread do?", "It is worn as protection.")],
 [MATCH("Protections", "Match each protection with where it is common.", [("Hamsa", "Jewish and Muslim communities"), ("Blue glass eye", "Greece and Turkey"), ("Red thread", "Worn on the wrist"), ("Bli ayin hara", "Said after good news")]),
  PL("Gematria", "Write gematria(word): the standard (absolute) value of a Hebrew word. Values: א1 ב2 ג3 ד4 ה5 ו6 ז7 ח8 ט9 י10 כ20 ל30 מ40 נ50 ס60 ע70 פ80 צ90 ק100 ר200 ש300 ת400, and the final forms ך20 ם40 ן50 ף80 ץ90. Return the sum.",
     "gematria(word)", """
def gematria(word):
    vals = {'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400}
    t = 0
    for ch in word:
        t += vals.get(ch, 0)
    return t
""", [["עין"], ["הרע"], ["שלום"], ["אב"], [""]], "Add up each letter's value.", approx=None)]))

A.append(CH(
 "Revelation 20:7 and the thousand years",
 ("Revelation", [
  "Revelation | is | The last book of the New Testament", "Chiliasm | means | Belief in a thousand-year reign", "Satan | is | Bound then released", "Koine Greek | is | The language of the text",
  "Premillennial | places | Christ's return before", "Postmillennial | places | It after", "Amillennial | reads | The thousand years as symbolic"]),
 ["The Greek line in the image is Revelation 20:7. Translated it says that when the thousand years are completed, Satan will be released from his prison. It belongs to the passage describing a thousand-year period in which Satan is bound.",
  "Christians have read this passage in different ways. Some take the thousand years literally, some symbolically, and the positions have names: premillennialism, postmillennialism and amillennialism. The Greek word for thousand, chilia, gives us chiliasm.",
  "This chapter explains the text, its language and the main readings, without arguing for any of them."],
 [("Revelation", "The final book of the Christian Bible, an apocalyptic text."), ("Apocalyptic", "Literature that uses visions to reveal hidden meaning."), ("Millennium", "From Latin, a thousand years."),
  ("Chilia", "The Greek word for a thousand."), ("Koine", "The common Greek of the New Testament era."), ("Eschatology", "The study of last things.")],
 ["Revelation 20:7 says Satan is released when the thousand years are completed.", "The passage in 20:1-6 describes a binding and a reign of a thousand years.", "Premillennialists expect Christ's return before the thousand years; postmillennialists, after; amillennialists read the period symbolically.",
  "Apocalyptic writing uses symbols heavily.", "Koine Greek has accents and breathing marks, as in the image.", "Translations differ slightly in wording."],
 [T("The Greek in the image can be read as: kai hotan telesthe ta chilia ete, lythesetai ho Satanas ek tes phylakes autou. In English: and when the thousand years are completed, Satan will be released from his prison. The first word kai means and, ta chilia ete means the thousand years, and lythesetai is the future passive of the verb lyo, to release."),
  T("The sentence belongs to the twentieth chapter of Revelation. Earlier verses describe an angel binding the dragon, identified as the devil and Satan, for a thousand years, and the faithful reigning during that time. Verse 7 says what happens at the end of the period."),
  T("Revelation is an apocalyptic book, written in a style full of visions, numbers and symbols, in a time when its first readers faced pressure from the Roman empire. Scholars therefore ask how much is to be read as literal prediction and how much as coded hope or warning."),
  T("Three main Christian readings exist. Premillennialism expects Christ to return before the thousand-year reign. Postmillennialism expects the reign to come through the spread of the gospel, with Christ returning afterward. Amillennialism treats the thousand years as symbolic of the present age of the church. Each tradition points to different features of the text and to the wider Bible."),
  T("In the collage the verse about Satan's release sits under the evil eye and above the eye in the triangle. Putting a verse about a release of evil near symbols of watching eyes invites a mood of foreboding. Remember that the verse is about a particular vision in Revelation, and that the picture adds the association, not the text.")],
 [("What does Revelation 20:7 say happens after the thousand years?", ["Satan is released", "The world ends at once", "A new law is given", "The temple is built"], 0, "That is the line in the image."),
  ("What does amillennialism hold?", ["The thousand years are symbolic", "The reign is literal and future", "Christ returns first", "There is no Satan"], 0, "The a means no literal millennium."),
  ("Which language is the line written in?", ["Koine Greek", "Latin", "Classical Hebrew", "Aramaic"], 0, "With accent marks.")],
 [("What does chilia mean?", "Thousand."), ("What is apocalyptic writing?", "Visionary writing that reveals hidden meaning."), ("What does lythesetai mean?", "Will be released."), ("What is eschatology?", "The study of last things.")],
 [MATCH("Readings", "Match each reading with its idea.", [("Premillennial", "Christ returns before the thousand years"), ("Postmillennial", "Christ returns after the thousand years"), ("Amillennial", "The thousand years are symbolic"), ("Chiliasm", "Belief in a thousand-year reign")]),
  FILL("Greek words", "In the Greek line, {{chilia|ta chilia}} means a thousand, and {{Satanas|Satan}} is the name of the one released."),
  PL("Year counter", "Write end_of_period(start, years): a period of the given length that starts in year start is completed in year start + years. Return that year, then return a second value in a list: whether the length is exactly 1000. Return [end_year, is_thousand].",
     "end_of_period(start, years)", """
def end_of_period(start, years):
    return [start + years, years == 1000]
""", [[0, 1000], [30, 1000], [100, 40]], "Add the years.", approx=None)]))

A.append(CH(
 "The Eye of Providence",
 ("Providence", [
  "Eye of Providence | is | An eye in a triangle", "Triangle | stands for | The Trinity", "Rays | show | Divine light", "Great Seal | shows | It on the reverse",
  "Dollar bill | has | It since 1935", "Freemasons | use | A similar eye", "Conspiracy stories | add | Later meanings"]),
 ["The eye inside a triangle, often with rays, is called the Eye of Providence. In Christian art from the Renaissance it stood for God watching over the world, with the triangle recalling the Trinity. It is a symbol of care and watchfulness, from the same family of ideas as the eye of God in many religions.",
  "The symbol appears on the reverse of the Great Seal of the United States, designed in 1782, and so on the one dollar bill. Freemasons also used a similar all-seeing eye. Later, popular stories claimed it as a sign of hidden control, a claim that historians do not support.",
  "This chapter follows the symbol from its religious origins to its modern uses."],
 [("Providence", "God's care and guidance of the world."), ("Trinity", "The Christian doctrine of one God in three persons."), ("All-seeing eye", "An eye symbolising constant watchfulness."),
  ("Great Seal", "The official emblem of the United States."), ("Pyramid", "The unfinished pyramid under the eye on the Great Seal."), ("Masonic", "Of the Freemasons.")],
 ["Early uses are Christian: an eye in a triangle for God's watching and the Trinity.", "A famous Renaissance example is Pontormo's painting of the Supper at Emmaus, about 1525.", "The Great Seal's reverse, adopted 1782, shows an eye over an unfinished pyramid.",
  "The one dollar bill has carried the reverse design since 1935.", "Freemasons used an all-seeing eye as an emblem of the Great Architect.", "Claims that it proves a secret plot are not supported by evidence."],
 [T("The idea of a watching divine eye is old. Egyptian art has the eye of Horus, a protective symbol. Hebrew scripture speaks of the eyes of the Lord running over the whole earth. When Renaissance artists wanted to show God's watchfulness, an eye inside a triangle became a neat picture: the three sides for the Trinity, the eye for seeing and caring."),
  T("The United States took the image for the reverse of its Great Seal. The design was completed in 1782, and its eye over an unfinished pyramid, with the Latin words Annuit Coeptis, which mean he has favoured our undertakings, expresses hope for success. The reverse was put on the dollar bill in 1935."),
  T("Freemasonry, the fraternal society that grew from medieval stonemasons' guilds, uses an eye as a symbol of the Great Architect of the Universe. Some Masonic documents use a similar eye, which fed later stories that the dollar bill carries a Masonic message. Historians point out that the Great Seal's designers were not mainly Masons and that the symbol had a long earlier Christian use."),
  T("The eye is also a symbol of surveillance. In modern art and media, a lone eye above a crowd often stands for being watched. That sits in an interesting tension with the evil eye at the top of the collage: one eye protects, one harms, and both watch."),
  T("The three coloured circles around the eye in the image are red, green and blue. They connect to the next chapter, where they are explained as the primary colours of light.")],
 [("What did the eye in a triangle first stand for in Christian art?", ["God's watchful care and the Trinity", "A secret society", "A bank", "A mathematical proof"], 0, "Providence."),
  ("When did the reverse of the Great Seal get its design?", ["1782", "1492", "1620", "1935"], 0, "It reached the dollar in 1935."),
  ("What do historians say about claims of a hidden Masonic plot?", ["The evidence does not support them", "They are proven", "They are the main source", "They are law"], 0, "The symbol is much older.")],
 [("What does Annuit Coeptis mean?", "He has favoured our undertakings."), ("What does the triangle stand for?", "The Trinity."), ("Where was the Eye used in Egypt?", "The eye of Horus is a protective symbol."), ("When was it added to the dollar bill?", "1935.")],
 [ORDER("Symbol history", "Put the stages in order from oldest to newest.", ["Ancient eye symbols of protection", "Renaissance eye in a triangle for God's care", "The Great Seal reverse of 1782", "The dollar bill reverse of 1935", "Modern stories of hidden control"]),
  PL("Years since", "Write years_since(events, now): events is a list of [name, year]. Return the list of [name, now - year] sorted by years since, smallest first.",
     "years_since(events, now)", """
def years_since(events, now):
    out = [[n, now - y] for n, y in events]
    out.sort(key=lambda e: (e[1], e[0]))
    return out
""", [[[["Great Seal", 1782], ["Dollar bill", 1935], ["Pontormo", 1525]], 2026], [[["a", 2000]], 2010], [[], 2026]], "Subtract and sort.", approx=None)]))

A.append(CH(
 "Light and colour: the red, green and blue circles",
 ("Colour", [
  "Red green blue | are | Light primaries", "Additive mixing | adds | Light", "Red plus green | makes | Yellow", "All three | make | White",
  "Screens | use | RGB pixels", "Hex colour | writes | RGB in base 16", "Cones | are | Colour sensors in the eye"]),
 ["The three overlapping circles of red, green and blue show how light mixes. Where red and green overlap you see yellow, where green and blue overlap cyan, where red and blue overlap magenta, and where all three overlap white. This is additive colour mixing, the way every screen works.",
  "Our eyes have three kinds of cone cells that respond most to long, medium and short wavelengths, roughly red, green and blue light. A screen fools the eye by combining three small lights in different strengths.",
  "The labs mix colours and convert them to the hexadecimal codes used on web pages."],
 [("Primary colours of light", "Red, green and blue."), ("Additive mixing", "Combining lights to make new colours."), ("Pixel", "A tiny dot made of red, green and blue parts."),
  ("Hexadecimal", "Base 16 numbers: 0-9 and a-f."), ("Cone cell", "A colour-sensing cell in the retina."), ("Subtractive mixing", "Mixing pigments, which absorb light.")],
 ["Each RGB channel runs from 0 to 255.", "Red + green = yellow; green + blue = cyan; red + blue = magenta; all three = white.", "Paint mixes differently: it is subtractive, with cyan, magenta and yellow as primaries.",
  "A hex colour is #RRGGBB, two hex digits per channel.", "The eye has three kinds of cones with overlapping sensitivity.", "Overlap regions in the image are brighter, not darker."],
 [T("Mix red and blue paint and you get a dull purple. Mix red and green light and you get bright yellow. The reason is that paint absorbs light, so each added pigment takes more away, while lights add to each other. This is why the overlap in the diagram is lighter than the circles."),
  T("A screen is a grid of pixels, and each pixel has three tiny lights. The strength of each runs from 0 to 255. Pure red is 255, 0, 0. Pure yellow is 255, 255, 0, because the red and green lights are both on. White is 255, 255, 255 and black is 0, 0, 0."),
  T("Web pages write these numbers in hexadecimal, base 16, with the digits 0 to 9 and a to f. Two hex digits make one channel from 00 to ff, which is 0 to 255. So pure red is the code #ff0000 and yellow is #ffff00."),
  T("Our eyes work in a similar way. The retina has three kinds of cone cells, each most sensitive to a different range of wavelengths. The brain compares their signals to see colour. That is why three lights can imitate almost any colour we can see."),
  T("In the collage, the red, green and blue circles frame the eye in the triangle. The overlap in the middle, which is white or light, is exactly where the eye sits. Whatever message the artist intended, the diagram itself is correct physics: the three primaries of light combine to white.")],
 [("What do red and green light make?", ["Yellow", "Brown", "Purple", "White"], 0, "Additive mixing."),
  ("What do all three primaries make?", ["White", "Black", "Grey", "Brown"], 0, "At full strength."),
  ("Why do paints mix differently?", ["They absorb light (subtractive)", "They are brighter", "They have no colour", "They use RGB"], 0, "Each pigment removes more light.")],
 [("How many values does a channel have?", "256, from 0 to 255."), ("What is #00ff00?", "Pure green."), ("What are the printer primaries?", "Cyan, magenta, yellow."), ("What senses colour in the eye?", "Cone cells.")],
 [MATCH("Mixes", "Match each overlap with its colour.", [("Red + green", "Yellow"), ("Green + blue", "Cyan"), ("Red + blue", "Magenta"), ("Red + green + blue", "White")]),
  PL("Mix lights", "Write mix(colors): colors is a list of [r, g, b] with values 0-255. Add the channels and cap each at 255. Return [r, g, b].",
     "mix(colors)", """
def mix(colors):
    out = [0, 0, 0]
    for c in colors:
        for i in range(3):
            out[i] += c[i]
    return [min(255, v) for v in out]
""", [[[[255, 0, 0], [0, 255, 0]]], [[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], [[[100, 100, 0], [100, 200, 0]]], [[]]], "Add each channel; cap at 255.", approx=None),
  PL("Hex code", "Write to_hex(r, g, b): return the colour as '#rrggbb' in lower-case hexadecimal, two digits per channel.",
     "to_hex(r, g, b)", """
def to_hex(r, g, b):
    d = '0123456789abcdef'
    out = '#'
    for v in (r, g, b):
        out += d[v // 16] + d[v % 16]
    return out
""", [[255, 0, 0], [255, 255, 0], [0, 0, 0], [18, 171, 205]], "Divide by 16 for the first digit.", approx=None)]))

A.append(CH(
 "Tartini's Devil's Trill",
 ("Music", [
  "Giuseppe Tartini | composed | The Devil's Trill sonata", "Violin sonata | is in | G minor", "Trill | is | Fast alternation of two notes", "Dream legend | tells of | The devil playing",
  "Tritone | is | Six semitones", "Equal temperament | uses | 12 equal steps", "Lalande | recorded | The story in 1766"]),
 ["Le Trille du Diable, the Devil's Trill, is a violin sonata in G minor by the Italian composer and violinist Giuseppe Tartini, who lived from 1692 to 1770. Its last movement is famous for a long trill, a fast alternation between two neighbouring notes, played together with other notes on the violin.",
  "The nickname comes from a story Tartini is said to have told the French astronomer Jerome Lalande: he dreamed the devil played a violin so beautifully that Tartini woke, grabbed his violin and tried to write down what he remembered, yet felt the result fell far short of the dream. Whether the story happened as told is unknown.",
  "The labs compute note frequencies and the tritone, the interval sometimes nicknamed the devil in music."],
 [("Trill", "Rapid alternation between a note and the next one."), ("Double stop", "Playing two strings at once."), ("Semitone", "The smallest step in Western music."),
  ("Tritone", "An interval of six semitones, half an octave."), ("Equal temperament", "Tuning with every semitone the same ratio."), ("A4", "The standard tuning note, 440 hertz.")],
 ["Tartini (1692-1770) wrote the Violin Sonata in G minor, called the Devil's Trill.", "Lalande published the dream story in his travel book in 1769 after meeting Tartini in 1766.", "A trill alternates a main note with the note above it.",
  "Twelve equal semitones make an octave, which doubles the frequency; each semitone multiplies by 2 to the power one twelfth.", "A tritone is six semitones, a ratio of the square root of two in equal temperament.", "The 'devil in music' nickname for the tritone is a separate, much older tale."],
 [T("Giuseppe Tartini was one of the great violinists of the eighteenth century, and he ran a famous violin school in Padua. His G minor sonata is hard to play. In the last movement, the player must produce a long trill while the other fingers play a melody or bass on the neighbouring strings, which was extraordinary for its time."),
  T("The dream story goes like this. Tartini dreamed he made a pact with the devil, who became his servant, and he handed the devil a violin to see if he could play. The devil played a sonata of such beauty that Tartini woke in a daze, seized his violin and tried to capture it. He said the piece he wrote, the Devil's Trill, was the best he ever wrote but far below what he heard in the dream. He is said to have claimed he would break his violin and give up music if he could have played the dream."),
  T("Historians treat the story with care. Lalande's account comes from a conversation years after the sonata was written, and the sonata's date is uncertain, probably between 1713 and the 1740s. It is a good example of how a legend gives a famous work a name and a mystery."),
  M(r"f_n \;=\; 440 \cdot 2^{(n-69)/12}"),
  T("In equal temperament, which divides the octave into twelve equal steps, a note n semitones above another has a frequency that is multiplied by two to the power n over twelve. The standard pitch is A above middle C at 440 hertz, which is MIDI note 69. The formula above gives the frequency of MIDI note n."),
  T("A tritone is six semitones, exactly half an octave, so its frequency ratio is the square root of two, about 1.414, an irrational number. Medieval theorists avoided it as unstable, and a later nickname called it the devil in music. That nickname is separate from Tartini's sonata, though the two stories are often mixed together, as in the collage, where the sonata is named but the tritone is only hinted at.")],
 [("Who composed the Devil's Trill sonata?", ["Giuseppe Tartini", "J. S. Bach", "Paganini", "Vivaldi"], 0, "G. Tartini is named on the image."),
  ("What is a trill?", ["Fast alternation of two neighbouring notes", "A loud chord", "A slow melody", "A tuning method"], 0, "Often with a note above."),
  ("How many semitones are in a tritone?", ["Six", "Three", "Seven", "Twelve"], 0, "Half an octave.")],
 [("What is the frequency of A4?", "440 hertz."), ("What does an octave do to frequency?", "Doubles it."), ("Who recorded the dream legend?", "Jerome Lalande."), ("What key is the sonata in?", "G minor.")],
 [FILL("Tuning", "A semitone multiplies frequency by the twelfth root of {{2|two}}, so twelve semitones make an {{octave}}."),
  PL("Note frequency", "Write freq(n): frequency in hertz of MIDI note n in equal temperament with A4 (note 69) = 440 Hz, rounded to 4 decimals. Use import math.",
     "freq(n)", """
import math
def freq(n):
    return round(440.0 * math.pow(2.0, (n - 69) / 12.0), 4)
""", [[69], [60], [81], [57], [67]], "Two to the power of the semitone distance over twelve.", approx=1e-3),
  PL("Tritone ratio", "Write interval_ratio(semitones): the frequency ratio of an interval of that many semitones in equal temperament, rounded to 6 decimals. Use import math.",
     "interval_ratio(semitones)", """
import math
def interval_ratio(semitones):
    return round(math.pow(2.0, semitones / 12.0), 6)
""", [[12], [7], [6], [0]], "Two to the power of semitones over twelve.", approx=1e-5),
  PL("Trill", "Write trill(main, upper, beats): a trill that alternates between the main note and the upper note, starting on the main, for the given number of beats. Return the list of notes.",
     "trill(main, upper, beats)", """
def trill(main, upper, beats):
    out = []
    for i in range(beats):
        out.append(main if i % 2 == 0 else upper)
    return out
""", [[67, 69, 6], [60, 62, 1], [60, 62, 0], [55, 57, 5]], "Alternate by even and odd beats.", approx=None)]))

A.append(CH(
 "Universal intelligence: the formulas",
 ("Intelligence", [
  "Legg and Hutter | defined | Universal intelligence", "Agent | acts in | Environments", "Reward | scores | Each step", "Kolmogorov complexity | measures | Simplicity",
  "Occam weight | is | 2 to the minus K", "Upsilon | sums | Weighted performance", "AIXI | is | The best possible agent"]),
 ["The formulas around the border come from a 2007 paper by Shane Legg and Marcus Hutter, which defined a measure of machine intelligence. An agent acts in an environment, receives rewards, and its intelligence is its expected reward averaged over all possible environments, giving simpler environments more weight.",
  "The central formula, written with the Greek letter upsilon, is a weighted sum. The weight of an environment is two to the power of minus its Kolmogorov complexity, which formalises Occam's razor: simpler explanations count for more.",
  "The labs compute a discounted reward and a toy universal intelligence score."],
 [("Agent", "Something that acts in an environment; here a policy pi."), ("Environment", "A rule for how the world responds; here mu."), ("Reward", "A number received after each action."),
  ("Kolmogorov complexity K(mu)", "Length of the shortest program that describes mu."), ("Value V", "Expected total reward of a policy in an environment."), ("Discount", "A weight gamma that makes later rewards count less.")],
 ["Upsilon(pi) = sum over environments mu of 2^(-K(mu)) times V(pi, mu).", "V(pi, mu) is the expected sum of rewards of policy pi in environment mu.", "The discounted form: V = E of the sum of gamma_i times r_i.",
  "Simple environments get exponentially larger weights.", "AIXI is the agent that maximises this measure; it cannot be computed exactly.", "The measure is a theoretical definition, not a test you can run."],
 [M(r"\Upsilon(\pi) \;:=\; \sum_{\mu\in E} 2^{-K(\mu)}\,V^{\pi}_{\mu}"),
  T("Read it from right to left. V with pi and mu is how much reward the agent pi expects to collect in the environment mu. Each environment gets the weight two to the minus K of mu, where K is its Kolmogorov complexity, the length in bits of the shortest program that produces it. Short programs mean big weights. The sum over all environments in E gives a single number, the universal intelligence of pi."),
  T("Why weight by simplicity? An agent could do very well in a strange, complicated world and poorly in everyday ones. Weighting simple worlds more rewards general ability, not narrow tricks. It is the formal version of Occam's razor, the idea that simpler explanations are more likely."),
  M(r"V^{\pi}_{\gamma} \;:=\; \mathbb{E}\!\left[\sum_{i=1}^{\infty} \gamma_i\, r_i\right]"),
  T("The second kind of formula in the border is the reward sum. The agent gets a reward r at each step i, and gamma is a discount that makes later rewards count a little less, so the infinite sum stays finite. The expectation E averages over everything random in the interaction."),
  T("The definition has a known limit: Kolmogorov complexity cannot be computed in general. So universal intelligence is a gold standard for thinking about intelligence, not a test one can give a chatbot. The ideal agent for this measure, called AIXI, was described by Hutter and also cannot be built exactly. Other courses in this app, such as the AIXI course, go deeper."),
  T("In the collage these formulas frame the whole picture. A reading that fits: the evil eye, the watching eye and the devil are stories about unseen minds, and the formulas are a mathematical attempt to say what a mind that does well everywhere would be. That is an interpretation, not a fact about the picture.")],
 [("What does the weight 2 to the minus K favour?", ["Simple environments", "Complex environments", "Large rewards", "Late rewards"], 0, "Short programs, big weights."),
  ("What is V of pi and mu?", ["Expected total reward of pi in mu", "The size of the program", "The number of steps", "A probability"], 0, "Performance in one environment."),
  ("Can universal intelligence be computed exactly?", ["No, K is not computable", "Yes, on a laptop", "Yes, with a GPU", "Only for chess"], 0, "It is a theoretical definition.")],
 [("Who defined universal intelligence?", "Shane Legg and Marcus Hutter, in 2007."), ("What does gamma do?", "Discounts later rewards."), ("What is AIXI?", "The ideal agent for this measure."), ("What is K(mu)?", "The length of the shortest program for mu.")],
 [MATCH("Symbols", "Match each symbol with its meaning.", [("Upsilon", "Universal intelligence of an agent"), ("pi", "The agent's policy"), ("mu", "An environment"), ("K(mu)", "Kolmogorov complexity"), ("gamma", "Discount factor")]),
  PL("Discounted return", "Write discounted(rewards, gamma): the sum of gamma^i times reward_i, for i starting at 0, rounded to 6 decimals.",
     "discounted(rewards, gamma)", """
def discounted(rewards, gamma):
    t = 0.0
    g = 1.0
    for r in rewards:
        t += g * r
        g *= gamma
    return round(t, 6)
""", [[[1, 1, 1], 0.5], [[0, 0, 10], 0.9], [[5], 0.99], [[], 0.9]], "Multiply by gamma each step.", approx=1e-5),
  PL("Toy universal intelligence", "Write upsilon(envs): envs is a list of [K, value] pairs, K the complexity in bits and value the agent's expected reward in that environment. Return the sum of 2^(-K) times value, rounded to 6 decimals.",
     "upsilon(envs)", """
def upsilon(envs):
    t = 0.0
    for k, v in envs:
        t += v * (0.5 ** k)
    return round(t, 6)
""", [[[[1, 1.0], [2, 0.5], [3, 0.0]]], [[[1, 0.0], [2, 0.0], [3, 1.0]]], [[[4, 0.8]]], [[]]], "Weight each value by one half to the power K.", approx=1e-5)]))

A.append(CH(
 "Reading symbols critically",
 ("Critical reading", [
  "Apophenia | is | Seeing patterns in noise", "Coincidence | is | Common by chance", "Source | should be | Checked", "Context | gives | Meaning",
  "Occam's razor | prefers | Simple explanations", "Symbols | have | Many readings", "Respect | belongs to | Traditions"]),
 ["Images like this one make a powerful impression because they pile up serious symbols: an eye, a devil, a verse about the end, a trill, mathematics. When many strong symbols sit together, the mind rushes to find a hidden plan. That rush is natural, and worth examining.",
  "This last chapter gives tools for looking at layered images and the stories around them. It teaches how common coincidences really are, how to check sources, and how to enjoy symbolism without being fooled by it.",
  "It also reminds us that the traditions behind these symbols are lived by real people, and deserve to be described accurately and with respect."],
 [("Apophenia", "Finding meaning in random or unrelated information."), ("Confirmation bias", "Noticing what fits what you already believe."), ("Base rate", "How common something is in general."),
  ("Primary source", "The original document or work."), ("Provenance", "The history of where a thing came from."), ("Occam's razor", "Prefer the simplest adequate explanation.")],
 ["Coincidences are far more likely than they feel (the birthday problem).", "Check the original source before accepting a claim about a symbol.", "A symbol can have several unrelated origins.",
  "Placing symbols together is a rhetorical choice, not evidence.", "Describe traditions as their followers would recognise them.", "Enjoying an image and doubting its claims can go together."],
 [T("People are pattern finders. That served our ancestors well, because mistaking a rock for a bear costs little while missing a bear costs a lot. The same habit makes us see faces in clouds and plots in coincidences. This is called apophenia, and it is strongest when the material feels charged with meaning."),
  T("Coincidences are more common than intuition says. In a room of just 23 people there is about a fifty percent chance that two share a birthday. When you consider how many pairs of things could be linked in an image full of symbols, some links will always appear. The question is whether they are surprising given how many chances there were."),
  T("Checking sources is the strongest habit. Where does this symbol come from? What did its first users mean? A claim that the eye on the dollar bill proves a plot fails when you learn the eye was a common Christian symbol long before. A claim that the sonata was written after a pact with the devil fails when you learn the story was told years later by a visitor."),
  T("Respect matters too. The evil eye is part of living Jewish, Greek, Arab, Turkish and other cultures. Revelation is sacred scripture to millions. Describing them as props in a spooky picture would miss what they are. You can analyse a collage as a work of art and still describe each tradition fairly."),
  T("So how should we read the collage in the end? As an artwork that gathers symbols of watching, danger, music, light and mind, and links them to the idea of a mathematically defined intelligence. It invites reflection on what it is to be watched, to create a mind, or to fear one. Those are real questions, and the symbols are a vivid way to raise them.")],
 [("What is apophenia?", ["Finding patterns in unrelated things", "A kind of music", "A colour", "A measurement"], 0, "A natural habit."),
  ("Why do coincidences feel rare?", ["We ignore how many chances there were", "They are impossible", "They are caused by symbols", "They need a plan"], 0, "The birthday problem shows the opposite."),
  ("What is the best habit for symbol claims?", ["Check the original sources", "Share them fast", "Trust the loudest", "Ignore context"], 0, "Provenance first.")],
 [("What is the birthday problem?", "A small group likely contains a shared birthday."), ("What is confirmation bias?", "Noticing what fits your beliefs."), ("What is provenance?", "A thing's history."), ("What does Occam's razor prefer?", "The simplest adequate explanation.")],
 [FILL("Habits", "Always check the {{source}} of a claim, and remember that {{coincidences|coincidence}} are more common than they feel."),
  PL("Birthday problem", "Write shared_birthday(n): the probability that among n people (365 equally likely days) at least two share a birthday, rounded to 4 decimals.",
     "shared_birthday(n)", """
def shared_birthday(n):
    p = 1.0
    for i in range(n):
        p *= (365 - i) / 365.0
    return round(1.0 - p, 4)
""", [[1], [10], [23], [50], [70]], "Multiply the chances that everyone differs, then subtract from one.", approx=1e-4),
  PL("Chances of a link", "Write pair_count(n): the number of different pairs among n symbols (each pair a possible 'connection'). Return n choose 2.",
     "pair_count(n)", """
def pair_count(n):
    return n * (n - 1) // 2
""", [[2], [6], [10], [0]], "n times n-1 over two.", approx=None)]))
