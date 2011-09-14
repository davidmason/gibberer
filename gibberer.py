"""Generates translation files with random strings for testing purposes.

Currently supports .properties format.

Run with no arguments for usage.

author: David Mason
email: damason@redhat.com

"""


# TODO see http://unicode.org/charts/ for more character ranges
# bangali uses some of 098x to 09Fx with a lot of holes http://unicode.org/charts/PDF/U0980.pdf


from datetime import datetime
import random, sys, codecs


# ranges of unicode characters for random string generation
# { locale : [(rangestart, rangeend), (rangestart, rangeend)] }
# None locale is used for the source strings (ascii range)
unicodeRanges = { None : [(0x0020, 0x005B), (0x005D, 0x007E)], #includes space, excludes \
                  'ja' : [(0x3041, 0x3096), (0x309B, 0x309F), (0x30A0, 0x30FF)],  # does not have kanji yet
                  'ru' : [(0x0400, 0x04FF)],
                  'th' : [(0x0E01, 0x0E3A), (0x0E3F, 0x0E5B)],
                  'zh' : [(0x4E00, 0x9FA5)],
                  'ar' : [(0x0600, 0x0603), (0x0606, 0x061B), (0x061E, 0x06FF)],
}

validPropsSeparators = ['=', ' = ', ':', ' ']


def generatePropertiesFiles(names=['test'], locales=[None], numDocs=1, numFlows=10, contentLength=20):
    """Generates a basic set of properties files with the given names, one
    set for each locale given"""
    
    print "generating {0} set(s) of files for {1} locale(s), each with {2} textflow(s).".format(len(names), len(locales), numFlows)
    
    for name in names:
        for locale in locales:
            print '.',
            sys.stdout.flush()
            f = createPropsFile(name, locale)
            writePropHeader(toFile=f, comment='Generated comment for {0} with locale {1}'.format(name, locale))
            writeTextFlows(toFile=f,
                           separators=validPropsSeparators,
                           textFlows=makeRandomTextFlows(locale=locale,
                                                         baseId=name+'id',
                                                         howMany=numFlows,
                                                         contentLength=contentLength), )
            f.write('\n')
            f.close()
    print ' Done!'


def createPropsFile(name='test', locale=None):
    """Returns a writeable properties file with the given name, in a directory
    for the locale and with a properties extension added."""
    
    # path = ''
    if locale is not None:
        name = name + '_' + locale
        # path = locale + '/'
    # name = path + name;
    return codecs.open(name+'.properties', mode='w', encoding='latin-1')

def writePropHeader(toFile, comment):
    """Writes a header for a property file.
    
    toFile will have the header written and will be left open"""
    
    toFile.write('# file generated at ' + str(datetime.now()) + '\n')
    toFile.write('# ' + comment + '\n')

    
def writeTextFlows(toFile, textFlows, separators):
    """Writes the given list of textflows to the given file.
    
    testFlows should be in the form [('id1', 'content1'), ('id2', 'content2')]
    separator should be a list of 1 or more standard separators to use between id and content
    """
    
    if len(separators) < 1:
        raise ValueError('This method needs at least one separator, but was given ' + str(separators))
    
    for flow in textFlows:
        try:
            ident, content = flow
        except ValueError:
            raise ValueError(''.join(['tuples in textFlows should have 2 items, but ' , str(flow), ' has ', str(len(flow))]))
        toFile.write(''.join([ident, random.choice(separators), content, '\n']))


def makeRandomTextFlows(locale=None, baseId='id', howMany=10, contentLength=20):
    """Generates text flows with random content in the unicode range for the
    given locale. Uses ascii range if locale is None
    
    locale must be one of: [jp, zh, ru, ar, th] TODO add more
    """
    
    flows = []
    for number in range(howMany):
        flows.append((baseId+str(number), makeRandomString(length=contentLength, locale=locale)))
    return flows


def makeRandomString(length, locale):
    """Returns a random string of characters used for the given locale"""
    # TODO need to check for escape characters \ in here, probably replace with \\
    # currently do not have \ in the list of characters so it isn't a problem
    return makeRandomUnicodeString(length, unicodeRanges[locale]).encode('unicode_escape')


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
    

def makeTextFlows(howMany=10, baseId='id', baseContent='content'):
    """Generates howMany text flows as tuples in the form (id, content)"""
    
    flows = []
    for number in range(1, howMany):
        flows.append((baseId+str(number), baseContent+str(number)))
    return flows
    
USAGE = 'USAGE:\npython gibberer.py <baseFileName> [<number of documents> [<number of flows> [<contentLength>]]]'

if __name__ == '__main__':
    
    # defaults
    numDocs = 1
    numFlows = 20    
    contentLen = 20
    
    if (len(sys.argv) == 1):
        print USAGE
    else:
        if (len(sys.argv) > 1):
            baseName = sys.argv[1]
        if (len(sys.argv) > 2):
            numDocs = int(sys.argv[2])
        if (len(sys.argv) > 3):
            numFlows = int(sys.argv[3])
        if (len(sys.argv) > 4):
            contentLen = int(sys.argv[4])
        
        if numDocs == 1:
            names = [baseName]
        else:
            names = []
            for num in range(numDocs):
                names.append(baseName + str(num))
        
        generatePropertiesFiles(names=names, locales=unicodeRanges.keys(), numFlows=numFlows, contentLength=contentLen)



