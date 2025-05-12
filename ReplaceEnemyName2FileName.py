import re

pattern = re.compile(r'"battle/enemies/"[^"(){}}]*?dup[^"(){}}]*?string EnemyBase::enemyName')
pattern1 = re.compile(r'"battle/enemies/"[^"(){}}]*?ldfld      string EnemyBase::enemyName')

with (open(input("File path: "), "r", encoding="utf-8-sig") as f):
	content = f.read()
	find = pattern.findall(content)
	print(find)
	for i in find:
		content = content.replace(i,i[:-9]+"fileName")
		print("Replaced "+i+"\n to \n"+i[:-9]+"fileName")
	find = pattern1.findall(content)
	print(find)
	for i in find:
		content = content.replace(i,i[:-9]+"fileName")
		print("Replaced "+i+"\n to \n"+i[:-9]+"fileName")
	f.seek(0)
	f.write(content)