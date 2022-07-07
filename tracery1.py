import json
import random
from pprint import pprint
from modifiers import modifier_dictionary
# 
# Make your own Python port of Tracery, a text expansion library from Dr Kate
# An example Tracery tutorial http://air.decontextualize.com/tracery/
# A tracery editor by Dr Kate: artbot.club
# Bots and other resources on Tracery at BotWiki: 
#  https://botwiki.org/?s=tracery&search-filters-options%5B%5D=everything
#
# This assignment will use both recusion and dictionaries
# Unlike previous assignments, all the functions will be used as part of the 
# same algorithm.  So it is very important to test each individual function
# well, rather than trying to debug the whole algorithm

def load_grammar(path_to_grammar):
	""" 
	Load a JSON grammar file from a given path
	Parameters: 
		path_to_grammar(str): path to the grammar e.g. "grammars/cafe.json"
	Returns: 
		dict: a grammar that is a dictionary of strings or lists of strings (Tracery rules)
			e.g. {
					"animal": ["corgi", "wildcat", "otter", "antelope"],
					"color": ["magenta", "silver"],
					"origin": "Some #color# #animal.s# went to #place#"
				}
	"""
	# Task 0: Load a grammar from JSON
	file = open(path_to_grammar)
	data = json.load(file)
	return data

def get_rule(grammar, key):
	"""
	Given a grammar and a key, find the rules for this key, select one randomly, and return it
		Parameters: 
			grammar(dict of lists or strings): a set of rule options for different keys
			key(str): a key that may be in the grammar
		Returns: 
			str: a randomly-selected rule from the grammar for this key if there is one
				if the key is *not* in this grammar, return "((key))" 
					for the name of that key, ie, "((animal))"
	"""

	# Task 1: given a key and a grammar (a dict), select a rule for that key
	# There are three cases to handle:
	# 	* that key is not in the grammar dict: return "((some_key))" for the name of the key
	# 	* the key is in the dict, and its value is a str, return the string (only one choice!)
	#	* the key is in the dict, and its value is a list, 
	#		use "random.choice" to return a randomly selected element of that list

	if key in grammar:
		v = grammar[key]
		if type(v) is not list:
			return v
		else:
			return random.choice(v)
	
	else:
		return f'(({key}))'
	
	


def apply_modifiers(modifier_names, text):
	"""
	Given a dictionary of modifiers, a list of modifier names, and some text,
	return the result of applying each modifier by that name. 
	(Skip any modifiers where we don't have a modifier by that name)
	in order, to that text
	ie: "apple", ["a", "capitalize"] => "An apple"
	ie: "apple", ["s", "capitalizeAll"] => "APPLES"
	ie: "apple", ["capitalizeAll", "s"] => "APPLEs"
	
	Parameters:
		modifier_names(list is str): a list of modifier names "a", "s", "capitalize" to apply in order to the string
		text(str): the text to be changed
	Returns: 
		(str): the modified string 
	"""
	


	# Task 2: given a text (str), and a list of modifiers, and a dict of functions, 
	# 	return the result of modifing this string with each of those functions 
	#		(hint, use a for-loop to apply each modifier and replace 
	#		the current value of "text" with the modified version)
	#	Notice that we can store any kinds of Python variable in a dictionary: 
	#		lists, str, numbers, bools, even functions!
	#	When get a value from this dictionary, it will be a function, 
	# 		you can store that as a variable, just like you would with any other type
	# 		and then call it like any other function
	#		e.g.: 	"my_fxn = some_dict[some_key]" 
	#				"my_fxn(x, y, z)"


	# NOTE: modifiers_dictionary(dict of functions) is a dictionary of 
	#   functions that take a string and return a modified copy of that string
	#	It is imported at the top of this file, and must be in the same directory as this file
	# print("The available modifiers are: ", modifier_dictionary.keys())


	#print("The available modifiers are: ", modifier_dictionary.keys())
	# print("The available modifiers are: ", modifier_dictionary.keys())
	if type(modifier_names) is list:
		for mod in modifier_names:
			if mod in modifier_dictionary:
				fn = modifier_dictionary[mod]
				text = fn(text)
		return text
				

	return "--TODO, TASK 2--"





