import csv
from pathlib import Path
from string import Template


class CsvReader:
    """
    This class is responsible for reading CSV files.

    Attributes:
        csv_file_path (str): The path to the CSV file to read.

    Methods:
        read_csv(self) -> List[Dict[str, str]]:
            Reads a CSV file and returns its contents as a list of dictionaries.

            :return: A list of dictionaries representing the contents of the CSV file.

        get_columnTitles(self) -> List[str]:
            Returns the titles of the columns in the CSV file.

            :return: A list of strings representing the column titles.

        make_head(self) -> str:
            Creates an HTML head template for the CSV file.

            :return: The HTML head template as a string.

        make_content_template(self) -> str:
            Creates an HTML content template for the CSV file.

            :return: The HTML content template as a string.
    """

    def __init__(self, csv_file_path: str) -> None:
        """
        Constructor for the CsvReader class.

        :param csv_file_path: The path to the CSV file to read.
        :type csv_file_path: str
        """
        self.file_path = csv_file_path

    def read_csv(self) -> list[dict[str, str]]:
        """
        Reads a CSV file and returns its contents as a list of dictionaries.

        :return: A list of dictionaries representing the contents of the CSV file.
        :rtype: List[Dict[str, str]]

        Example:
            >>> csv_reader = CsvReader('example.csv')
            >>> csv_data = csv_reader.read_csv()
            >>> print(csv_data)
            [{'column1': 'value1', 'column2': 'value2'}, {'column1': 'value3', 'column2': 'value4'}]
        """
        table = []
        with open(self.file_path, newline="") as file:
            reader = csv.reader(file, delimiter=self.get_delimiter())
            first_row = next(reader)
            for row in reader:
                rows = dict(zip(first_row, row))
                table.append(rows)
        return table

    def get_columnTitles(self) -> list[str]:
        """
        Returns the titles of the columns in the CSV file.

        :return: A list of column titles.
        :rtype: List[str]

        Example:
            >>> csv_reader = CsvReader('example.csv')
            >>> column_titles = csv_reader.get_column_titles()
            >>> print(column_titles)
            ['column1', 'column2']
        """
        with open(self.file_path, newline="") as file:
            reader = csv.reader(file, delimiter=self.get_delimiter())
            return next(reader)

    def make_head(self) -> str:
        """
        Creates an HTML head template for the CSV file.

        :return: The path to the saved HTML head template.
        :rtype: str

        Example:
            >>> csv_reader = CsvReader('example.csv')
            >>> head_template_path = csv_reader.make_head()
            >>> print(head_template_path)
            templates/template-head.html
        """
        first_row = self.get_columnTitles()
        head_template = "<thead><tr>"
        for title in first_row:
            head_template += "<th>" + title + "</th>"
        with open("templates/template-head.html", "w") as file:
            file.write(head_template + "</tr></thead>")
        return "templates/template-head.html"

    def make_content_template(self) -> str:
        """
        Creates an HTML content template for the CSV file.

        :return: The path to the saved HTML content template.
        :rtype: str

        Example:
            >>> csv_reader = CsvReader('example.csv')
            >>> content_template_path = csv_reader.make_content_template()
            >>> print(content_template_path)
            templates/template-content.html
        """
        first_row = self.get_columnTitles()
        content_template = "<tbody><tr>"
        for title in first_row:
            content_template += "<td>$" + title + "</td>"
        with open("templates/template-content.html", "w") as file:
            file.write(content_template + "</tr></tbody>")
        return "templates/template-content.html"

    def get_filename(self) -> str:
        """
        Returns the name of the CSV file

        Returns:
            str: Name of the CSV file
        """
        return self.file_path.split("/")[-1]

    def get_delimiter(self) -> str:   
        """
        Gets the delimiter used in the CSV file at the specified file path.

        Returns:
            str: The delimiter used in the CSV file.
        """
        with open(self.file_path, "r") as file:
            sample = file.read(2048)  # read the first 2048 bytes of the file
            sniffed = csv.Sniffer().sniff(sample)
            return sniffed.delimiter



class TemplateToHtml:
    """
    This class is responsible for converting an HTML template to a new HTML file.

    Attributes:
        base_template_path (str): The path to the base HTML template file.
        csv_reader (CsvReader): An instance of the CsvReader class.

    Methods:
        convert(self) -> str:
            Converts an HTML template for multiple rows in a table.

            :return: The converted HTML as a string.

        write_new_html(self, new_html_path: str, converted: str):
            Writes the converted HTML to a new file.

            :param new_html_path: The path to the new HTML file.
            :param converted: The converted HTML as a string.
    """

    def __init__(self, base_template_path: str, csv_reader: CsvReader) -> None:
        """
        Initialize the TemplateToHtml class with the path to the base HTML template file and a CsvReader object.

        :param base_template_path: The path to the base HTML template file
        :param csv_reader: An instance of CsvReader
        """
        self.template_path = base_template_path
        self.csv_reader = csv_reader

    def convert(self) -> str:
        """
        Convert the base HTML template and CSV data to a new HTML string.

        :return: A string of the new HTML
        """
        base_template = Template(Path(self.template_path).read_text())
        head_template = [Path(self.csv_reader.make_head()).read_text()]
        table_template = Template(
            Path(self.csv_reader.make_content_template()).read_text()
        )
        table_html = [
            table_template.substitute(row) for row in self.csv_reader.read_csv()
        ]
        return base_template.safe_substitute(
            {
                "table_content": table_html,
                "table_head": list(head_template),
                "title": self.csv_reader.get_filename(),
            }
        )

    def write_new_html(self, new_html_path: str) -> None:
        """
        Write the new HTML to a file.

        :param new_html_path: The path to the new HTML file
        """
        with open(new_html_path, "w") as file:
            file.write(self.convert())


class App:
    """
    This class is responsible for creating an instance of the CsvReader class and
    converting an HTML template to a new HTML file.

    Attributes:
        csv_file_path (str): The path to the CSV file.
        html_template_path (str): The path to the base HTML template file.
        output_path (str): The path to the output HTML file.

    Methods:
        make_converted(self):
            Creates the converted HTML and writes it to a new file.
    """

    def __init__(
        self, csv_file_path: str, html_template_path: str, output_path: str
    ) -> None:
        """
        Initialize the App class with the file paths for the CSV file, HTML template,
        and output HTML file.

        :param csv_file_path: The path to the CSV file
        :param html_template_path: The path to the HTML template file
        :param output_path: The path to the output HTML file
        """
        self.csv_reader = CsvReader(csv_file_path)
        self.tmp_path = html_template_path
        self.output_path = output_path

    def make_converted(self) -> None:
        """
        Create the output HTML file from the CSV file and HTML template.
        """
        tth = TemplateToHtml(self.tmp_path, self.csv_reader)
        tth.write_new_html(new_html_path=self.output_path)


if __name__ == "__main__":
    print("Bitte führe die app.py aus!")