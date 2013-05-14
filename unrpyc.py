#!/usr/bin/env python2

# Copyright (c) 2012 Yuri K. Schlesner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import optparse
import os.path
import sys
import cPickle as pickle
import codecs
import glob
import itertools

class Dummy:
    def record_pycode(self,*args,**kwargs):
        return
    all_pycode = []

def import_renpy(basedir=None):
    #import renpy from another location.
    if basedir:
        sys.path.append(basedir)
    global renpy
    global decompiler
    
    # Needed for pickle to read the AST
    try:
        import renpy
    except ImportError:
        print "\nFailed at importing renpy. Are you sure that the renpy directory can be found in sys.path or the current working directory?\n"
        raise
    # try to import as much renpy modules as possible, but some modules might not exist
    # in older ren'py versions. 
    try: import renpy.log
    except: pass
    try: import renpy.display
    except: pass
    try: import renpy.object
    except: pass
    try: 
        import renpy.game
        renpy.game.script = Dummy()
    except: pass
    try: import renpy.loader
    except: pass
    try: import renpy.ast
    except: pass
    try: import renpy.atl
    except: pass
    try: import renpy.curry
    except: pass
    try: import renpy.easy
    except: pass
    try: import renpy.execution
    except: pass
    try: import renpy.loadsave
    except: pass
    try: import renpy.parser
    except: pass
    try: import renpy.python
    except: pass
    try: import renpy.script
    except: pass
    try: import renpy.statements
    except: pass
    try: import renpy.style
    except: pass

    import decompiler
    if basedir:
        sys.path.remove(basedir)


def read_ast_from_file(in_file):
    raw_contents = in_file.read().decode('zlib')
    data, stmts = pickle.loads(raw_contents)
    return stmts

def decompile_rpyc(input_filename, overwrite=False):
    # Output filename is input filename but with .rpy extension
    path, ext = os.path.splitext(input_filename)
    out_filename = path + '.rpy'

    print "Decompiling %s to %s..." % (input_filename, out_filename)

    with open(input_filename, 'rb') as in_file:
        ast = read_ast_from_file(in_file)

    if not overwrite and os.path.exists(out_filename):
        sys.exit("Output file already exists. Pass --clobber to overwrite.")

    with codecs.open(out_filename, 'w', encoding='utf-8') as out_file:
        decompiler.pretty_print_ast(out_file, ast)

if __name__ == "__main__":
    parser = optparse.OptionParser(
            usage="usage: %prog [options] script1 script2 ...",
            version="%prog 0.1")

    parser.add_option('-c', '--clobber', action='store_true', dest='clobber',
            default=False, help="overwrites existing output files")
            
    parser.add_option('-b', '--basedir', action='store', dest='basedir', 
            help="specify the game base directory in which the 'renpy' directory is located") 

    options, args = parser.parse_args()
    

    if options.basedir:
        import_renpy(options.basedir)
    else:
        import_renpy()

    # Expand wildcards
    args = map(glob.glob, args)
    # Concatenate lists
    args = list(itertools.chain(*args))

    if len(args) == 0:
        parser.print_help();
        parser.error("No script files given.")

    for filename in args:
        decompile_rpyc(filename, options.clobber)
else:
    import_renpy()

