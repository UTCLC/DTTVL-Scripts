import re

pattern = re.compile("Awake\\(\\) cil managed\n  {[^}]*?instance void EnemyBase::Awake\\(\\)[^}]*?ldstr      \"(.*)?\"[^}]*?stfld      string EnemyBase::enemyName[^}]*?\"(.*)?\"[^}]*?stfld      string EnemyBase::fileName")

with (open(input("File path: "), "r", encoding="utf-8-sig") as f):
	content = f.read()
	find = pattern.findall(content)
	print(find)
	for search in find:
		if (search[0].lower() != search[1]):
			print(search[0] + " != " + search[1])
			for search1 in find:
				if (search1[0].lower() == search1[1] and search[1] == search1[1]):
					print(" - But: " + search1[0] + " == " + search1[1])