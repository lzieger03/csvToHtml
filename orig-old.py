import csv
from pathlib import Path
from pprint import pprint
from string import Template


class CSV:
    def read_CSV(csv_file):
        table = []
        rows = {}
        with open(csv_file) as file:
            reader = csv.reader(file, delimiter=";")
            first_row = next(reader)
            for row in reader:
                index = 0
                for column in row:
                    rows.update({first_row[index]: column})
                    index += 1
                table.append(dict(rows))
        return table

    def print_Table(table):
        pprint(table)


class TemplateToHtml:
    def convert(template_file, table):
        template = Template(Path(template_file).read_text())
        new_html = template.substitute(table)
        return new_html

    def write_new_html(new_html_path, converted):
        with open(new_html_path, "w") as file:
            file.write(converted)

    def convertMultiple(base_template_file, tableTMP, table):
        template = Template(Path(base_template_file).read_text())
        table_template = Template(Path(tableTMP).read_text())
        table_html = [table_template.substitute(row) for row in table]
        new_html = template.safe_substitute({"table": table_html})
        return new_html


csv = CSV.read_CSV("dta2.csv")
# CSV.print_Table(csv)

# converted = TemplateToHtml.convert("template.html", csv[0])
# new_html = TemplateToHtml.write_new_html("newHTML.html", converted)


converted2 = TemplateToHtml.convertMultiple(
    base_template_file="bt.html", tableTMP="bt-table.html", table=csv
)
new_html = TemplateToHtml.write_new_html("newHTML2.html", converted2)
