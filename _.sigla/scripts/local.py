import inquirer


def main(node):
    questions = [
        inquirer.Text("name", message="What's your name"),
        inquirer.Text("surname", message="What's your surname"),
    ]
    answers = inquirer.prompt(questions)
    return answers
