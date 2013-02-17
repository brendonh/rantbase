import argparse

from rantbase import commands

parser = argparse.ArgumentParser(description='Manage a rantbase.')
subparsers = parser.add_subparsers(help='sub-command help')

init = subparsers.add_parser('init', help="Initialize a rantbase")
init.add_argument('dir', help="Base directory of rantbase (default '.')", 
                  nargs='?', default=".")
init.set_defaults(func=commands.runInit)

update = subparsers.add_parser('update', help="Update everything")
update.add_argument('dir', help="Base directory of rantbase (default '.')", 
                  nargs='?', default=".")
update.add_argument('-f', '--force', help="Update files even if they don't seem out of date", 
                    action='store_const', const=True)
update.set_defaults(func=commands.runUpdate)

args = parser.parse_args()
args.func(args)
