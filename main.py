# import excel2json

# excel2json.convert_from_file('school_timetable.xls')
from http import server
from operator import mod
import yaml
import pandas
from yaml.loader import SafeLoader
from datetime import datetime
import math
import json
import subprocess
# import commands
from datetime import timedelta

def getWeekDate(*args):
    year,month,day = args
    year = int(year)
    year = year - int(year / 100) * 100    
    century = year // 100
    month = int(month)

    if month == 1 or month == 2:
        month = month + 12
        if year == 0:
            year = 99
            century = century - 1
        else:
            year = year - 1
    day =int(day)
    week = year + int(year/4) + int(century/4) - 2 * century + int(26 * (month + 1)/10) + day - 1
    if week < 0:
        weekDay = (week % 7 + 7) % 7
    else:
        weekDay = week % 7
    return weekDay

def open_class_yaml(class_name):

    excel_data_fragment = pandas.read_excel('school_timetable.xlsx', sheet_name=class_name)
    excel_to_json_string = excel_data_fragment.to_json()
    excel_string_to_json = json.loads(excel_to_json_string)

    class_schema = ['Student ID', 'Password', 'CPU', 'Memory', 'GPU', 'Node Port']
    
    yaml_data=[]

    with open("deploy.yaml", "r") as stream:
        try:
            yaml_data = list(yaml.load_all(stream, Loader=SafeLoader))
        except yaml.YAMLError as exc:
            print(exc)
    deploy = yaml_data[0]
    service = yaml_data[1]

    

    for i in range(len(excel_string_to_json[class_schema[0]])):
        # print(deploy['metadata']['name'])
        # print(excel_string_to_json[class_schema[1]][str(i)])

        # print(deploy)

        deploy['metadata']['namespace'] = class_name
        deploy['metadata']['name'] = "student-deploy-" + excel_string_to_json[class_schema[0]][str(i)]
        deploy['spec']['selector']['matchLabels']['app'] = "student-select" + excel_string_to_json[class_schema[0]][str(i)]
        deploy['spec']['template']['metadata']['labels']['app'] = "student-select" + excel_string_to_json[class_schema[0]][str(i)]
        deploy['spec']['template']['spec']['containers'][0]['args'] = [excel_string_to_json[class_schema[1]][str(i)]]
        deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = excel_string_to_json[class_schema[2]][str(i)]
        deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = excel_string_to_json[class_schema[3]][str(i)]
        deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = excel_string_to_json[class_schema[4]][str(i)]
        deploy['spec']['replicas'] = 1
        
        service['metadata']['namespace'] = class_name
        service['metadata']['name'] = "student-service-" + excel_string_to_json[class_schema[0]][str(i)]
        service['spec']['ports'][0]['nodePort'] = excel_string_to_json[class_schema[5]][str(i)]
        service['spec']['selector']['app'] = "student-select" + excel_string_to_json[class_schema[0]][str(i)]

        # print(deploy)
        # print(service)

        str_deploy = json.dumps(deploy)
        str_service = json.dumps(service)

        create_deploy([["echo", str_deploy],["kubectl", "apply","-f",'-']])
        create_deploy([["echo", str_service], ["kubectl", "apply","-f",'-']])

def turnoff_class_yaml(class_name):

    class_schema = ['Student ID', 'Password', 'CPU', 'Memory', 'GPU', 'Node Port']
    yaml_data=[]

    for value in class_name:

        excel_data_fragment = pandas.read_excel('school_timetable.xlsx', sheet_name=value)
        excel_to_json_string = excel_data_fragment.to_json()
        excel_string_to_json = json.loads(excel_to_json_string)

        for i in range(len(excel_string_to_json[class_schema[0]])):
            with open("deploy.yaml", "r") as stream:
                try:
                    yaml_data = list(yaml.load_all(stream, Loader=SafeLoader))
                except yaml.YAMLError as exc:
                    print(exc)
          
            deploy = yaml_data[0]
            deploy['metadata']['namespace'] = value
            deploy['metadata']['name'] = "student-deploy-" + excel_string_to_json[class_schema[0]][str(i)]
            deploy['spec']['selector']['matchLabels']['app'] = "student-select" + excel_string_to_json[class_schema[0]][str(i)]
            deploy['spec']['template']['metadata']['labels']['app'] = "student-select" + excel_string_to_json[class_schema[0]][str(i)]
            deploy['spec']['template']['spec']['containers'][0]['args'] = [excel_string_to_json[class_schema[1]][str(i)]]
            deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = excel_string_to_json[class_schema[2]][str(i)]
            deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = excel_string_to_json[class_schema[3]][str(i)]
            deploy['spec']['template']['spec']['containers'][0]['resources']['limits']['nvidia.com/gpu'] = excel_string_to_json[class_schema[4]][str(i)]
            deploy['spec']['replicas'] = 0

            str_deploy = json.dumps(deploy)

            create_deploy([["echo", str_deploy],["kubectl", "apply","-f",'-']])
            # print(command(deploy + " | kubectl apply -f"))

