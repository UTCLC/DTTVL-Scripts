import os
import re
import json
import codecs
pattern = re.compile(r'"((?:\\"|\\\\|\\[^"]|[^"\\])*)"')

def find(dir):
	for dirfile in os.listdir(dir):
		path = os.path.join(dir, dirfile)
		if (os.path.isfile(path) and not (os.path.basename(path) in outputs)):
			print("Searching "+path)
			try: 
				with (open(path, mode="r", encoding="utf-8-sig") as f):
					lines = f.readlines()
					linen = 0
					for line in lines:
						search = pattern.search(line)
						if (search):
							string = search.group()[1:][:-1]
							print(f"Found {string} in {path} at line {linen}")
							strings[path.replace(directory,"").lstrip("\\")+":"+str(linen)] = string
						linen += 1
			except:
				print("Error encountered when loading "+path)
		elif (os.path.isdir(path) and not (path.rstrip("/").rstrip("\\").endswith("Repacked"))):
			find(path)

def output(dir):
	start_with_asterisk = {}
	contain_slash_underline = {}
	contain_space = {}
	contain_upper = {}
	others = {}
	for file in strings.keys():
		if ("* " in strings[file] or "*\\t" in strings[file]):
			start_with_asterisk[file] = strings[file]
		elif (" " in strings[file] or "\\t" in strings[file]):
			contain_space[file] = strings[file]
		elif ("/" in strings[file] or "_" in strings[file]):
			contain_slash_underline[file] = strings[file]
		elif (strings[file].lower() != strings[file]):
			contain_upper[file] = strings[file]
		else:
			others[file] = strings[file]
	with open(dir+"/asterisk.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(start_with_asterisk, indent=4, separators=(',', ': '), ensure_ascii=False))
	with open(dir+"/space.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(contain_space, indent=4, separators=(',', ': '), ensure_ascii=False))
	with open(dir+"/slash_underline.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(contain_slash_underline, indent=4, separators=(',', ': '), ensure_ascii=False))
	with open(dir+"/upper.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(contain_upper, indent=4, separators=(',', ': '), ensure_ascii=False))
	with open(dir+"/others.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(others, indent=4, separators=(',', ': '), ensure_ascii=False))

def inputt(jsonf):
	global strings
	with open(jsonf+"/others.json", mode="r", encoding="utf-8") as f:
		strings.update(json.loads(f.read()))
	with open(jsonf+"/upper.json", mode="r", encoding="utf-8") as f:
		strings.update(json.loads(f.read()))
	with open(jsonf+"/space.json", mode="r", encoding="utf-8") as f:
		strings.update(json.loads(f.read()))
	with open(jsonf+"/slash_underline.json", mode="r", encoding="utf-8") as f:
		strings.update(json.loads(f.read()))
	with open(jsonf+"/asterisk.json", mode="r", encoding="utf-8") as f:
		strings.update(json.loads(f.read()))

def write(dir):
	dir+="/"
	count = 0
	paths = {}
	for file in strings.keys():
		pathi = file.split(":")[0].replace("\\","/")
		if (pathi in paths.keys()):
			paths[pathi].append(count)
		else:
			paths[pathi] = [count]
		count += 1
	for path in paths.keys():
		os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
		lines = []
		try:
			with (open(dir+path, mode="r", encoding="utf-8-sig") as f):
				lines = f.readlines()
		except:
			print("Error encountered when reading "+dir+path)
		try:
			ff = codecs.open(dir+"Repacked/"+path, mode="w", encoding="utf-8-sig")
			for stringslinen in paths[path]:
				key = list(strings.keys())[stringslinen].split(":")
				linen = int(key[1])
				line = lines[linen]
				search = pattern.search(line)
				if (search):
					print(f"{search} was found in line {linen} of {path}")
					print("Replacing "+search.group()+" with \""+list(strings.values())[stringslinen]+"\" into "+path+" at line "+str(linen))
					lines[linen] = line.replace(search.group(),"\""+list(strings.values())[stringslinen]+"\"",1)
				#else:
					#print(f"No string was found in {path}")
			ff.writelines(lines)
			ff.close()
		except:
			print("Error encountered when writing "+dir+"Repacked/"+path)

strings = {}
outputs = ["asterisk.json","slash_underline.json","space.json","upper.json","others.json"]
directory = input("Directory: ").replace("\\","/")
if (directory.endswith("/")):
	directory = dir[:-1]
inpt = input("Extract(e) / Repack(r)\nIf nothing input, found all output JSONs will repack, otherwise extract: ")
if (inpt == ""):
	inpt = "r"
	for outputt in outputs:
		if (os.path.exists(directory+"/"+outputt)):
			print(outputt+" was found in "+directory)
		else:
			print(outputt+" was not found in "+directory)
			inpt = "e"
if (inpt == "e" or inpt == "extract"):
	find(directory)
	output(directory)
elif (inpt == "r" or inpt == "repack"):
	inputt(directory)
	write(directory)
else:
	print("Invalid input")