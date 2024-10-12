from hyperon import MeTTa, SymbolAtom, ExpressionAtom, GroundedAtom
import os
import glob
import json

metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f'''
                !(load-ascii &space {path})
                ''')
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    print(f"Finished loading {len(paths)} datasets.")

# Example usage:
try:
    dataset = load_dataset("./Data")
   
except Exception as e:
    print(f"An error occurred: {e}")

# 2 Points
def get_transcript(node):
     #TODO Implement the logic to fetch the transcript
     print("------------ get transcript")
     transcript = metta.run(f'''
!(match &space (transcribed_to ({node[0]}) $x) (transcribed_to ({node[0]}) $x))
''')
     return transcript[0]     

#2 Points
def get_protein(node):
    print("------------get protein--------------")
    #TODO Implement the logic to fetch the protein
    protein = metta.run(f'''
;!({node[0]})
!(match &space (
    , (transcribed_to ({node[0]}) $x)
        (translates_to $x $y))
        (translates_to $x $y)
)
''') 
    return protein[0]

# def get_edge(first) : 
#     edge = metta.run(f'''
# ;!({first})
# !(let $x (car-atom {first}) (car-atom $x))
# ''')
#     res = str(edge[0][0])
#     return res
#6 Points
def metta_seralizer(metta_result):
    print("-----------Serializer-----------")
    result = []
    for n in metta_result:
        # print(n)
        # c = ExpressionAtom.get_children(n)
        children = ExpressionAtom.get_children(n)
        # print(children)
        result.append({'edge':children[0],"source":children[1],"target":children[2]})      
    # print(result)
    return result



#1
transcript_result= (get_transcript(['gene ENSG00000166913']))
print(transcript_result) 
"""
Expected Output Format::
# [[(, (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))), (, (transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)))]]
""" 

#2
protein_result= (get_protein(['gene ENSG00000166913']))
print(protein_result) 
"""
Expected Output Format::
# [[(, (translates_to (transcript ENST00000353703) (protein P31946))), (, (translates_to (transcript ENST00000372839) (protein P31946)))]]
"""

#3
parsed_result = metta_seralizer(protein_result)
parsed_result1 = metta_seralizer(transcript_result)
print(parsed_result) 
print(parsed_result1) 
"""
Expected Output Format:
[
    {'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}
]
"""

