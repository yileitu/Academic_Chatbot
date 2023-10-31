# Building an Intelligent Conversational Agent

This repository contains the code that was created to build a conversational agent that is able to hold conversations with humans about the topic of academic literature.

## TO DO (OpenAlex team)
**1) Input:** Yilei (with Noah's help) is working on the input part. He is fine-tuning an LLM (e.g. Llama 2) on the OpenAlex dataset. The input will be a question and the output will be a query. The query will be used to retrieve the relevant information from the knowledge graph. The input part includes multi-label classification of the academic graph, entity and relation extraction, and the creation of the input for the querying part.

**2) Querying:** Noah is creating a chatbot that is able to take the previously extracted user inputs and formulate them into SPARQL queries that can be used to query the knowledge graph. The queries will be used to retrieve the relevant information from the knowledge graph. The querying part includes the creation of SPARQL queries and the retrieval of information from the knowledge graph.

**3) Evaluating:** Prakhar and Susie are evaluating the fine-tuned LLM. The evaluation will be done on the OpenAlex dataset. The evaluation part includes the evaluation of the multi-label classification of the academic graph.

**4) Parsing and Output:**  Yilei (with Prakhar's help) is working on the output part. He is parsing the retrieved information from the knowledge graph and formulates it into a human-readable answer. The output part includes the parsing of the retrieved information from the knowledge graph and the creation of the output for the user.

**5) Webapp:** Prakhar and Noah are creating a user-friendly interface for the chatbot. The webapp will be used to interact with the chatbot and allows users to ask questions about the topic of academic literature.