def expand_rule_section(grammar, section_text, index):
	"""
	*** A helper function for expand_text *** 
	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
		section_text(str): the text of this section "animal" or "animal.a.capitalize"
		index: the index of this section in the rule, this will determine if we need to expand it (odd) or not (even)
	Returns: 
		str: the expanded and modified rule (if we are expanding) or the section_text (if not)
	"""
	

	# Checking types!
	assert isinstance(grammar, dict), "expected a dict as grammar"
	assert isinstance(section_text, str), "expected a string as section_text"
	assert isinstance(index, int), "expected a int as index"

	# TASK 3: Expand this rule section
	# (I'm putting it outside the function so we can test it independently -Dr. Kate)
	# For even sections (index%2==0), return the original section text (we don't need to do anything further)
	# For odd sections, this is a *socket* (ie, "animal.a.capitalize", and we need to figure out what to fill it with
	# To expand a socket:
	#  * split the socket text with "." to get a list
	#  * the "key" for this socket is the *first* element in the list (ie: "animal")
	#  * the remaining elements are a list of modifier names (ie ["a", "capitalize"])
	#		* It may be an empty list! []
	#     (hint, you can use a "slice" to get a list containing all the remaining elements
	#     (https://www.programiz.com/python-programming/methods/built-in/slice))
	#  * get a rule for this key using "get_rule"
	#  * expand the rule using "expand_rule" (RECURSION!) to get the finished expanded rule
	#  * apply the modifiers to the expanded rule
	#  * return the final modified expanded rule

	if index % 2 == 0:
		return section_text
	else:
		list = section_text.split('.')
		key = list[0]
		#key
		fn = list[1:]
		rule = get_rule(grammar, key)
		new_rule = expand_rule(grammar, rule)
		expanded_text = apply_modifiers(fn, new_rule)
	
	return expanded_text
def expand_rule(grammar, rule):
	"""
	To expand a Tracery rule using a Tracery replacement grammar
	  e.g. "the #animal# went to #place# and ate #food#"
	* Split the text into a list of sections using text.split("#")
	* Create a *new list* from the list of sections using a list comprehension or a for loop
	*   For each section, use expand_rule_section to expand this section into its final form
	* Use "".join(some_list) to merge the list back into a single string
		(note that just casting it to a string "str(some_list" would add unwanted commas)

	Hint: Using "enumerate" in your for-loop or list comprehension 
		will make it much easier to get an index to pass to "expand_rule_section"
	   https://realpython.com/python-enumerate/

	Parameters: 
		grammar(dict of lists or strings): a set of rule options for different keys
		rule(str): a Tracery rule to expand, e.g. "Some #color# #animal.s# went to #place.a#" 
			or "#color#" or "magenta"<-(no expansion needed for this one!)
	Returns
		str: the finished text of the expanded rule, e.g. "Some magenta corgis went to the zoo"
	"""

	# Task 4: Expand this rule (using the algorithm above, and the expand_rule_section helper function)
	text = list(rule.split("#"))
	updated_rule = []
	for count, section in enumerate(text):
		result = expand_rule_section(grammar, section, count)
		updated_rule.append(result)
	
	answer = ''.join(updated_rule)
	return answer

	return "--TODO, TASK 4--"



# Task 5
# Create your own grammar to create stories, or poetry, or dialogue, or fancy coffee drinks (whatever you want!)
# It should have at least 5 different keys, and at least 15 total rules, and an "origin" key that
# is the start of your generator.  
# **don't change the name from "my_grammar", it needs this same name for the autograder to read it!**

my_grammar = {
	"food": ["steamed buns", "spaghetto", "pancake", "vinegar"],
	"nouns": ["poem", "story", "#food# recipe", "trick", "joke", "sitution", "episode"],
	"vehicle": ["boat", "bobsled", "bird", "tractor", "bulldozer", "steamroller"],
	"people": ["astronaut", "food critic", "farmer", "student"],
	"adjectives": ["salty", "stanky", "jank", "wack", "busted", "toasted"],
	"origin": "Here is a cool #nouns#: 'Thanks for the #food#!' I said as the #people# ran off on a #adjectives# #vehicle.capitalizeALL#"
}



