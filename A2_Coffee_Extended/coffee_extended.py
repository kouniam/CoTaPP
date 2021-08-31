
"""
Created on Mon Mar  8 14:20:17 2021

@author: ruggerobelluomo (6898009), brunorodrigues (3929736), nelsonvanduin (1195875), kimbutter (1715607)
"""

import pandas as pd
import random 
from ast import literal_eval
import time
import re

#-----------------------------------------------------------------------------#
#                          EXTENDED MYSTERY COFFEE
#-----------------------------------------------------------------------------#

# The following script will suggest the best group size according to the number of 
#participants signed into the local .csv file (we provide an example template).
# The user can then select the group size (restricted to 2,3,4,5 as large groups can't
#really be considered good for cohesive conversations).
# Groups are then allocated and stored in an external text file that is used to
#compare future groups formed by the program (multiple rounds correspond to multiple
#runnings of this program). If a certain group pairing has already occured, a
#function was written in order to shuffle participants around and form new, unique
#pairings. Please note that this can lead to unique pairings being exhausted if not
#enough (new) participants are signed up on the .csv file. For this reason we have
#set an upper limit to the number of shuffling attempts.
# Each group is assigned a random conversation starter that is extrated from a web
#page; the string cleaning of the topics is done by a separate function.
# Finally, we send personalized emails to every participant, informing them of the 
#group pairings and which group they are in. Running the program too frequently may 
#result in an error sending emails due them getting marked as spam.

#Sets local .csv file to use
local_form = 'Coffee_extended.csv' 

#Import and read file
df = pd.read_csv(local_form, error_bad_lines=False)
participant_name_list = df["Your name:"].tolist()
emails_list = df["Your e-mail:"].tolist()

#initialization variables
coupling_memory=[]

#unshuffled name storage
unsh_names = participant_name_list.copy()

def check_n():
    global n
    n=0
    rec = []
    for i in range(2,6):
        if (len(participant_name_list) % i == 0 ):
            rec.append(i)
    
    #check again if no recommendations were added
    if len(rec) == 0:
        for i in range(2,6):
            if (len(participant_name_list) % i == 1 ):
                rec.append(i)
            
    print(f"\nGiven the number of signed participants, we recommend the following group size(s): {rec}")
    time.sleep(1)    
    while (n < 2) or (n > 5):
        time.sleep(2)
        print("\nHow many people per group would you like to have? ")
        n=int(input(">>> "))
        if n == 1:
            print("\nGroups of one person don't make much sense, do they? Please insert a valid input.\n")
            time.sleep(3)
        elif n > 5:
            print("Group size too big. More than five people is hardly a conversation. Please insert a valid input.\n")
            time.sleep(3)
    if len(participant_name_list)%n==1:
         print("Be aware, one person with no matching has been added to another group!")
         time.sleep(3)
        

