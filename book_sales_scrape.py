from bs4 import BeautifulSoup
import urllib2
import os
import codecs


# Set environment variables based on .env file if present.  
#sing this along with a .env file, WHICH IS NOT CHECKED INTO YOUR REPO! 
#(aka is listed in your .gitignore) will allow you to set environment variables per 
#project in each project's own .env when working locally.
if os.path.exists('.env'):
    print('Detected local .env, importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]
            print "Setting environment variable:", var[0]
            sys.stdout.flush()

#  Later, you can access variables set in the environment, whether loaded above 
#from .env or loaded from the actual environment 
#(as in Heroku or AWS or Domino, etc.) with something like:
# foo = os.getenv('BAR')


wiki = "https://en.wikipedia.org/wiki/List_of_best-selling_books#List_of_best-selling_single-volume_books"
header = {'User-Agent': os.getenv(WIKIPEDIA_USER)} #Use wikipedia user in .env file
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, "lxml")
 

tables = soup.findAll("table", { "class" : "wikitable" })

for tn in range(len(tables)):
    table = tables[tn]

    # Initialize tables to be filled in
    rows = table.findAll("tr")
    row_lengths =[len(r.findAll(['th','td'])) for r in rows]
    ncols = max(row_lengths)
    nrows = len(rows)
    data = []
    for i in range(nrows):
        row_data = []
        for j in range(ncols):
            row_data.append('')
        data.append(row_data)
    
    #Process html, fill lists with data from table
    for i in range(len(rows)):
        row = rows[i]
        row_data = []
        cells = row.findAll(["td","th"])
        for j in range(len(cells)):
            cell = cells[j]
            
            #for cells that span columns and rows
            cspan = int(cell.get('colspan',1))
            rspan = int(cell.get('rowspan',1))
            for k in range(rspan):
                for l in range(cspan):
                    data[i+k][j+l] += cell.text
    
        data.append(row_data)
        
    #Write data to CSV
    
        page = os.path.split(wiki)[1]
    fname='{}_tbl_{}.csv'.format(page.split('#')[1],tn)
    f = codecs.open(fname, 'w') #encoding='utf-8')
    for i in range(nrows):
        rowStr=','.join(data[i])
        rowStr=rowStr.replace('\n','')
        rowStr=rowStr.encode('unicode_escape')
        f.write(rowStr+'\n')      
        
        
    f.close()