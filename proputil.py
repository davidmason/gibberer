"""Generates properties files from text flows"""

import codecs, flowutil, random, sys
from datetime import datetime
from fileutil import ensure_dir
from flowutil import makeRandomTextFlows

#TODO escape the \ character, like \\

validPropsSeparators = ['=', ' = ', ':', ' ']
outputDir = 'output/properties/'

def generatePropertiesFiles(names, locales, numFlows, contentLength):
    """Generates a basic set of properties files with the given names, one
    set for each locale given"""
    
    ensure_dir(outputDir)
    
    for name in names:
        flows = makeRandomTextFlows(locales, name+'_id', numFlows, contentLength)
        
        f = createPropsFile(outputDir, name)
        writePropHeader(toFile=f, comment='Generated comment for {0} with locale {1}'.format(name, None))
        writeTextFlows(toFile=f, separators=validPropsSeparators,
                       textFlows=flows)
        f.write('\n')
        f.close()

        for locale in locales:
            f = createPropsFile(outputDir, name, locale)
            writePropHeader(toFile=f, comment='Generated comment for {0} with locale {1}'.format(name, locale))
            writeTextFlows(toFile=f, separators=validPropsSeparators,
                           textFlows=flows, locale=locale)
            f.write('\n')
            f.close()



def createPropsFile(path, name, locale=None):
    """Returns a writeable properties file with the given name and locale code
    and a properties extension added."""
    #TODO add option to put targets in subdirectories
    if locale is not None:
        name = name + '_' + locale
        # path = locale + '/'
    #ensure_dir(path)
    return codecs.open(path+name+'.properties', mode='w', encoding='latin-1')


def writePropHeader(toFile, comment):
    """Writes a header for a property file.
    
    toFile will have the header written and will be left open"""
    
    toFile.write('# file generated at ' + str(datetime.now()) + '\n')
    toFile.write('# ' + comment + '\n')

    
def writeTextFlows(toFile, textFlows, separators=validPropsSeparators, locale=None, useEach=1):
    """Writes the given list of textflows to the given file.
    
    textFlows should be in the form [('id1', 'content1'), ('id2', 'content2')]
    separator should be a list of 1 or more standard separators to use between id and content
    
    set useEach to a value higher than one to write out less textflows.
    """
    if len(separators) < 1:
        raise ValueError('This method needs at least one separator, but was given ' + str(separators))
    
    isSource = (locale is None)
    count = 0

    for flow in textFlows:
        count += 1
        if count % useEach == 0:
            ident = flow.flowId
            
            if isSource:
                content = flow.content
            else:
                target = flow.getTarget(locale)
                content = target.content
                #not doing target comments etc. for now
            
            toFile.write(''.join([ident, random.choice(separators), content.encode('unicode_escape'), '\n']))

