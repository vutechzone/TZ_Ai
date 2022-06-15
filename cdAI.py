from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline
from cdqa.utils.download import download_model

# download_model(model='distilbert-squad_1.1', dir='./models')

df = pdf_converter(directory_path='./data')
df = filter_paragraphs(df, min_length=20)
df.head()
cdqa_pipeline = QAPipeline(reader='./models/bert_qa.joblib', max_df=1.0, retriever="tfidf")

# Fit Retriever to documents
cdqa_pipeline.fit_retriever(df=df)


def getResponse(query):
    prediction = cdqa_pipeline.predict(query)
    return format(prediction[0])
