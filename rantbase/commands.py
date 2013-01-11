from rantbase import init, update

def runInit(args):
    init.init(args.dir)

def runUpdate(args):
    update.update(args.dir, bool(args.force))
