
import codecs, polib

from fileutil import ensure_dir
from flowutil import makeRandomTextFlows

outputDir = 'output/po/'


def generatePoFiles(names, locales, numFlows, contentLength):
    """Generates a mock pot file for each name with associated mock po files for each locale"""
    
    ensure_dir(outputDir)
    
    for name in names:
        flows = makeRandomTextFlows(locales, name, numFlows, contentLength)
        
        #write the source file
        f = polib.POFile()
        #TODO write some sort of header (in targets too)
        # see here for header info http://translate.sourceforge.net/wiki/guide/project/howto
        addTextFlows(toFile=f, textFlows=flows)
        savePoFile(f, outputDir, name, None)
        
        #write the targets
        for locale in locales:
            f = polib.POFile()
            f.encoding='utf-8'
            addTextFlows(toFile=f, textFlows=flows, locale=locale)
            savePoFile(f, outputDir, name, locale)


def addTextFlows(toFile, textFlows, locale=None):
    """Writes text flows. If no locale is specified, source is assumed."""
    
    isSource = (locale is None)
    
    for flow in textFlows:
        poentry = polib.POEntry()
        poentry.msgid = flow.content

        if isSource:
            poentry.msgstr = ''
        else:
            target = flow.getTarget(locale)
            poentry.msgstr = target.content
            poentry.occurrences = target.occurrences
            poentry.comment = target.extracted_comment
            poentry.tcomment = target.comment
            
        toFile.append(poentry)
    



#TODO add options for subdirs and for whether to append locale to name
#TODO put the dir and locale appending stuff in fileutil
#TODO add encoding option here - aim is to support all encodings listed here:
# http://www.gnu.org/software/gettext/manual/gettext.html#index-charset-of-PO-files-268
def savePoFile(pofile, path, name, locale):
    """Writes a po file with the given name, in a directory
    for the locale and with a po or pot extension added."""
    
    if locale is not None:
        path += locale + '/'
        name = name + '.po'
    else:
        name = name + '.pot'

    ensure_dir(path)
    
    #TODO this currently lacks an encoding header, could be an issue
    pofile.save(path+name)


