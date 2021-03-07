import streamlit as st
import pandas as pd
import json
import sqlite3

db = sqlite3.connect('data.db').cursor()

def create_table():
    db.execute("""
               CREATE TABLE IF NOT EXISTS 
               todo(name TEXT, category TEXT, duedate DATE)
               """)

def view_all_todos():
    db.execute("select * from todo")
    data = db.fetchall()
    return data

def add_data(name, category, duedate):
    data = {
        "name": name,
        "category": category,
        "duedate": duedate.strftime("%Y/%m/%d")
    }
    with open("tasts.csv", "a") as f:
        json.dump(data, f)
        f.write("\n")
    # db.execute("insert into todo(name, category, duedate) VALUES (?, ?, ?)", (name, category, duedate))
    # db.commit()
    
def remove_item(task_name):
    items = []
    with open("tasts.csv", "r") as f:
        for line in f:
            d = json.loads(line)
            if d["name"] != task_name:
              items.append(d)
    
    with open("tasts.csv", "w") as f:
        for item in items:
            json.dump(item, f)
            f.write("\n")
    

@st.cache
def load_data():
    return pd.read_json("tasts.csv", lines=True)
    
st.write(
    """
    ## TODO App
    This is a basic Todo App to keep track of my things.         
    """)

st.write("## My Todos")

st.title("Add Todo")
name = st.text_input("name")
category = st.selectbox("Type", ["School", "Music", "Hobby"])
date = st.date_input("Due date")

if st.button("Add Todo"):
    add_data(name, category, date)

df = load_data()
st.write(df)


done_task = st.selectbox("Tasks", df["name"].values)
if st.button("Done"):
    remove_item(done_task)
