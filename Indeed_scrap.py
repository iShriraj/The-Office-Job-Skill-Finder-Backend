import csv,re,json,time,requests
from datetime import datetime
from bs4 import BeautifulSoup
start_time = time.time()
count = 0
di=dict()
def get_record(card,recrd):
    try:
        string = card.find('span','salaryText').text.strip()
        salary = ''.join(e for e in string if e.isprintable())
        job_title = card.h2.a['title']
        job_url = 'https://www.indeed.co.in'+card.h2.a.get('href')
        company = card.find('span','company').text.strip()
        response = requests.get(job_url)
        soup = BeautifulSoup(response.text,'html.parser')
        content = soup.find('div','jobsearch-jobDescriptionText').text.strip()
    except AttributeError:
        return

    skillset=['Python', 'R', 'SQL', 'Spark', 'Hadoop', 'Java', 'SAS', 'Tableau',
          'Hive', 'Scala', 'AWS', 'TensorFlow', 'Matlab', 'C', 'Excel', 
          'Linux', 'NoSQL', 'Azure', 'Scikit-learn', 'SPSS', 'Pandas', 'Numpy', 
          'Pig', 'D3', 'Keras', 'Javascript', 'C#', 'Perl', 'Hbase', 'Docker', 
          'Git', 'MySQL', 'MongoDB', 'Cassandra', 'PyTorch', 'Caffe']
    newcontent=""
    for skill in skillset:
        match = re.search(skill,content)
        if match:
            newcontent=newcontent+skill+" " 
            
    
    dict['jobtitle']=job_title
    dict['company']=company
    dict['skills']=newcontent
    dict['salary']=salary
    
    for key in dict.keys:
        recrd.append(dict)
        

    #print(dict)

    print(recrd)
  
    global count
    count+=1
    
    return dict

def main(position,location):
    jobrecord=[]
    recrd=[]
    template = "https://www.indeed.co.in/jobs?q={}&l={}"
    url = template.format(position,location)
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        cards = soup.find_all('div','jobsearch-SerpJobCard')
        for card in cards:
            global count
            if(card.find('span','salaryText') and count<5):
                record=get_record(card,recrd)
                jobrecord.append(record)
        try:
            url = 'https://www.indeed.co.in' + soup.find('a',{'aria-label':'Next'}).get('href')
        except AttributeError:
            break       
    
    jobrecord.append(dict)
    print(jobrecord)
    data=jobrecord
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile,indent=4)
    
    t=int((time.time() - start_time))/60
    print("--- %s minutes ---" % t)
    print("Entries scraped : %d"%count)
    
main("Software Engineer","Pune")