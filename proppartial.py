"""Custom properties file generator for only partial translation coverage.

"""

import proputil
from fileutil import ensure_dir
from flowutil import makeRandomTextFlows
from proputil import createPropsFile, writePropHeader, writeTextFlows

outputDir = 'output/properties/partial/'

partials = {'ja' : 1,
            'zh' : 2,
            'ru' : 20,
}

def generatePartialTransPropertiesFiles(names, locales, numFlows, contentLength):
    """Generate properties files with different translation coverage between locales"""
    
    ensure_dir(outputDir)
    
    for name in names:
        flows = makeRandomTextFlows(locales, name+'_id', numFlows, contentLength)
        
        f = createPropsFile(outputDir, name)
        writePropHeader(toFile=f, comment='Generated comment for {0} with locale {1}'.format(name, None))
        writeTextFlows(toFile=f, textFlows=flows)
        f.write('\n')
        f.close()

        for locale in locales:
            f = createPropsFile(outputDir, name, locale)
            writePropHeader(toFile=f, comment='Generated comment for {0} with locale {1}'.format(name, locale))
            writeTextFlows(toFile=f, textFlows=flows, locale=locale, useEach=partials[locale])
            f.write('\n')
            f.close()


if __name__ == "__main__":
    names=[]
    for num in range(6):
        names.append("doc"+str(num))
    locales = ['ja', 'zh', 'ru']
    numFlows = 200
    contentLength = 100
    generatePartialTransPropertiesFiles(names, locales, numFlows, contentLength)
    
