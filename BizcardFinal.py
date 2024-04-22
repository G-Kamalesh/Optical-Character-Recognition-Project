import streamlit as st
import streamlit as st
from PIL import Image, ImageDraw
import easyocr
import numpy as np
import mysql.connector
import pandas as pd
import re

@st.cache_resource
def ocr():
    reader = easyocr.Reader(["en"],gpu=False)
    return reader

def scan(image):
    img_np = np.array(image) 
    reader = ocr()
    result = reader.readtext(img_np,detail=0)
    coordinates = reader.readtext(img_np)

    draw = ImageDraw.Draw(image)

    for detection in coordinates:
        top = tuple(detection[0][0])
        bottom = tuple(detection[0][2])
        bbox = [top, bottom]
        draw.rectangle(bbox, outline="green",width = 6)

    return image, result



def collection(result):
    sec = {'name':[],'website':[],'address':[],'email':[],'pincode':[],'mobile no':[],'designation':[],'business':[[]],'others':[[]]}

    sec['name'] = [result[0]]
    sec['designation'] = [result[1]]

    c = (" & ".join(result))
    m = re.findall(r"(\d{3}-\d{3}-\d{4})",c)
    if m:
        if len(m) == 2:
            sec["mobile no"].append(" & ".join(m))
        else:
            sec['mobile no'].append([m])

    for i in result:
    
        
        if re.search("www",i,re.IGNORECASE):
            sec['website'].append(i)
        elif re.search("@",i,re.IGNORECASE):
            sec['email'].append(i)
        elif re.search(r"(\d{6})",i,re.IGNORECASE):
            sec['pincode'].append(i)
        elif re.search(r"\d+\s+(?:[A-Za-z]+\s*)+",i,re.IGNORECASE):
            sec['address'].append(i)
        elif re.search(r"^[A-Z]",i,re.IGNORECASE):
                sec["business"][0].append(i)
        else:
            sec['others'][0].append(i)
    
    df = pd.DataFrame(sec)
    
    return df

def update(df,name,website,address,email,pincode,mobile,designation,business,others):
    df.loc[0, 'name'] = name
    df.loc[0, 'website'] = website
    df.loc[0, 'address'] = address
    df.loc[0, 'email'] = email
    df.loc[0, 'pincode'] = pincode
    df.loc[0, 'mobile no'] = mobile
    df.loc[0, 'designation'] = designation
    df.loc[0, 'business'] = business
    df.loc[0, 'others'] = others

    return df

@st.cache_resource
def sqlconnect():
    sqldb = mysql.connector.connect(host= 'localhost',user='root',password='012345',database='bizcard')
    cursor = sqldb.cursor()
    return cursor ,sqldb

def sql_upload(df):
    cursor,sqldb = sqlconnect()
    query= """create table if not exists bizcard( 
                                                name varchar(20) primary key,
                                                website varchar(20),
                                                address varchar(80),
                                                email varchar(20),
                                                pincode varchar(60),
                                                mobile varchar(20),
                                                designation varchar(20),
                                                business varchar(20)                                
                                                ) """
    cursor.execute(query)

    insert = """insert into bizcard(  
                name,
                website,
                address,
                email,
                pincode,
                mobile,
                designation,
                business
                )
                        
                values(%s,%s,%s,%s,%s,%s,%s,%s)"""

    try:
        values = [(df.loc[0,'name'],
                        df.loc[0,'website'],
                        df.loc[0,'address'],
                        df.loc[0,'email'],
                        df.loc[0,'pincode'],
                        df.loc[0,'mobile no'],
                        df.loc[0,'designation'],
                        df.loc[0,'business']
                        )]

        cursor.executemany(insert,values)
        st.success("Upload success")
        sqldb.commit()
    except:
        st.error("Data Already Exist in Database")

def extract():
    cursor,sqldb = sqlconnect()
    query = "use bizcard"
    cursor.execute(query)
    query ="select * from bizcard"
    cursor.execute(query)
    y = cursor.fetchall()

    return y


def change():
    if st.session_state['Mykey'] == "Home":
        st.session_state['Mykey'] = "Correction"

def server():
    if st.session_state['Mykey'] == "Correction":
        st.session_state['Mykey'] = "Server"


if 'Mykey' not in st.session_state:
    st.session_state['Mykey'] = "Home"
if 'd' not in st.session_state:
    st.session_state['d'] = []
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'server' not in st.session_state:
    st.session_state['server'] = None


st.set_page_config(page_title="BizCard",layout="wide",initial_sidebar_state="auto")
with st.sidebar:
    st.title("BizCard Extraction")
    uploads = st.file_uploader(label="Upload card",type=['png', 'jpg'],accept_multiple_files=True)
    option = ["Home","Correction","Server"]
    s = st.selectbox("Select",option,key= 'Mykey')
    
c1,c2 = st.columns([0.5,0.5])
scan_cache = {}

if s == "Home":  
    if uploads:
        for id,upload in enumerate(uploads):
            image = Image.open(upload)
            c1.image(upload,caption=f"Image {id+1}")
            if c1.button(f"Extract Image {id+1}"):
                if id+1 in scan_cache:
                    result = scan_cache[id+1]
                else:
                    result = scan(image)
                    scan_cache[id+1] = result
                st.session_state['d'].append(result[1])
                c2.image(result[0],caption=f"Image {id+1}")
                c2.write(result[1])
                edit_button = c2.button(f"Edit {id+1}",on_click=change)
      
                                        
elif s == "Correction":
    if st.session_state['Mykey'] =="Home":
        st.session_state['Mykey'] = "Correction"
    d = st.session_state['d']
    df = collection(d[0])
    name = st.text_input("Name:", value=df.loc[0, 'name'])
    website = st.text_input("Website:", value=df.loc[0, 'website'])
    address = st.text_input("Address:", value=df.loc[0, 'address'])
    email = st.text_input("Email", value = df.loc[0,"email"])
    pincode = st.text_input("Pincode", value= df.loc[0,"pincode"])
    mobile = st.text_input("Mobile Number", value = df.loc[0,"mobile no"])
    designation = st.text_input("Designation", value = df.loc[0,"designation"])
    business = st.text_input("Business Name",value = df.loc[0,"business"])
    others = st.text_input("Others",value = df.loc[0,"others"])

    # Update DataFrame based on user input
    if st.button("Update Data"):
        st.session_state['d'] = []
        v = update(df,name,website,address,email,pincode,mobile,designation,business,others)
        st.session_state['df'] = v
        st.write(v.T)
        st.button("Upload to MySql",on_click=server)
            
if s == "Server":
    df = st.session_state['df']
    try:
        if df.empty == False:
            sql_upload(df)
            s = extract()
            sql = pd.DataFrame(s,columns=["Name","Website","Address","Email","Pincode","Mobile No","Designation","Business Name"])
            st.dataframe(sql)
            st.session_state['df'] = None
    except:
        st.write("No Data Available")
    
    if st.sidebar.checkbox("View DataBase"):
        c= extract()
        sql = pd.DataFrame(c,columns=["Name","Website","Address","Email","Pincode","Mobile No","Designation","Business Name"])
        st.dataframe(sql)

