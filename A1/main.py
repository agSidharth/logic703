import sys
import re

def readFormulaFile(formula_file):
    text = open(formula_file,"r")
    lines = text.readlines()

    num_clauses = -1
    num_props = -1
    formula_dict = {}
    clause_idx = 0

    for line in lines:
        clause_idx += 1
        words = line.split()

        if (words[0]=="c"):
            continue
        elif(words[0]=="p"):
            num_props = (int)(words[2])
            num_clauses = (int)(words[3])
            continue

        formula_dict[clause_idx] = []
        for prop in words:
            if(prop=="0"):
                break
            formula_dict[clause_idx].append((int)(prop))

    return formula_dict

def returnFormula(word,formula_dict,proof_dict):
    lineIndex = (int)(word[0:(len(word)-1)])
    if(word[-1]=='f'):
        return formula_dict[lineIndex]
    return proof_dict[lineIndex]

def returnSet(formula):
    thisSet = {}

    for prop in formula:
        if ((-1*prop) in thisSet):
            thisSet.clear()
            break
        thisSet[prop] = 1
    
    return thisSet

def check(result_form,form1,form2):
    if(DEBUG): print("New operation")

    dict1 = returnSet(form1)
    dict2 = returnSet(form2)
    dictR = returnSet(result_form)

    if(DEBUG): print("1: "+str(dict1))
    if(DEBUG): print("2: "+str(dict2))
    if(DEBUG): print("R: "+str(dictR))

    resolution = -1
    for key in dict1:
        if (((-1*key) in dict2) and resolution==-1):
            resolution = key
        elif(((-1*key) in dict2)):
            return False
    
    if(DEBUG): print("Resolution: "+str(resolution))

    final_form = []
    for key in dict1:
        if(abs(key)!=abs(resolution)):
            final_form.append(key)
    
    for key in dict2:
        if(abs(key)!=abs(resolution)):
            final_form.append(key)
    
    finalSet = returnSet(final_form)
    
    if(DEBUG): print("finalSet: "+str(finalSet))

    if(len(finalSet)!=len(dictR)):
        return False
    
    for key in finalSet:
        if not (key in dictR):
            return False
    
    return True


if __name__ == "__main__":

    TEST = True
    DEBUG = False

    formula_file = sys.argv[1]
    proof_file = sys.argv[2]

    formula_dict = readFormulaFile(formula_file)
    if(DEBUG): print(formula_dict)

    proof_dict = {}
    proof_idx = 0

    ptext  = open(proof_file,"r")
    lines = ptext.readlines()

    for line in lines:
        proof_idx += 1
        words = line.split()

        form1 = returnFormula(words[0],formula_dict,proof_dict)
        form2 = returnFormula(words[1],formula_dict,proof_dict)

        result_form = []
        for idx in range(2,len(words)):
            if(words[idx]=='0'):
                break
            result_form.append((int)(words[idx]))
        
        proof_dict[proof_idx] = result_form

        if(not check(result_form,form1,form2)):
            TEST = False
            break
    
    if(DEBUG): print(proof_dict)

    if(TEST):
        print("correct")
    else:
        print("incorrect")
    

