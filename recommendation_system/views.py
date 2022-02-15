from django.shortcuts import render, redirect

# Create your views here.
import json
import psycopg2
import pandas as pd
from .contentbased import *
import spacy
from CPRS_admin.models import StudentGroup, Project, Client
from django.conf import settings


def make_recommendations_view(request, group_id):
    connection = psycopg2.connect(
        user="dev",
        password="dev1234",
        host="127.0.0.1",
        port="5432",
        database="test2",
    )
    postgreSQL_student_Query = (
        "select * from "
        + '"CPRS_admin_student_profile"'
        + f" where group_id ={group_id}"
    )

    postgreSQL_project_Query = (
        "select * from " + '"CPRS_admin_project"' + f" where is_assigned = False"
    )
    df_student = pd.read_sql_query(postgreSQL_student_Query, connection)
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
    nlp = settings.LANGUAGE_MODELS["en"]
    rec = make_recommendations(df_project, df_group, nlp)
    context = {"rec": rec}
    template_name = "HOD/recommendations_view.html"
    return render(request, template_name, context)


def assign_recommended_project(request, group_id, client_id, project_id):
    client = Client.objects.get(id=client_id)
    group = StudentGroup.objects.get(id=group_id)
    project = Project.objects.get(id=project_id)
    print(client)
    group.client = client
    group.project = project
    group.has_project = True
    group.save()
    project.is_assigned = True
    project.save()
    return redirect("coordinator_view_groups")

def change_recommended_project(request,group_id,project_id):
    group = StudentGroup.objects.get(id=group_id)
    project = Project.objects.get(id=project_id)
    group.client = None 
    group.project = None 
    group.has_project = False 
    project.is_assigned = False 
    group.save()
    project.save()
    return redirect("coordinator_view_project_recommendations",group_id)
