import wget

for i in range(0,55):
    url = 'http://stash.osgconnect.net/+rvanguri/AEOLUS_all_reports_'+str(i)+'.npy'
    print wget.download(url)