if __name__ == '__main__':


	#----------------------------
	# Task 0

	# Load a known grammar to test against
	grammar = load_grammar("grammars/simple.json")
	assert isinstance(grammar, dict), "The grammar should be a dictionary"
	assert len(grammar.keys()) > 0, "There should be at least one key in this grammar, did you load it yet?"

	print(f"The keys of this grammar are {grammar.keys()}")
	
	# Pretty print this grammar, format it nicely
	pprint(grammar) 
	for i in range(0, 5):
		print(expand_rule(grammar, "#origin#"))

	#----------------------------
	# Task 1

	# Random seeds allow us to generate the same random choices in a repeatable way
	# Calling random multiple times may cause you to get DIFFERENT ANSWERS than the asserts.
	# ** The main thing to watch for is that you get a *variety* of answers (it will repeat sometimes) 

	# Look, mostly different!
	for i in range(0, 7):
		print("get rule for 'animal': ", get_rule(grammar, "animal"))

	# # Look, all the same!
	for i in range(0, 7):
		random.seed(10)
		print("get rule for 'animal', but with a seed: ", get_rule(grammar, "animal"))
	
	my_seed = 0

	# # We can set the seed, pick a random rule, and print it
	random.seed(my_seed)
	print(f"Getting a rule with seed {my_seed}:", get_rule(grammar, "animal"))
	# # If we set the same seed, we will pick the same rule again!
	random.seed(my_seed)
	assert get_rule(grammar, "animal") == "corgi", "get_rule does not return 'corgi' for seed 0"

	my_seed = 10
	random.seed(my_seed)
	print(f"Getting a rule with seed {my_seed}:", get_rule(grammar, "animal"))
	random.seed(my_seed)
	assert get_rule(grammar, "animal") == "boa", "get_rule does not return 'corgi' for seed 0"
	assert get_rule(grammar, "insect") == "((insect))", "Not the right format for missing keys, expecting: '((insect))'"

	assert get_rule(grammar, "origin") == "#adj.a# pack of #adj# #animal.s#", "Make sure you can handle if the rule is a single string, not a list"

	#----------------------------
	# Task 2

	# Test out the modifiers
	words = ["apple", "run", "flower", "mouse", "eagle"]
	for word in words:
		modified_word = apply_modifiers(["a", "capitalize"], word)
		print(f"{word} => {modified_word}")
	
	for word in words:
		modified_word = apply_modifiers(["ALLCAPS", "s"], word)
		print(f"{word} => {modified_word}")

	assert apply_modifiers(["a", "capitalize"], "coffee") == "A coffee" 
	assert apply_modifiers(["ALLCAPS", "s"], "coffee") == "COFFEEs" 
	
	#----------------------------
	# Task 3

	assert isinstance(expand_rule_section(grammar, "animal", 0), str), "expand_rule_section should return a string"

	random.seed(10)
	rule_section0 = expand_rule_section(grammar, "animal", 0)
	random.seed(10)
	rule_section1 = expand_rule_section(grammar, "animal", 1)
	random.seed(10)
	rule_section2 = expand_rule_section(grammar, "animal.a.capitalize", 1)
	print("EVEN:", rule_section0)
	print("ODD:", rule_section1)

	assert rule_section0 == "animal", "Even sections should return the text unaltered"
	assert rule_section1 == "boa", "Odd sections should expand the key for this socket"
	assert rule_section2 == "A boa", "Are you applying modifiers correctly?"

	#----------------------------
	# Task 4
	
	assert isinstance(expand_rule(grammar, "#animal#"), str), "Expand rule should return a string"

	
	plain_rule = "animal"
	medium_rule = "Hello, #animal#!"
	modifier_rule = "Hello, lots of #animal.s#"
	modifier_rule2 = "'#adj.a.ALLCAPS# AND #adj.ALLCAPS# #animal.ALLCAPS#!!', I exclaimed, in #adj.a# voice"
	complicated_rule = "#adj.a.capitalize# #animal#, and lots of #adj# #animal.s#"
	origin_rule = "#origin#"

	# # Which rule to try out? Change this to test various rules
	current_rule = complicated_rule
	random.seed(0)
	print(f"Expanding '{current_rule}'")
	for i in range(0, 10):
		finished = expand_rule(grammar, current_rule)
		print(finished)
	

	#random.seed(0)
	#assert expand_rule(grammar, complicated_rule) == "A cyan corgi, and lots of ((size)) emus", "It's ok if your output doesn't match this, but it should do the capitalization, plurals, and handling missing keys properly"
	
	#random.seed(20)
	#print(expand_rule(grammar, modifier_rule2))	
	#random.seed(20)
	#assert expand_rule(grammar, modifier_rule2) == "'AN AMBIDEXTROUS AND RED EMU!!', I exclaimed, in an ancient voice", "It's ok if your output doesn't match this, but it should do the capitalization, plurals, and handling missing keys properly"
	
	#----------------------------
	# Task 5
	# Try our your grammar, or the two sample grammars
	# grammar = load_grammar("grammars/cafe.json")
	# grammar = load_grammar("grammars/magicschool.json")
	# grammar = load_grammar("grammars/losttesla.json")
	grammar = my_grammar
	print('SHEEEESH')
	for i in range(1):

		finished_rule = expand_rule(grammar, "#origin#")	
		print(finished_rule)

  