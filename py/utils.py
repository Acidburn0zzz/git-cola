#!/usr/bin/env python
import os
import re
import commands

KNOWN_FILE_TYPES = {
	'ascii c':   'c.png',
	'python':    'script.png',
	'ruby':      'script.png',
	'shell':     'script.png',
	'perl':      'script.png',
	'java':      'script.png',
	'assembler': 'binary.png',
	'binary':    'binary.png',
	'byte':      'binary.png',
	'image':     'image.png',
}

ICONSDIR = os.path.join (os.path.dirname (__file__), 'icons')

def ident_file_type (filename):
	'''Returns an icon based on the contents of filename.'''
	if os.path.exists (filename):
		quoted_filename = shell_quote (filename)
		fileinfo = commands.getoutput('file -b %s' % quoted_filename)
		for filetype, iconname in KNOWN_FILE_TYPES.iteritems():
			if filetype in fileinfo.lower():
				return iconname
	else:
		return 'removed.png'
	# Fallback for modified files of an unknown type
	return 'generic.png'

def get_icon (filename):
	'''Returns the full path to an icon file corresponding to
	filename's contents.'''
	icon_file = ident_file_type (filename)
	return os.path.join (ICONSDIR, icon_file)

def get_staged_icon (filename):
	'''Special-case method for staged items.  These are only
	ever 'staged' and 'removed' items in the staged list.'''

	if os.path.exists (filename):
		return os.path.join (ICONSDIR, 'staged.png')
	else:
		return os.path.join (ICONSDIR, 'removed.png')

def get_untracked_icon():
	return os.path.join (ICONSDIR, 'untracked.png')

def get_directory_icon():
	return os.path.join (ICONSDIR, 'dir.png')

def get_file_icon():
	return os.path.join (ICONSDIR, 'generic.png')

def shell_quote (*inputs):
	'''Quote strings so that they can be suitably martialled
	off to the shell.  This method supports POSIX sh syntax.
	This is crucial to properly handle command line arguments
	with spaces, quotes, double-quotes, etc.'''

	regex = re.compile ('[^\w!%+,\-./:@^]')
	quote_regex = re.compile ("((?:'\\''){2,})")

	ret = []
	for input in inputs:
		if not input:
			continue

		if '\x00' in input:
		    raise AssertionError, ('No way to quote strings '
				'containing null (\\000) bytes')

		# = does need quoting else in command position it's a
		# program-local environment setting
		match = regex.search (input)
		if match:
			# ' -> '\''
			input = input.replace ("'", "'\\''")

			# make multiple ' in a row look simpler
			# '\'''\'''\'' -> '"'''"'
			quote_match = quote_regex.match (input)
			if quote_match:
				quotes = match.group (1)
				input.replace (quotes,
					("'" * (len(quotes)/4)) + "\"'")

			input = "'%s'" % input
			if input.startswith ("''"):
				input = input.lstrip ("''")

			if input.endswith ("''"):
				input = input.rstrip ("''")
		ret.append (input)
	return ' '.join (ret)

ANSI_BACKGROUND_COLOR = '41'
ANSI_TABLE = {
	'1':  'grey',
	'30': 'black',
	'31': 'red',
	'32': 'green',
	'33': 'yellow',
	'34': 'blue',
	'35': 'magenta',
	'36': 'cyan',
	'37': 'white',
}

def ansi_to_html (ansi):
	'''Converts a block of ANSI text into an equivalent html fragment.'''

	html = []
	regex = re.compile ('(.*?)\x1b\[(\d*)m')

	for line in ansi.split ('\n'):

		linecopy = html_encode(line)
		match = regex.match (linecopy)
		tagged = False

		while match:
			start, end = match.span()

			prefix = match.group (1)
			middle = match.group (2)
			postfix = linecopy[end:]

			if middle in ANSI_TABLE:
				color = ANSI_TABLE[middle]
				middle = '<span style="color: %s">' % color
				tagged = True

			elif middle == ANSI_BACKGROUND_COLOR:
				middle = '<span style="background-color:red">'
				tagged = True

			else:
				if tagged:
					middle = '</span>'
				else:
					middle = ''

			linecopy = prefix + middle + postfix
			match = regex.match (linecopy)

		html.append (linecopy)

	return '<br/>'.join (html)

