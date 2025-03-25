#!/usr/bin/python3
import settings
import sys
import os
import re

def render_template(template, **kwargs):
    """
    Render a template with the given arguments.
    """
    with open(template, 'r') as file:
        content = file.read()
        for key, value in kwargs.items():
            content = content.replace('{{ ' + key + ' }}', value)
    return content

def render(output, **kwargs):
    """
    Render the output file with the given arguments.
    """
    with open(output, 'w') as file:
        file.write(render_template(settings.TEMPLATE, **kwargs))


def main():
    """
    Main function.
    """
    if len(sys.argv) != 2:
        print("Usage: python render.py <*.template>")
        sys.exit(1)
    if settings.name is None:
        print("Name does not exist")
        sys.exit(1)
    if settings.surname is None:
        print("Surname does not exist")
        sys.exit(1)
    if settings.age is None:
        print("Age does not exist")
        sys.exit(1)
    if settings.profession is None:
        print("Profession does not exist")
        sys.exit(1)
    if settings.title is None:
        print("Title does not exist")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print("The file does not exist")
        sys.exit(2)
    regex_verify = re.compile(".*\\.template$")
    print(path)
    if not regex_verify.match(path):
        print("The file is not a template")
        sys.exit(3)
    print("The file is a template")
    tmp_file  = open(path, "r")
    content = tmp_file.read()
    tmp_file.close()

    file  = content.format(name=settings.name, surname=settings.surname, age=settings.age, profession=settings.profession, title=settings.title)
    output = path.replace(".template", ".html")
    new_file = open(output, "w")
    new_file.write(file)
    new_file.close()

if __name__ == '__main__':
    main()
