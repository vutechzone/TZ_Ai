import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

start_chat_log = '''Mac Imaging Documentation\nOverview: This documentation will walk you through the Mac imaging " 
"process.\nRequirements: USB imaging key, power cord, ethernet connection.\n\nSteps:\nStep 1) Connect " "power and 
ethernet to MacBook and insert USB key.\nStep 2) Restart the Mac and hold CMD+R while " "rebooting, until the Apple 
logo with a white loading bar appears.\nStep 3) When booted in, " "select “TechZone loaner” as the user, 
and enter the TZ password.\nStep 4) Select disk utility\nStep " "5) Select the primary disk volume (Usually labeled 
as Macintosh HD and/or Data.\nStep 6) Select " "“erase”.\nStep 7) Once these partitions are erased, delete any 
sub-volumes (such as those labeled " "“data”).\nStep 8) Reboot the Mac and hold the option key.\nStep 9) Select 
“Install MacOS X” from the " "boot key option.\nStep 10) Follow install prompts and select “Macintosh HD” as the 
primary " "installation disk.\nStep 11) Installation will now begin. Once MacOS has finished installing, " "proceed 
to step 12.\nStep 12) Select language- English, and country- US.\nStep 13) Make sure you see " "the “Remote 
Management” setup page, and press continue.\nStep 14) Set username as precat, " "with the Wildcat password.\nStep 15) 
Enable location services. You will then be signed into the " "device.\nStep 16) Wait for self service to pop up, 
then follow the prompts. This will download " "Villanova software and will take ~20 minutes.\nStep 17) Create a new 
user. Do this by going to System " "preferences> Users and Groups> Add account\nStep 18) Set the user as 
Administrator and name the " "account techzone (with no caps).\nStep 19) Set the account with the TZ password.\nStep 
20) Exit " "settings and restart device.\nStep 21) Sign in with the TZ account, and open terminal.\nStep 22) Run " 
"the following commands through terminal:\nSudo jamf recon\nSudo jamf policy\nStep 22) Navigate back " "to users and 
groups and delete the Precat account with its home folder.\nStep 22) Re-run the sudo " "commands listed in step 22. 
This will prompt a reboot script.\nStep 23) After the reboot, sign in to " "techzone and open terminal, then run the 
above commands again. To check for encryption, run one last " "command:\n \t\tSudo fdesetup status\t\nStep 24) If 
file vault is enabled, then device is encrypted " "and ready to be placed back on shelf.\n\n\nHuman: What is the 
username of the account after imaging?\nAI: " "precat\n\nHuman: How to make an Admin account on Mac?\nAI: Create a 
new user. Do this by going to System " "preferences> Users and Groups> Add account\n\nHuman: What are the commands I 
have to run after imaging " "the mac?\nAI: Sudo jamf recon\n     Sudo jamf policy\n\nHuman: How to erase the 
disk?\nAI: Restart the Mac and hold CMD+R while rebooting, until the Apple logo with a white loading bar appears.
When booted in, select “TechZone loaner” as the user, and enter the TZ password.\nSelect disk utility\nSelect the 
primary disk volume and Select “erase”.\nOnce these partitions are erased, delete any sub-volumes '''


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    '''response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.1, presence_penalty=1, best_of=1,
        max_tokens=256)'''

    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.4,
        top_p=1, frequency_penalty=0, presence_penalty=0, best_of=1,
        max_tokens=255)
    answer = response.choices[0].text.strip()
    return answer


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'


def upload_doc(doc, purpose):
    response = openai.File.create(file=open("docs/" + doc), purpose=purpose)
    return response


def search_query(query):
    search_response = openai.Engine("davinci").search(
        search_model="davinci",
        query=query,
        max_rerank=5,
        file="file-KhsR8sdViDnrTQsQbDoiXQPT",
        return_metadata=True
    )
    return search_response


def answerQ(query):
    response = openai.Answer.create(
        search_model="davinci",
        model="davinci",
        question=query,
        file="file-KhsR8sdViDnrTQsQbDoiXQPT",
        examples_context="In 2017, U.S. life expectancy was 78.6 years.",
        examples=[["What is human life expectancy in the United States?", "78 years."]],
        max_rerank=10,
        max_tokens=256,
        stop=["\n", "<|endoftext|>"])
    return response.answers[0]
