# Software is free software released under the "GNU General Public License v3.0"
# Copyright (c) 2021 Yuning-Jiang - yuning.jiang17@gmail.com

import math
import pickle
from trainScoreCVSSV3 import get_top_k_predictions

def calculate_ISC(document):
    test_features_Confidentiality=transformerConfidentialityImpact.transform(document)
    confidentiality_label=get_top_k_predictions(modelConfidentialityImpact,test_features_Confidentiality,1)
    confidentiality_label=eval(str(confidentiality_label).strip('[]'))
    if confidentiality_label=='HIGH':
        confidentiality_value=0.56
        confidentiality_label='H'
    elif confidentiality_label=='LOW':
        confidentiality_value=0.22
        confidentiality_label='L'
    else:
        confidentiality_value=0
        confidentiality_label='N'

    test_features_Integrity=transformerIntegrityImpact.transform(document)
    integrity_label=get_top_k_predictions(modelIntegrityImpact,test_features_Integrity,1)
    integrity_label=eval(str(integrity_label).strip('[]'))
    if integrity_label=='HIGH':
        integrity_value=0.56
        integrity_label='H'
    elif integrity_label=='LOW':
        integrity_value=0.22
        integrity_label='L'
    else:
        integrity_value=0
        integrity_label='N'

    test_features_Availability=transformerAvailabilityImpact.transform(document)
    availability_label=get_top_k_predictions(modelAvailabilityImpact,test_features_Availability,1)
    availability_label=eval(str(availability_label).strip('[]'))
    if availability_label=='HIGH':
        availability_value=0.56
        availability_label='H'
    elif availability_label=='LOW':
        availability_value=0.22
        availability_label='L'
    else:
        availability_value=0
        availability_label='N'

    ISC=(1-(1-confidentiality_value)*(1-integrity_value)*(1-availability_value))
    return ISC,confidentiality_label,integrity_label,availability_label

def get_scopeValue(document):
    test_features_Scope=transformerScope.transform(document)
    scope_label=get_top_k_predictions(modelScope,test_features_Scope,1)
    scope_label=eval(str(scope_label).strip('[]'))
    return scope_label

def calculate_exploitabilityScore(document):
    test_features_AttackVector=transformerAttackVector.transform(document)
    attackVector_label=get_top_k_predictions(modelAttackVector,test_features_AttackVector,1)
    attackVector_label=eval(str(attackVector_label).strip('[]'))
    if attackVector_label=='NETWORK':
        attackVector_value=0.85
        attackVector_label='N'
    elif attackVector_label=='ADJACENT_NETWORK':
        attackVector_value=0.62
        attackVector_label='A'
    elif attackVector_label=='LOCAL':
        attackVector_value=0.55
        attackVector_label='L'
    else:
        attackVector_value=0.2
        attackVector_label='P'

    test_features_AttackComplexity=transformerAttackComplexity.transform(document)
    attackComplexity_label=get_top_k_predictions(modelAttackComplexity,test_features_AttackComplexity,1)
    attackComplexity_label=eval(str(attackComplexity_label).strip('[]'))
    if attackComplexity_label=='LOW':
        attackComplexity_value=0.77
        attackComplexity_label='L'
    else:
        attackComplexity_value=0.44
        attackComplexity_label='H'

    test_features_UserInteraction=transformerUserInteraction.transform(document)
    userInteraction_label=get_top_k_predictions(modelUserInteraction,test_features_UserInteraction,1)
    userInteraction_label=eval(str(userInteraction_label).strip('[]'))
    if userInteraction_label=='NONE':
        userInteraction_value=0.85
        userInteraction_label='N'
    else:
        userInteraction_value=0.62
        userInteraction_label='R'

    test_features_Privileges=transformerPrivilegesRequired.transform(document)
    privileges_label=get_top_k_predictions(modelPrivilegesRequired,test_features_Privileges,1)
    privileges_label=eval(str(privileges_label).strip('[]'))
    scope_label=get_scopeValue(document)
    if scope_label=='UNCHANGED' and privileges_label=='LOW':
        privileges_value=0.62
        privileges_label='L'
    elif scope_label=='CHANGED' and privileges_label=='LOW':
        privileges_value=0.68
        privileges_label='L'
    elif scope_label=='UNCHANGED' and privileges_label=='HIGH':
        privileges_value=0.27
        privileges_label='H'
    elif scope_label=='CHANGED' and privileges_label=='HIGH':
        privileges_value=0.5
        privileges_label='H'
    else :
        privileges_value=0.85
        privileges_label='N'

    exploitabilityScore=8.22*attackVector_value*attackComplexity_value*userInteraction_value*privileges_value
    return exploitabilityScore,attackVector_label,attackComplexity_label,privileges_label,userInteraction_label

