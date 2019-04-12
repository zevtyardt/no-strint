import sys
import symtable
import parser
import types
import tokenize
import token
import symbol
import random

class LambdaSymTable:
    def __init__(self, symtabs, argnames):
        self.symtabs = symtabs
        self.mysymbs = {}
        for argname in argnames:
            self.mysymbs[argname] = symtable.Symbol(argname, symtable.DEF_PARAM)

    def lookup(self, name):
        lsymb = self.mysymbs.get(name)
        if lsymb:
            return lsymb
        else:
            try:
                return self.symtabs[-1].lookup(name)
            except KeyError:
                return self.symtabs[0].lookup(name)

    def get_type(self):
        return self.symtabs[-1].get_type()

    def is_lambda_arg(self, id):
        return self.mysymbs.has_key(id)

class CSTWalker:
    def __init__(self, source_no_encoding):
        self.pubapi = []
        self.modnames = []
        self.symtab = symtable.symtable(source_no_encoding, "-", "exec")
        cst = parser.suite(source_no_encoding)
        elements = parser.ast2tuple(cst, line_info=1)
        self.names = {}
        self.walk(elements, [self.symtab])

    def getNames(self):
        return self.names

    def addToNames(self, line, name, doreplace):
        namedict = self.names.get(line, {})
        if not namedict:
            self.names[line] = namedict
        occurancelist = namedict.get(name, [])
        if not occurancelist:
            namedict[name] = occurancelist
        occurancelist.append(doreplace)

    def res_name(self, name):
        if name.startswith("__") and name.endswith("__"):
            return 1
        if name in self.modnames:
            return 1
        if hasattr(__builtins__, name):
            return 1
        return 0

    def walk(self, elements, symtabs):
        if type(elements) != types.TupleType:
            return
        if token.ISTERMINAL(elements[0]):
            return
        production = elements[0]
        if production == symbol.funcdef:
            self.handle_funcdef(elements, symtabs)
        elif production == symbol.varargslist:
            self.handle_varargslist(elements, symtabs)
        elif production == symbol.fpdef:
            self.handle_fpdef(elements, symtabs)
        elif production == symbol.import_as_name:
            self.handle_import_as_name(elements, symtabs)
        elif production == symbol.dotted_as_name:
            self.handle_dotted_as_name(elements, symtabs)
        elif production == symbol.dotted_name:
            self.handle_dotted_name(elements, symtabs)
        elif production == symbol.global_stmt:
            self.handle_global_stmt(elements, symtabs)
        elif production == symbol.atom:
            self.handle_atom(elements, symtabs)
        elif production == symbol.trailer:
            self.handle_trailer(elements, symtabs)
        elif production == symbol.classdef:
            self.handle_classdef(elements, symtabs)
        elif production == symbol.argument:
            self.handle_argument(elements, symtabs)
        elif production == symbol.lambdef:
            self.handle_lambdef(elements, symtabs)
        elif production == symbol.decorator:
            self.handle_decorator(elements, symtabs)
        else:
            for node in elements:
                self.walk(node, symtabs)

    def mangle_name(self, symtabs, name):
        if self.res_name(name):
            return name
        if not name.startswith("__"):
            return name
        for i in xrange(len(symtabs)):
            tab = symtabs[-1 - i]
            tabtype = tab.get_type()
            if tabtype == "class":
                classname = tab.get_name().lstrip("_")
                return "_" + classname + name
        return name

    def should_obfuscate(self, id, symtabs):
        tab = symtabs[-1]
        if self.res_name(id):
            return False
        orig_id = id
        id = self.mangle_name(symtabs, id)
        try:
            s = tab.lookup(id)
        except Exception:
            return False
        debug_symbols = []
        if id in debug_symbols:
            print >>sys.stderr, "%s:" % id
            print >>sys.stderr, "  Imported:", s.is_imported()
            print >>sys.stderr, "  Parameter:", s.is_parameter()
            print >>sys.stderr, "  Global:", s.is_global()
            print >>sys.stderr, "  Local:", s.is_local()
        if s.is_imported():
            return False
        if s.is_parameter():
            if isinstance(tab, LambdaSymTable):
                if tab.is_lambda_arg(id):
                    return True
            return False
        if isinstance(tab, LambdaSymTable):
            while True:
                symtabs = symtabs[:-1]
                if symtabs == []:
                    raise RuntimeError("Lambda symbol '%s' is not present on any scope" % id)
                if id in symtabs[-1].get_identifiers():
                    return self.should_obfuscate(orig_id, symtabs)
        if s.is_global():
            topsymtab = symtabs[0]
            if id not in topsymtab.get_identifiers():
                return False
            topsym = topsymtab.lookup(id)
            if id in debug_symbols:
                print >>sys.stderr, "  Imported (G):", topsym.is_imported()
                print >>sys.stderr, "  Parameter (G):", topsym.is_parameter()
                print >>sys.stderr, "  Global (G):", topsym.is_global()
                print >>sys.stderr, "  Local (G):", topsym.is_local()
            if topsym.is_imported():
                return False
            if not topsym.is_local():
                return False
            return id not in self.pubapi
        if not s.is_local():
            if len(symtabs) <= 2:
                raise RuntimeError("Symbol '%s' is not present on any scope" % id)
            return self.should_obfuscate(orig_id, symtabs[:-1])
        tabtype = tab.get_type()
        if tabtype == "module":
            return id not in self.pubapi
        elif tabtype == "function":
            return True
        elif tabtype == "class":
            return False
        else:
            raise RuntimeError("Unknown scope '%s' for symbol '%s'" % (tabtype, id))

    def handle_funcdef(self, elements, symtabs):
        name = elements[2]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        obfuscate = self.should_obfuscate(id, symtabs)
        self.addToNames(line, id, obfuscate)
        tab = symtabs[-1]
        orig_id = id
        id = self.mangle_name(symtabs, id)
        functabs = tab.lookup(id).get_namespaces()
        if len(functabs) == 0:
            functabs = []
            for child in tab.get_children():
                if child.get_name() == orig_id:
                    functabs.append(child)
        for node in elements:
            self.walk(node, symtabs + functabs)

    def handle_varargslist(self, elements, symtabs):
        tab = symtabs[-1]
        for tok in elements:
            if type(tok) != types.TupleType:
                continue
            toktype = tok[0]
            if toktype == symbol.test:
                for node in tok:
                    self.walk(node, symtabs[:-1])
            elif toktype == token.NAME:
                id = tok[1]
                line = tok[2]
                obfuscate = self.should_obfuscate(id, symtabs)
                self.addToNames(line, id, obfuscate)
            elif toktype == symbol.fpdef:
                self.handle_fpdef(tok, symtabs)
            else:
                assert(toktype in [token.STAR, token.DOUBLESTAR,
                                   token.COMMA, token.EQUAL])

    def handle_fpdef(self, elements, symtabs):
        name = elements[1]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        obfuscate = self.should_obfuscate(id, symtabs)
        self.addToNames(line, id, obfuscate)
        for node in elements:
            self.walk(node, symtabs)

    def handle_import_as_name(self, elements, symtabs):
        name1 = elements[1]
        assert name1[0] == token.NAME
        id1 = name1[1]
        line1 = name1[2]
        self.addToNames(line1, id1, 0)
        if len(elements) > 2:
            assert len(elements) == 4
            name2 = elements[2]
            assert name2[0] == token.NAME
            id2 = name2[1]
            assert id2 == "as"
            line2 = name2[2]
            self.addToNames(line2, id2, 0)
            name3 = elements[3]
            assert name3[0] == token.NAME
            id3 = name3[1]
            line3 = name3[2]
            self.addToNames(line3, id3, 0)
            self.modnames.append(id3)
        for node in elements:
            self.walk(node, symtabs)

    def handle_dotted_as_name(self, elements, symtabs):
        dotted_name = elements[1]
        modname = dotted_name[1]
        assert modname[0] == token.NAME
        mod_id = modname[1]
        mod_line = modname[2]
        self.addToNames(mod_line, mod_id, 0)
        self.modnames.append(mod_id)
        if len(elements) > 2:
            assert len(elements) == 4
            asname = elements[2]
            assert asname[0] == token.NAME
            asid = asname[1]
            assert asid == "as"
            asline = asname[2]
            self.addToNames(asline, asid, 0)
            name = elements[3]
            assert name[0] == token.NAME
            id = name[1]
            line = name[2]
            self.addToNames(line, id, 0)
            self.modnames.append(id)
        for node in elements:
            self.walk(node, symtabs)

    def handle_dotted_name(self, elements, symtabs):
        name = elements[1]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        self.addToNames(line, id, 0)
        assert (len(elements) % 2 == 0)
        for x in range(2, len(elements), 2):
            dot = elements[x]
            name = elements[x+1]
            assert dot[0] == token.DOT
            assert name[0] == token.NAME
            id = name[1]
            line = name[2]
            self.addToNames(line, id, 0)
        for node in elements:
            self.walk(node, symtabs)

    def handle_global_stmt(self, elements, symtabs):
        gname = elements[1]
        assert gname[0] == token.NAME
        gid = gname[1]
        assert gid == "global"
        name1 = elements[2]
        assert name1[0] == token.NAME
        id1 = name1[1]
        line1 = name1[2]
        obfuscate = self.should_obfuscate(id1, symtabs)
        self.addToNames(line1, id1, obfuscate)
        assert (len(elements) % 2)
        for x in range(3, len(elements), 2):
            comma = elements[x]
            name = elements[x+1]
            assert comma[0] == token.COMMA
            assert name[0] == token.NAME
            id = name[1]
            line = name[2]
            obfuscate = id not in self.pubapi
            self.addToNames(line, id, obfuscate)
        for node in elements:
            self.walk(node, symtabs)

    def handle_atom(self, elements, symtabs):
        name = elements[1]
        if name[0] == token.NAME:
            id = name[1]
            line = name[2]
            obfuscate = self.should_obfuscate(id, symtabs)
            self.addToNames(line, id, obfuscate)
        for node in elements:
            self.walk(node, symtabs)

    def handle_trailer(self, elements, symtabs):
        trailer = elements[1]
        if trailer[0] == token.DOT:
            name = elements[2]
            assert name[0] == token.NAME
            id = name[1]
            line = name[2]
            self.addToNames(line, id, 0)
        for node in elements:
            self.walk(node, symtabs)

    def handle_classdef(self, elements, symtabs):
        name = elements[2]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        obfuscate = self.should_obfuscate(id, symtabs)
        self.addToNames(line, id, obfuscate)
        aftername = elements[3]
        aftername2 = elements[4]
        assert aftername[0] in (token.COLON, token.LPAR)
        if aftername[0] == token.LPAR and aftername2[0] != token.RPAR:
            testlist = elements[4]
            assert testlist[0] == symbol.testlist
            for node in testlist:
                self.walk(node, symtabs)
            elements = elements[5:]
        tab = symtabs[-1]
        classtab = tab.lookup(id).get_namespace()
        for node in elements:
            self.walk(node, symtabs + [classtab])

    def handle_argument(self, elements, symtabs):
        if len(elements) >= 4:
            if sys.hexversion >= 0x2040000:
                keyword = elements[1][1][1][1][1][1][1][1][1][1][1][1][1][1][1]
            else:
                keyword = elements[1][1][1][1][1][1][1][1][1][1][1][1][1][1]
            assert keyword[0] == token.NAME
            keyword_id = keyword[1]
            keyword_line = keyword[2]
            self.addToNames(keyword_line, keyword_id, False)
            elements = elements[3]
        for node in elements:
            self.walk(node, symtabs)

    def handle_lambdef(self, elements, symtabs):
        if elements[2][0] == token.COLON:
            test = elements[3]
            lambdatab = LambdaSymTable(symtabs, [])
            for node in test:
                self.walk(node, symtabs + [lambdatab])
        else:
            varargslist = elements[2]
            arguments = self.get_varargs_names(varargslist)
            for line, name in arguments:
                self.addToNames(line, name, 1)
            argnames = [e[1] for e in arguments]
            lambdatab = LambdaSymTable(symtabs, argnames)
            test = elements[4]
            for node in test:
                self.walk(node, symtabs + [lambdatab])

    def handle_decorator(self, elements, symtabs):
        name = elements[2][1]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        obfuscate = self.should_obfuscate(id, symtabs)
        self.addToNames(line, id, obfuscate)
        for node in elements:
            self.walk(node, symtabs)

    def get_varargs_names(elements):
        result = []
        next_is_name = False
        for tok in elements:
            if type(tok) != types.TupleType:
                continue
            toktype = tok[0]
            if next_is_name:
                assert tok[0] == token.NAME
                id = tok[1]
                line = tok[2]
                result.append((line, id))
                next_is_name = False
            elif toktype in [token.STAR, token.DOUBLESTAR]:
                next_is_name = True
            elif toktype == symbol.fpdef:
                result.extend(CSTWalker.get_fpdef_names(tok))
        return result
    get_varargs_names = staticmethod(get_varargs_names)

    def get_fpdef_names(elements):
        result = []
        if type(elements) != types.TupleType:
            return result
        if token.ISTERMINAL(elements[0]):
            return result
        name = elements[1]
        assert name[0] == token.NAME
        id = name[1]
        line = name[2]
        result.append((line, id))
        for node in elements:
            result.extend(CSTWalker.get_fpdef_names(node))
        return result
    get_fpdef_names = staticmethod(get_fpdef_names)

