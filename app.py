from flask import Flask, render_template, request
import random

app = Flask(__name__)

total_chance = 3
win_count = 0
lose_count = 0

@app.route('/')
def index():
    return render_template('index.html')


def cash_memo(level_input, cash_deposite, win_count):
    message = ""
    if level_input == 1:
        if cash_deposite >= 100:
            if win_count > 0:
                message = f"You won the match! You got {cash_deposite * 2} Rs. Thank you!"
            else:
                message = f"Your current balance is {cash_deposite - 100} Rs."
        else:
            message = "Invalid input"
    
    elif level_input == 2:
        if cash_deposite >= 500:
            if win_count > 0:
                message = f"You won the match! You got {cash_deposite * 3} Rs. Thank you!"
            else:
                message = f"Your current balance is {cash_deposite - 500} Rs."
        else:
            message = "Invalid input"
    
    elif level_input == 3:
        if cash_deposite >= 1000:
            if win_count > 0:
                message = f"You won the match! You got {cash_deposite * 3} Rs. Thank you!"
            else:
                message = f"Your current balance is {cash_deposite - 1000} Rs."
        else:
            message = "Invalid input"
    
    return message


def gambling(level_input, user_choices):
    global win_count, lose_count
    win_count = 0
    lose_count = 0
    
    if level_input == 1:
        number_list = list(range(10))
        for choise in user_choices:
            if choise<0 and choise>9:
                return [f"number should be in the range of 0 to 9"]
    elif level_input == 2:
        number_list = list(range(51))
        for choise in user_choices:
            if choise<0 and choise>50:
                return [f"number should be in the range of 0 to 50"]
    else:
        number_list = list(range(101))
        for choise in user_choices:
            if choise<0 and choise>100:
                return [f"number should be in the range of 0 to 100"]

    results = []
    for i in range(total_chance):
        user_choice = user_choices[i]
        random_choice = random.choice(number_list)
        if user_choice == random_choice:
            results.append(f"You chose {user_choice} and computer chose {random_choice} - You won!")
            win_count += 1
        else:
            results.append(f"You chose {user_choice} and computer chose {random_choice} - You lost!")
            lose_count += 1
    return results


@app.route('/play', methods=['POST'])
def play():
    try:
        level_input = int(request.form.get('level_input', 0))
        cash_deposite = int(request.form.get('cash_deposite', 0))

        #give the check condition
        if level_input == 1 and cash_deposite < 100:
            return f"Money should be more than or equal to 100",400
        if level_input == 2 and cash_deposite < 500:
            return f"Money should be more than or equal to 500",400
        if level_input == 3 and cash_deposite < 1000:
            return f"Money should be more than or equal to 1000",400
        
        
        # Collect user input numbers
        user_choices = []
        for i in range(total_chance):
            choice = request.form.get(f'user_choice_{i}')
            if choice is None:
                return f"Missing input for choice {i+1}", 400
            user_choices.append(int(choice))
    
        results = gambling(level_input, user_choices)
        memo = cash_memo(level_input, cash_deposite, win_count)
        
        return render_template('result.html', results=results, memo=memo)
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400


if __name__ == '__main__':
    app.run(debug=True)
