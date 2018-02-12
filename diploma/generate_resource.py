import sys
import json
import os.path
import random
from string import Template
from datetime import datetime

import babel
from babel import Locale, dates
from elizabeth import Personal, exceptions


class StartResource:
    def on_get(self, request, response):
        response.set_header("Strict-Transport-Security", "max-age=31536000")
        start_template = Template(open("diploma/views/start.html", "r").read())
        response.content_type = "text/html"
        response.body = start_template.substitute(
            site="%s://%s" % (request.protocol, request.headers["HOST"]),
            diploma_id=generate_seed()
        )

class GenerateResource:
    def on_get(self, request, response):
        response.set_header("Strict-Transport-Security", "max-age=31536000")
        diploma_template = Template(open("diploma/views/diploma.html", "r").read())
        response.content_type = "text/html"
        response.body = diploma_template.substitute(
            site="%s://%s" % (request.protocol, request.headers["HOST"]),
            new_diploma_id=generate_seed(),
            **diploma(
                seed=request.get_param("diploma_id") or generate_seed(),
                name=request.get_param("name") or "John Doe"
            )
        )

def generate_seed():
    random.seed()
    return random.randint(0, sys.maxsize)

def diploma(seed, name):
    random.seed(seed)

    if os.path.isfile("universities.json"):
        with open("universities.json", "r") as f:
            university = random.choice(json.load(f))
    else:
        assert False, "Please run 'python run.py --get_universities'"

    # Guess language from country
    try:
        locale = Locale.parse("und_" + university["alpha_two_code"])
    except babel.core.UnknownLocaleError:
        locale = None

    signature1_name, signature2_name = get_names(locale.language if locale else "en", 2)
    signature1_title, signature2_title = get_titles(2)
    signature1_font, signature2_font = get_handwriting_fonts(2)

    if len(university["name"]) < 20:
        title_font_size = "4em"
    elif len(university["name"]) < 40:
        title_font_size = "3.3em"
    else:
        title_font_size = "2.5em"

    degree = random.choice(DEGREE_PREFIXES) + " " + random.choice(DEGREE_TYPES)
    major = random.choice(MAJORS)

    return {
        "fancy_font": random.choice(FANCY_FONTS),
        "title_font_size": title_font_size,
        "background": random.choice(BACKGROUNDS),
        "seal": random.choice(SEALS),

        "university_name": avoid_hanging_word(university["name"]),
        "university_country": university["country"].split(",")[0],
        "university_alpha_two_code": university["alpha_two_code"].lower(),
        "verb": avoid_hanging_word(random.choice(VERBS)),
        "name": name,
        "accomplishment": avoid_hanging_word(random.choice(ACCOMPLISHMENTS)),
        "degree": avoid_hanging_word(degree),
        "major": avoid_hanging_word(major),
        "granter": random.choice(GRANTERS),
        "proof": avoid_hanging_word(random.choice(PROOFS)),
        "signature1_name": signature1_name,
        "signature1_title": signature1_title,
        "signature1_font": signature1_font,
        "signature2_name": signature2_name,
        "signature2_title": signature2_title,
        "signature2_font": signature2_font,
        "date": dates.format_date(datetime.today(), locale=locale or "en")
    }

def get_names(language, num_names):
    names = set()

    while len(names) < num_names:
        try:
            name = Personal(language).full_name()
        except exceptions.UnsupportedLocale:
            name = Personal("en").full_name()

        name = avoid_hanging_word(name)
        names.add(name)

    return list(names)

def get_titles(num_titles):
    titles = set()

    while len(titles) < num_titles:
        title = avoid_hanging_word(random.choice(TITLES))
        titles.add(title)

    return list(titles)

def get_handwriting_fonts(num_fonts):
    fonts = set()

    while len(fonts) < num_fonts:
        font = random.choice(HANDWRITING_FONTS)
        fonts.add(font)

    return list(fonts)

def avoid_hanging_word(s):
    if len(s.split(" ")) > 3:
        return " ".join(s.split(" ")[:-2]) + " " + "&nbsp;".join(s.split(" ")[-2:])

    return s


