# -*- coding: utf-8 -*-
from func import extract_entities

samples = [
	"Looking for research akin to 'Explaining and Harnessing Adversarial Examples' by Ian J. Goodfellow et al., 2015? Recommend me papers that delve into similar topics.",
	"Could you suggest studies parallel to 'Generative Adversarial Nets' by Ian Goodfellow et al., 2014, focusing on generative models?",
	"I'm interested in more works like 'ImageNet Classification with Deep Convolutional Neural Networks' by Alex Krizhevsky et al., 2012. Please guide me to similar groundbreaking research in image recognition.",
	"Point me towards publications that explore themes close to 'Sequence to Sequence Learning with Neural Networks' by Ilya Sutskever et al., 2014, especially in natural language processing.",
	"What are some papers related to 'Large-Scale Video Classification with Convolutional Neural Networks' by Andrej Karpathy et al., 2014, that discuss video content analysis?",
	"Seeking additional insights from studies resembling 'Mastering the game of Go with deep neural networks and tree search' by David Silver et al., 2016. Any recommendations on AI strategies in games?",
	"Identify for me articles that resonate with 'DenseNet: Densely Connected Convolutional Networks' by Gao Huang et al., 2017, especially those that improve upon image classification techniques.",
	"I'm on the hunt for literature akin to 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding' by Jacob Devlin et al., 2018. Suggestions for similar transformative works in NLP?",
	"Please recommend papers that align with the innovations of 'GPT-3: Language Models are Few-Shot Learners' by Tom B. Brown et al., 2020, particularly in the realm of language understanding.",
	"Direct me to research that parallels 'Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks' by Alec Radford, Luke Metz, and Soumith Chintala, 2016, in the field of unsupervised learning.",
	"I'm seeking studies similar to 'Fast R-CNN' by Ross Girshick, 2015, that discuss advancements in object detection. Any recommendations?",
	"Can you suggest papers that expand upon the ideas presented in 'The PageRank Citation Ranking: Bringing Order to the Web' by Lawrence Page et al., 1999, particularly those exploring web search algorithms?",
	"I'd like to explore more research related to 'DeepFace: Closing the Gap to Human-Level Performance in Face Verification' by Yaniv Taigman et al., 2014. Can you recommend studies with similar findings in facial recognition technology?",
	"Please provide me with titles of papers that have a thematic resemblance to 'Graph-Based Knowledge Representation: Computational Foundations of Conceptual Graphs' by Michel Chein and Marie-Laure Mugnier, 2009, especially those focusing on knowledge representation.",
	"In quest of discussions related to 'Understanding the Mechanisms of Deep Transfer Learning for Medical Images' by Hoo-Chang Shin et al., 2016. Can you recommend articles that explore deep learning applications in medical imaging?",
	"I am eager to find research papers that parallel the work in 'Neural Machine Translation by Jointly Learning to Align and Translate' by Dzmitry Bahdanau et al., 2014. What are some similar pivotal studies in machine translation?",
	"Seeking papers that extend the findings of 'Playing Atari with Deep Reinforcement Learning' by Volodymyr Mnih et al., 2013. Any leads on studies involving reinforcement learning in gaming environments?",
	"I would appreciate recommendations for studies that follow up on 'A Few Useful Things to Know about Machine Learning' by Pedro Domingos, 2012. Are there more insights into practical advice for applying machine learning techniques?",
	"Interested in further explorations similar to 'Efficient Object Detection for High Resolution Images' by Mingxing Tan et al., 2020. What are other significant contributions to object detection techniques?",
	"Looking for research that aligns with 'Graph Attention Networks' by Petar Veličković et al., 2018. Can you suggest studies that further investigate the use of attention mechanisms in graph neural networks?",
	]

for query in samples:
	res = extract_entities(query)
	print(res)