def calculate_impactScore(document):
    scope_label=get_scopeValue(document)
    ISC,confidentiality_label,integrity_label,availability_label=calculate_ISC(document)
    if scope_label=='UNCHANGED':
        impactScore=6.42*ISC
    elif scope_label=='CHANGED':
        impactScore=7.52*(ISC-0.029)-3.25*((ISC-0.02)**15)
    else:
        impactScore=0
    return impactScore

def round_up(n, decimals=1):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def calculate_baseScore(document):
    load_trainedModels()
    scope_label=get_scopeValue(document)
    exploitabilityScore,attackVector_label,attackComplexity_label,privileges_label,userInteraction_label=calculate_exploitabilityScore(document)
    impactScore=calculate_impactScore(document)
    if impactScore>0 and scope_label=='UNCHANGED':
        baseScore=round_up(min((impactScore+exploitabilityScore),10))
    elif impactScore>0 and scope_label=='CHANGED':
        baseScore=round_up(min((impactScore+exploitabilityScore)*1.08,10))
    else:
        baseScore=0
    return baseScore

def get_CVSSV3_Vector(document):
    load_trainedModels()
    scope = ''
    vector = ''
    scope_label=get_scopeValue(document)
    if scope_label=='UNCHANGED':
        scope='U'
    else:
        scope='C'
    ISC,conf,inte,avail=calculate_ISC(document)
    exploitabilityScore,aV,aC,priv,userI=calculate_exploitabilityScore(document)
    vector = 'CVSS:3.1/AV:' + aV + '/AC:' + aC + '/PR:' + priv +'/UI:'+userI+'/S:'+scope+'/C:'+conf+'/I:'+inte+'/A:'+avail
    return vector, exploitabilityScore, aV, aC, priv, userI, scope, conf, inte, avail


def load_trainedModels():
    global modelIntegrityImpact, transformerIntegrityImpact
    transformerIntegrityImpact = pickle.load(open("trainedModel/transformerIntegrityImpact.pickle", "rb"))
    modelIntegrityImpact = pickle.load(open("trainedModel/modelIntegrityImpact.pickle", "rb"))
    global modelAvailabilityImpact, transformerAvailabilityImpact
    transformerAvailabilityImpact = pickle.load(open("trainedModel/transformerAvailabilityImpact.pickle", "rb"))
    modelAvailabilityImpact = pickle.load(open("trainedModel/modelAvailabilityImpact.pickle", "rb"))
    global modelConfidentialityImpact, transformerConfidentialityImpact
    transformerConfidentialityImpact = pickle.load(open("trainedModel/transformerConfidentialityImpact.pickle", "rb"))
    modelConfidentialityImpact = pickle.load(open("trainedModel/modelConfidentialityImpact.pickle", "rb"))
    global modelScope, transformerScope
    transformerScope = pickle.load(open("trainedModel/transformerScope.pickle", "rb"))
    modelScope = pickle.load(open("trainedModel/modelScope.pickle", "rb"))
    global modelAttackVector, transformerAttackVector
    transformerAttackVector = pickle.load(open("trainedModel/transformerAttackVector.pickle", "rb"))
    modelAttackVector = pickle.load(open("trainedModel/modelAttackVector.pickle", "rb"))
    global modelAttackComplexity, transformerAttackComplexity
    transformerAttackComplexity = pickle.load(open("trainedModel/transformerAttackComplexity.pickle", "rb"))
    modelAttackComplexity = pickle.load(open("trainedModel/modelAttackComplexity.pickle", "rb"))
    global modelUserInteraction, transformerUserInteraction
    transformerUserInteraction = pickle.load(open("trainedModel/transformerUserInteraction.pickle", "rb"))
    modelUserInteraction = pickle.load(open("trainedModel/modelUserInteraction.pickle", "rb"))
    global modelPrivilegesRequired, transformerPrivilegesRequired
    transformerPrivilegesRequired = pickle.load(open("trainedModel/transformerPrivilegesRequired.pickle", "rb"))
    modelPrivilegesRequired = pickle.load(open("trainedModel/modelPrivilegesRequired.pickle", "rb"))
