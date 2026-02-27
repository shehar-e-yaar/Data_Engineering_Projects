import psycopg2
import pandas as pd
import pandas as pd

student=pd.read_csv("students_raw.csv" )
score=pd.read_csv("scores.csv" )

conn = psycopg2.connect(
    host="localhost",
    database="School",
    user="postgres",
    password="4946849"
)

print("Connected successfully!")


student["name"]=student["name"].str.strip().str.capitalize()
student["city"]=student["city"].str.strip().str.capitalize()

print("Data cleaned successfully!")


cur=conn.cursor()

for _,row in student.iterrows():
    cur.execute(
        "INSERT INTO stud (name, age, city) VALUES (%s, %s, %s)",
        (row["name"], row["age"], row["city"])
    )
conn.commit()
cur.close()
conn.close()

cus=conn.cursor()
for _,row in score.iterrows():
    cus.execute(
        "INSERT INTO scores (student_id,score) VALUES (%s,%s)",
        (row["student_id"],row["score"])
    )
conn.commit()
cur.close()
conn.close()




