import xml.etree.ElementTree as ET
import collections
import itertools
import sys


a=''

def PrintElement(element, level):
	global a
	a+='!br!'
	while level > 0:
		a+='<tab>'
		level -= 1

	a+=ET.tostring(element).strip()

def PrintAttributes(e1, e2):
	global a
	for key, value in e1.attrib:
		a+=str(' ' + key + '="' + value + '"')

def CompareAndPrintElement(e1, e2, level):
	global a
	if e1 == None:
		a+='[1]-'
		PrintElement(e2, level)
		a+='-[1]'
		return

	if e2 == None:
		a+='[2]-'
		PrintElement(e1, level)
		a+='-[2]'
		return

	if e1.tag == e2.tag:
		#if ET.tostring(e1).strip().endswith('/>'):
		#	templevel = level
		#	while templevel > 0:
		#		sys.stdout.write('<tab>')
		#		templevel -= 1

		#	print ET.tostring(e1).strip()

		elementName = splitHeadTail(ET.tostring(e1))
		print 'shameer elementName',elementName
		templevel = level
		a+='!br!'
		while templevel > 0:
			a+='<tab>'
			templevel -= 1

		if not CompareAttributes(e1, e2):
			a+=str(elementName.head[0:elementName.find(ET.tostring(e1).strip())+len(e1.tag)])
			print 'shameer a',a
			PrintAttributes(e1, e2)
			if ET.tostring(e1).strip().endswith('/>'):
				a+=('/>'+'-br-')
			else:
				a+=('>'+'-br-')
		else:
			if ET.tostring(e1).strip().endswith('/>'):
				#templevel = level
				#while templevel > 0:
				#	sys.stdout.write('<tab>')
				#	templevel -= 1

				a+=ET.tostring(e1).strip()
			else:
				a+=elementName.head.strip()

		children1 = sorted(list(e1), key = lambda x: x.tag)
		children2 = sorted(list(e2), key = lambda x: x.tag)
		print 'shameer children',children1,children2
		if len(children1) == 0 and len(children2) == 0:
			templevel = level
			a+='!br!'
			while templevel >= 0:
				a+=('<tab>')
				templevel -= 1

			if e1.text == e2.text:
				a+=e1.text.strip()
			else:
				#templevel = level
				#while templevel > 0:
				#	sys.stdout.write('<tab>')
				#	templevel -= 1
				a+=('[1]-' + e1.text + '-[1][2]-' + e2.text + '-[2]')
				
		i = 0
		while i < len(children1):
			j = 0
			removei = False
			while j < len(children2):
				removej = False
				if CompareElement(children1[i], children2[j]):
					print 'shameer calling CompareElement'
					removei = True
					removej = True

				if removej:
					children2.pop(j)
					break
				else:
					j += 1

			if removei:
				PrintElement(children1[i], level+1)
				children1.pop(i)
			else:
				i += 1

		#if len(children2) > len(children1):
		#	children1, children2 = children2, children1

		for x, y in itertools.izip_longest(children1, children2):
			CompareAndPrintElement(x, y, level+1)

		templevel = level
		a+='!br!'
		while templevel > 0:
			a+=('<tab>')
			templevel -= 1

		a+=str(elementName.tail.strip())

#			for i in range(math.min(len(children1), len(children2))):
#				#if CompareElement(children1[i], children[2]):
#				PrintElement(children1[i], children2[i])
#
#			if len(children1) > len(children2):
#				for i in range(len(children1) - len(children2)):
#					PrintElement(children1[i+1+len(children2)]

def CompareAttributes(e1, e2):
	global a
	#print('collections.Counter(e1)' + str(collections.Counter(e1)))
	#print('collections.Counter(e2)' + str(collections.Counter(e2)))
	return collections.Counter(e1.attrib) == collections.Counter(e2.attrib)

def CompareElement(e1, e2):
	global a
	if e1.tag == e2.tag and e1.text == e2.text:
		attributesMatch = CompareAttributes(e1, e2)
		#print('attributesMatch = ' + str(attributesMatch))
		if attributesMatch:
			children1 = sorted(list(e1), key = lambda x: x.tag)
			children2 = sorted(list(e2), key = lambda x: x.tag)
			childrenMatch = False
			print 'inner CompareElement children1',children1,children2,e1,e2
			if len(children1) == len(children2):
				childrenMatch = True
				for i in range(len(children1)):
					if not CompareElement(children1[i], children2[i]):
						#print('children do not match - ' + str(children1[i]) + '----' + str(children2[i]))
						return False
			return childrenMatch
		
	#print('CompareElement (False) - ' + str(e1) + '----' + str(e2))
	return False

def splitHeadTail(element):
	global a
	Token = collections.namedtuple('Token', ['head', 'tail'])
	headcount = element.find('>')
	tailcount = element.rfind('<')

	if headcount > 0:
		head = element[0:headcount+1]
	else:
		#print 'Head could not be split' + element
		exit()
	
	if tailcount > 0:
		tail = element[tailcount:]
	else:
		#print 'Tail could not be split' + element
		exit()
	return Token(head, tail)

def printTree(root):
	global a
	if ET.tostring(root).strip().endswith('/>'):
		a+=ET.tostring(root)
		return

	elementName = splitHeadTail(ET.tostring(root))
	a+=str(elementName.head)
	if len(list(root)) > 0:
		for element in list(root):
			printTree(element)

	else:
		a+=root.text

	a+=elementName.tail


def xml_diff(obj_name,xml_obj_1,xml_obj_2):
	global a
	a=''
	root1=ET.fromstring(xml_obj_1)
	root2=ET.fromstring(xml_obj_2)	
	CompareAndPrintElement(root1, root2,0)
	return obj_name,a
	
#	tree1=ET.parse('D:/tutorial/python/xml_parser/abc.xml')
#	tree2=ET.parse("D:/tutorial/python/xml_parser/xyz.xml")
#	root1=tree1.getroot()
#	root2=tree2.getroot()
#	print 'value before',a
#	CompareAndPrintElement(root1, root2,0)
#	a+='end'



#print(Fore.RED + 'some red text')
#
#	option = 0
#	while option != 1 and option != 2:
#		print 'Enter input format:'
#		print '1.Filename'
#		print '2.XmlString'
#		option = int(raw_input())
#
#
#	if option == 1:
#		print 'Enter filename'
#		inputstring = raw_input()
#		tree1 = ET.parse(inputstring)
#	elif option == 2:
#		print 'Enter xmlstring'
#		inputstring = raw_input()
#		tree1 = ET.fromstring(inputstring)
#
#	option = 0
#	while option != 1 and option != 2:
#		print 'Enter input format:'
#		print '1.Filename'
#		print '2.XmlString'
#		option = int(raw_input())
#
#	if option == 1:
#		print 'Enter filename'
#		inputstring = raw_input()
#		tree2 = ET.parse(inputstring)
#	elif option == 2:
#		print 'Enter xmlstring'
#		inputstring = raw_input()
#		tree2 = ET.fromstring(inputstring)
#
#	CompareAndPrintElement(tree1.getroot(), tree2.getroot(), 0)
#	#if CompareElement(tree1.getroot(), tree2.getroot()):
#	#	print 'The two files are identical'
#	#else:
#	#	print 'The two files are different'

