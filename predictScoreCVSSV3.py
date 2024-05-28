# Software is free software released under the "GNU General Public License v3.0"
# Copyright (c) 2021 Yuning-Jiang - yuning.jiang17@gmail.com

import argparse
import os
import sys
import logging
import pandas as pd
from os import listdir
from os.path import isfile, join
from calculateCVSSV3 import calculate_baseScore
from calculateCVSSV3 import get_CVSSV3_Vector

# Init various variables :-)
getDoc = ""
#getText = ""
assignScore = ""
assignVector = ""

# Create the parser
my_parser = argparse.ArgumentParser(description='List the content of a folder')

# Add the arguments
my_parser.add_argument('-p',
                       metavar='path',
                       type=str,
                       required=True,
                       help='the path to the documents that would be assessed')
#my_parser.add_argument('-t',
                       #metavar='text',
                       #type=str,
                       #help='directly provide the text that would be assessed')
my_parser.add_argument('-s',
                       metavar='score',
                       default=False,
                       help='generate CVSS v3 scores for the assessed document(s)')
my_parser.add_argument('-v',
                       metavar='vector',
                       default=False,
                       help='generate CVSS v3 vectors for the assessed document(s)')
# Execute parse_args()
args = my_parser.parse_args()
getDoc = args.p
#getText = args.t
assignScore = args.s
assignVector = args.v

attackVector = {
    'N': 'Network',
    'A': 'Adjacent',
    'L': 'Local',
    'P': 'Physical'
}

scale = {
    'N': 'None',
    'L': 'Low',
    'H': 'High'
}

userInteraction = { 
    'N': 'None',
    'R': 'Required'
}

scope_label = {
    'U': 'Unchanged',
    'C': 'Changed'
}
  

if getDoc:
    if not os.path.isdir(getDoc):
        logging.error('The path specified does not exist')
        sys.exit(1)
    else:
        files = [f for f in listdir(getDoc) if isfile(join(getDoc, f))]
        lst = []
        for file in files:
            df = pd.read_csv(getDoc + '/' + file)
            cwe_ids = df['CVE_ID'].tolist()
            docs=df['Report'].tolist()
            for i in range(0,len(df)):
                print("The document being analysed is: " + docs[i])
                if assignScore:
                    pred_score = calculate_baseScore([docs[i]])
                    print("CVSS V3 score: " + str(pred_score))
                if assignVector:
                    vector, exploitabilityScore, aV, aC, priv, userI, scope, conf, inte, avail = get_CVSSV3_Vector([docs[i]])
                    print("CVSS V3 vector: " + vector)

                lst.append([cwe_ids[i], pred_score, attackVector[aV], scale[aC], scale[priv], userInteraction[userI], scope_label[scope], scale[conf], scale[inte], scale[avail]])
                
        dw = pd.DataFrame(lst, columns=['CVE_ID', 'CVSS V3 Score', 'Attack Vector', 'Attack Complexity', 'Privileges Required', 'User Interaction', 'Scope', 'Confidentiality Impact', 'Integrity Impact', 'Availability Impact'])
        dw.to_csv('testDataResult/test_predicted.csv', index=False)    
        
    sys.exit(0)




