import os
import io 
from google.cloud import vision_v1 
from google.cloud.vision_v1 import types 
import pandas as pd 

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'/Users/mubarekabdela/Desktop/Fall2020Projects/C-Text/env/account_token.json'

client = vision_v1.ImageAnnotatorClient()
def multiplechoice(string):
    lst=[]
    questions=''
    current=''
    choices = {'A','B','C','D','E','F'}
    sign = {'.',')'}


    for i in range(0,len(string)):
        if i == (len(string)-1):
            lst.append(current)
        if string[i] in choices and string[i+1] in sign:
            lst.append(current)
            current=''
            current+=string[i]
        elif string[i] == '?':
            current+=string[i]
            lst.append(current)
            current=''
        elif string[i]=="\n" or string[i] in sign:
            i+=1
        elif string[i].isdigit() and string[i+1]=='.' and current:
            lst.append(current)
            current=''
            current+=string[i]
        else:
            current+=string[i]
    lst.append(current)
    return questions_json(lst)
def questions_json(list_of_questions):
    dicc={}
    new=[]
    for i in list_of_questions:
        choices = {'A','B','C','D','E','F'}
        if i==" " or i== "":
            pass
        elif i[0] in choices:
            dicc[i[0]]=i[1:]
        elif i[0].isdigit() and not dicc:
            dicc[i[0]]=i[1:]
        elif i[0].isdigit() and dicc:
            new.append(dicc)
            dicc={}
            dicc[i[0]]=i[1:]
        else:
            pass
    new.append(dicc)
    return new

    

def detectText(img):
    with io.open(os.path.join(FOLDER_PATH, FILE_NAME),'rb') as image_file:
        content = image_file.read()
    image= vision_v1.types.Image(content=content)
    response= client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['locale','description'])

    for text in texts:
        df = df.append(
        dict(
            locale=text.locale,
            description=text.description 
        ),
        ignore_index=True 
        )
    return df['description'][0] 
FILE_NAME = 'Q1.png'
FOLDER_PATH=r'/Users/mubarekabdela/Desktop/Fall2020Projects/C-Text'
txt=detectText(os.path.join(FOLDER_PATH,FILE_NAME))
print(multiplechoice(txt))
