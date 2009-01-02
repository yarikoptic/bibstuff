#! /usr/bin/env python
# File: bibgrammar.py

"""
Provides an EBNF description of the bibtex bibliography format.
The grammar draws largely from
the grammar description in Nelson Beebe's `Lex/Yacc parser`_
and also from
Greg Ward's btOOL_ documentation.

:author: Dylan Schwilk
:contact: http://www.schwilk.org
:author: Alan G Isaac (minor edits)
:license: MIT (see `license.txt`_)
:date: 2008-06-28


.. _license.txt: ./license.txt
.. _`Lex/Yacc parser`: http://www.math.utah.edu/~beebe/
.. _btooL: http://www.tug.org/tex-archive/biblio/bibtex/utils/btOOL/
"""
__docformat__ = "restructuredtext en"
__needs__ = '2.4'
__version__ = "1.7"
__author__  =    ["Dylan W. Schwilk", "Alan G Isaac"]


###################  IMPORTS  ##################################################
#import from standard library
# (some if  run as main; see below)

#import dependencies
from simpleparse.parser import Parser
from simpleparse.common import numbers, strings, chartypes

#local imports
################################################################################


# EBNF description of a bibtex file

# 2008-06-27: There may be a bug in simpleparse that sometimes causes certain entries to
# not be recognized. The problem, however, can disapear if the order of entries
# in a bibfile is changed! I do not believe it is a problem with the grammar
# but is a bug in simpleparse itself.

# modification 2009-01-01
#  change `key` to `citekey`
#  add `alpha_name`
#  change `macro` def (use case insenstive string)
#  change `macro_contents` def (field instead of fields)
#  change `fields` def (comma is allowed after last field)
dec = r"""
bibfile              := entry_or_junk+
>entry_or_junk<      := (tb, object) / (tb, junk)
>object<             := entry / macro / preamble / comment_entry
entry                := '@', entry_type, tb,  ( '{' , tb, contents, tb, '}' ) / ( '(' , tb, contents, tb, ')' )
macro                := c'@string', tb,  ( '{' , tb, macro_contents, tb, '}' ) / ( '\"' , tb, macro_contents, tb, '\"' )
preamble             := '@', entry_type, tb,  ( '{' , tb, preamble_contents, tb, '}' ) / ( '(' , tb, preamble_contents, tb, ')' )
comment_entry        := '@', entry_type, tb, string
>contents<           := citekey , tb, ',' , tb, fields
>macro_contents<     := field
>preamble_contents<  := value
entry_type           := alpha_name
citekey              := number / name
fields               := (field_comma / field)+
>field_comma<        := field , tb, ',', tb
field                := name, tb, '=' , tb, value
value                := simple_value  / (simple_value, (tb,'#', tb, simple_value)+)
>simple_value<       :=  string / number / name
alpha_name           := [a-zA-Z]+
name                 := []-[a-z_A-Z!$&+./:;<>?^`|] , []-[a-z_A-Z0-9!$&+./:;<>?^`|]*
number               :=  [0-9]+ / ([[0-9]+, tb, [-]+, tb, [0-9]+)
string               :=  ('\"' , quotes_string?, '\"') / ('{' , braces_string?, '}')
<braces_string>      := (-[{}]+ / string)+
<quotes_string>      := (-[\"]+ / string)+
<junk>               := -[ \t\r\n]+
<tb>                 := (comment / ws)*
<ws>                 := [ \t\n\r]
<comment>            := '%' , -[\n]*, '\n'
"""

## The parsers
parser = Parser(dec,'bibfile')
entry_parser = Parser(dec,'entry')

## or a default parse function
def Parse(src, processor = None) :
	'''Parse the bibtex string in src, process with processor.'''
	return parser.parse(src,  processor =  processor)

## self-test
if __name__ =="__main__":
	import sys, pprint
	if len(sys.argv) > 1 :
		src = open(sys.argv[1]).read()
		taglist = Parse(src)
		pprint.pprint(taglist)

