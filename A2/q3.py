import sys
import re
import math

DEBUG = False

# for reading the formula file to return a formula dictionary..
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

# for printing the output accordingly..
def printOutput(file_name,final_dict,this_dict,numOfProofs):
    outFile = open(file_name,"w")

    for jdx in range(1,numOfProofs+1):
        outFile.write(str(final_dict[jdx][0]) + " " + str(final_dict[jdx][1])+" ")

        for kdx in range(len(this_dict[jdx])):
            outFile.write(str(this_dict[jdx][kdx])+" ")

        outFile.write("0\n")
    
    outFile.close()


# for converting a list to a set 
def returnSet(formula):
    thisSet = {}

    for prop in formula:
        thisSet[prop] = 1
    
    return thisSet

# for resolving two formulas stored as lists...
def resolve(formula1,formula2):
    thisSet1 = returnSet(formula1)
    thisSet2 = returnSet(formula2)

    literal = math.inf
    for key in thisSet1:
        if -1*key in thisSet2 and abs(literal)>abs(key):
            literal = key
    
    if literal==math.inf:
        return False,[]
    
    finalSet = {}
    for key in thisSet1:
        if (abs(key) != abs(literal)): 
            finalSet[key] = 1
    
    for key in thisSet2:
        if (abs(key) != abs(literal)):
            finalSet[key] = 1
    
    finalList = []
    for key in finalSet:
        finalList.append(key)

    return True, finalList


# for returning formula for the given pointer.. and returning false if not found..
def returnFormula(word,formula_dict,this_dict):
    lineIndex = (int)(word[0:(len(word)-1)])

    if(word[-1]=='f'):
        if lineIndex not in formula_dict:
            return False, []
        return True, formula_dict[lineIndex]

    if(lineIndex not in this_dict):
        return False,[]
    return True,this_dict[lineIndex]

def recursive(this_dict,out_dict,formula_dict,proof_dict,proofNum,lastNum):

    word1 = proof_dict[proofNum][0]
    word2 = proof_dict[proofNum][1]

    case = 3
    listOfWords = [word2]

    if(word1=="??" or word2=="??"):

        if(word2=="??"): case = 1
        else:
            case = 2
            word1 = word2
            word2 = "??"
        
        listOfWords = []
        for key in formula_dict:
            listOfWords.append(str(key) + "f")
        for key in this_dict:
            listOfWords.append(str(key) + "p")
    
    if(DEBUG):
        print("ProofNum: "+str(proofNum)+str(':')+str(listOfWords))

    for thisWord in listOfWords:
        word2 = thisWord
        if(word1==word2): continue

        test1,form1 = returnFormula(word1,formula_dict,this_dict)
        test2,form2 = returnFormula(word2,formula_dict,this_dict)
        test3,outProof = resolve(form1,form2)

        if(DEBUG):
            print(word2+","+str(form1)+"|"+str(test1)+":"+str(test2)+":"+str(test3)+"|"+str(outProof))

        if not (test1 and test2 and test3):
            continue
        
        this_dict[proofNum] = outProof
        if(case!=2): out_dict[proofNum] = [word1,word2]
        else: out_dict[proofNum] = [word2,word1]

        if(proofNum==lastNum):
            if(len(outProof)==0):
                return True
            else: 
                del this_dict[proofNum]
                del out_dict[proofNum]
                continue

        if(recursive(this_dict,out_dict,formula_dict,proof_dict,proofNum+1,lastNum)):
            return True

        del this_dict[proofNum]
        del out_dict[proofNum]
    
    return False
    
def solve(formula_file,modified_proof_file,ouput_file):
    proof_file = modified_proof_file
    outputFileName = ouput_file

    TEST = False

    formula_dict = readFormulaFile(formula_file)
    if(DEBUG): print("FORMULA: "+str(formula_dict))

    proof_dict = {}
    proof_idx = 0

    ptext  = open(proof_file,"r")
    lines = ptext.readlines()

    for line in lines:
        proof_idx += 1
        words = line.split()
        
        proof_dict[proof_idx] = [words[0],words[1]]
    
    this_dict = {}
    out_dict = {}
    
    TEST = recursive(this_dict,out_dict,formula_dict,proof_dict,1,proof_idx)

    if(DEBUG):
        print("PROOF_DICT....THIS_DICT....OUT_DICT")
        print(proof_dict)
        print(this_dict)
        print(out_dict)

    if(TEST): printOutput(outputFileName,out_dict,this_dict,proof_idx)
    else:  
        outFile = open(outputFileName,"w")
        for jdx in range(1,proof_idx+1):

            outFile.write(proof_dict[jdx][0] if proof_dict[jdx][0]!="??" else "np")
            outFile.write(" ")
            outFile.write(proof_dict[jdx][1] if proof_dict[jdx][1]!="??" else "np")
            outFile.write("\n")
        
        outFile.close()


if __name__ == "__main__":
    
    solve(sys.argv[1],sys.argv[2],sys.argv[3])