#!/usr/bin/python2
# vim:fileencoding=utf8
import subprocess, parameters

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
if options.output is None:
    options.output = "films/%s-%sfps.avi" % \
    (datetime.now().strftime("%Y%m%d%H%M"), options.fps)


args = [
    'mencoder',
    '-profile', 'mpeg4.singlepass',
    '-o', options.output, 
    '-mf', 'type=png:fps=%s' % options.fps,
    'mf://%s*.png' % options.prefix,
]

subprocess.call(args)
