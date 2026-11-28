import ast, dis, inspect, pathlib, subprocess, sys, types
from player import brain

BASE='e4a267cd1ab5ff85c3b2399bab713f2870da6ccb'
oldsrc=subprocess.check_output(['git','show',BASE+':player/brain.py'],text=True)
files=[pathlib.Path('player/brain')/n for n in ('core.py','resident.py','client.py','__init__.py')]
def entries(src):
    result={}
    for node in ast.parse(src).body:
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            result[node.name]=node
        elif isinstance(node,ast.Assign):
            assert len(node.targets)==1 and isinstance(node.targets[0],ast.Name)
            result[node.targets[0].id]=node
        else:
            assert isinstance(node,(ast.Import,ast.ImportFrom,ast.If)) or (isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str)),ast.dump(node)
    return result
old=entries(oldsrc); new={}
class Normalize(ast.NodeTransformer):
    count=0
    def visit_Attribute(self,node):
        if isinstance(node.value,ast.Name) and node.value.id=='B':
            assert node.attr in {'Brain','serve','answer','_lock','_await'}
            self.count+=1
            return ast.copy_location(ast.Name(id=node.attr,ctx=node.ctx),node)
        return self.generic_visit(node)
normalizer=Normalize()
for p in files:
    for name,node in entries(p.read_text()).items():
        assert name not in new,name
        new[name]=normalizer.visit(node)
assert set(old)==set(new)
for name in old:
    assert ast.dump(old[name])==ast.dump(new[name]),name
assert normalizer.count==8 # eight name lookups on the seven changed source lines
baseline=types.ModuleType('player._split_review_baseline')
baseline.__package__='player'
exec(compile(oldsrc,'<base brain.py>','exec'),baseline.__dict__)
names={n for n in baseline.__dict__ if not n.startswith('__')}
assert len(names)==57
assert names <= set(brain.__dict__)
assert set(n for n in brain.__dict__ if not n.startswith('__'))-names=={'core','resident','client'}
def same_binding(a,b):
    if (inspect.isfunction(a) or inspect.isclass(a)) and a.__module__==baseline.__name__:
        return a.__qualname__==b.__qualname__
    return a is b or type(a)==type(b) and a==b
checked=set()
def globals_in(code):
    yield from (i.argval for i in dis.get_instructions(code) if i.opname=='LOAD_GLOBAL')
    for item in code.co_consts:
        if isinstance(item,types.CodeType): yield from globals_in(item)
for name in names:
    a,b=getattr(baseline,name),getattr(brain,name)
    assert same_binding(a,b),name
    pairs=[]
    if inspect.isfunction(a) and a.__module__==baseline.__name__:
        pairs=[(a,b)]
    if inspect.isclass(a) and a.__module__==baseline.__name__:
        pairs=[(v,getattr(b,k)) for k,v in vars(a).items() if inspect.isfunction(v)]
    for before,after in pairs:
        before,after=inspect.unwrap(before),inspect.unwrap(after)
        for g in set(globals_in(before.__code__)):
            if g not in before.__globals__: continue
            if g=='__doc__':
                assert after.__globals__[g].startswith(before.__globals__[g].rstrip())
                assert before.__globals__[g].split('\n\n')[1]==after.__globals__[g].split('\n\n')[1]
            elif g in after.__globals__:
                assert same_binding(before.__globals__[g],after.__globals__[g]),(name,g)
            else:
                assert g in {'Brain','serve','answer','_lock','_await'}
                assert after.__globals__['B'] is brain
            checked.add((name,g))
assert brain.client.B is brain and brain.resident.B is brain
print(f'{len(old)} top-level definitions/constants, including decorators and all Brain methods: equal after the exact eight B lookups are normalized')
print(f'57 original names retained; only core/resident/client added; {len(checked)} global binding checks passed')
