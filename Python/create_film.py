#!/usr/bin/python2
# vim:fileencoding=utf8
import subprocess, shutil, os, sys

from optparse import OptionParser
from datetime import datetime

import constants

parser = OptionParser()
parser.add_option("-f", "--fps", dest="fps", default=100, help="Film frames per second")
parser.add_option("-o", "--output", dest="output", help="Output to FILE", 
        metavar="FILE")
parser.add_option("-d", "--directory", dest="directory", help="Image directory")

(options, args) = parser.parse_args()

if options.directory is None:
    options.directory = constants.image_dir

if not len(args):
    print "Missing scenario name"
    sys.exit(1)

scenario = args[0]

parameters_file = "%s-parameters" % os.path.join(options.directory, scenario)
try:
    pfile = open(parameters_file)
    s = [i for i in pfile if i.startswith(" 'run_time'")][0]
    d = eval("{%s}" % s)
    run_time = datetime.strptime(d['run_time'], "%Y-%m-%d %H:%M:%S")
except IOError:
    print "Unable to open parameters file - wrong scenario or missing files?"
    sys.exit(1)

if options.output is None:
    options.output = "films/%s-%s-%sfps.avi" % \
    (scenario, run_time.strftime("%Y%m%d_%H%M"), options.fps)

shutil.copy(parameters_file, "%s.parameters" % options.output)

image_path = os.path.join(options.directory, scenario)

try:
    os.stat("%s-00001.png")
    ext = "png"
except OSError:
    ext = "tga"

args = [
    'mencoder',
    '-profile', 'mpeg4.singlepass',
    '-o', options.output, 
    '-mf', 'type=%s:fps=%s' % (ext, options.fps),
    'mf://%s-*.%s' % (os.path.join(options.directory, scenario),ext),
]

subprocess.call(args)
