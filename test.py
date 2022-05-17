import re

text = "{noun} of {verb} of {noun}"
regex = re.compile(r"(\{noun\})|(\{verb\})", re.A | re.I | re.M)
replacement_dict = {"{noun}": "Paris", "{verb}": "born"}
matcher = lambda x, d: re.subn(
    regex,
    lambda m: d[x[m.start() : m.end()]],
    x,
    re.I | re.M | re.A | re.M,
)[0]
print(matcher(text, replacement_dict))
