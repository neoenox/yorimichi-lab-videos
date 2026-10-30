import sys,time,importlib.util
vid=sys.argv[1]; sys.argv=['x']
spec=importlib.util.spec_from_file_location('yt','scripts/yt_api.py'); yt=importlib.util.module_from_spec(spec); spec.loader.exec_module(yt)
s=yt.service()
for i in range(120):
    v=s.videos().list(part='status,contentDetails',id=vid).execute()['items'][0]
    st=v['status']['uploadStatus']; d=v['contentDetails'].get('duration','')
    if st=='processed' or d not in ('','P0D'):
        print('READY',vid,st,d); break
    time.sleep(60)
else: print('TIMEOUT',vid)
