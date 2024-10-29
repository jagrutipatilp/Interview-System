import json
import spacy
import random

class InterviewAI:
    def __init__(self, keyword_file):
        self.question_count = 0
        self.max_questions = 10
        self.genralqueasked=0
        self.responses = {}
        self.mustqueasked =0
        self.asked_questions = set()  # Track asked questions
        self.asked_topics = set()  # Track asked topics to ensure diversity
        self.load_keywords(keyword_file)
        self.nlp = spacy.load("en_core_web_sm")  # Load the spaCy language model
def load_keywords(self, keyword_file):
        with open(keyword_file, 'r') as file:
            self.keywords = json.load(file)

    def generate_followup(self, exkeywords):
        questions = []
        followups = None
        for key in exkeywords:
            if key in self.keywords:
                followups = random.choice(self.keywords[key])
                if isinstance(followups, dict):
                    for sub_key, sub_followups in followups.items():
                        for followup in sub_followups:
                            if followup not in self.asked_questions and self.is_diverse_topic(followup):
                                priority = self.calculate_priority(key, followup)
                                questions.append((priority, followup))
                else:
                    if followups not in self.asked_questions and self.is_diverse_topic(followups):
                        priority = self.calculate_priority(key, followups)
                        questions.append((priority, followups))
        questions.sort(reverse=True, key=lambda x: x[0])
        final_questions = None
        if questions:
            final_questions = questions[0][1]
        if not final_questions:
            que = random.choice(self.keywords.get("general", []))
            if que not in self.asked_questions and self.is_diverse_topic(que):
                final_questions = que
        self.genralqueasked += 1
        return final_questions

    def genrate_behave_quetion(self):
        final_questions = None
        que = random.choice(self.keywords.get("behavioral", []))
        if que not in self.asked_questions and self.is_diverse_topic(que):
            final_questions = que
        return final_questions

    def genrate_Company_Experience_quetion(self):
        final_questions = None
        que = random.choice(self.keywords.get("job_Experience", []))
        if que not in self.asked_questions and self.is_diverse_topic(que):
            final_questions = que
        return final_questions

    def genrate_must_ask_que_quetion(self):
        final_questions = None
        for que in self.keywords.get("must_ask_que", []):
            if que not in self.asked_questions and self.is_diverse_topic(que):
                final_questions = que
        self.mustqueasked += 1
        return final_questions

    def genrate_Company_Fit_quetion(self):
        que = random.choice(self.keywords.get("Company_Fit", []))
        if que not in self.asked_questions:
            return que

    def is_diverse_topic(self, question):
        topic = self.extract_topic(question)
        if topic not in self.asked_topics:
            self.asked_topics.add(topic)
            return True
        return False

    def calculate_priority(self, keyword, question):
        keyword_doc = self.nlp(keyword)
        question_doc = self.nlp(question)
        similarity = keyword_doc.similarity(question_doc)
        return similarity

    def extract_topic(self, question):
        doc = self.nlp(question)
        topics = [token.lemma_.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"}]
        return topics[0] if topics else ""

    def ask_next_question(self, response_text):
        keywords = self.extract_keywords(response_text)
        if self.question_count == 0:
            question = "Tell me about yourself."
        elif self.genralqueasked == 4:
            question = "Do you have any work related experience any internship or Company job? Please elaborate it."
        elif self.question_count == 3 and self.mustqueasked < 2:
            question = self.genrate_must_ask_que_quetion()
        elif self.genralqueasked < 4:
            question = self.generate_followup(keywords)
        else:
            question = self.genrate_behave_quetion()

        if question is None:
            question = self.genrate_Company_Fit_quetion()

        if question:
            self.asked_questions.add(question)
            self.question_count += 1

        return question

    def store_response(self, questions, response):
        self.responses[questions] = response

    def extract_keywords(self, response):
        doc = self.nlp(response)
        keywords = set()

        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            if token.pos_ in {"NOUN", "PROPN", "VERB"}:  # Extract nouns, proper nouns, and verbs
                keywords.add(token.lemma_.lower())

        return list(keywords)