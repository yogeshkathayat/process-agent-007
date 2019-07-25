import psutil
import datetime
import time
from pymongo import MongoClient 
  

def getListOfProcessSortedByMemory(sortParam):
    '''
    Get list of running process sorted by the parameter
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username','memory_percent','cpu_percent'])
           # Append dict to list
           listOfProcObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
 
    # Sort list of dict by key sortParam i.e. memory_percent
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj[sortParam], reverse=True)
 
    return listOfProcObjects


def capture():
    
    try: 
        conn = MongoClient("mongodb://localhost:27017/") #you can put your mongodb connection string
        print("Connected successfully!!!")
        mydb = conn["Python-hackathon"]
        mycol = mydb["processes"]
        
        listOfRunningProcess = getListOfProcessSortedByMemory('memory_percent') #pass the sorting parameter for processes
        mycol.insert_one({"timeStamp":datetime.datetime.now(), "processes":listOfRunningProcess}) #insert data into mongodb
        
        print('*** process with sorted by memory_percent %***')
        for elem in listOfRunningProcess:
            print(elem)
                 
    except:   
        print("Could not connect to MongoDB") 
    time.sleep(60)

def main():
   while True:
    capture()
    

if __name__ == '__main__':
   main()