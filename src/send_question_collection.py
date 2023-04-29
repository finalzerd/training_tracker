__author__ = "noah.provenzano@fischerjordan.com"

import os
import sys
from typing import List


sys.path.append(r"C:\Users\noahp\Documents\Fischer Jordan\AWS Instance\custom_trackers\training_tracker")
from classes.fj_email_simple import FJEmailSimple

collection_members = [
    {"name": "Mohammed",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Mohammed+Abdul+Muqeet&entry.1782741899=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.1354554490=*Please+provide+response+here*&entry.296939417=*Please+provide+response+here*&entry.219889879=*Please+provide+response+here*&entry.1153475970=*Please+provide+response+here*",
     "email": "mohammedabdul.muqeet@fischerjordan.com",
     },
    {"name": "Yash",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Yash+Jain&entry.1121456460=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.359040718=*Please+provide+response+here*&entry.1118719493=*Please+provide+response+here*&entry.296939417=*Please+provide+response+here*&entry.1162655785=*Please+provide+response+here*",
     "email": "yash.jain@fischerjordan.com",
     },
    {"name": "Digvijay",
     "link": "",
     "email": "digvijay.chakrabarti@fischerjordan.com",
     },
    {"name": "Abhigya",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Abhigya+Singh&entry.1782741899=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.1354554490=*Please+provide+response+here*&entry.296939417=*Please+provide+response+here*&entry.219889879=*Please+provide+response+here*&entry.1153475970=*Please+provide+response+here*",
     "email": "abhigya.singh@fischerjordan.com",
     },
    {"name": "Abhishek",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSdwquJZFdCx1c3cPz4OUExO1w8RJL2MbBK56tUildM47zSwBw/viewform?usp=pp_url&entry.1961833826=abhishek.sahu@fischerjordan.com&entry.263768831=Abhishek+Sahu&entry.1892952282=SQL+-+MySQL+for+Data+Analytics+and+Business+Intelligence",
     "email": "abhishek.sahu@fischerjordan.com",
     },
    {"name": "Eeshita",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Eeshita+Verma&entry.1121456460=*Please+provide+response+here*&entry.1782741899=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.1118719493=*Please+provide+response+here*",
     "email": "eeshita.verma@fischerjordan.com",
     },
    {"name": "Raghav",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Raghav+Goel&entry.1121456460=*Please+provide+response+here*&entry.1782741899=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.1118719493=*Please+provide+response+here*",
     "email": "raghav.goel@fischerjordan.com",
     },
    {"name": "Kriti",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Kriti+Bhasin&entry.1121456460=*Please+provide+response+here*&entry.1782741899=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1478620376=*Please+provide+response+here*&entry.1118719493=*Please+provide+response+here*",
     "email": "kriti.bhasin@fischerjordan.com",
     },
    {"name": "Kavya",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Kavya+Shree&entry.1782741899=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*&entry.1354554490=*Please+provide+response+here*",
     "email": "kavya.shree@fischerjordan.com",
     },
    {"name": "Neeyati",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Neeyati&entry.1782741899=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1621869890=*Please+provide+response+here*",
     "email": "neeyati.fitkariwala@fischerjordan.com",
     },
    {"name": "Samiksha",
     "link": "https://docs.google.com/forms/d/e/1FAIpQLSeDsBsTAOI8A3VrBZ__nc3YA1JQjcShwCoaa13RTaGGI3HxZQ/viewform?usp=pp_url&entry.101362756=Samiksha+Rai&entry.903154698=*Please+provide+response+here*&entry.1121456460=*Please+provide+response+here*&entry.1782741899=*Please+provide+response+here*&entry.331756342=*Please+provide+response+here*&entry.1354554490=*Please+provide+response+here*",
     "email": "samiksha.rai@fischerjordan.com",
     },

    
    
    
]

noah = "noah.provenzano@fischerjordan.com"
manager_emails: List[str] = ["anoushka.khanna@fischerjordan.com", "darshana.shetty@fischerjordan.com"]
for member in collection_members[-3:]:
    
    subject = "FJ Training Course - Action Required"
    message: str = f"""Hi {member['name']},<br><br>
                        Just a friendly reminder to fill out the quiz collection form.<br><br>
                        Please use the following link to submit your responses:<br><br>
                        <a href="{member['link']}">FJ Training Quiz Question Collection</a><br><br>
                        Thanks,<br><br>
                        FJ Training"""
        
    email = FJEmailSimple(to=[member['email']],
                        cc=manager_emails,
                        bcc=[noah],
                        subject=subject,
                        title=subject,
                        text=message)
    email.send()