BACKGROUNDS = [
    "01-whitepaper.png",
    "paper-5.jpg",
    "paper-10.jpg",
    "04-whitepaper.png",
]
SEALS = [
    "gold_seal.png",
    "wax_seal.png",
    "cwa_seal.png",
    "frat_seal.png",
    "navy_seal.png",
    "paper_stamp.gif",
    "stamp.gif",
]
FANCY_FONTS = [
    "diploma_regular.ttf",
    "chunkfive.otf",
    "proclamate_heavy.ttf",
    "proclamate_incised.ttf",
    "polaris.ttf",
]
HANDWRITING_FONTS = [
    "herr_von_muellerhoff.otf",
    "daniel_regular.otf",
    "scriptina.ttf",
    "toubib.ttf",
]
VERBS = [
    "has conferred on",
    "have conferred upon",
    "Be it know that",
    "This is to certify that",
]
ACCOMPLISHMENTS = [
    "having successfully completed the prescribed necessary requirements of this University",
    "has successfully completed all of the courses prescribed by the County Board of Administration for Graduation and is hereby awarded",
    "has met the standards established by the State Board of Education for successful completion of the tests of General Education Development and is",
]
DEGREE_PREFIXES = [
    "Master of",
    "Associate of",
    "Bachelor of",
    "Doctor of",
]
DEGREE_TYPES = [
    "Arts",
    "Fine Arts",
    "Science",
    "Applied Science",
    "Occupational Studies",
    "Business Adminstration",
]
MAJORS = [
    "Adventure Education",
    "Animal Breeding",
    "Astrobiology",
    "Auctioneering",
    "Audio Technology",
    "Bagpiping",
    "Bakery Science",
    "Baking Technology Management",
    "Bassoon",
    "Beatles, Popular Music and Society",
    "Bowling Industry Management and Technology",
    "Brewing and Distilling Master",
    "Cannabis Cultivation",
    "Caribbean Studies",
    "Chemical Hygiene Officer",
    "Circus and Physical Performance",
    "Citrus",
    "Clownology",
    "Conducting",
    "Cryptozoology",
    "Dairy Herd Management",
    "Ecogastronomy",
    "Egyptology",
    "Equestrian Psychology and Sports Science",
    "Ethical Hacking",
    "Fire Engineering",
    "Floral Design",
    "Folklore",
    "Gunsmithing",
    "Hand Embroidery",
    "Herbalism",
    "Horology",
    "Jazz Studies",
    "Juvenile Corrections",
    "Licensed Midwifery",
    "Logic",
    "Manga",
    "Mental Health Administration",
    "Metalsmithing",
    "Metaphysical Humanistic Science",
    "Mortuary Science",
    "Nannying",
    "Nautical Archaeology",
    "Packaging",
    "Paper Science and Engineering",
    "Parapsychology",
    "Parasitology",
    "Pastoral Counseling",
    "Personal Hygiene and Cosmetics",
    "Piano Pedagogy",
    "Popular Culture",
    "Poultry Science",
    "Puppet Arts",
    "Recreation and Leisure Studies",
    "Reiki",
    "Sacred Music",
    "Sexual Health Studies",
    "Somatic Psychology",
    "Speech-Language Pathology",
    "Stand-up Comedy",
    "Surf Science and Technology",
    "Theatre Practice & Puppetry",
    "Theme Park Engineering",
    "Turf and Golf Course Management",
    "Viking and Old Norse Studies",
    "Viticulture and Oenology",
    "Yacht Operations",
    "Yodelling",
]
GRANTERS = [
    "The Faculty and the Board of Trustees",
    "The State Board of Regents for the State University",
    "On recommendation of the Faculty and by virtue of the authority vested in them the trustees of this University",
    "By authority of the Board of Trustees on the recommendation of the Faculty",
    "The State Board of Regents",
]
PROOFS = [
    ", as evidence of the attainment and the granting of all rights pertaining to that degree.",
    "has issued this diploma."
    "and have granted this diploma as evidence thereof.",
    "in testimony whereof, this diploma is issued with the seal of the University and the signatures authorized by the Trustees hereunto affixed.",
    "with all the rights and privileges thereto pertaining.",
    "with all rights, privileges and honors thereunto appertaining.",
    "and has satisfactorily completed all required courses prescribed by an accredited Institution of Learning."

]
TITLES = [
    "Chairman of the Board of Governors",
    "President of the University",
    "Chairman of the Board of Trustees",
    "Chancellor",
    "Dean, Graduate School",
    "Secretary of the Board of Trustees",
    "President of the University",
    "Secretary of the University",
    "Officer of Development",
]
