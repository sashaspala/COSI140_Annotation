import os
from xml.dom.minidom import parse, Node
import re


class cleanup:
	def __init__(self, path):
		print("init..")
		self.save_path = path
		self.counter_dict = {}

	def clean_files(self, path):
		print("setting up cleaning...")
		for file in os.listdir(path):
			full_path = os.path.join(path, file)
			if os.path.isfile(full_path):
				# open this goldstandard and read it in
				xml_file = parse(full_path)
				# now parse this file
				self.parse_xml(xml_file)


	def parse_xml(self, xml_file):
		print("getting ready to parse")
		annotated_items = xml_file.getElementsByTagName('TAGS')
		for element in annotated_items:
			print(element.tagName)
			for item in element.childNodes:
				if item.nodeType == Node.ELEMENT_NODE:
					print(item.getAttribute('text'))
					cleaned = self.clean_utt(item.getAttribute('text'))
					# now make new file under the correct folder path
					tag = item.getAttribute('type')
					print()

					self.save_new_item(cleaned, tag)

	def save_new_item(self, content, tag):
		print("saving into a new file...")
		full_path = os.path.join(self.save_path, tag)
		if not os.path.isdir(full_path):
			os.makedirs(full_path)

		self.counter_dict[tag] = self.counter_dict.get(tag, 0) + 1
		# now make a new file
		to_write_file = open(os.path.join(full_path, tag + '_' + str(self.counter_dict[tag])), 'w')
		to_write_file.write(content)
		to_write_file.close()


	def clean_utt(self, utterance):
		print("cleaning up the utterance...")
		# <RESPONSE id="R1" spans="372~399" text="20.69 21.19	DORIS:  	.. So," type="backchannel" />
		# first clean off the timespans
		split_utt = utterance.split()

		# now check if there's a new speaker in here
		match = re.match('[A-Z]+:', split_utt[2])
		if match:
			# everything past index 2 is our actual text

			index = 3
		else:
			index = 2
		# get rid of anything in between parenthesis, and extract any words between []
		content = ' '.join(split_utt[index:])
		paren_match = re.sub('\(.+\)', '', content)
		left_bracket_match = re.sub('\[[0-9]+', '', paren_match)
		right_bracket_match = re.sub('[0-9]+\]', '', left_bracket_match)
		print right_bracket_match
		return right_bracket_match

if __name__ == "__main__":
	cl = cleanup('corpus/')
	cl.clean_files('Goldstandard_Data/')