"""Socket-free tests. Fixtures are synthetic, never live content evidence."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image
import collect_godstorm_art as m


def fixtures():
    def cap(proc, data, ident):
        key = 'userId' if proc == 'profile.getAi' else 'id'
        return {'proc':proc,'input':{key:ident},'data':data,'ok':True,
                'persist':'full','persistOk':True,'error':None,
                'rows':1,'snapshotKey':proc+':'+ident,'at':'synthetic-time'}
    def result(caps, source):
        return {'state':'DONE','outcome':'success','entries':[], 'at':'synthetic-time',
                'journal':{'items':[],'manifestPath':m.SOURCES[source][2]},'captures':caps}
    qs=[]
    for n,name in enumerate(m.QUEST_NAMES):
        nodes=[]
        for b in range(25):
            nodes.append({'id':f'b{b}','task':'start_battle',
                          'opponentAIs':[{'ids':[f'ai{n*9+b%9:02d}']}],
                          'sceneBackground':f'bg{b%3}' if n==0 else ''})
        q={'id':f'q{n}','name':name,'questType':'battlepyramid',
           'image':f'https://ui0arpl8sm.ufs.sh/f/quest{n}',
           'content':{'objectives':nodes}}
        qs.append(cap('quests.get',q,q['id']))
    qs.append(cap('quests.get',{'id':'excluded','name':'Dawnless Crown'},'excluded'))
    rel=[]
    for i in range(23):
        aid=f'ai{i:02d}'
        image=(f'https://ui0arpl8sm.ufs.sh/f/avatar{i}' if i>=5
               else 'https://uploadthing.b-cdn.net/f/fixture_default.webp')
        rel.append(cap('profile.getAi',{'userId':aid,'username':f'Enemy {i}', 'avatar':image},aid))
    for i in range(3):
        rel.append(cap('item.get',{'id':f'item{i}'},f'item{i}'))
    for i in range(4):
        aid=f'bg{i}'
        rel.append(cap('gameAsset.get',{'id':aid,'name':'StormCourtyard' if i==3 else f'Marrow {i}',
              'image':f'https://ui0arpl8sm.ufs.sh/f/bg{i}.webp','type':'SCENE_BACKGROUND'},aid))
    return result(qs,0),result(rel,1)


def png():
    b=io.BytesIO(); Image.new('RGB',(12,8)).save(b,format='PNG'); return b.getvalue()


class CollectorTests(unittest.TestCase):
    def setUp(self): self.roots,self.related=fixtures()
    def test_capture_accepts_checked_bytes(self):
        data=json.dumps(self.roots).encode()
        self.assertEqual(m.checked_source(data,m.git_blob_hash(data),m.SOURCES[0][2],
                                         {'quests.get':3})['state'],'DONE')
    def test_rejects_changed_source_hash(self):
        with self.assertRaises(ValueError): m.checked_source(b'{}','0'*40,'x',{})
    def test_rejects_mutation(self):
        self.roots['journal']['items']=[{'write':True}]
        data=json.dumps(self.roots).encode()
        with self.assertRaises(ValueError):
            m.checked_source(data,m.git_blob_hash(data),m.SOURCES[0][2],{'quests.get':3})
    def test_rejects_missing_persistence(self):
        self.roots['captures'][0]['persistOk']=False
        data=json.dumps(self.roots).encode()
        with self.assertRaises(ValueError):
            m.checked_source(data,m.git_blob_hash(data),m.SOURCES[0][2],{'quests.get':3})
    def test_inventory_scope(self):
        rows=m.inventory(self.roots,self.related)
        self.assertEqual(len(rows),24)
        self.assertEqual(sum(r['state']=='assigned' for r in rows),19)
        self.assertEqual(sum(r['state']=='default' for r in rows),5)
        self.assertNotIn('ai22',{r['entity_id'] for r in rows})
    def test_missing_ai_fails(self):
        self.related['captures'].pop(0)
        with self.assertRaises(ValueError): m.inventory(self.roots,self.related)
    def test_duplicate_ai_fails(self):
        self.related['captures'].append(copy.deepcopy(self.related['captures'][0]))
        with self.assertRaises(ValueError): m.inventory(self.roots,self.related)
    def test_population_drift_fails(self):
        self.roots['captures'][0]['data']['content']['objectives'].pop()
        with self.assertRaises(ValueError): m.inventory(self.roots,self.related)
    def test_unknown_background_fails(self):
        self.related['captures'][-1]['data']['name']='unapproved candidate'
        with self.assertRaises(ValueError): m.inventory(self.roots,self.related)
    def test_url_allowlist(self):
        valid='https://ui0arpl8sm.ufs.sh/f/OWdh17MrZJdFBObZtBSIs.webp'
        self.assertEqual(m.validate_url(valid),valid)
        for bad in ['http://ui0arpl8sm.ufs.sh/f/a','https://ui0arpl8sm.ufs.sh.evil.test/f/a',
                    'https://theninja-rpg.com/api/trpc/a','https://127.0.0.1/f/a',
                    'https://user@ui0arpl8sm.ufs.sh/f/a','https://ui0arpl8sm.ufs.sh:444/f/a',
                    valid+'?token=x',valid+'#x','https://ui0arpl8sm.ufs.sh/f/../admin']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):m.validate_url(bad)
    def test_redirect_refused(self):
        with self.assertRaises(ValueError):
            m.NoRedirect().redirect_request(None,None,302,'',{},'https://other.test/f/a')
    def test_decode_original(self):
        b=png(); info=m.image_info(b)
        self.assertEqual((info['format'],info['width'],info['height']),('PNG',12,8))
        self.assertEqual(info['bytes'],len(b))
    def test_nonimage_and_oversize_fail(self):
        with self.assertRaises(Exception):m.image_info(b'<html>login</html>')
        with patch.object(m,'MAX_BYTES',1),self.assertRaises(ValueError):m.image_info(png())
    def test_archive_url_dedup_and_byte_preservation(self):
        records=m.inventory(self.roots,self.related)[:2]
        records[1]['source_url']=records[0]['source_url']; calls=[]; b=png()
        def fake(url):calls.append(url);return b,{'downloaded_at':'fixture'}
        with tempfile.TemporaryDirectory() as t,patch('socket.socket',side_effect=AssertionError('network')):
            out=Path(t)/'pack'; data=m.collect(records,out,[],fake)
            self.assertEqual(len(calls),1);self.assertEqual(len(data['assets']),1)
            self.assertEqual(data['assets'][0]['inventory_indices'],[0,1])
            self.assertEqual((out/data['assets'][0]['file']).read_bytes(),b)
            self.assertTrue(out.with_suffix('.zip').exists())
            self.assertNotIn('https://',(out/'gallery.html').read_text())
    def test_failure_remains_partial(self):
        def fake(url):raise OSError('fixture denied')
        records=m.inventory(self.roots,self.related)[:1]
        with tempfile.TemporaryDirectory() as t:
            out=Path(t)/'pack'; data=m.collect(records,out,[],fake)
            self.assertEqual(data['status'],'partial');self.assertEqual(len(data['failures']),1)
            self.assertEqual(list((out/'originals').iterdir()),[])
    def test_existing_output_refused(self):
        with tempfile.TemporaryDirectory() as t,self.assertRaises(ValueError):
            m.collect([],Path(t),[],lambda url:None)


if __name__=='__main__':unittest.main()
