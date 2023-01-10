from flask import Blueprint, redirect, render_template, request, url_for
import random
import string


generator = Blueprint('generator', __name__)


@generator.route('/gen', methods=['GET'])
def index():
    password = []
    upper = string.ascii_uppercase
    letter = string.ascii_letters
    lower = string.ascii_lowercase
    num = string.digits
    symbols = string.punctuation
    charList = ''
    length = request.args.get('number')
    choice = request.args.getlist('type')
    p = " ".join(choice)
    user_password = ''
    if (p == "Digits"):
        charList += num
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Letters Uppercase"):
        charList += upper
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Letters Lowercase"):
        charList += lower
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Letters"):
        charList += letter
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Special Characters"):
        charList += symbols
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Uppercase"):
        charList += symbols
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Lowercase"):
        charList += symbols
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Digits Letters"):
        charList += num + letter
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Digits Letters Special Character"):
        charList += symbols + num + letter
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Digits Letters Special Character Uppercase"):
        charList += symbols + num + letter + upper
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    elif (p == "Digits Letters Special Character Uppercase Lowercase"):
        charList += symbols + num + letter + upper + lower
        for i in range(int(length)):
            randomChar = random.choice(charList)
            password.append(randomChar)
            user_password = "".join(password)
    else:
        if (p == "Letters Special Character"):
            charList += symbols + letter
            for i in range(int(length)):
                randomChar = random.choice(charList)
                password.append(randomChar)
                user_password = "".join(password)
        elif (p == "Letters Special Character Uppercase"):
            charList += symbols + letter + upper
            for i in range(int(length)):
                randomChar = random.choice(charList)
                password.append(randomChar)
                user_password = "".join(password)
        elif (p == "Letters Special Character Lowercase"):
            charList += symbols + letter + lower
            for i in range(int(length)):
                randomChar = random.choice(charList)
                password.append(randomChar)
                user_password = "".join(password)
        elif (p == "Letters Special Character Uppercase Lowercase"):
            charList += symbols + letter + upper + lower
            for i in range(int(length)):
                randomChar = random.choice(charList)
                password.append(randomChar)
                user_password = "".join(password)

        else:
            if (p == "Special Character Uppercase"):
                charList += symbols + upper
                for i in range(int(length)):
                    randomChar = random.choice(charList)
                    password.append(randomChar)
                    user_password = "".join(password)
            elif (p == "Special Character Lowercase"):
                charList += symbols + lower
                for i in range(int(length)):
                    randomChar = random.choice(charList)
                    password.append(randomChar)
                    user_password = "".join(password)
            elif (p == "Special Character Uppercase Lowercase"):
                charList += symbols + lower + upper
                for i in range(int(length)):
                    randomChar = random.choice(charList)
                    password.append(randomChar)
                    user_password = "".join(password)
            else:
                if (p == "Uppercase Lowercase"):
                    charList += lower + upper
                    for i in range(int(length)):
                        randomChar = random.choice(charList)
                        password.append(randomChar)
                        user_password = "".join(password)
                elif (p == "Letter Uppercase"):
                    charList += letter + upper
                    for i in range(int(length)):
                        randomChar = random.choice(charList)
                        password.append(randomChar)
                        user_password = "".join(password)

    return render_template('gen.html', password=password, length=length, choice=choice, user_password=user_password, p=p)
