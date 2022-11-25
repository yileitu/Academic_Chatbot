import pandas as pd
import numpy as np
class CrowdSource:
    def __init__(self, ent2lbl, lbl2ent, rel2lbl, lbl2rel):
        self.ent2lbl = ent2lbl
        self.lbl2ent = lbl2ent
        self.rel2lbl = rel2lbl
        self.lbl2rel = lbl2rel
        self.crowd_answers = pd.read_csv('data/crowdsource/crowd_answers.csv')
        print('Crowd sourcing initialized')

    def ask_crowd(self, subjects, predicate) -> tuple:
        """
        Returns the details of the crowd sourced answers
        """
        # check if subject and object in query are in the crowd sourced answers
        for val in subjects.values():
            ent = self.lbl2ent[val]
        subject = ent.split('/')[-1]
        predicate = predicate.split('/')[-1]
        print(subject, predicate)
        for idx, row in self.crowd_answers.iterrows():
            if row['label'] == 'CORRECT':
                if row['Subject'] == subject and row['Predicate'] == predicate:
                    return row['kappa'], row['support'], row['Object']
            else:
                if row['FixPosition'] == 'Subject':
                    if row['FixValue'] == subject and row['Predicate'] == predicate:
                        return row['kappa'], row['support'], row['Object']
                elif row['FixPosition'] == 'Predicate':
                    if row['Subject'] == subject and row['FixValue'] == predicate:
                        return row['kappa'], row['support'], row['Object']
                elif row['FixPosition'] == 'Object':
                    if row['Subject'] == subject and row['Predicate'] == predicate:
                        return row['kappa'], row['support'], row['FixValue']
        return ('None', 'None', 'None')