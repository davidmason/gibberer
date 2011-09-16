
import codecs, polib

from datetime import datetime
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
        header = makePoHeader(name)
        f.header = header
        meta = makePoMetadata()
        f.metadata.update(meta)
        addTextFlows(toFile=f, textFlows=flows)
        savePoFile(f, outputDir, name, None)
        
        #write the targets
        for locale in locales:
            f = polib.POFile()
            f.encoding='utf-8' #TODO is this needed?
            f.header = header
            f.metadata.update(meta)
            
            addTextFlows(toFile=f, textFlows=flows, locale=locale)
            savePoFile(f, outputDir, name, locale)


# see here for header info http://translate.sourceforge.net/wiki/guide/project/howto

def makePoHeader(name):
    header = "Generated title for %(name)s\n"
    header += "Copyright (C) %(name)s %(year)s.\n"
    header += "This file is distributed under the same license as the %(name)s package.\n"
    header += "Gibberer Gibberer gibberer@example.com, %(year)s\n"
    return header % {'name': name, 'year': datetime.now().year}
    
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

def makePoMetadata():
    """Pass the po file's metadata to this function to have the values set"""
    
    meta = {
        u'Project-Id-Version' : u'0',
        u'Report-Msgid-Bugs-To' : u'gibberer@example.com',
        u'POT-Creation-Date' : unicode(datetime.now().strftime(TIME_FORMAT)),
        u'PO-Revision-Date' : unicode(datetime.now().strftime(TIME_FORMAT)),
        u'Last-Translator' : u'The Gibberer',
        u'Language-Team' : u'Gibberish Team',
        u'MIME-Version' : u'1.0',
        u'Content-Type' : u'application/x-publican; charset=UTF-8',
        u'Content-Transfer-Encoding' : u'8bit',
        u'Plural-Forms' : u'nplurals=2; plural=n != 1;'
    }
    
    #could make plural forms correct for different locales. Not worth the bother at the moment
    
    return meta



def addTextFlows(toFile, textFlows, locale=None):
    """Writes text flows. If no locale is specified, source is assumed."""
    
    isSource = (locale is None)
    
    for flow in textFlows:
        poentry = polib.POEntry()
        poentry.msgid = flow.content
        poentry.occurrences = flow.occurrences
        poentry.comment = flow.extracted_comment


        if isSource:
            poentry.msgstr = ''
        else:
            target = flow.getTarget(locale)
            poentry.msgstr = target.content
            poentry.tcomment = target.comment
            poentry.flags = target.flags
            
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


