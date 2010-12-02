#!/usr/bin/python2
# vim:fileencoding=utf8
import subprocess, parameters, shutil, os

from optparse import OptionParser
from datetime import datetime

parser = OptionParser()
parser.add_option("-f", "--fps", dest="fps", default=100, help="Film frames per second")
parser.add_option("-o", "--output", dest="output", help="Output to FILE", 
        metavar="FILE")
parser.add_option("-p", "--prefix", dest="prefix", help="Image prefix (default from parameters.py)")

(options, args) = parser.parse_args()

if options.prefix is None:
    options.prefix = parameters.image_prefix

parameters_file = "%sparameters" % options.prefix
pfile = open(parameters_file)
s = [i for i in pfile if i.startswith(" 'run_time'")][0]
d = eval("{%s}" % s)
run_time = datetime.strptime(d['run_time'], "%Y-%m-%d %H:%M:%S")

if options.output is None:
    (dirpart, filepart) = os.path.split(options.prefix)
    options.output = "films/%s%s-%sfps.avi" % \
    (filepart, run_time.strftime("%Y%m%d_%H%M"), options.fps)

shutil.copy(parameters_file, "%s.parameters" % options.output)


args = [
    'mencoder',
    '-profile', 'mpeg4.singlepass',
    '-o', options.output, 
    '-mf', 'type=png:fps=%s' % options.fps,
    'mf://%s*.png' % options.prefix,
]

subprocess.call(args)
