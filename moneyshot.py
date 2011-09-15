#!/usr/bin/python

import sys
import colors
import outputter
import codelibrary
import codeparameters
import pprint

def banner():
	ms_fancy  = colors.bold() + colors.fg('yellow') + "$$$ " + colors.end()
	ms_fancy += colors.bold() + "moneyshot" + colors.end()
	ms_fancy += " by "
	ms_fancy += colors.bold() + "blasty"  + colors.end()
	ms_fancy += colors.bold() + colors.fg('yellow') + " $$$" + colors.end()

	print "\n " + ms_fancy + "\n"

def warning(instr):
	print "  " + colors.fg('red') + colors.bold() + "!!" + colors.end() + " " + instr

def action_list(path = ""):
	codes = codelibrary.find_codes(path)
	codelibrary.print_codes(codes)

def action_build(codename, inparams):
	params = { }

	outfunc = {
		'c'       : outputter.c,
		'php'     : outputter.php,
		'perl'    : outputter.perl,
		'hexdump' : outputter.hexdump
	}

	# parse user args
	for keyval in inparams:
		if len(keyval.split("=")) == 2:
			(key, val) = keyval.split("=")
			params[key] = val

	if 'outformat' not in params:
		params['outformat'] = "c"

	codenames = codename.split(',')

	bincode = ''

	for curname in codenames:
		shellcode = codelibrary.get_by_name(curname)

		if "parameters" in shellcode:
			shellcode = codeparameters.handle_parameters(shellcode, params)

		bincode += outputter.hex_bin(shellcode['code'])


	outformat = params['outformat']
	print "\n\n" + outfunc[ outformat ](bincode, fancy = True)

	if 'outfile' in params:
		rawoutput = outfunc[ outformat](bincode, fancy = False)
		f = open(params['outfile'], 'w')
		f.write(rawoutput)
		f.close()


## main program flow
banner()

if len(sys.argv) == 1:
	print "no action given"
	exit()

action = sys.argv[1]

codelibrary.load_codes("codes")

if action == "list":
	if len(sys.argv) == 3:
		action_list(sys.argv[2])
	else:
		action_list()

elif action == "build":
	action_build(sys.argv[2], sys.argv[2:])