from haystack.utils import (
    clean_wiki_text,
    print_answers,
    print_documents,
    fetch_archive_from_http,
    convert_files_to_docs,
    launch_es,
)
from pprint import pprint
from haystack import Pipeline
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import (
    ElasticsearchRetriever,
    EmbeddingRetriever,
    FARMReader,
    RAGenerator,
    BaseComponent,
    JoinDocuments,
)
from haystack.pipelines import ExtractiveQAPipeline, DocumentSearchPipeline, GenerativeQAPipeline


def tutorial11_pipelines():
    # Download and prepare data - 517 Wikipedia articles for Game of Thrones
    doc_dir = "data/tutorial11"
    s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt11.zip"
    fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

    # convert files to dicts containing documents that can be indexed to our datastore
    got_docs = convert_files_to_docs(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)

    # Initialize DocumentStore and index documents
    launch_es()
    document_store = ElasticsearchDocumentStore()
    document_store.delete_documents()
    document_store.write_documents(got_docs)

    # Initialize Sparse retriever
    es_retriever = ElasticsearchRetriever(document_store=document_store)

    # Initialize dense retriever
    embedding_retriever = EmbeddingRetriever(
        document_store,
        model_format="sentence_transformers",
        embedding_model="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    )
    document_store.update_embeddings(embedding_retriever, update_existing_embeddings=False)

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")

    print()
    print("# Extractive QA Pipeline")
    print("########################")

    query = "Who is the father of Arya Stark?"
    p_extractive_premade = ExtractiveQAPipeline(reader=reader, retriever=es_retriever)
    res = p_extractive_premade.run(query=query, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    print("\nQuery: ", query)
    print("Answers:")
    print_answers(res, details="minimum")

    print()
    print("# Document Search Pipeline")
    print("##########################")

    query = "Who is the father of Arya Stark?"
    p_retrieval = DocumentSearchPipeline(es_retriever)
    res = p_retrieval.run(query=query, params={"Retriever": {"top_k": 10}})
    print()
    print_documents(res, max_text_len=200)

    print()
    print("# Generator Pipeline")
    print("####################")

    # We set this to True so that the document store returns document embeddings
    # with each document, this is needed by the Generator
    document_store.return_embedding = True

    # Initialize generator
    rag_generator = RAGenerator()

    # Generative QA
    query = "Who is the father of Arya Stark?"
    p_generator = GenerativeQAPipeline(generator=rag_generator, retriever=embedding_retriever)
    res = p_generator.run(query=query, params={"Retriever": {"top_k": 10}})
    print()
    print_answers(res, details="minimum")

    # We are setting this to False so that in later pipelines,
    # we get a cleaner printout
    document_store.return_embedding = False

    print()
    print("# Ensembled Retriever Pipeline")
    print("##############################")

    # Create ensembled pipeline
    p_ensemble = Pipeline()
    p_ensemble.add_node(component=es_retriever, name="ESRetriever", inputs=["Query"])
    p_ensemble.add_node(component=embedding_retriever, name="EmbeddingRetriever", inputs=["Query"])
    p_ensemble.add_node(
        component=JoinDocuments(join_mode="concatenate"),
        name="JoinResults",
        inputs=["ESRetriever", "EmbeddingRetriever"],
    )
    p_ensemble.add_node(component=reader, name="Reader", inputs=["JoinResults"])

    # Run pipeline
    query = "Who is the father of Arya Stark?"
    res = p_ensemble.run(
        query="Who is the father of Arya Stark?",
        params={"ESRetriever": {"top_k": 5}, "EmbeddingRetriever": {"top_k": 5}},
    )
    print("\nQuery: ", query)
    print("Answers:")
    print_answers(res, details="minimum")

    print()
    print("# Query Classification Pipeline")
    print("###############################")

    class CustomQueryClassifier(BaseComponent):
        outgoing_edges = 2

        def run(self, query):
            if "?" in query:
                return {}, "output_2"
            else:
                return {}, "output_1"

    # Here we build the pipeline
    p_classifier = Pipeline()
    p_classifier.add_node(component=CustomQueryClassifier(), name="QueryClassifier", inputs=["Query"])
    p_classifier.add_node(component=es_retriever, name="ESRetriever", inputs=["QueryClassifier.output_1"])
    p_classifier.add_node(component=embedding_retriever, name="EmbeddingRetriever", inputs=["QueryClassifier.output_2"])
    p_classifier.add_node(component=reader, name="QAReader", inputs=["ESRetriever", "EmbeddingRetriever"])
    p_classifier.draw("pipeline_classifier.png")

    # Run only the dense retriever on the full sentence query
    query = "Who is the father of Arya Stark?"
    res_1 = p_classifier.run(query=query)
    print()
    print("\nQuery: ", query)
    print(" * Embedding Retriever Answers:")
    print_answers(res_1, details="minimum")

    # Run only the sparse retriever on a keyword based query
    query = "Arya Stark father"
    res_2 = p_classifier.run(query=query)
    print()
    print("\nQuery: ", query)
    print(" * ES Answers:")
    print_answers(res_2, details="minimum")
