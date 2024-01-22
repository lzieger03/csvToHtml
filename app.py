from datetime import datetime
from backend import App

if __name__ == "__main__":
    # first datetime element to determine duration
    dt1 = datetime.now()

    app = App(
        csv_file_path="csv/data-test.csv", # Path to the .csv file
        html_template_path="templates/template-base.html", # Path to the .html Base Template
        output_path="output-html/converted.html", # Path to the wished output folder
    )
    app.make_converted() # Run conversion process 

    # second datetime element to determine duration
    dt2 = datetime.now()
    duration = dt2 - dt1
    print(f"Runtime: {duration.microseconds/1000}ms")

