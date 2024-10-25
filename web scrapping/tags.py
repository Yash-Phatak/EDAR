import requests
from bs4 import BeautifulSoup

with open("test.html", "r") as f:
    html_doc = f.read()

# converting to soup object
soup = BeautifulSoup(html_doc, 'html.parser')

# gives html content
print(soup.prettify())

# gives title
print(soup.title.string)

# get all div's
print(soup.findAll("div"))

# get div at specified index from start
print(soup.findAll("div")[0])

# get all links/a-anchor tags in website
for i in soup.findAll("a"):
    print(i.get("href"))

# get links with specific id
s = soup.find(id="link3")
print(s.get("href"))

# get div with class italic
print(soup.select("div.italic"))
# get span with id italic
print(soup.select("span#italic"))

# using for loop get all class with italic
# get parents or children of container class
for j in soup.find(class_="container").parents:
    print(j)
for j in soup.find(class_="container").children:
    print(j)

# modify tags
cont = soup.find(class_="container")
# changing class anme from div to span
cont.name = "span"
print(cont)

# add new tags and put to new html file
ulTag = soup.new_tag("ul")

# adding elements ot ul tag
liTag = soup.new_tag("li")
liTag.string = "Home"  # adding value to li tag
ulTag.append(liTag)

liTag = soup.new_tag("li")
liTag.string = "About"  # adding value to li tag
ulTag.append(liTag)

# adding ul tag to the soup(html file) to the starting (0th index)
soup.html.body.insert(0, ulTag)
# creating new file with modifications
with open("modified.html", "w") as f:
    f.write(str(soup))


# check if any attribute exists or not
cont1 = soup.find(class_="container")
print(cont1.has_attr("class"))
print(cont1.has_attr("contentEditable"))


# function to check if tag has class and not id
def has_class_but_not_id(tag):
    return tag.has_attr("class") and not tag.has_attr("id")


# print all whose class is set but not id
results = soup.findAll(has_class_but_not_id)
print(results)
