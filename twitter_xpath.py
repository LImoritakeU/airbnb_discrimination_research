'''
Twitter Advance Search Page
'''

# Search Form

ands_xpath = "//input[@name='ands']"
phrase_xpath = "//input[@name='phrase']"
ors_xpath = "//input[@name='ors']"
nots_xpath = "//input[@name='nots']"
tag_xpath = "//input[@name='tag']"
from_xpath = "//input[@name='from']"
to_xpath = "//input[@name='to']"
ref_xpath = "//input[@name='ref']"
near_xpath = "//input[@name='near']"
lang_xpath = "//select[@id='lang']"
since_xpath = "//input[@id='since']"  # time format yyyy/mm/dd
until_xpath = "//input[@id='until']"  # time format yyyy/mm/dd
button_xpath = "//div[@class='main']//form//button[@type='submit']"
