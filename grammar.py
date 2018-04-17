import nltk
from nltk import word_tokenize, RegexpParser, parse
from nltk.tree import Tree, ParentedTree
import sys


# sent = "
#The slow lane of East Kowloon Way 
#Tsim Sha Tsui bound near San Lau Street 
#which 
#was closed 
#due to traffic accident 
#is re-opened to all traffic"

sent = "All lanes of Cheung Sha Wan Road Mei Foo bound near Wong Chuk Street which were closed due to traffic accident is re-opened to all traffic."
sent = word_tokenize(sent)
sent = nltk.pos_tag(sent)

# From Low to High
# NPC: Designed for parse location attri
# VP: Verb Phrase
# RP: Reason Prefix
# AC: Attributive clause


grammar2 = r""" 
	NP: {<NNP>+}  
   		{<NN><NN>+}
   		{<DT>?<JJ>*<NN|NNS>}
   	NPC:{(<NP><IN>)*<NP>}
   	VP: {<VB.><VB.|JJ><TO>?}
   	RP: {<JJ><TO>}
   	AC: {<WDT><VP>(<RP><NPC>)?}
   	FATHER : {<NPC><AC>?<VP><NPC|PP|JJ>?}
"""
# 		{<NPC><IN><NP>}

cp = nltk.RegexpParser(grammar2)
result = cp.parse(sent)

print(result)
result.draw()
