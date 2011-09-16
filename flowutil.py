"""A collection of methods for generating randomized text flows in various
unicode ranges.

"""

# TODO see http://unicode.org/charts/ for more character ranges
# bangali uses some of 098x to 09Fx with a lot of holes http://unicode.org/charts/PDF/U0980.pdf

# ranges of unicode characters for random string generation
# { locale : [(rangestart, rangeend), (rangestart, rangeend)] }
# None locale is used for the source strings (ascii range)
unicodeRanges = { #None : [(0x0020, 0x005B), (0x005D, 0x007E)], #includes space, excludes \
                  None : [(0x0020, 0x007E)], #includes \ as this should be escaped if required
                  'ja' : [(0x3041, 0x3096), (0x309B, 0x309F), (0x30A0, 0x30FF)],  # does not have kanji yet
                  'ru' : [(0x0400, 0x04FF)],
                  'th' : [(0x0E01, 0x0E3A), (0x0E3F, 0x0E5B)],
                  'zh' : [(0x4E00, 0x9FA5)],
                  'ar' : [(0x0600, 0x0603), (0x0606, 0x061B), (0x061E, 0x06FF)],
}


import random

SOURCE_EXTENSIONS = ['.c', '.py', '.cpp', '.sh', '.xml']


def listSupportedLocales():
    locales = unicodeRanges.keys()
    locales.remove(None)
    return locales


def makeRandomTextFlows(locales, baseId, howMany, contentLength):
    """Generates text flows with targets for the given locales.
    
    Valid locales for this function are returned by listSupportedLocales()
    
    """
    
    flows = []
    for number in range(howMany):
        flow = TextFlow(baseId+str(number),
                        content=makeRandomString(length=contentLength, locale=None),
                        extracted_comment=makeRandomString(length=contentLength, locale=None))
        flow.addRefs([(baseId+'ref'+random.choice(SOURCE_EXTENSIONS), random.randint(0, 1000))])
        for locale in locales:
            targ = Target(content=makeRandomString(length=contentLength,locale=locale),
                          comment=makeRandomString(length=contentLength, locale=locale),
                          flags=random.choice([ [], ['fuzzy'] ]))
            flow.putTarget(locale, targ)
        flows.append(flow)
    return flows


def makeRandomString(length, locale):
    """Returns a random string of characters used for the given locale"""

    return makeRandomUnicodeString(length, unicodeRanges[locale])


def makeRandomUnicodeString(length, ranges):
    """Returns a string of random unicode characters within the given unicode
    code points"""
    
    points = []
    for r in ranges:
        start, end = r
        points.extend(range(start, end))
    
    theString = u''
    for pos in range(length):
        theString = theString + unichr(random.choice(points))
    return theString




#TODO don't think this is used anywhere, or will be used.
# may be able to offer a non-random option for source content, could be useful for some tests
def makeTextFlows(howMany, baseId, baseContent):
    """Generates howMany text flows as tuples in the form (id, content)"""
    
    flows = []
    for number in range(1, howMany):
        flows.append((baseId+str(number), baseContent+str(number)))
    return flows



class TextFlow:
    """A source string and associated """
    
    def __init__(self, flowId, content, extracted_comment=''):
        self.flowId=flowId
        self.content=content
        self.targets = {}
        self.occurrences = []
        self.extracted_comment = extracted_comment

    def addRefs(self, references):
        self.occurrences.extend(references)
    
    def putTarget(self, locale, target):
        """target should be of type Target"""
        self.targets[locale] = target
    
    def getTarget(self, locale):
        """Return a target, or None if locale is None"""
        if locale is None:
            return None
        else:
            return self.targets.get(locale)
    
class Target:
    """A single target content with comments and other extensions.
    
    Uses identifiers like gettext at the moment, but could expand to include
    things used for other formats.
    """
    
    def __init__(self, content, comment='', flags=[]):
        self.content = content
        self.flags = flags
        self.comment = comment











