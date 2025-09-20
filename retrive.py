import sqlite3
import csv
from lxml import html

source = '''
<div id="question-content">
    <span class="fmt-text">Až mě z toho <span class="nobreak">mraz<span class="gap short">_</span></span>.</span>
</div>
'''

tree = html.fromstring(source)
text = tree.xpath('//*[@id="question-content"]/span')[0]
op1 = tree.xpath('//*[@id="option0"]/span[@class="fmt-text"]')[0]
op2 = tree.xpath('//*[@id="option1"]')
print(text.text_content())
print(op1.text)
print(op2)