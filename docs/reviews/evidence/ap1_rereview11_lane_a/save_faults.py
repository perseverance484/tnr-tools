import json,os,pathlib,tempfile,time
from unittest.mock import patch
from player import brain
from player.world import World,takeovers

for fail in ('counter','world'):
    live=tempfile.mkdtemp(prefix='ap1-r11-save-fault-')
    path=pathlib.Path(live)/'world.json'; path.write_bytes(b'')
    now=time.time()+1
    with patch.dict(os.environ,{'TNR_PLAYER_FIGHTS':live+'/fights'}):
        home=brain.Brain(live,clock=lambda:now)
        first=home.budget.loose()[0][1]
        write=World._write; writes=[]
        def faulty(p,obj):
            writes.append(pathlib.Path(p).name)
            if pathlib.Path(p).name==('takeovers.json' if fail=='counter' else 'world.json'):
                raise OSError('injected write failure')
            write(p,obj)
        with patch.object(World,'_write',staticmethod(faulty)):
            try: home.world.save()
            except OSError: pass
        assert path.read_bytes()==b''
        n=takeovers(live)
        restarted=brain.Brain(live,clock=lambda:now+120)
        later=restarted.budget.loose()[0][1]
        released=restarted.budget.ended(first,now)
        assert n==(0 if fail=='counter' else 1)
        assert (first==later)==(fail=='counter')
        assert released==(30 if fail=='counter' else 0)
        home.world.save(); home.world.save()
        assert takeovers(live)==1
        print(json.dumps({'failed_write':fail,'attempt_order':writes,'count_after_failure':n,'restart_reuses_name':first==later,'old_word_releases_rows':released,'count_after_same_brain_recovers_and_saves_twice':takeovers(live)}))
