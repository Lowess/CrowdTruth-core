import pandas as pd
import cProfile

crowd_noOffset = pd.read_csv("crowdflower/causal_relation_noOffset_lemma_all_batch2.csv")
annotations = list(pd.concat([crowd_noOffset['pair1_noOffset'], crowd_noOffset['pair2_noOffset'], crowd_noOffset['pair3_noOffset'], crowd_noOffset['pair4_noOffset'], crowd_noOffset['pair5_noOffset'], crowd_noOffset['pair6_noOffset']]).unique())

cleanedList = [x for x in annotations if pd.isnull(x) != True]

final_vector = []
for item in cleanedList:
    final_vector.append(item.replace(', ', '--'))
    final_vector.append(item.replace(', ', '-r-'))
final_vector.append('no_relation')  
print(len(final_vector))


import sys
sys.path.append('../')
#stdout = sys.stdout

from defaultconfig import Configuration

class CausalRelationsConfig(Configuration):
    inputColumns = ["index", "number", "events1", "sentence1", "sentence1_id", "pair1_noOffset", "pair2_noOffset", "pair3_noOffset", "pair4_noOffset", "pair5_noOffset", "pair6_noOffset", "relations"]
    outputColumns = ["relations_noOffset"]
    
    # processing of a closed task
    open_ended_task = False
    annotation_vector = final_vector
    
    column_separator = ","
    
    def processJudgments(self, judgments):
        # change default separator to whitespace to make it work with our file
        for col in self.outputColumns:
            #judgments[col] = judgments[col].apply(lambda x: x.replace('no_relation', 'no_causal_relation'))
            judgments[col] = judgments[col].apply(lambda x: x.replace('\n', ','))
        return judgments

config = CausalRelationsConfig()

from controllers.inputController import processFile
from models import Metrics

def do_stuff():
    pre_processed_results = processFile(root=".", directory="", filename="crowdflower/causal_relation_noOffset_lemma_all_batch2.csv", config=config)
    processed_results_noOffsets = Metrics.run(pre_processed_results, config)
    print list(processed_results_noOffsets["units"])
    print list(processed_results_noOffsets["workers"])
    print list(processed_results_noOffsets["annotations"])

    sortWQS = processed_results_noOffsets["workers"].sort(['wqs'], ascending=[1])
    sortWQS = sortWQS.reset_index()

    sortAQS = processed_results_noOffsets["annotations"].sort(['aqs'], ascending=[1])
    sortAQS = sortAQS.reset_index()

    sortUQS = processed_results_noOffsets["units"].sort(['uqs'], ascending=[1])
    sortUQS = sortUQS.reset_index()
    #print processed_results_noOffsets
    sortWQS.to_csv("Results/all_batch2_workers_withAnnotationQuality_noOffsets.csv", index=False)
    sortAQS.to_csv("Results/all_batch2_annotations_withAnnotationQuality_noOffsets.csv", index=False)
    
    rows = []
    header = list(sortUQS)
    header.extend(["event-event_pair", "no_of_annotations", "event-event_pair_final_score", "event-event_pair_initial_score"])

    remove_indices = [13, 18, 20]
    header = [i for j, i in enumerate(header) if j not in remove_indices]

    rows.append(header)

    for i in range(len(sortUQS.index)):
        keys = []
        if (str(sortUQS["input.pair1_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair1_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair1_noOffset"].iloc[i]).replace(', ', '-r-'))
        if (str(sortUQS["input.pair2_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair2_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair2_noOffset"].iloc[i]).replace(', ', '-r-'))
        if (str(sortUQS["input.pair3_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair3_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair3_noOffset"].iloc[i]).replace(', ', '-r-'))
        if (str(sortUQS["input.pair4_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair4_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair4_noOffset"].iloc[i]).replace(', ', '-r-'))
        if (str(sortUQS["input.pair5_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair5_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair5_noOffset"].iloc[i]).replace(', ', '-r-'))
        if (str(sortUQS["input.pair6_noOffset"].iloc[i]) != "nan"):
            keys.append(str(sortUQS["input.pair6_noOffset"].iloc[i]).replace(', ', '--'))
            keys.append(str(sortUQS["input.pair6_noOffset"].iloc[i]).replace(', ', '-r-'))
        keys.append("no_relation")
    
    
        for j in range(len(keys)):
            #print(keys[j])
            row = list(sortUQS.iloc[i])
            newRow = [k for l, k in enumerate(row) if l not in remove_indices]
            newRow.append(keys[j])
            if (keys[j] not in sortUQS["output.relations_noOffset"].iloc[i]):
                print(keys[j])
            newRow.append(sortUQS["output.relations_noOffset"].iloc[i][keys[j]])
            newRow.append(sortUQS["unit_annotation_score"].iloc[i][keys[j]])
            newRow.append(sortUQS["unit_annotation_score_initial"].iloc[i][keys[j]])
    
            rows.append(newRow)

    import csv

    with open('Results/all_batch2_results_withAnnotationQuality_noOffsets.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

#cProfile.run("do_stuff()")
do_stuff()





