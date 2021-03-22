import json
import pandas as pd
import streamlit as st
import requests

api_key = "efee0d94-c0da-4cc5-b77e-e9f7d15243fd"
headers = {"Api-Key": api_key, "Content-Type": "application/json"}
store_name = "todo-app"
store_url = f"https://json.psty.io/api_v1/stores/{store_name}"


def add_todo(name, date):
    new_todo = {"name": name, "date": date.strftime("%Y/%m/%d")}
    data = load_data()
    data.append(new_todo)
    res = requests.put(store_url, headers=headers, data=json.dumps(data))
    return data


def load_data():
    res = requests.get(store_url, headers=headers)
    data = res.json()["data"]
    return data

def remove_item(task_name):
    items = []
    data = load_data()
    for d in data:
        if d["name"] != task_name:
            print(d, data)
            data.remove(d)
            break
    print(data)
    res = requests.put(store_url, headers=headers, data=json.dumps(data))            

st.write("# Todo App")
st.write("List of my Todos")

name = st.text_input("Name")
date = st.date_input("Due Date")
if st.button("Add Todo"):
    add_todo(name, date)

st.write("## My Tasks")
df = pd.DataFrame(load_data())
st.write(df)

st.write("## Mark it Done")
done_task = st.selectbox("Task", df["name"].values)
if st.button("Done!"):
    remove_item(done_task)
