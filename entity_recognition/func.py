# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from typing import List, Tuple

import spacy
from spacy_llm.util import assemble

ner_model = spacy.load(
	"en_core_web_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"]
	)  # Disable everything except NER
is_llama_loaded = False
llama = None

dir_path = os.path.dirname(os.path.realpath(__file__))
llm_config_path = os.path.join(dir_path, 'llm_config.cfg')

@dataclass
class NamedEntity:
	"""
	Entities for academic papers
	"""
	paper: str = 'PAPER'
	author: str = 'AUTHOR'
	institution: str = 'INSTITUTION'

def load_llama():
	"""
	Load Llama-2-7b-hf model
	"""
	global llama, is_llama_loaded
	llama = assemble(config_path=llm_config_path)
	is_llama_loaded = True
	print("Llama loaded")


def extract_entities(text: str, extract_paper_title: bool = True) -> List[Tuple[str, str]]:
	"""
	Extract entities (author, institution and paper title) from text
	"""
	doc = ner_model(text)
	entities = []
	for ent in doc.ents:
		if ent.label_ in ['PERSON']:
			entities.append((ent.text, NamedEntity.author))
		elif ent.label_ in ['ORG']:
			entities.append((ent.text, NamedEntity.institution))
		if extract_paper_title and ent.label_ in ['WORK_OF_ART']:
			entities.append((ent.text, NamedEntity.paper))

	# Extract paper title
	if extract_paper_title:
		if not is_llama_loaded:
			load_llama()
		doc = llama(text)
		for ent in doc.ents:
			if ent.label_ == 'PAPER':
				entities.append((ent.text, ent.label_))

	return entities
