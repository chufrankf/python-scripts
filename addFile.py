import argparse
import json
import os.path
import sys
from shutil import copyfile

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__home__ = os.path.expanduser('~')

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    else:
        return False

# Open the json file
with open(os.path.join(__location__,'addFile.json'), 'r') as json_file:
    data = json.load(json_file)

# Create a file given name, template, and folder
parser = argparse
parser = argparse.ArgumentParser(description='This is a generic script used to add files into a folder based off a template')
parser.add_argument("filename", type=str, help="the name of the file you want to save, please dont include the extension")
parser.add_argument("-t", "--template", type=str, help="copy everything from this file to the new file")
parser.add_argument("-f", "--folder", type=str, help="folder where you want to save the file")
parser.add_argument("-v", "--verbose", action="store_true", help="increases verbosity")
parser.add_argument("--add-folder", type=str, help="add a folder to contain the new file in")

for key,val in data['cmds'].items():
    parser.add_argument("--" + key, action="store_true", help="Default folder:{" + val["folder"] + "} Default template:{" + val["template"] +"}")

args = parser.parse_args()

# Generate default folders and templates
folder = None
template = None

if( args.verbose ):
    print args

for key,val in data['cmds'].items():
    if getattr(args, key):
        folder = val["folder"]
        template = val["template"]

folder = ( (os.path.realpath(args.folder) if args.folder else None ) or folder ) or __home__
folder = ( os.path.join(folder, args.add_folder) if args.add_folder else folder)
template = ( (os.path.realpath(args.template) if args.template else None ) or template ) or None

if template:
    template = os.path.expanduser(template)
if folder:
    folder = os.path.expanduser(folder)

# Validate
if template and not os.path.isfile(template):
    print "ERROR: " + template + " is not a valid file. Setting template to None"
    template = None

if( not yes_or_no( "CREATE " + args.filename + " IN " + folder +  (" USING " + template if template else "") + "?" ) ):
    sys.exit("Stopped")

# Check that the folder exists, if not create it
if not os.path.isdir(folder):
    os.makedirs(folder)

# Create the new file
if template:
    copyfile(template, os.path.join(folder, args.filename) )
else:
    open(os.path.join(folder, args.filename), 'a').close()
