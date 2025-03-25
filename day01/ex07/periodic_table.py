""" 
• Each element must be in a ’box’ of a HTML table.
• The name of an element must be in a level 4 title tag.
• The attributes of an element must appear as a list. The lists must state at least
the atomic numbers, the symbol and the atomic mass.
• You must at least abide to the layout of the Mendeleiev’s Table as it appears on
Google. There must be empty boxes where there should, as well as carriage return
where it should.
Your program must create the result file periodic_table.html. Of course, this HTML
file must be readable in any browser and must be W3C valid.
You’re free to design you program as you like. Don’t hesitate to fragment your code
in specific functionalities you may reuse. You can customize the tags with a CSS "inline"
style to make your turn-in prettier (think of the table’s borders’ colors). You can even
13

generate periodic_table.css file if you prefer.
Here is an excerpt of an output example that will give you an idea:
[...]
<table>
<tr>
<td style="border: 1px solid black; padding:10px">
<h4>Hydrogen</h4>
<ul>
<li>No 42</li>
<li>H</li>
<li>1.00794</li>
<li>1 electron</li>
<ul>
</td>
[...]

"""

import sys

def parse_elements(file_path):
    elements = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split(", ")
            name = parts[0].split(" = ")[0]
            position = int(parts[0].split(":")[1])
            number = int(parts[1].split(":")[1])
            symbol = parts[2].split(": ")[1]
            molar = float(parts[3].split(":")[1])
            electrons = parts[4].split(":")[1].strip()
            elements.append({
                "name": name,
                "position": position,
                "number": number,
                "symbol": symbol,
                "molar": molar,
                "electrons": electrons
            })
    return elements

def generate_html(elements):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Periodic Table</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            td { border: 1px solid black; padding: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <table>
    """
    
    max_columns = 17  
    current_position = 0  
    first_in_row = True  

    for element in elements:        
        if element["position"] == 0:
            if not first_in_row:  
                while current_position <= max_columns :  
                    html_content += "<td></td>"
                    current_position += 1
                html_content += "</tr>"
            
            html_content += "<tr>"  
            current_position = 0  
            first_in_row = False  
        
        while current_position < element["position"]:
            html_content += "<td></td>"
            current_position += 1

        html_content += f"""
        <td>
            <h4>{element['name']}</h4>
            <ul>
                <li>No {element['number']}</li>
                <li>{element['symbol']}</li>
                <li>{element['molar']}</li>
                <li>{element['electrons']} electron(s)</li>
            </ul>
        </td>
        """
        current_position += 1

    
    while current_position <= max_columns:
        html_content += "<td></td>"
        current_position += 1
    html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """
    
    return html_content


def periodic_table():
    elements = parse_elements("periodic_table.txt")
    html_content = generate_html(elements)
    with open("periodic_table.html", "tw") as file:
        file.write(html_content)

if __name__ == "__main__":
    periodic_table()