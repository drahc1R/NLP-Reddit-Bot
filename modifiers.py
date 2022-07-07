def mod_a(text):
	if len(text) == 0:
		return text
	if text.upper()[0] in "AEIOU":
		return "an " + text
	return "a " + text

def mod_s(text):
	if len(text) == 0:
		return text
	if text[-1] in "sxzh" or text[-1] in "SXZH":
		return text + "es"
	return text + "s"

def mod_ing(text):
	if len(text) == 0:
		return text
	if text[-1] in "e":
		return text + "ing"
	# Double the last consonant in short words "running"
	if len(text) < 5 and len(text) >= 2 and text[-1] not in "aeiouyw" and text[-2] in "aeiou" :
		return text + text[-1] + "ing"
	return text + "ing"

def mod_ed(text):
	if len(text) == 0:
		return text
	if text[-1] in "e":
		return text + "d"
	if text[-1] in "y":
		return text[:-1] + "ied"
	
	# Double the last consonant in short words "can->canned"
	if len(text) < 5 and len(text) >= 2 and text[-1] not in "aeiouyw"  and text[-2] in "aeiou" :
		return text + text[-1] + "ed"
	return text + "ed"

def mod_er(text):
	if len(text) == 0:
		return text
	text = mod_ed(text)
	return text[0:-1] + "r"

def mod_est(text):
	if len(text) == 0:
		return text
	text = mod_ed(text)
	return text[0:-1] + "st"

def mod_capitalize(text):
	return text[0].upper() + text[1:]
def mod_capitalizeall(text):
	return text.upper()

modifier_dictionary = {
	"a": mod_a,
	"firstS": mod_s,
	"s": mod_s,
	"ed": mod_ed,
	"er": mod_er,
	"est": mod_est,
	"ing": mod_ing,
	"ALLCAPS": mod_capitalizeall,
	"capitalize": mod_capitalize,
	"capitalizeAll": mod_capitalize,
}