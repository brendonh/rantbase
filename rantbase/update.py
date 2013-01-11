import sys
import os.path
import shutil
import codecs
import re
import collections

import yaml
import markdown
from mako.template import Template

def update(dir, force=False):
    print "Updating", dir

    configFile = os.path.join(dir, 'rantbase.yml')

    if not os.path.isfile(configFile):
        print "Can't find config file at", configFile
        sys.exit(1)
    
    config = yaml.load(open(configFile))

    docDir = os.path.join(dir, 'docs')

    if not os.path.isdir(docDir):
        print "Doc dir is not a directory:", docDir
        sys.exit(1)

    markdowns = []
    assets = []

    for root, dirs, files in os.walk(docDir):
        relRoot = os.path.relpath(root, docDir)
        webRoot = os.path.normpath(os.path.join(dir, 'web', relRoot))

        for f in files:

            docPath = os.path.join(root, f)
            webPath = os.path.join(webRoot, f)

            if os.path.exists(webPath) and not force:
                docTime = os.stat(docPath).st_mtime
                webTime = os.stat(webPath).st_mtime
                if docTime <= webTime:
                    print "Skipping", docPath
                    continue

            (baseName, ext) = os.path.splitext(webPath)
            if ext.lower() == '.md':
                collection = markdowns
                webPath = "%s.html" % baseName
            else:
                collection = assets

            collection.append((docPath, webPath))


    for _, webPath in assets + markdowns:
        webDir = os.path.dirname(webPath)
        
        if not os.path.exists(webDir):
            print "Creating directory", webDir
            os.makedirs(webDir)


    for docPath, webPath in assets:
        print "Copying", docPath, "to", webPath
        shutil.copyfile(docPath, webPath)


    if markdowns:
        templatePath = os.path.join(dir, ".rant", "page_template.html")
        if not os.path.exists(templatePath):
            print "Template file missing:", templatePath
            sys.exit(1)

        template = Template(filename=templatePath)
        tagRE = re.compile(r'#(\w+)')
        byTag = collections.defaultdict(list)

        for docPath, webPath in markdowns:
            print "Markdowning", docPath, "to", webPath
            
            title = os.path.splitext(os.path.basename(docPath))[0].replace('_', ' ').title()

            markupFile = codecs.open(docPath, mode="r", encoding="utf-8")
            
            tagLine = markupFile.next().strip()
            
            if tagLine.startswith('#'):
                tags = tagRE.findall(tagLine)
                webUrl = os.path.relpath(webPath, os.path.join(dir, 'web'))
                for tag in tags:
                    byTag[tag].append((title, webUrl))
            else:
                markupFile.seek(0)
                tags = []

            markup = markupFile.read()

            content = markdown.markdown(markup)
            html = template.render_unicode(
                config=config,
                content=content,
                title=title,
                tags=tags)
            codecs.open(webPath, mode='w', encoding="utf-8").write(html)


        indexTemplatePath = os.path.join(dir, ".rant", "index_template.html")
        if not os.path.exists(indexTemplatePath):
            print "Index template file missing:", indexTemplatePath
            sys.exit(1)

        indexTemplate = Template(filename=indexTemplatePath)

        indexContent = indexTemplate.render_unicode(
            config=config,
            title=u"Index",
            byTag=dict(byTag))

        indexHtml = template.render_unicode(
            config=config,
            content=indexContent,
            title=u"Index",
            tags=[])

        indexPath = os.path.join(dir, 'web', 'index.html')
        codecs.open(indexPath, mode='w', encoding="utf-8").write(indexHtml)

