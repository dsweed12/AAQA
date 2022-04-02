import pandas as pd


def is_already_added(section, xml_sections):
    for x in xml_sections:
        if x[0] == section:
            return True
    return False


# find the index before adding a case
def find_index(xml_sections, section):
    for x in xml_sections:
        if x[0] == section:
            return x[1]


#
def update_section_index(xml_sections, section, i):
    for x in xml_sections:
        if x[0] == section:
            x[1] = i


df = pd.read_csv('tests.csv')
f = open("AAQA_TEST.xml", 'w')
f.write("<sections>")
# Define a list that will contain lists of two values:
# 1. the sections of the test cases (such as "Login", "Registration"...) as strings
# 2. The index in 'xml_cases' where the last <case> was added after.
sections = []
for index, row in df.iterrows():
    if not is_already_added(row.Section, sections):
        f.write(f"{f.read()} <section>"
                f"<name>{row.Section}</name>"
                "<cases>")
        sections.append([row.Section, len(f.read())])
        f.write(f"{f.read()}</cases>"
                "</section>")

    i = len(f.read())
    f.write(f"{f.read()[:find_index(sections, row.Section)]}"
            "<case>"
            f"<title>{row.Title}</title>"
            "</case>"
            f"{f.read()[find_index(sections, row.Section):]}")
    update_section_index(sections, row.Section, i)
f.write(f"{f.read()}</sections>")

print(f"{f.read()}\n\n**\nlength:{len(f.read())}\nNo. of cases ready: {f.read().count('<case>')}\n**")