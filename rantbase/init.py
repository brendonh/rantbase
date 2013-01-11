import sys
import os
import os.path
import shutil

def init(dir):
    print "Initializing in", dir

    if not os.path.exists(dir) or not os.path.isdir(dir):
        print "Not a directory"
        sys.exit(1)

    docDir = os.path.join(dir, 'docs')

    if not os.path.isdir(docDir):
        if os.path.exists(docDir):
            print "Doc path exists and is not a directory", docDir
            sys.exit(1)
        os.mkdir(docDir)

    htmlDir = os.path.join(dir, 'web')

    if not os.path.isdir(htmlDir):
        if os.path.exists(htmlDir):
            print "HTML path exists and is not a directory", htmlDir
            sys.exit(1)
        os.mkdir(htmlDir)

    webDir = os.path.join(os.path.dirname(__file__), 'priv/web')

    if not os.path.isdir(webDir):
        print "Can't find web dir at", webDir
        sys.exit(1)

    for thing in os.listdir(webDir):
        subDir = os.path.join(htmlDir, thing)
        if not os.path.exists(subDir):
            shutil.copytree(os.path.join(webDir, thing), subDir)

    defaultsDir = os.path.join(os.path.dirname(__file__), 'priv/defaults')
    configFile = os.path.join(defaultsDir, 'config.yml')

    if not os.path.exists(configFile):
        print "Can't find config file at", configFile
        sys.exit(1)

    configDest = os.path.join(dir, 'rantbase.yml')
    if not os.path.isfile(configDest):
        if os.path.exists(configDest):
            print "Config path exists and is not a file", configDest
            sys.exit(1)

        shutil.copyfile(configFile, configDest)

    dotRantDir = os.path.join(defaultsDir, 'dotrant')

    if not os.path.exists(dotRantDir):
        print "Can't find .rant dir at", dotRantDir
        sys.exit(1)

    dotRantDest = os.path.join(dir, '.rant')
    if not os.path.isdir(dotRantDest):
        if os.path.exists(dotRantDest):
            print ".rant exists and is not a file"
            sys.exit(1)

        shutil.copytree(dotRantDir, dotRantDest)
    
    import rantbase
    rantPath = os.path.dirname(os.path.dirname(rantbase.__file__))

    rantBin = """#!/usr/bin/env python
import sys
sys.path.insert(0, '%s')
import rantbase.__main__
""" % rantPath.replace(r"'", r"\'")

    rantDest = os.path.join(dir, 'rant')
    open(rantDest, 'w').write(rantBin)
    os.chmod(rantDest, 0755)

    print "Done"
