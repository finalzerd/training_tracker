
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from typing import List


class Email:
    def __init__(self, to:List[str]=None, cc:List[str]=None, bcc:List[str]=None, subject:str="", html:str="", images:List[MIMEImage]=None) -> None:
        self.to = [] if to == None else to
        self.cc = [] if cc == None else cc
        self.bcc = [] if bcc == None else bcc

        self.subject = subject
        self.html = html
        self.images = [] if images == None else images

        self.username = 'fjhr@fischerjordan.com'
        self.password = 'Lockheed01'

    def send(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.username
        msg['To'] = ", ".join(self.to)
        msg['Cc'] = ", ".join(self.cc)
        cc_address = self.cc
        bcc_address = self.bcc
        
        msg.attach(MIMEText(self.html, 'html'))

        for image in self.images:
            msg.attach(image)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self.username, self.password)
        server.sendmail(msg['From'], self.to + cc_address +  bcc_address,  msg.as_string())
        server.close()

        print (f"Email sent: {self.subject}")
    
    def load_images(self, image_directories:List[str]):
        for directory in image_directories:
            image_file = open(directory, 'rb')
            image = MIMEImage(image_file.read(), 'png')
            image_file.close()

            image.add_header('Content-ID', f'<img_id_{os.path.basename(directory)}>')
            image.add_header('Content-Disposition', 'inline', filename=os.path.basename(directory))
            self.images.append(image)
        

class TextEmail(Email):
    def __init__(self, to:List[str]=None, cc:List[str]=None, bcc:List[str]=None, subject:str="", text:str="") -> None:
        super().__init__(to=to, 
                         cc=cc, 
                         bcc=bcc, 
                         subject=subject, 
                         html=f"<html><body><p>{text}</p></body></html>")