def create_ns(command):
    # The command you want to execute   
    # cmd = 'kubectl'
  
    # send one packet of data to the host 
    # this is specified by '-c 1' in the argument list 
    outputlist = []
    # Iterate over all the servers in the list and ping each server
    # for server in servers:
    p1 = subprocess.Popen(command, stdout = subprocess.PIPE) 

    output = str(p1.communicate()) 
    # store the output in the list
    outputlist.append(output)

    return outputlist

def create_deploy(servers):
    
    # The command you want to execute   
    # cmd = 'kubectl'
  
    # send one packet of data to the host 
    # this is specified by '-c 1' in the argument list 
    outputlist = []
    # Iterate over all the servers in the list and ping each server
    # for server in servers:
    # print(servers[0])
    # print(servers[1])

    p1 = subprocess.Popen(servers[0], stdout = subprocess.PIPE) 
    p2 = subprocess.run(servers[1], stdin=p1.stdout)

    output = str(p2) 
    # store the output in the list
    outputlist.append(output)

    return outputlist

def ping(servers):
    
    # The command you want to execute   
    cmd = 'ping'
  
    # send one packet of data to the host 
    # this is specified by '-c 1' in the argument list 
    outputlist = []
    # Iterate over all the servers in the list and ping each server
    for server in servers:
        # temp = subprocess.Popen([cmd, '-c 1', server], stdout = subprocess.PIPE) 
        temp = subprocess.Popen(['kubectl', 'get', 'nodes'], stdout = subprocess.PIPE) 

        # get the output as a string
        output = str(temp.communicate()) 
    # store the output in the list
        outputlist.append(output)
    return outputlist

def main():

    today = datetime.today().strftime('%Y %m %d')
    # today = "2022 3 8"
    now_time = datetime.today()
    # now_time = "2022 3 8 16:30:30"

    year,month,day = today.split(' ')
    week= getWeekDate(year,month,day)


    sheet_class_name_lsit  = ["a-class", "b-class", "c-class"]

    for value in sheet_class_name_lsit:
        # commands("kubectl", "create ns " + value)
        create_ns(["kubectl", "create", "ns", value])
        

    excel_data_fragment = pandas.read_excel('school_timetable.xlsx', 'timetable')
    excel_to_json_string=excel_data_fragment.to_json()
    excel_string_to_json = json.loads(excel_to_json_string)

    week_list = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]

    week_string = week_list[week]

    time_table_interval = excel_string_to_json["Time"]
    time_interval = excel_string_to_json["Time interval"][str(0)]

    print(time_table_interval)

    today_time_table = excel_string_to_json[week_string]

    print(today_time_table)

    fmt = '%Y %m %d %H:%M:%S'
    
    first_time_in_table = datetime.strptime(today + " " + time_table_interval[str(0)], fmt)
    last_time_in_table = datetime.strptime(today + " " + time_table_interval[str(len(time_table_interval) - 1)], fmt)


    if now_time < first_time_in_table or now_time > last_time_in_table:
        turnoff_class_yaml(sheet_class_name_lsit)
    else:
        for i in range(len(time_table_interval) - 1):
            start_time = datetime.strptime(today + " " + time_table_interval[str(i)], fmt)
            next_interval_time = start_time + timedelta(minutes=time_interval)

            if start_time <= now_time and next_interval_time >= now_time:
                print(start_time)
                print(now_time)
                print(next_interval_time)
                time_table_class = today_time_table[str(i)]
                print(time_table_class)

                if time_table_class != None:
                    open_class_yaml(time_table_class)

                    x = [j for j in sheet_class_name_lsit if j != time_table_class]
                    turnoff_class_yaml(x)
                else:
                    turnoff_class_yaml(sheet_class_name_lsit)

                break
        
main()

