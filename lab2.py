from spyne import Application, rpc, ServiceBase
from spyne import    Integer, Unicode, String, Iterable
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
import logging
from wsgiref.simple_server import make_server
import requests

class Lab2(ServiceBase):
    @rpc(String, String, String, _returns=Iterable(String))
    def checkcrime(ctx,lat,lon,radius):
        
        
        output_data={"crime_type_count":[],"event_time_count":[], "the_most_dangerous_street":[]}
        total_crime=0
        Assaul=0
        Arres=0
        Burglar=0
        Robber=0
        Thef=0
        Othe=0
        crime_type_count={}
        event_time_count={}
        street_name={}
        block_flag=0
        the_most_dangerous_street=[]
        
        twelve_to_three_am=0
        three_to_six_am=0
        six_to_nine_am=0
        nine_to_twelve_am=0
        
        twelve_to_three_pm=0
        three_to_six_pm=0
        six_to_nine_pm=0
        nine_to_twelve_pm=0
        No_Data_fetched=0
        
        
        parameters={"lat":lat,"lon":lon,"radius":radius,"key":"."}
        response = requests.get("https://api.spotcrime.com/crimes.json?",params=parameters)
        data=response.json()
        jsondata=data["crimes"]
        if not jsondata:
            No_Data_fetched=1
            No_data="No data fetched/Wrong Co-ordinates"
            yield No_data
        
        
        
        
        """total_crime"""
        for item in jsondata:
            total_crime=total_crime+1
        output_data["total_crime"]=total_crime
       
       
        OF_flag_count=0
        and_flag_count=0
        no=0
        
        """most_dangerous_street"""
        for item in jsondata: 
            and_occur=0
            street=""
            street1=""
            block_flag=0
            and_flag=0
            street1_flag=0
            address=item.get("address")
            add1=address.split()
            match_block="BLOCK"
            match_and=" & "
            
            if(match_and in address):
                and_flag=1
            
            if(match_block in address):
                block_flag=1
                and_flag=0
                
            
            
            if block_flag==1:
                OF_flag_count +=1
                for i in range(2,len(add1)):
                    if(add1[i]!= "OF" and add1[i]!= "BLOCK"):
                        street=street+add1[i]+" "
                if street in street_name:
                    street_name[street] += 1
                else:
                    street_name[street] = 1
            
            
            elif and_flag==1:
                and_flag_count +=1
                street1_flag=1
                for i in range (0,len(add1)):
                    if add1[i]=="&":
                        and_occur=1
                        
                    if and_occur == 0:
                        street=street+add1[i]+" "
                    
                    if and_occur == 1:
                        street1=street1+add1[i]+" "
                
                if street in street_name:
                    street_name[street] += 1
                else:
                    street_name[street] = 1
                    
                if street1_flag==1:
                    if street1 in street_name:
                        street_name[street1] += 1
                    else:
                        street_name[street1] = 1
            else:
                no +=1
                street=address+" "
                if street in street_name:
                    street_name[street] += 1
                else:
                    street_name[street] = 1
                        
            
                
        c=sorted(street_name,key=street_name.__getitem__, reverse=True)
        clen=len(c)
        
        
        if int(clen>0):
            the_most_dangerous_street.append(c[0])
        if int(clen)>1:
            the_most_dangerous_street.append(c[1])
        if int(clen)>2:
            the_most_dangerous_street.append(c[2])
        
        output_data["the_most_dangerous_street"].append(the_most_dangerous_street)   
        
        
        
        
        """crime_type_count_dynamic"""
        for item in jsondata:
            crime_name=""
            crime_name=item.get("type")
            if crime_name in crime_type_count:
                crime_type_count[crime_name] += 1
            else:
                crime_type_count[crime_name] = 1
        output_data['crime_type_count'].append(crime_type_count)
        
        
        counter=0
        
        
        """ event_time_count"""
        for item in jsondata: 
            time1=item.get("cdid")
            time=item.get("date")
            timesp=time.split()
            for word in timesp:
                if word == "AM":
                    counter +=1
                    key=timesp
                    values=key[1].split(":")
                    if int(values[0])==12:
                        if int(values[1])!=00:
                            twelve_to_three_am=twelve_to_three_am+1
                            
                            
                            
                        elif int(values[1])==00:
                            nine_to_twelve_am=nine_to_twelve_am+1
                            
                    elif int(values[0])>0 and int(values[0])<3:
                        twelve_to_three_am=twelve_to_three_am+1
                        
                    elif int(values[0])==3:
                        if int(values[1])!=00:
                            three_to_six_am=three_to_six_am+1
                            
                        elif int(values[1])==00:
                            twelve_to_three_am=twelve_to_three_am+1
                            
                    elif int(values[0])>3 and int(values[0])<6:
                        three_to_six_am=three_to_six_am+1
                        
                    elif int(values[0])==6:
                        if int(values[1])!=00:
                            six_to_nine_am=six_to_nine_am+1
                            
                        elif int(values[1])==00:
                            three_to_six_am=three_to_six_am+1
                            
                    elif int(values[0])>6 and int(values[0])<9:
                        six_to_nine_am=six_to_nine_am+1 
                        
                    elif int(values[0])==9:
                        if int(values[1])!=00:
                            nine_to_twelve_am=nine_to_twelve_am+1
                            
                        elif int(values[1])==00:
                            six_to_nine_am=six_to_nine_am+1
                            
                    elif int(values[0])>9 and int(values[0])<12:
                        nine_to_twelve_am=nine_to_twelve_am+1   
                        
                    
                elif word == "PM":
                    counter +=1
                    key=timesp
                    values=key[1].split(":")
                    if int(values[0])==12:
                        if int(values[1])!=00:
                            twelve_to_three_pm=twelve_to_three_pm+1
                            
                            
                        elif int(values[1])==00:
                            nine_to_twelve_pm=nine_to_twelve_pm+1
                            
                    elif int(values[0])>0 and int(values[0])<3:
                        twelve_to_three_pm=twelve_to_three_pm+1
                        
                    elif int(values[0])==3:
                        if int(values[1])!=00:
                            three_to_six_pm=three_to_six_pm+1
                            
                        elif int(values[1])==00:
                            twelve_to_three_pm=twelve_to_three_pm+1
                            
                    elif int(values[0])>3 and int(values[0])<6:
                        three_to_six_pm=three_to_six_pm+1
                        
                    elif int(values[0])==6:
                        if int(values[1])!=00:
                            six_to_nine_pm=six_to_nine_pm+1
                            
                        elif int(values[1])==00:
                            three_to_six_pm=three_to_six_pm+1
                            
                    elif int(values[0])>6 and int(values[0])<9:
                        six_to_nine_pm=six_to_nine_pm+1
                        
                        
                    elif int(values[0])==9:
                        if int(values[1])!=00:
                            nine_to_twelve_pm=nine_to_twelve_pm+1
                            
                            
                        elif int(values[1])==00:
                            six_to_nine_pm=six_to_nine_pm+1
                           
                            
                    elif int(values[0])>9 and int(values[0])<12:
                        nine_to_twelve_pm=nine_to_twelve_pm+1    
                      
                    
                
        event_time_count["12:01 to 03:00 AM"]=twelve_to_three_am
        event_time_count["03:01 to 06:00 AM"]=three_to_six_am
        event_time_count["06:01 to 09:00 AM"]=six_to_nine_am
        event_time_count["09:01 to 12:00 AM"]=nine_to_twelve_am
        event_time_count["12:01 to 03:00 PM"]=twelve_to_three_pm
        event_time_count["03:01 to 06:00 PM"]=three_to_six_pm
        event_time_count["06:01 to 09:00 PM"]=six_to_nine_pm
        event_time_count["09:01 to 12:00 PM"]=nine_to_twelve_pm            
        output_data['event_time_count'].append(event_time_count)
        
        
        
        
        if No_Data_fetched == 0:
            yield output_data    

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)

    application = Application([Lab2],'spyne.examples.hello.http',
    in_protocol=HttpRpc(validator='soft'),
    out_protocol=JsonDocument(),
    )
    wsgi_app=WsgiApplication(application)

    server=make_server('127.0.0.1', 8000, wsgi_app)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/wsdl")

    server.serve_forever()

