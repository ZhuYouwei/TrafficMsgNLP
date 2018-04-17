import sys
import json
import nltk
from nltk import word_tokenize, RegexpParser, parse
from nltk.tree import Tree, ParentedTree


def main():
	input = sys.argv[1]
	output = get_attri(input)
	json_string = json.dumps(output)
	print(json_string)
	sys.stdout.flush()

# one input:
def get_attri(x):
	text = word_tokenize(x)

	sentence = nltk.pos_tag(text)
	for index1, item1 in enumerate(sentence):
		if (item1 == ('bound', 'VBD')) or (item1 == ('bound', 'NN')):
			sentence[index1] = ('bound', 'NNP')
		## Handle case for misclassifciation Capital letter Name
		if index1 > 0 and item1[0][0].isupper():
			sentence[index1] = (sentence[index1][0], 'NNP')	
	# From Low to High
	# NPC: Designed for parse location attri
	# VP: Verb Phrase
	# RP: Reason Prefix
	# AC: Attributive clause
	grammar2 = r""" 
	
		NP: {<NNP>+<POS>?<NNP>+}
			{<NNP>+}
			{<NN><NN>+}
			{<DT>?<JJ>*<NN|NNS>}
		NPC:{(<NP><IN>)*<NP>}
		VP: {<VB.|MD><VB.|JJ><TO>?}
		RP: {<JJ><TO>}
		AC: {<WDT><VP>(<RP><NPC>)?}
		FATHER : {<RP><NPC><,><NPC><AC>?<VP><NPC|PP|JJ>?}
				 {<NPC><AC>?<VP><NPC|PP|JJ>?}

	"""

	cp = nltk.RegexpParser(grammar2)
	result = cp.parse(sentence)

	df = {}
	for index1, item1 in enumerate(result):
		if hasattr(item1, 'label'):
			if item1.label() == "FATHER": # structure identified
				loc_check = 0
				for index2, item2 in enumerate(item1):
					if hasattr(item2, 'label'):
						
						# Current Status
						if item2.label() == "VP" and (item2[0][1] == "VBZ" or item2[0][1] == "VBP"):
							df["Current Status"] = item2[1][0]
						
						# Previous Status
						if item2.label() == "AC":
							for index_psta, item_psta in enumerate(item2):
								if hasattr(item_psta, 'label'):
									if item_psta.label() == "VP":
										if item_psta[0][1] == "VBD":
											df["Previous Status"] = item_psta[1][0]
						
						# Incident Type
						if item2.label() == "AC":
							for index_reason, item_reason in enumerate(item2):
								if hasattr(item_reason, 'label'):
									if item_reason.label() == "RP":
										if item2[index_reason + 1].label() == "NPC":
											i = 0
											df["Incident Type"] = ""
											while (i < len(item2[index_reason + 1][0])):
												df["Incident Type"] = df["Incident Type"] + item2[index_reason + 1][0][i][0] + " "
												i = i + 1
						if hasattr(item2, 'label'):
							if item2.label() == "RP":
								if item1[index2 + 1].label() == "NPC":
									i = 0
									df["Incident Type"] = ""
									while (i < len(item1[index2 + 1][0])):
										df["Incident Type"] = df["Incident Type"] + item1[index2 + 1][0][i][0] + " "
										i = i + 1
						
						# Location
						if loc_check == 0 and item2.label() == "NPC":
							if not item1[index2+1][0] == ",":
								count_loc = 0
								for index_loc, item_loc in enumerate(item2):
									if not hasattr(item_loc, 'label'):
										if item_loc[0] == "near":
											i = 0
											df["Location"] = ""
											while (i < len(item2[index_loc-1])):
												df["Location"] = df["Location"] + item2[index_loc-1][i][0] + " "
												i = i + 1
											count_loc = 1
											loc_check = 1
									if index_loc == len(item2) - 1 and count_loc == 0:
										i = 0
										df["Location"] = ""
										while (i < len(item2[index_loc])):
											df["Location"] = df["Location"] + item2[index_loc][i][0] + " "
											i = i + 1
										loc_check = 1

						# Affected Lanes
						if item2.label() == "NPC":
							for index_loc, item_loc in enumerate(item2):
								if not hasattr(item_loc, 'label'):
									if item_loc[0] == "of":
										j = 0
										df["Affected Lanes"] = ""
										while (j < index_loc):
											i = 0
											while (i < len(item2[j])):
												if len(item2[j][i][0]) > 1:
													df["Affected Lanes"] = df["Affected Lanes"] + item2[j][i][0] + " "
													i = i + 1
												else:
													df["Affected Lanes"] = df["Affected Lanes"] + item2[j][i] + " "
													i = i + 2
											j = j + 1
						
						# Nearby Location
						if item2.label() == "NPC":
							for index_loc, item_loc in enumerate(item2):
								if not hasattr(item_loc, 'label'):
									if item_loc[0] == "near":
										i = 0
										df["Nearby Location"] = ""
										while (i < len(item2[index_loc+1])):
											df["Nearby Location"] = df["Nearby Location"] + item2[index_loc+1][i][0] + " "
											i = i + 1

						loc_map_check = 0
						for loc_var in ["Road", "Tunnel", "Highway", "Flyover", "Bridge", "Corridor","By-Pass"]:
							if loc_map_check == 0:
								if not df["Location"].find(loc_var) == -1:
									df["Road Name"] = df["Location"][0:df["Location"].find(loc_var)]+loc_var
									df["Direction"] = df["Location"][df["Location"].find(loc_var)+len(loc_var)+1:df["Location"].find("bound")]
									loc_map_check = 1
						if loc_map_check == 0:
							df["Road Name"] = df["Location"]
	return df

def bash_input(xs):
	res = []
	for x in xs:
		res.append(get_attri(x))
	return res
if __name__ == "__main__":
	main()
