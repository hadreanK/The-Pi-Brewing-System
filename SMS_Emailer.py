import smtplib

class SMS_emailer():
    def __init__(self):
        self.email_acct = 'piespyder@gmail.com'
        self.pw = 'pys'
        self.recipients = []
        self.server = smtplib.SMTP( "smtp.gmail.com", 587 )
        self.server.starttls()
        self.server.login( self.email_acct, self.pw + 'pider')

    def add_recipient(self, sms_email):
        self.recipients.append(sms_email)
    
    def send_sms(self, message_text):
        i = -1
        for i in range(0,len(self.recipients)):
            self.server.sendmail( '<from>', 
                        self.recipients[i],
                        message_text)
        print('Sent ' + str(i+1) + ' texts to recipeients!')


    
#perso_phone = '12063512893@newtextmail.com'
#perso_phone = '2063512893@tmomail.net'
#work_phone = '2535690029@vtext.com'

#TestText = SMS_emailer()
#TestText.send_sms("Hello world! Your beer is chugging along. No pun intended.")
#TestText.add_recipient(perso_phone)
#TestText.send_sms("Hello world! Your beer is chugging along. No pun intended.")
#TestText.add_recipient(work_phone)
#TestText.send_sms("Hello world! Your beer is chugging along. No pun intended.")