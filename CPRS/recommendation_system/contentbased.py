import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from django.conf import settings
import pandas as pd 
def clean_txt(text):
    # load spacy
    nlp = settings.LANGUAGE_MODELS['en']
    doc = nlp(text)
    words = [
        token.lemma_
        for token in doc
        if not (token.is_stop or token.is_punct or token.is_space)
    ]
    return " ".join(words)


def get_recommendation(user, top, df_project, scores):
    recommendation = pd.DataFrame(
        columns=["group", "project_id", "title", "client", "score"]
    )
    count = 0
    for i in top:
        recommendation.at[count, "group"] = user
        recommendation.at[count, "project_id"] = df_project["id"][i]
        recommendation.at[count, "title"] = df_project["title"][i]
        recommendation.at[count, "client"] = df_project["client_id"][i]
        recommendation.at[count, "score"] = scores[count]
        count += 1
    return recommendation


def make_recommendations(df_project, df_group, nlp):
    # clean the datasets
    df_project["details"] = df_project["details"].apply(clean_txt)
    df_group["details"] = df_group["details"].apply(clean_txt)
    # change the group details into a nlp doc
    doc2 = nlp(df_group.at[0, "details"])
    # change the project details into a nlp doc
    doc1 = df_project["details"].tolist()
    doc1list = [nlp(x) for x in doc1]
    # find the similarity between these two docs
    cos_stud_group_rec = [doc2.similarity(x) for x in doc1list]
    # find the top 10 highest suggested projects
    top10_stud_group_rec = sorted(
        range(len(cos_stud_group_rec)),
        key=lambda i: cos_stud_group_rec[i],
        reverse=True,
    )[:10]
    list_scores = [cos_stud_group_rec[i] for i in top10_stud_group_rec]
    # get the recommendations in  a dataframe
    rec = get_recommendation(
        df_group.at[0, "id"], top10_stud_group_rec, df_project, list_scores
    )
    return rec
