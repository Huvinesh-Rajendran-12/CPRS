import spacy 
from sklearn.feature_extraction.text import TfidfVectorizer

# load the english spacy module 
nlp = spacy.load('en_core_web_sm')


def clean_txt(text):
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not (token.is_stop or token.is_punct or token.is_space)]
    return " ".join(words)

def get_recommendation(user, top, df_project, scores):
    recommendation = pd.DataFrame(columns=["Group", "Title", "Client", "Score"])
    count = 0
    for i in top:
        recommendation.at[count, "Group"] = user
        recommendation.at[count, "Title"] = df_project["Title"][i]
        recommendation.at[count, "Client"] = df_project["client"][i]
        recommendation.at[count, "Score"] = scores[count]
        count += 1
    return recommendation

def make_recommendations(df_project,df_group):
    # clean the datasets 
    df_project['details'] = df_project['details'].apply(clean_txt)
    doc2 = df_group['details'].apply(clean_txt)

    cos_stud_group_rec = list(
    map(lambda x: doc2.similarity(x), df['details'])
)

    top10_stud_group_rec = sorted(
        range(len(cos_stud_group_rec)), key=lambda i: cos_stud_group_rec[i], reverse=True
    )[:10]

    listscores = [cos_stud_group_rec[i][0][0] for i in top10_stud_group_rec]

    rec = get_recommendation(df_group['id'], top10_stud_group_rec, df_project, list_scores)

    return rec 

