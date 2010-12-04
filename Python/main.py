#!/usr/bin/python2
# vim:fileencoding=utf8

import constants
from parameters import scenarios

import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--show-simulation", 
        default=constants.show_simulation, action="store_true", dest="show_simulation",
        help="show the simulation while running")
parser.add_option("-S", "--hide-simulation", 
        action="store_false", dest="show_simulation",
        help="hide the simulation while running")
parser.add_option("-i", "--create-images",
        default=constants.create_images, action="store_true", dest="create_images",
        help="store images of each frame")
parser.add_option("-I", "--no-create-images",
        action="store_false", dest="create_images",
        help="do not store images of each frame")
parser.add_option("-p", "--create-plots",
        default=constants.create_plots, action="store_true", dest="create_plots",
        help="create plots")
parser.add_option("-P", "--no-create-plots",
        action="store_false", dest="create_plots",
        help="do not create plots")
parser.add_option("", "--trace",
        action="store_true", dest="trace", default=False,
        help="enable trace when drawing")
parser.add_option("", "--profile",
        action="store_true", dest="profile", default=False,
        help="enable profiling of code")


def main(options, args):

    if not len(args):
        print "Missing scenario (options: %s)" % ",".join(scenarios.keys())
        return

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
