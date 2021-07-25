
START = '<S> '
UNK = 'NONE'
Landa1 = 0.99
Landa2 = 0.008
Landa3 = 0.002
Epsilon = 0.0001
Eps = Landa3*Epsilon
uni_dictionary = dict()
bi_dictionary = dict()
backoff_dictionary = dict()
back_ferdowsi = dict()
back_molavi = dict()
back_hafez  = dict()

# make the dictionary of each file 
def Make_dictionary(fileName):
    #make the file name fix
    file = fileName + ".txt"
    text = open(file, "r" , 1,"Utf-8") 

    # Create an empty dictionary 
    dictionary = dict() 
    
    for line in text: 
        line = line.strip() 
        words = line.split(" ") 
    
        for word in words: 
            # Check if the word is already in dictionary 
            if word in dictionary: 
                dictionary[word] = dictionary[word] + 1
            else: 
                dictionary[word] = 1
    
    # make the destination file name 
    name = fileName + "-dictionary.txt"

    #write if file
    # Write_file(name , 2 , dictionary)
    # UNK_file(fileName , dictionary)
    text.close()


# make the uniagram of text
def Unigram(fileName):
    #make the file name fix
    file = fileName + ".txt"
    text = open(file, "r" , 1,"Utf-8")

    
    for line in text: 
        line = line.strip() 
        words = line.split(" ") 
    
        for word in words: 
            # Check if the word is already in dictionary 
            if word in uni_dictionary: 
                uni_dictionary[word] = uni_dictionary[word] + 1
            else: 
                uni_dictionary[word] = 1

    for key, value in uni_dictionary.items(): 
            uni_dictionary[key] = value/sum(uni_dictionary.values())

    # make the destination file name 
    # name = fileName + "-unigram.txt"

    #write if file
    # Write_file(name , 0 , uni_dictionary)
    text.close()


# make the bigram of text
def Bigram(fileName):
    #make the file name fix
    file = fileName + ".txt"
    text = open(file, "r" , 1,"Utf-8")
    # count = word_count(fileName)
    
    for line in text:
        line = line.strip()
        line = START + line 
        words = line.split(" ")
        for i in range(len(words)-1): 
            word = words[i] + " " + words[i+1]
            # Check if the word is already in dictionary
            if word in bi_dictionary: 
                bi_dictionary[word] = bi_dictionary[word] + 1
            else: 
                bi_dictionary[word] = 1
    
    for key, value in bi_dictionary.items(): 
            bi_dictionary[key] = value/sum(bi_dictionary.values())
    # make the destination file name 
    # name = fileName + "-bigram.txt"

    #write if file
    # Write_file(name , 0 , bi_dictionary)
    text.close()


# make Backoff model to expect sente
def Backoff_model(fileName):
    Uni_dict = uni_dictionary
    bi_dict = bi_dictionary
    for key, value in bi_dict.items():
        words = key.split(' ')
        backoff_dictionary[key] = value*Landa1 + Uni_dict[words[1]]*Landa2 + Eps

    # make the destination file name 
    # name = fileName + "_Backoff-Model4.txt"
    # Write_file(name , 0 , backoff_dictionary)
    

#make UNK file that one repeated word deleted   
def UNK_file(fileName , dictionary):
    file = fileName + ".txt"
    fin = open(file ,"r" , 1,"Utf-8")
    Auk_fileName =  fileName + "-UNK.txt"
    fout = open(Auk_fileName ,"wt" , 1,"Utf-8")
    seprate = ' '
    for line in fin:
        line = line.strip()
        words = line.split(" ")
        for i in range(len(words)-1): 
            for key, value in dictionary.items():
                if(value < 2 and key == words[i]):
                    words[i] = UNK
        for i in range(len(words)-1):
            line = seprate.join(words)
        fout.write('%s\n' % line)
    

    fout.close()

# Counting the word
def word_count(fileName):
    #make the file name fix
    file = fileName + ".txt"
    text = open(file, "r" , 1,"Utf-8") 
    data = text.read()
    words = data.split()
    text.close()
    return (len(words))


#write to the file
def Write_file(fileName , limitation  , dictionary:dict()):
    with open(fileName, 'w' , 1 , 'Utf-8') as fout: 
        for key, value in dictionary.items(): 
            fout.write('%s\t :\t %s \n' % (key, value/sum(dictionary.values())))


def predict_unigram(line):
    line = line.strip() 
    words = line.split(" ") 
    uni_perdict = 1
    for word in words:
        if(word in uni_dictionary):
            uni_perdict = (uni_dictionary[word]) * uni_perdict
        else :
            uni_perdict = 0.0000001 * uni_perdict
    return uni_perdict

def predict_bigram(line):
    line = line.strip() 
    line = START + line
    words = line.split(" ") 
    bi_perdict = 1
    for i in range(len(words)-1): 
        word = words[i] + " " + words[i+1]
        if(word in bi_dictionary):
            bi_perdict = (bi_dictionary[word]) * bi_perdict
        else :
            bi_perdict = 0.0000001 * bi_perdict
    return bi_perdict

def predict_backoff(line):
    line = line.strip() 
    line = START + line
    words = line.split(" ") 
    backoff_perdict = 1
    for i in range(len(words)-1): 
        word = words[i] + " " + words[i+1]
        if(word in backoff_dictionary):
            backoff_perdict = (backoff_dictionary[word])* backoff_perdict
        else :
            backoff_perdict = 0.0000001 * backoff_perdict
    return backoff_perdict


def predict(fileName):
    #make the file name fix
    file = fileName + ".txt"
    text = open(file, "r" , 1 , 'Utf-8')
    backoff_predict = dict()
    for line in text:
        line = line.strip()
        words = line.split('\t')
        backoff_predict[line] = predict_backoff(words[1])
    return backoff_predict


def write_result(fileName ,ferdowsi , hafez , molavi):
    filename = fileName + ".txt"
    fout = open(filename ,"w" , 1,"Utf-8")
    hafez_value = list(hafez.values())
    molavi_value = list(molavi.values())
    
    count = 0
    for key , value in ferdowsi.items():
        values = [value , hafez_value[count] , molavi_value[count]]
        index = values.index(max(values))
        fout.write('%s\t%s\t%s\t%s\t%s\n' % (key , value , hafez_value[count] , molavi_value[count] , index+1))
        count = count + 1 

def precision(fileName):
    file = fileName + ".txt"
    text = open(file, "r" , 1 , 'Utf-8')
    correct = 0
    all = 0 
    for line in text:
        line = line.strip()
        words = line.split('\t')
        if(words[0] == words[5]):
            correct = correct + 1
        all = all + 1
    print(all , correct)
    return correct/all

# Make_dictionary("./train_set/ferdowsi_train")
Unigram("./train_set/ferdowsi_train")
Bigram("./train_set/ferdowsi_train")
Backoff_model("./train_set/ferdowsi_train")


back_ferdowsi = predict("./test_set/test_file")
# Make_dictionary("./train_set/hafez_train")
Unigram("./train_set/hafez_train")
Bigram("./train_set/hafez_train")
Backoff_model("./train_set/hafez_train")


back_hafez = predict("./test_set/test_file")
# Make_dictionary("./train_set/molavi_train")
Unigram("./train_set/molavi_train")
Bigram("./train_set/molavi_train")
Backoff_model("./train_set/molavi_train")


back_molavi = predict("./test_set/test_file")
write_result("result" , back_ferdowsi , back_hafez ,back_molavi)
print(precision("result"))