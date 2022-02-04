from django.shortcuts import render

# Create your views here.
import psycopg2
import pandas as pd
from .contentbased import * 

def make_recommendations_view(request,group_id):
    connection = psycopg2.connect(
            user="dev",
            password="dev1234",
            host="127.0.0.1",
            port="5432",
            database="test3",
        )
    postgreSQL_student_Query = "select * from " + '"CPRS_admin_student"' + f" where group_id ={group_id}"

    postgreSQL_project_Query = "select * from " + '"CPRS_admin_project"' + f" where is_assigned = False"
    df_student = pd.read_sql_query(postgreSQL_group_Query,connection)
    df_project = pd.read_sql_query(postgreSQL_project_Query,connection)
    df_student['details'] = df_student['course_taken'] + " " + df_student['specialization'] + " " + df_student['area_of_interest'] 
    df_project['details'] = df_project['title'] + " " + df_project['overview'] + " " + df_project['requirements'] 
    df_group = pd.DataFrame(columns=['id','details'])
    df_group['id'] = group_id
    for row in df_student.iterrows():
        df_group['details'] = row['details']

    
