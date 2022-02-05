from django.shortcuts import render, redirect

# Create your views here.
import json
import psycopg2
import pandas as pd
from .contentbased import *
import spacy
from CPRS_admin.models import StudentGroup, Project


def make_recommendations_view(request, group_id):
    connection = psycopg2.connect(
        user="dev",
        password="dev1234",
        host="127.0.0.1",
        port="5432",
        database="test3",
    )
    postgreSQL_student_Query = (
        "select * from " + '"CPRS_admin_student"' + f" where group_id ={group_id}"
    )

    postgreSQL_project_Query = (
        "select * from " + '"CPRS_admin_project"' + f" where is_assigned = False"
    )
    df_student = pd.read_sql_query(postgreSQL_group_Query, connection)
    df_project = pd.read_sql_query(postgreSQL_project_Query, connection)
    df_student["details"] = (
        df_student["course_taken"]
        + " "
        + df_student["specialization"]
        + " "
        + df_student["area_of_interest"]
    )
    df_project["details"] = (
        df_project["title"]
        + " "
        + df_project["overview"]
        + " "
        + df_project["requirements"]
    )
    df_group = pd.DataFrame(columns=["id", "details"])
    df_group.at[0, "id"] = group_id
    df_group.at[0, "details"] = " "
    for index, row in df_student.iterrows():
        df_group.at[0, "details"] = df_group.at[0, "details"] + " " + row["details"]
    nlp = spacy.load("en_core_web_md")
    rec = make_recommendations(df_project, df_group, nlp)
    rec_data = rec.to_json()
    rec_data = json.loads(rec_data)
    context = {"rec": rec_data}
    template_name = "HOD/recommendations_view.html"
    return render(request, template_name, context)


def assign_recommended_project(request, group_id, client_id, project_id):
    group = StudentGroup.objects.get(id=group_id)
    group.client = client_id
    group.project = project_id
    group.save()
    project = Project.objects.get(id=project_id)
    project.is_assigned = True
    project.save()
    return redirect("")
