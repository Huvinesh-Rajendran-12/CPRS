from django.shortcuts import render

# Create your views here.
import psycopg2
import pandas as pd


def make_recommendations_view(request,group_id):
    connection = psycopg2.connect(
            user="dev",
            password="dev1234",
            host="127.0.0.1",
            port="5432",
            database="test3",
        )
    postgreSQL_group_Query = "select * from " + '"CPRS_admin_studentgroup"' + f" where id ={group_id}"

    postgreSQL_project_Query = "select * from " + '"CPRS_admin_project"' + f" where is_assigned = False"
    df_group = pd.read_sql_query(postgreSQL_group_Query,connection)
    df_project = pd.read_sql_query(postgreSQL_project_Query,connection)


