import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, set_seed

from final_output.natural_output import set_llama_config

input_text = """
The following performs a describe query for the paper with id 2040986908.
DESCRIBE <http://aida.kmi.open.ac.uk/resource/2040986908>


The following query returns all papers written by authors from the industrial sector computing and it associated with the topic robotics:
PREFIX aida-ont:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX aida:<http://aida.kmi.open.ac.uk/resource/>
PREFIX aidaDB: <http://aida.kmi.open.ac.uk/resource/DBpedia/>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
    
SELECT ?paperId
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?paperId aida-ont:hasIndustrialSector aida:computing_and_it .
    ?paperId aida-ont:hasTopic cso:robotics .
}
LIMIT 20


The following query counts how many papers have been written by authors from an industrial affiliation.
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
SELECT (COUNT(?sub) as ?count)
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?sub aida:hasAffiliationType "industry"
}


The next query counts how many authors are affiliated with The Open University.
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX schema:<http://schema.org/>
SELECT (COUNT(DISTINCT(?sub)) as ?count)
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?sub schema:memberOf ?aff .
    ?aff foaf:name "the_open_university"
}


The following query returns the industrial sectors of all the papers having Semantic Web as a topic.
PREFIX aida:<http://aida.kmi.open.ac.uk/ontology#>
PREFIX cso: <http://cso.kmi.open.ac.uk/topics/>
SELECT DISTINCT ?ind
FROM <http://aida.kmi.open.ac.uk/resource>
WHERE {
    ?sub aida:hasTopic cso:semantic_web .
    ?sub aida:hasIndustrialSector ?ind
}

Please output the SPARQL query that returns the topic distribution of a given affiliation (in this case The Open University)
"""

LLM_PARAM: int = 13
LLM_NAME: str = f"Llama-2-{LLM_PARAM}b-chat"
LLM_HF_PATH: str = f"meta-llama/{LLM_NAME}-hf"
set_seed(42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = LlamaForCausalLM.from_pretrained(
	pretrained_model_name_or_path=LLM_HF_PATH,
	torch_dtype=torch.bfloat16,
	)
tokenizer = LlamaTokenizer.from_pretrained(LLM_HF_PATH)
gen_config = set_llama_config(model=model, tokenizer=tokenizer, device=device)
input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
with torch.no_grad():
	output_ids = model.generate(input_ids, generation_config=gen_config)
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print(output_text.strip())
