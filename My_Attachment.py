import sys
import email
import imaplib, os, getpass

dir = '.'
if 'Resume_Download' not in os.listdir(dir):
    os.mkdir('Resume_Download')

userName = raw_input('Enter your gmail id: ')
passwd = getpass.getpass('Enter your password: ')

try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, mail = imapSession.login(userName,passwd)
    if typ != 'OK':
        print 'Wrong Username or Password'
        raise

    print typ, mail

    imapSession.select('Inbox')
    typ, data = imapSession.search(None,'(SUBJECT "Resume")')
    if typ != 'OK':
        print 'Error'
    if data is not []:
        print 'No emails found with Subject "Resume"'

    #Checking all the emails with Subject 'Resume' 
    for msgId in data[0].split():
        typ, messageParts = imapSession.fetch(msgId,'(RFC822)')
        if typ != 'OK':
            print 'Error fetching mail'
            
        emailBody = messageParts[0][1]
        mail = email.message_from_string(emailBody)

        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            print fileName

            if bool(fileName):
                filePath = os.path.join(dir, 'Resume_Download', fileName)
                print filePath
                if not os.path.isfile(filePath):
                    print fileName
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
    imapSession.close()
    imapSession.logout()
    
except Exception, e:
    print repr(e)