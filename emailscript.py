import smtplib
import ssl
import csv
import pandas as pd
import openpyxl
import io
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
import webbrowser

# Add new email to the email file
def newEmail(name, randomEmail):
    csvFile = open('emails.csv', mode='a')
    csvWriter = csv.DictWriter(csvFile, fieldnames=["name", "email"])
    csvWriter.writerow({"name": name, "email": randomEmail})

# Find a corresponding email based on a name
def findEmail(name):
    with open('emails.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if name in row:
                data = list(reader)
                return data[1]

# Convert the schedule to an interpretable dataframe
def conSchedule(file):
    schedule = pd.read_excel(file, engine='openpyxl')
    schedule.columns = schedule.iloc[3]
    schedule = schedule[4:]
    return schedule

# Find the row of the schedule with the individual's name
def parseSchedule(schedule, name):
    row = schedule[schedule.iloc[:, 0].str.match(name, na=False)]
    return row

# Convert the extracted row of a dataframe as a readable excel file
def exportExcel(df):
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(writer)
        return buffer.getvalue()

# Send the actual email
def sendEmail(receive, subject, df, export):
    multipart = MIMEMultipart()
    multipart['From'] = email
    multipart['To'] = receive
    multipart['Subject'] = subject
    for filename in export:
        attachment = MIMEApplication(export[filename])
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        multipart.attach(attachment)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls(context=context)
    s.ehlo()
    s.login(email, password)
    s.sendmail(email, receive, multipart.as_string())
    s.quit()

# Combine the functions in order to email each person their portion of the schedule
def sendSchedules(file):
    workerNames = []
    workerEmails = []
    with open('emails.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        for i in range(1, len(data)):
            try:
                workerNames.append(data[i][0])
                workerEmails.append(data[i][1])
            except IndexError:
                pass
    schedule = conSchedule(file)
    for i in range(len(workerNames)):
        snippet = parseSchedule(schedule, workerNames[i])
        excel = exportExcel(snippet)
        export = {'schedule.xlsx': excel}
        sendEmail(workerEmails[i], "A&W Schedule", snippet, export)

# Change the screen to upload a new email
def newEmailScreen(buttons):
    for i in range(len(buttons)):
        buttons[i].forget()
    nameLabel = Label(canvas, text="Employee Name:", bg="dodgerblue")
    nameEntry = Entry(canvas)
    emailLabel = Label(canvas, text="Employee Email:", bg="dodgerblue")
    emailEntry = Entry(canvas)
    submit = Button(canvas, text="Submit", bg="aqua", command=lambda: [newEmail(nameEntry.get(), emailEntry.get()),
                                                                             returnMainMenu([nameLabel, nameEntry,
                                                                                             emailLabel, emailEntry,
                                                                                             submit])])
    nameLabel.pack(padx=305, pady=(80, 1))
    nameEntry.pack(padx=305, pady=(0, 40))
    emailLabel.pack(padx=305, pady=(0, 1))
    emailEntry.pack(padx=305, pady=(0, 40))
    submit.pack(padx=305, pady=(0, 80))

# Return to the main menu
def returnMainMenu(widgets):
    for i in range(len(widgets)):
        widgets[i].forget()
        add.pack(padx=305, pady=(80, 40))
        send.pack(padx=305, pady=(0, 40))
        message.pack(padx=305, pady=(0, 40))
        opening.pack(padx=305, pady=(0, 80))

# Write a message to be sent out to all employees
def messageScreen(buttons):
    for i in range(len(buttons)):
        buttons[i].forget()
    subjectLabel = Label(canvas, text="Subject:", bg="dodgerblue")
    subjectEntry = Entry(canvas)
    messageLabel = Label(canvas, text="Message:", bg="dodgerblue")
    messageEntry = Entry(canvas)
    submit = Button(canvas, text="Submit", bg="aqua", command=lambda: [sendMessage(subjectEntry.get(),
                                                                                   messageEntry.get()),
                                                                       returnMainMenu([subjectLabel, subjectEntry,
                                                                                       messageLabel, messageEntry,
                                                                                       submit])])
    subjectLabel.pack(padx=305, pady=(80, 1))
    subjectEntry.pack(padx=305, pady=(0, 40))
    messageLabel.pack(padx=305, pady=(0, 1))
    messageEntry.pack(pady=(0, 40), ipadx=250)
    submit.pack(padx=305, pady=(0, 80))

# Send the written message to all employees
def sendMessage(subject, message):
    workerNames = []
    workerEmails = []
    with open('emails.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        for i in range(1, len(data)):
            try:
                workerNames.append(data[i][0])
                workerEmails.append(data[i][1])
            except IndexError:
                pass
    for i in range(len(workerNames)):
        sendEmail2(workerEmails[i], subject, message)

# Send a message with text opposed to an excel file with a schedule
def sendEmail2(receive, subject, message):
    multipart = MIMEMultipart()
    multipart['From'] = email
    multipart['To'] = receive
    multipart['Subject'] = subject
    message = MIMEText(message)
    multipart.attach(message)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls(context=context)
    s.ehlo()
    s.login(email, password)
    s.sendmail(email, receive, multipart.as_string())
    s.quit()

# Create the main menu and execute functions in the GUI
email = "AWCanada.no.reply@gmail.com"
password = "Drillers03"
context = ssl.create_default_context()
root = Tk()
root.title("EmailBot")
canvas = Canvas(root, bg="dodgerblue", height=375, width=640)
canvas.pack()
add = Button(canvas, text="Add New Email", bg="aqua", command=lambda: newEmailScreen([add, send, opening, message]))
send = Button(canvas, text="Send New Schedule", bg="aqua", command=lambda: sendSchedules(fd.askopenfilename()))
opening = Button(canvas, text="See Current Employees", bg="aqua", command=lambda: webbrowser.open('emails.csv'))
message = Button(canvas, text="Send New Message", bg="aqua", command=lambda: messageScreen([add, send, opening,
                                                                                            message]))
add.pack(padx=305, pady=(80, 40))
send.pack(padx=305, pady=(0, 40))
message.pack(padx=305, pady=(0, 40))
opening.pack(padx=305, pady=(0, 80))
root.mainloop()
