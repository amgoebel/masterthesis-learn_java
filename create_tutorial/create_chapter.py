import json

chapter_nr = 3
filename = "chapter" + str(chapter_nr) + ".html"

f_tutorial = open('tutorial.json','r')
data = json.load(f_tutorial)
f_tutorial.close()


f = open(filename,'w')
text = data['html_head']
text += data['tutorial'][chapter_nr - 1]['content']
text += data['tutorial'][chapter_nr - 1]['assignment']
text += data['html_tail']
f.write(text)
f.close()