def html_header (header):
	return '''
		<p style="color: black;
			background-color: yellow">
			%s
		</p>''' % header

def html_encode (ascii):
	'''HTML-encodes text.  This method explicitly avoids encoding
	alphanumeric and ANSI-escape sequences.'''

	html = []
	for char in ascii:
		if char.isalnum():
			html.append (char)

		elif char == '\t':
			# There is no HTML equivalent to a tab, so just
			# insert eight spaces
			html.append ( '&nbsp;' * 8 )

		elif char == '\x1b' or char == '[':
			# Don't encode ANSI characters since these
			# are stripped out during ansi_to_html
			html.append (char)

		else:
			html.append (ENTITIES[char])

	return ''.join (html)

# Keep this at the bottom of the file since it's generated output.
# Generated by html2py.pl from HTML::Entities on Wed Dec  5 16:28:55 PST 2007
ENTITIES = {
	chr(0)	:	'&#0;',
	chr(1)	:	'&#1;',
	chr(2)	:	'&#2;',
	chr(3)	:	'&#3;',
	chr(4)	:	'&#4;',
	chr(5)	:	'&#5;',
	chr(6)	:	'&#6;',
	chr(7)	:	'&#7;',
	chr(8)	:	'&#8;',
	chr(9)	:	'&#9;',
	chr(10)	:	'&#10;',
	chr(11)	:	'&#11;',
	chr(12)	:	'&#12;',
	chr(13)	:	'&#13;',
	chr(14)	:	'&#14;',
	chr(15)	:	'&#15;',
	chr(16)	:	'&#16;',
	chr(17)	:	'&#17;',
	chr(18)	:	'&#18;',
	chr(19)	:	'&#19;',
	chr(20)	:	'&#20;',
	chr(21)	:	'&#21;',
	chr(22)	:	'&#22;',
	chr(23)	:	'&#23;',
	chr(24)	:	'&#24;',
	chr(25)	:	'&#25;',
	chr(26)	:	'&#26;',
	chr(27)	:	'&#27;',
	chr(28)	:	'&#28;',
	chr(29)	:	'&#29;',
	chr(30)	:	'&#30;',
	chr(31)	:	'&#31;',
	chr(32)	:	'&#32;',
	chr(33)	:	'&#33;',
	chr(34)	:	'&quot;',
	chr(35)	:	'&#35;',
	chr(36)	:	'&#36;',
	chr(37)	:	'&#37;',
	chr(38)	:	'&amp;',
	chr(39)	:	'&#39;',
	chr(40)	:	'&#40;',
	chr(41)	:	'&#41;',
	chr(42)	:	'&#42;',
	chr(43)	:	'&#43;',
	chr(44)	:	'&#44;',
	chr(45)	:	'&#45;',
	chr(46)	:	'&#46;',
	chr(47)	:	'&#47;',
	chr(48)	:	'&#48;',
	chr(49)	:	'&#49;',
	chr(50)	:	'&#50;',
	chr(51)	:	'&#51;',
	chr(52)	:	'&#52;',
	chr(53)	:	'&#53;',
	chr(54)	:	'&#54;',
	chr(55)	:	'&#55;',
	chr(56)	:	'&#56;',
	chr(57)	:	'&#57;',
	chr(58)	:	'&#58;',
	chr(59)	:	'&#59;',
	chr(60)	:	'&lt;',
	chr(61)	:	'&#61;',
	chr(62)	:	'&gt;',
	chr(63)	:	'&#63;',
	chr(64)	:	'&#64;',
	chr(65)	:	'&#65;',
	chr(66)	:	'&#66;',
	chr(67)	:	'&#67;',
	chr(68)	:	'&#68;',
	chr(69)	:	'&#69;',
	chr(70)	:	'&#70;',
	chr(71)	:	'&#71;',
	chr(72)	:	'&#72;',
	chr(73)	:	'&#73;',
	chr(74)	:	'&#74;',
	chr(75)	:	'&#75;',
	chr(76)	:	'&#76;',
	chr(77)	:	'&#77;',
	chr(78)	:	'&#78;',
	chr(79)	:	'&#79;',
	chr(80)	:	'&#80;',
	chr(81)	:	'&#81;',
	chr(82)	:	'&#82;',
	chr(83)	:	'&#83;',
	chr(84)	:	'&#84;',
	chr(85)	:	'&#85;',
	chr(86)	:	'&#86;',
	chr(87)	:	'&#87;',
	chr(88)	:	'&#88;',
	chr(89)	:	'&#89;',
	chr(90)	:	'&#90;',
	chr(91)	:	'&#91;',
	chr(92)	:	'&#92;',
	chr(93)	:	'&#93;',
	chr(94)	:	'&#94;',
	chr(95)	:	'&#95;',
	chr(96)	:	'&#96;',
	chr(97)	:	'&#97;',
	chr(98)	:	'&#98;',
	chr(99)	:	'&#99;',
	chr(100)	:	'&#100;',
	chr(101)	:	'&#101;',
	chr(102)	:	'&#102;',
	chr(103)	:	'&#103;',
	chr(104)	:	'&#104;',
	chr(105)	:	'&#105;',
	chr(106)	:	'&#106;',
	chr(107)	:	'&#107;',
	chr(108)	:	'&#108;',
	chr(109)	:	'&#109;',
	chr(110)	:	'&#110;',
	chr(111)	:	'&#111;',
	chr(112)	:	'&#112;',
	chr(113)	:	'&#113;',
	chr(114)	:	'&#114;',
	chr(115)	:	'&#115;',
	chr(116)	:	'&#116;',
	chr(117)	:	'&#117;',
	chr(118)	:	'&#118;',
	chr(119)	:	'&#119;',
	chr(120)	:	'&#120;',
	chr(121)	:	'&#121;',
	chr(122)	:	'&#122;',
	chr(123)	:	'&#123;',
	chr(124)	:	'&#124;',
	chr(125)	:	'&#125;',
	chr(126)	:	'&#126;',
	chr(127)	:	'&#127;',
	chr(128)	:	'&#128;',
	chr(129)	:	'&#129;',
	chr(130)	:	'&#130;',
	chr(131)	:	'&#131;',
	chr(132)	:	'&#132;',
	chr(133)	:	'&#133;',
	chr(134)	:	'&#134;',
	chr(135)	:	'&#135;',
	chr(136)	:	'&#136;',
	chr(137)	:	'&#137;',
	chr(138)	:	'&#138;',
	chr(139)	:	'&#139;',
	chr(140)	:	'&#140;',
	chr(141)	:	'&#141;',
	chr(142)	:	'&#142;',
	chr(143)	:	'&#143;',
	chr(144)	:	'&#144;',
	chr(145)	:	'&#145;',
	chr(146)	:	'&#146;',
	chr(147)	:	'&#147;',
	chr(148)	:	'&#148;',
	chr(149)	:	'&#149;',
	chr(150)	:	'&#150;',
	chr(151)	:	'&#151;',
	chr(152)	:	'&#152;',
	chr(153)	:	'&#153;',
	chr(154)	:	'&#154;',
	chr(155)	:	'&#155;',
	chr(156)	:	'&#156;',
	chr(157)	:	'&#157;',
	chr(158)	:	'&#158;',
	chr(159)	:	'&#159;',
	chr(160)	:	'&nbsp;',
	chr(161)	:	'&iexcl;',
	chr(162)	:	'&cent;',
	chr(163)	:	'&pound;',
	chr(164)	:	'&curren;',
	chr(165)	:	'&yen;',
	chr(166)	:	'&brvbar;',
	chr(167)	:	'&sect;',
	chr(168)	:	'&uml;',
	chr(169)	:	'&copy;',
	chr(170)	:	'&ordf;',
	chr(171)	:	'&laquo;',
	chr(172)	:	'&not;',
	chr(173)	:	'&shy;',
	chr(174)	:	'&reg;',
	chr(175)	:	'&macr;',
	chr(176)	:	'&deg;',
	chr(177)	:	'&plusmn;',
	chr(178)	:	'&sup2;',
	chr(179)	:	'&sup3;',
	chr(180)	:	'&acute;',
	chr(181)	:	'&micro;',
	chr(182)	:	'&para;',
	chr(183)	:	'&middot;',
	chr(184)	:	'&cedil;',
	chr(185)	:	'&sup1;',
	chr(186)	:	'&ordm;',
	chr(187)	:	'&raquo;',
	chr(188)	:	'&frac14;',
	chr(189)	:	'&frac12;',
	chr(190)	:	'&frac34;',
	chr(191)	:	'&iquest;',
	chr(192)	:	'&Agrave;',
	chr(193)	:	'&Aacute;',
	chr(194)	:	'&Acirc;',
	chr(195)	:	'&Atilde;',
	chr(196)	:	'&Auml;',
	chr(197)	:	'&Aring;',
	chr(198)	:	'&AElig;',
	chr(199)	:	'&Ccedil;',
	chr(200)	:	'&Egrave;',
	chr(201)	:	'&Eacute;',
	chr(202)	:	'&Ecirc;',
	chr(203)	:	'&Euml;',
	chr(204)	:	'&Igrave;',
	chr(205)	:	'&Iacute;',
	chr(206)	:	'&Icirc;',
	chr(207)	:	'&Iuml;',
	chr(208)	:	'&ETH;',
	chr(209)	:	'&Ntilde;',
	chr(210)	:	'&Ograve;',
	chr(211)	:	'&Oacute;',
	chr(212)	:	'&Ocirc;',
	chr(213)	:	'&Otilde;',
	chr(214)	:	'&Ouml;',
	chr(215)	:	'&times;',
	chr(216)	:	'&Oslash;',
	chr(217)	:	'&Ugrave;',
	chr(218)	:	'&Uacute;',
	chr(219)	:	'&Ucirc;',
	chr(220)	:	'&Uuml;',
	chr(221)	:	'&Yacute;',
	chr(222)	:	'&THORN;',
	chr(223)	:	'&szlig;',
	chr(224)	:	'&agrave;',
	chr(225)	:	'&aacute;',
	chr(226)	:	'&acirc;',
	chr(227)	:	'&atilde;',
	chr(228)	:	'&auml;',
	chr(229)	:	'&aring;',
	chr(230)	:	'&aelig;',
	chr(231)	:	'&ccedil;',
	chr(232)	:	'&egrave;',
	chr(233)	:	'&eacute;',
	chr(234)	:	'&ecirc;',
	chr(235)	:	'&euml;',
	chr(236)	:	'&igrave;',
	chr(237)	:	'&iacute;',
	chr(238)	:	'&icirc;',
	chr(239)	:	'&iuml;',
	chr(240)	:	'&eth;',
	chr(241)	:	'&ntilde;',
	chr(242)	:	'&ograve;',
	chr(243)	:	'&oacute;',
	chr(244)	:	'&ocirc;',
	chr(245)	:	'&otilde;',
	chr(246)	:	'&ouml;',
	chr(247)	:	'&divide;',
	chr(248)	:	'&oslash;',
	chr(249)	:	'&ugrave;',
	chr(250)	:	'&uacute;',
	chr(251)	:	'&ucirc;',
	chr(252)	:	'&uuml;',
	chr(253)	:	'&yacute;',
	chr(254)	:	'&thorn;',
	chr(255)	:	'&yuml;',
}