class NameTranslator:
    def __init__(self):
        self.realnames = {}
        self.bogusnames = []

    def get_name(self, name):
        if not self.realnames.has_key(name):
            self.realnames[name] = self.gen_unique_name()
        return self.realnames[name]

    def get_bogus_name(self,):
        if len(self.bogusnames) < 20:
            newname = self.gen_unique_name()
            self.bogusnames.append(newname)
            return newname
        else:
            return random.choice(self.bogusnames)

    def gen_unique_name(self):
        existing_names = self.realnames.values() + self.bogusnames
        name = ""
        while 1:
            name += self.gen_name()
            if name not in existing_names:
                break
        return name

    def gen_name():
        if random.choice((True, False)):
            chars = ("i", "I", "1")
        else:
            chars = ("o", "O", "0")
        result = random.choice(chars[:2])
        for x in range(random.randint(1, 12)):
            result += random.choice(chars)
        return result
    gen_name = staticmethod(gen_name)

class var_obf:
    def __init__(self, file):
        self.file = file
        self.names = CSTWalker(self.file).names
        self.gn = NameTranslator()

    def obf_var(self):
        res = []
        for num, token in enumerate(tokenize.generate_tokens(iter(self.file.splitlines(1)).next), start=1):
            t_type, t_string, t_srow_scol, t_erow_ecol, t_line = token
            if t_type == tokenize.NAME:
                x = self.names.get(t_srow_scol[0])
                if x:
                    if t_string in x.keys():
                        if x[t_string] in [[1], [True]]:
                            t_string = self.gn.get_name(t_string)
            res.append([t_type, t_string, t_srow_scol, t_erow_ecol, t_line])
        return tokenize.untokenize(res)

if __name__ == '__main__' and len(sys.argv) == 2:
    var(sys.argv[1])