import urllib
from googletrans import Translator
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %a %H:%M:%S')
LOGGER = logging.getLogger(__name__)


def make_soup(url):
	req = urllib.request.Request(
		url,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)
	f = urllib.request.urlopen(req)
	soupdata = BeautifulSoup(f, "html.parser")
	return soupdata


def srape_sinonimai(search_string, custom_string=""):
	"""
	Scrape http://sinonimas.lt
	:param search_string:
	:param custom_string:
	:return:
	"""
	first_letter = search_string[0]
	words = []
	link = "http://sinonimas.lt/lt/sinonimai/" + first_letter + custom_string + "/" + search_string
	soup = make_soup(link)
	for x in soup.find("ul", class_="list-inline list-unstyled wordList"):
		try:
			word = x.a.text
			word_href = x.a['href']
			words.append((word, word_href))
		except AttributeError:
			pass
	logging.debug(words)

	return words


def scrape_lt_word_meaning(search_string):
	"""
	Scraping from
	http://www.zodynas.lt/terminu-zodynas/P/patirtis
	:param search_string:
	:return:
	"""
	first_letter = search_string[0]
	word_meaning = ""
	link = "http://www.zodynas.lt/terminu-zodynas/" + first_letter + "/" + search_string
	soup = make_soup(link)
	for x in soup.find("h1", class_="m-t0 capitilize"):
		try:
			word_meaning = x.next.text
			logging.debug(word_meaning)
		except AttributeError:
			pass
	return word_meaning


def strip_lt(word_to_parse):
	"""
	Strips lt letters and repleces with counterparts like ą to ą
	:param word_to_parse:
	:param w:
	:return:
	"""
	ltd = {
		"ą": "a",
		"č": "c",
		"ę": "e",
		"ė": "e",
		"į": "i",
		"š": "s",
		"ų": "u",
		"ū": "u",
		"ž": "z"
	}
	w = ""
	for letter in word_to_parse.lower():
		remember = 0
		for key in ltd:
			if letter == key:
				w += ltd[key]
				remember = 1
		if remember != 1:
			w += letter
	return w


def get_word(word):
	"""
	Process words from srape_sinonimai
	:param word:
	:return:
	"""
	try:
		fweb_synonyms = srape_sinonimai(word)
	except TypeError as err:
		logging.debug(err)
		logging.info("Found nothing, trying different link")
		try:
			fweb_synonyms = srape_sinonimai(word, custom_string="-1")
		except TypeError:
			LOGGER.info("No word found")
			return None
		return fweb_synonyms
	return fweb_synonyms


def get_en_word_etymology(search_word):
	#:TODO Fix etymology
	"""
	Scrape words from www.etymonline.com
	:param search_word:
	:return:
	"""
	link = "http://www.etymonline.com/index.php?allowed_in_frame=0&search=" + search_word
	soup = make_soup(link)
	result = ""
	for index, element in enumerate(soup.find("dl")):
		if index == 4: break
		if len(element) > 1:
			if len(element) < 40:
				print("")
			print(element.text)
			result += element.text + "\n"
	return result


def get_lt_word_etymology(search_word):
	"""
	Scrape words from http://etimologija.baltnexus.lt/?w=%search_word%
	:param search_word:
	:return:
	"""
	link = "http://etimologija.baltnexus.lt/?w=" + search_word
	soup = make_soup(link)
	result = ""
	for index, element in enumerate(soup.find_all("dl")):
		print(element)
		try:
			antraste = element.find("dd", {"class": "title"}).text
		except:
			antraste = ""
		try:
			reiksme = element.find("dd", {"class": "meaning"}).text
		except:
			reiksme = ""
		try:
			straipsnelis = element.find("dd", {"class": "description"}).text
		except:
			straipsnelis = ""
		result += "Antraštė: {}\nReikšmė: {}\nStraipsnelis: {}\n".format(antraste, reiksme, straipsnelis)
	return result


def translate_from_lt_english(word):
	"""
	Translate from lithuanian to english
	:param word: input work lt
	:return: output work en
	"""
	translator = Translator()
	detect = translator.translate(word, src="lt", dest="en")
	return detect.text


def translate_from_en_to_lt(word):
	"""
	Translate from lithuanian to english
	:param word: input work lt
	:return: output work en
	"""
	translator = Translator()
	detect = translator.translate(word, src="en", dest="lt")
	return detect.text


def translate_auto(word):
	"""
	Translate from lithuanian to english
	:param word: input work lt
	:return: output work en
	"""
	translator = Translator()
	if translator.detect(word).lang == "lt":
		detect = translator.translate(word, src="lt", dest="en")
		return detect.text
	if translator.detect(word).lang == "en":
		detect = translator.translate(word, src="en", dest="lt")
		return detect.text
	else:
		return "Cant translate"


def get_synonims(word):
	"""
	Get only synonims, without links
	:param word:
	:param result:
	:return:
	"""
	result = ""
	synonyms_lt = get_word(strip_lt(word))
	LOGGER.debug(synonyms_lt)
	try:
		for synonym, link in synonyms_lt:
			result += synonym + ","
	except TypeError:
		return None
	return result


def _run_as_standalone():
	word = "rytas"
	# # print(word)
	# #
	# print(get_synonims(word))
	print(scrape_lt_word_meaning(word))

# lt_to_en = translate_from_lt_english(word)
# print(lt_to_en)
# print(translate_auto("car"))


# print()
# print("Vertimas: {}".format(detect.text))

# print(get_en_word_etymology(lt_to_en))
# get_lt_word_etymology("labas")


if __name__ == "__main__":
	_run_as_standalone()
