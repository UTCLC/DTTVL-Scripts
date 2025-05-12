## ILStringsExtract.py

从 IL 文件中提取/重封字符串<br>
正则表达式：`"((?:\\"|\\\\|\\[^"]|[^"\\])*)"`<br>
输出的 JSON 的键格式：`文件名:行`<br>
文件名：文件名，包含相对路径<br>
行：第几行

根据规则筛选分为五个 JSON，从上至下筛选<br>
`asterisk.json`：含有`* `的，基本可以确定是正常对话文本，可以无脑翻译<br>
`space.json`：含有空格的，基本都是菜单选项或者对话的后半段，可以看着来翻译<br>
`slash_underline.json`：含有斜杠或下划线的，基本可以确定不需要翻译<br>
`upper.json`：含有大写的<br>
`others.json`：剩下的

## UpdateLineAfterUpdated.py
> [!NOTE]
> 使用 DeepSeek 编写

在原有 IL 更新后用来更新 Json 中 key 的行数

## UABEAJsonTextCollect.py
从用 UABEA Dump 出的 MonoBehaviour 的 Json 里提取/重封文本<br>
`lines` `lines2` 与 `phrases` 是对话组<br>
`m_Text` 是散的文本<br>
`left` `right` `up` `down` 是对话选项

## EnemyNameFileNameDiffCheck.py
在 IL 中检查有哪些 enemyName 与 fileName 不一致
