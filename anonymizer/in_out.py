import os
from email import policy
from email.parser import BytesParser


def list_of_files(path):
    """Get all the eml files in the directory and put them in a list."""
    email_list = [f for f in os.listdir(path) if f.endswith(".eml")]
    return email_list


def get_text(name):
    with open(name, "rb") as fp:
        msg = BytesParser(policy=policy.default).parse(fp)
        if msg.get_body(preferencelist="plain") is None:
            print("ATTENTION ATTENTION ATTENTION")
            print("Could not parse email {}".format(name))
            print("ATTENTION ATTENTION ATTENTION")
            content = None
        else:
            content = msg.get_body(preferencelist="plain").get_content()
    return content


def delete_header(text):
    items_to_delete = [
        "Von:",
        "Gesendet:",
        "Betreff:",
        "An:",
        "Cc:",
        "Sujet :",
        "Date :",
        "De :",
        "Pour :",
        "Copie :",
        "Mailbeispiel",
        "Mailbeispil",
        "transféré",
        "Sent:",
        "https:",
        "Von meinem iPhone gesendet",
        "Anfang der weitergeleiteten",
    ]
    lines_to_delete = []
    text_out_list = text.splitlines()
    for index, line in enumerate(text_out_list):
        if any(i == "@" for i in line):
            # print("Deleting: found @: {}".format(line))
            lines_to_delete.append(index)
        # elif any(i == ">" for i in line):
        # lines_to_delete.append(index)
        # print("Deleting: found >: {}".format(line))
        elif any(i in line for i in items_to_delete):
            lines_to_delete.append(index)
            # print("Deleting {}".format(line))
    # check if any lines have been found
    if lines_to_delete:
        # delete lines
        for i in reversed(lines_to_delete):
            # print("xxxxx {}".format(text_out_list[i]))
            del text_out_list[i]
    # reduce whitespace not to confuse spacy
    # remove tabs and outer whitespace
    text_out_list = [line.replace("\t", " ").strip() for line in text_out_list]
    # remove hyphens - this is risky though -
    text_out_list = [line.replace("-", " ").strip() for line in text_out_list]
    text_out_list = [line.replace("_", " ").strip() for line in text_out_list]
    # reduce whitespace to one
    text_out_list = [" ".join(line.split()) for line in text_out_list]
    # delete empty lines
    text_out_list = [line for line in text_out_list if line]
    return " ".join(text_out_list)


def write_file(text, name):
    with open("{}.out".format(name), "w") as file:
        file.write(text)
