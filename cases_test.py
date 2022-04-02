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

xml_cases = "<sections>"
# Define a list that will contain lists of two values:
# 1. the sections of the test cases (such as "Login", "Registration"...) as strings
# 2. The index in 'xml_cases' where the last <case> was added after.
sections = []
for row in df.itertuples():
    if not is_already_added(row.Section, sections):
        xml_cases += "<section>" \
                     f"<name>{row.Section}</name>" \
                     "<cases>"
        sections.append([row.Section, len(xml_cases)])
        xml_cases += "</cases>" \
                     "</section>"

    i = len(xml_cases)
    xml_cases = f"{xml_cases[:find_index(sections, row.Section)]}" \
                f"<case>" \
                f"<title>{row.Title}</title>" \
                "</case>"\
                f"{xml_cases[find_index(sections, row.Section):]}"
    update_section_index(sections, row.Section, i)
xml_cases += "</sections>"

print(f"{xml_cases}\n\n**\nlength:{len(xml_cases)}\nNo. of cases ready: {xml_cases.count('<case>')}\n**")


