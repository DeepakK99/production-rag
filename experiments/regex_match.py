import re

chapter_regex = re.compile(r"^chapter\s+\d+", re.IGNORECASE)

test_strings = [
    "Chapter 12",
    "chapter 1",
    "Chapter 3: Indian Recipes",
    "See Chapter 12",
    "Chapter",
    "CHAPTER 12. DESSERTS AND OTHER GOODIES",
]

for s in test_strings:
    if chapter_regex.match(s):
        print(True, f"-> '{s}' matches!")
    else:
        print(False, f"-> '{s}' fails.")