def make_groups(lst):  
    global coupling_memory 
    
    coupling_memory=sorted(coupling_memory) #sort the memory by character 
    my_dict={} #create a dict for the groups
    groups_list=[]  #create the list of groups
    random.shuffle(lst) #shuffle the participants
    count=1
    for e in range(0,len(lst),n):
        my_elem=sorted(lst[e:e+n])  #make groups in steps of n from the participant
        if ((my_elem in coupling_memory or my_elem in groups_list) and len(groups_list)>=1):  #if the group is already in the memory
            my_elem=shuffling(my_elem,groups_list,participant_name_list) #shuffle the group
 
        else:
            groups_list.append(my_elem) #if the group is unique make it as a group and add to the group list
            
    for e in range(0,len(groups_list)):
        if (len(groups_list[e])<len(groups_list[e-1])-2 or len(groups_list[e])==1): #if a groups has less than 2 people compared to others
            print("Unequal groups detected...joining groups in unique ways!")
            time.sleep(2)
            if groups_list[e][0:] not in groups_list[e:e-1]: #if the smaller group is not in the previous groups
                groups_list[e-1]=groups_list[e-1] + groups_list[e][0:len(groups_list)//2] #split and add half group to the 2 priovius groups
                groups_list[e-2]=groups_list[e-2] + groups_list[e][len(groups_list)//2:]
                del groups_list[e] #delete the element
            if groups_list[e-1] in coupling_memory:
                groups_list=shuffling(groups_list[e-1])# if the new groups are not unique...shuffle them
            if groups_list[e-2] in coupling_memory:
                groups_list=shuffling(groups_list[e-2])
         
                
    for e in range(0,len(groups_list)): #create the nice printing
        my_dict[count]=groups_list[e] #print every key (group number) and name of the people in the group
        count+=1 #increase count of the group
    for values in my_dict.values():
        coupling_memory.append(values) #append the new groups to coupling memory                 
    return my_dict


def shuffling(lst, lst2,participant_name_list):   #shuffling function when an old pair is tried to be added
    global coupling_memory
    print("Shuffling...couple already matched detected!") 
    while True:  #until you don't find a new group


        for e in range(lst): #change every element of the group with a random one
            lst[e]= random.choice(participant_name_list) 
        for j in range(lst):
            if any( lst[j] in sublist for sublist in lst2)==True :
                continue  #if the new group formed is already in the memory, or it's already being formed ...keep swapping
            else:
                break #if it is a new group, finish shuffling
     
    return lst2


def send_emails(my_dict):
    import smtplib
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    MY_ADDRESS="host_bot@outlook.com"
    MY_PASSWORD="Password12345"
    s.login(MY_ADDRESS,MY_PASSWORD)
    names=unsh_names # read contacts
    emails=emails_list
    
    message_template = "Here are next Friday's Mistery Coffee groups! \n\n"
    
    for k in coffee_groups.keys():
        message_template = message_template + str(k) + " : " + str(coffee_groups[k]) + "\n"
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        first_name = name.split(' ', 1)[0]
        message = "Hi there " + first_name + ". "
        
        for k in coffee_groups.keys():
            if name in coffee_groups[k]:
                message = message + "You have been placed into group " +str(k) + ".\n"

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Mystery Coffee Pairings"

        # add in the message body
        message = message + message_template
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
    
        del msg
        print(f"Message sent to {name} with email: {email}.")   #OPTIONAL
    print ("\nAll done! See you next time.")


def get_topics():
    import requests
    import bs4
    topics=[]

    try:
        response=requests.get("https://conversationstartersworld.com/250-conversation-starters/")
    except Exception as err:
             print("Something went wrong:", err)
             response = None
    if response!=None:
         if response.ok:
             html_doc = response.text
         else:
             print("Something went wrong with status code", \
                   response.status_code)
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    topic_generator=soup.find_all("h3")
    for tg in topic_generator:
         topics.append(tg.contents[0].strip())     
    return topics


def repair_topics():
    new_topics=[]
    new_new_topic=[]
    final_topics=[]
    our_topics=get_topics()
    
    for topic in our_topics:
        file_lst_trimmed = re.sub(r'\n', ' ', topic)
        new_topics.append(file_lst_trimmed)
        
    for topic in new_topics:
        file_lst_trimmed = re.sub('\d+', ' ', topic)
        new_new_topic.append(file_lst_trimmed)
        
    for topic in new_new_topic:
       topic= topic.replace(topic[0:2],"")
       final_topics.append(topic)
       
    #webpage has an issue with entry 44 and the last one, so we delete them  
    del final_topics[44]
    del final_topics[-1]
    return final_topics
        
   
try:
    file_object= open('coupling_memory.txt')   #try opening the  file with coupling memory
    for line in file_object:    #for every group in the file
        line=line.strip('\r\n')   #split groups by \n
        coupling_memory.append(literal_eval(line))  #append every group to the memory

except FileNotFoundError:  #if the file cannot load (first time running the code)
      with open("coupling_memory.txt","w") as file:
            begin=""
            file.write(begin)  #create a new empty file
     
print("For program performances, a limit of trials for creating unique groups has been added...sorry for that!")   #OPTIONAL
time.sleep(2)                                                                           #OPTIONAL

check_n()
print("Creating groups....please wait.")
time.sleep(0.5)

all_topics=repair_topics()
attempt=0

while attempt <= 500:
    if attempt==500:
            print("Too many groups run with these participants and group size...please change the group size or the participants!")
            time.sleep(2)
    try:
        coffee_groups=make_groups(participant_name_list)    #run the function and create groups
        print("\nToday's Coffe groups are:") #print them
        for k in coffee_groups.keys():
            print(f"{k}:{coffee_groups[k]} and here's a conversation starter for you: {random.choice(all_topics)}\n")
        with open("coupling_memory.txt","w") as file: #save the memory as a list of lists txt file
                new_couples=coupling_memory
                for couple in new_couples:
                   
                    file.write('%s\n' % couple)
        break
    except:
        attempt+=1
        continue
    
send_emails(coffee_groups)    



