import os
import json

def find(dir):
	contents = {}
	for dirfile in os.listdir(dir):
		path = os.path.join(dir, dirfile)
		if (os.path.isfile(path) and not (path.endswith("strings.json"))):
			print("Searching "+path)
			with (open(path, mode="r", encoding="utf-8") as f):
				try:
					contents = json.loads(f.read())
				except:
					print("Error encountered when loading "+path)
				if ("left" in contents.keys()):
					string = contents["left"]
					print(f"Found {string} in {path}")
					strings[path.replace(directory,"").lstrip("\\")+":left"] = string
				if ("right" in contents.keys()):
					string = contents["right"]
					print(f"Found {string} in {path}")
					strings[path.replace(directory,"").lstrip("\\")+":right"] = string
				if ("up" in contents.keys()):
					string = contents["up"]
					print(f"Found {string} in {path}")
					strings[path.replace(directory,"").lstrip("\\")+":up"] = string
				if ("down" in contents.keys()):
					string = contents["down"]
					print(f"Found {string} in {path}")
					strings[path.replace(directory,"").lstrip("\\")+":down"] = string
				if ("phrases" in contents.keys()):
					stringss = contents["phrases"]["Array"]
					print(f"Found {stringss} in {path}")
					i = 0
					for string in stringss:
						strings[path.replace(directory,"").lstrip("\\")+":phrases:"+str(i)] = string
						i += 1
				for keyy in contents.keys():
					if (("text" in keyy.lower()) and (type(contents[keyy]) == str)):
						string = contents[keyy]
						print(f"Found {string} in {path}")
						strings[path.replace(directory,"").lstrip("\\")+":"+keyy] = string
					if (("lines" in keyy.lower()) and (type(contents[keyy]) == dict) and ("Array" in contents[keyy].keys())):
						stringss = contents[keyy]["Array"]
						print(f"Found {stringss} in {path}")
						i = 0
						for string in stringss:
							strings[path.replace(directory,"").lstrip("\\")+":"+keyy+":"+str(i)] = string
							i += 1
		elif (os.path.isdir(path) and not (path.rstrip("/").rstrip("\\").endswith("Repacked"))):
			find(path)

def output(dir):
	with open(dir+"/strings.json", mode="w", encoding="utf-8") as f:
		f.write(json.dumps(strings, indent=4, separators=(',', ': '), ensure_ascii=False))

def inputt(jsonf):
	global strings
	with open(jsonf+"/strings.json", mode="r", encoding="utf-8") as f:
		print(jsonf+"/strings.json")
		strings = json.loads(f.read())

def write(dir):
	cont = {}
	dir+="/"
	for file in strings.keys():
		path = file.replace("\\","/").split(":")[0]
		print("Writing "+strings[file]+" into "+path)
		with (open(dir+path, mode="r", encoding="utf-8") as f):
			try:
				cont = json.loads(f.read())
			except:
				print("Error encountered when loading "+path)
			if (":left" in file):
				if ("left" in cont.keys()):
					if (os.path.exists(dir+"Repacked/"+path)):
						with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
							cont = json.loads(f.read())
					os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
					with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
						cont["left"] = strings[file]
						f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
				else:
					print(f"No left was found in {path}")
			if (":right" in file):
				if ("right" in cont.keys()):
					if (os.path.exists(dir+"Repacked/"+path)):
						with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
							cont = json.loads(f.read())
					os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
					with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
						cont["right"] = strings[file]
						f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
				else:
					print(f"No right was found in {path}")
			if (":up" in file):
				if ("up" in cont.keys()):
					if (os.path.exists(dir+"Repacked/"+path)):
						with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
							cont = json.loads(f.read())
					os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
					with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
						cont["up"] = strings[file]
						f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
				else:
					print(f"No up was found in {path}")
			if (":down" in file):
				if ("down" in cont.keys()):
					if (os.path.exists(dir+"Repacked/"+path)):
						with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
							cont = json.loads(f.read())
					os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
					with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
						cont["down"] = strings[file]
						f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
				else:
					print(f"No down was found in {path}")
			if ("phrases" in file):
				if ("phrases" in cont.keys()):
					if (os.path.exists(dir+"Repacked/"+path)):
						with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
							cont = json.loads(f.read())
					os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
					with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
						cont["phrases"]["Array"][int(file.split(":")[-1])] = strings[file]
						f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
				else:
					print(f"No phrases was found in {path}")
			if ("text" in file.lower()):
				for keyy in cont.keys():
					if ((file.split(":")[1] == keyy) and (type(cont[keyy]) == str)):
						if (os.path.exists(dir+"Repacked/"+path)):
							with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
								cont = json.loads(f.read())
						os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
						with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
							cont[keyy] = strings[file]
							f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
					else:
						print(f"No *text* was found in {path}")
			if ("lines" in file.lower()):
				for keyy in cont.keys():
					if ((file.split(":")[1] == keyy) and (type(cont[keyy]) == dict) and ("Array" in cont[keyy].keys())):
						if (os.path.exists(dir+"Repacked/"+path)):
							with (open(dir+"Repacked/"+path, mode="r", encoding="utf-8") as f):
								cont = json.loads(f.read())
						os.makedirs(os.path.dirname(dir+"Repacked/"+path),exist_ok=True)
						with (open(dir+"Repacked/"+path, mode="w", encoding="utf-8") as f):
							cont[keyy]["Array"][int(file.split(":")[-1])] = strings[file]
							f.write(json.dumps(cont, indent=2, separators=(',', ': '), ensure_ascii=False))
					else:
						print(f"No *lines* was found in {path}")

strings = {}
directory = input("Directory: ").replace("\\","/")
if (directory.endswith("/")):
	directory = dir[:-1]
inpt = input("Extract(e) / Repack(r)\nIf nothing input, found strings.json will repack, otherwise extract: ")
if (inpt == ""):
	if (os.path.exists(directory+"/strings.json")):
		print("strings.json was found in "+directory)
		inpt = "r"
	else:
		print("strings.json was not found in "+directory)
		inpt = "e"
if (inpt == "e" or inpt == "extract"):
	find(directory)
	output(directory)
elif (inpt == "r" or inpt == "repack"):
	inputt(directory)
	write(directory)
else:
	print("Invalid input")