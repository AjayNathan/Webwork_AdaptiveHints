import sys
import nltk
import numpy as np

def preprocess_text_file(filename):
    '''Given a text file with filename 'filename', preprocess it into a 
       bag-of-words matrix of counts X.  Only words that appear at least
       5 times in the corpus are counted.  
       
       Returns: (lines of the file, bag-of-words model)
       '''    
    #read all lines in the file in a string list
    with open(filename,'r') as f:
        lines = f.readlines()
    #get the word counts after splitting the lines read
    vocab_dist = nltk.FreqDist(
        (word for line in lines for word in line.split()) )
    #keep the words with the count greater than 5
    #FreqDist is a subclass of dict
    vocab_list = [word 
        for word,count in vocab_dist.iteritems() if count > 5]
    #sort the selected words i.e. with count > 5
    vocab_list = sorted(vocab_list)
    #give indices i to the selected words and create a dictionary with pairs word:index
    vocab_hash = dict((s,i) for i,s in enumerate(vocab_list) )
    #create a zero matrix X with size (#lines, #selectedWords)
    #NOTE: type can be specified to save from memory
    X = np.zeros( shape=(len(lines),len(vocab_list)) )
    #find the count of selected words in each line and create BOW representation
    for i,line in enumerate(lines):
        for word in line.split():
            if word in vocab_hash:
                X[i,vocab_hash[word]] += 1
    return lines, X

#script implementation
if __name__ == '__main__':            
    (lines, X) = preprocess_text_file(sys.argv[1])

    #NOTE: No stemming and stop-word removal applied
    #NOTE: Transformation of counts generally give better results in the case of classification