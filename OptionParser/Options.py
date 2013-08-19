

from optparse import OptionParser
parser = OptionParser("Options.py [options]")
parser.add_option("--logging",dest="log_on", action='store_true', help="Enable Logging")
parser.add_option("--port",dest="port", default="1023", help="UDP Port")

(opts, args) = parser.parse_args()



if opts.log_on == True:
    print "Logging Enabled"
elif opts.log_on == False:
    print "Logging Disabled"
else:
    parser.print_help()

# print opts.port
