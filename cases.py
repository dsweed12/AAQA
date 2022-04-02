import pandas as pd
import re
import html


def is_already_added(section, xml_sections):
    for x in xml_sections:
        if x == section:
            return True
    return False


def add_cases(dataframe, section):
    cases = ""
    for dfrow in dataframe.itertuples():
        steps = ""
        if dfrow.Section is section:
            cases += "<case>"
            title = f"{dfrow.Title}"
            cases += f"<title>{html.escape(title)}</title>" \
                     "<custom>"
            if dfrow[6] == "write":
                cases += "<preconds>This test cannot be tested in the current test plan (will be marked " \
                         "&apos;Blocked&apos; on the test run</preconds>"

            # cases += "<steps_separated>"
            # steps = f"<step><content>{html.escape(f'{dfrow.Steps}')}"
            #
            # if f"{dfrow.Title}".__contains__("Verify related links work as expected"):
            #     print(steps)
            # not_only_content = re.search(r'(?i)expected result', steps)
            # if not_only_content:
            #     steps = re.sub(r"(?i)(expected result[:][\n]?)", '</content> <expected>', steps)
            #     steps = re.sub(r"(<expected> ?[\n]?.*\n?.*)", r'\1</expected><content>', steps)
            # if steps.endswith("<content>"):
            #     steps = steps[:len(steps) - 9]
            # else:
            #     if re.search(r"(<content>[.*\n?\n?.*])(?!</content>$)", steps):
            #         steps = re.sub(r"(<content>.*\n\n.*(?!\n))(?!</content>)$", r'\1</content><expected></expected>', steps)
            #     #else:
            #         re.sub(r"(<content> ?[\n\n ?.*]+)(?!</content>)", r'\1</content><expected></expected>', steps)
            #         #re.sub(r"(<content>( ?[[.+\n\n]|\n\n.+])*)(?!</content>)", r'\1</content><expected></expected>',
            #                #steps)
            #         # re.sub(r"(<content> ?\n\n.+)(?!</content>)", r'\1</content><expected></expected>', steps)
            # if steps.endswith("</content>"):
            #     steps = steps[:len(steps) - 10]
            #
            # steps += "</step>"
            # cases += steps
            # cases += "</steps_separated>" \
            cases +=         "</custom>" \
                     f"</case>"
    return cases


df = pd.read_csv('Automation Anywhere testing list.csv')

f = open("Automation Anywhere.xml", 'w')
f.write("<sections>")
# Define a list that will contain list of the sections of the te
sections = set()
sections_to_cases = {}
for index, row in df.iterrows():
    if row.Section not in sections:
        sections.add(row.Section)
        f.write("<section>"
                f"<name>{row.Section}</name>"
                "<cases>")
        cases = add_cases(df, row.Section)
        sections_to_cases[row.Section] = cases.count('<case>')
        f.write(cases)
        f.write("</cases>"
                "</section>")
f.write("</sections>")
print("file written successfully √\n")
print(f"Cases: {sum(sections_to_cases.values())}\nSections: {len(sections_to_cases.keys())}\n\n{sections_to_cases}")
f.close()
