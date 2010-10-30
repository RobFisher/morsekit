#!/usr/bin/python
"""
Copyright (C) 2001 Randall S. Bohn

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.  

"""

# This file generates cw.h - all the morse code compressed
# in a set of three binary strings
# Each character is represented in 'code' as follows
# SSSPPPPP (Three bits for the character size, five for the offset)
# crypt is a condensed version of all the 'dotscii' morse characters.
# To convert a char to morse code, find the char in 'plain'
# get the key from code at the same offset,
# then starting with crypt[key&00011111] 
# take (key>>5)&00000111 characters

# here is the traditional morse code table in a dictionary
morse={'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..',
'e':'.', 'f':'..-.', 'g':'--.', 'h':'....',
'i':'..', 'j':'.---', 'k':'-.-', 'l':'.-..',
'm':'--', 'n':'-.', 'o':'---', 'p':'.--.',
'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-',
'y':'-.--', 'z':'--..', '0':'-----', '1':'.----',
'2':'..---', '3':'...--', '4':'....-', '5':'.....',
'6':'-....', '7':'--...', '8':'---..', '9':'----.',
'.':'.-.-.-', ',':'--..--', ':':'---...', '?':'..--..', '-':'-....-',
'/':'-..-.', '=':'.-.-.', '@': '...-.-', '!':'...-.-', ' ':' '}

from string import lower
from string import find

# generate the header file cw.h
# I hand optimized the crypt string through several iterations
# so that all offsets would fit in 5 bits. There may be a more
# compact version possible, but this fits my needs.
def mkcw_h():
 crypt=".....-----....-.-.--..--..-...--.- "
 plain='.,:?-/=@!0123456789abcdefghijklmnopqrstuvwxyz'
 code=''
 for n in plain:
  slot = find(crypt, morse[n])
  if slot > 31:
   print "/* %s out of bounds (%d). Must be <= 31 */"
  if slot >= 0:
   plen=slot+(len(morse[n])<<5)
   code=code+"\\x"+hex(plen)[2:] 
  else:
   crypt = crypt + morse[n]
   print n, hex(find(crypt, morse[n])), len(morse[n]), hex(len(morse[n]))
 print "/* International Morse Code */"
 print "#define CWSTARTMASK (0x1f)"
 print "#define CWSIZEMASK (0x07)"
 print "#define CWSIZESHIFT (0x05)"
 print "char *crypt=\"%s\";" % crypt
 print "char *plain=\"%s\";" % plain
 print "char *code=\"%s\";" % code

if __name__ == '__main__':
 mkcw_h()
	
