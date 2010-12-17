#!/usr/bin/python2
# vim:fileencoding=utf8

import constants
from parameters import scenarios

import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-S", "--hide-simulation", 
        default=True, action="store_false", dest="show_simulation",
        help="hide the simulation while running")
parser.add_option("-i", "--create-images",
        default=False, action="store_true", dest="create_images",
        help="store images of each frame")
parser.add_option("-p", "--create-plots",
        default=False, action="store_true", dest="create_plots",
        help="create plots")
parser.add_option("-a", "--aggregate",
        default=False, action="store_true", dest="aggregate",
        help="aggregate from multiple runs (implies -p)")
parser.add_option("-t", "--tikz",
        default=False, action="store_true", dest="tikz",
        help="Draw tikz images")
parser.add_option("", "--profile",
        action="store_true", dest="profile", default=False,
        help="enable profiling of code")

def main(options, args):
    if options.aggregate:
        options.create_plots = True

    if not len(args):
        if len(scenarios) > 1:
            print "Missing scenario (options: %s)" % ",".join(scenarios.keys())
            return
        else:
            scenario = scenarios.keys()[0]
    else:
        scenario = args[0]

    if not scenario in scenarios:
        print "Invalid scenario: %s (options: %s)" % (scenario,
                ",".join(scenarios.keys()))
        return

    scenarios[scenario].run(options)


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.profile:
        import cProfile
        cProfile.run("main(options, args)")
    else:
        main(options, args)
