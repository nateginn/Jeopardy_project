import pandas as pd
import random
import numpy as np
import re
import difflib

# Read the CSV file
jeopardy_data = pd.read_csv('jeopardy.csv')
# Rename columns for ease of use
jeopardy_data.columns = ['show_number', 'air_date', 'round', 'category', 'value', 'question', 'answer']

# Select show_number/episode randomly
def select_random_episode(jeopardy_data):
    random_show_number = jeopardy_data['show_number'].sample().iloc[0]
    return jeopardy_data[jeopardy_data['show_number'] == random_show_number] 

# Identify the categories from Jeopardy! round from selected episode
def get_j_categories(jeopardy_data):
    jeopardy_categories = jeopardy_data[jeopardy_data['round'] == 'Jeopardy!']
    return jeopardy_categories['category'].unique()

# Initialize available questions
def initialize_available_questions(episode_data):
    available_questions = {}
    jeopardy_round_data = episode_data[episode_data['round'] == 'Jeopardy!']
    
    for category in jeopardy_round_data['category'].unique():
        values = jeopardy_round_data[jeopardy_round_data['category'] == category]['value'].unique().tolist()
        available_questions[category] = values
    
    return available_questions

# Function to check answer similarity
def is_answer_correct(contestant_answer, correct_answer):
    contestant_answer = contestant_answer.lower().strip()
    correct_answer = correct_answer.lower().strip()

    # Check for exact match
    if contestant_answer == correct_answer:
        return True

    # Check if correct answer is a substring of contestant's answer or vice versa
    if correct_answer in contestant_answer or contestant_answer in correct_answer:
        return True

    # Token matching
    correct_tokens = set(correct_answer.split())
    contestant_tokens = set(contestant_answer.split())
    if correct_tokens.issubset(contestant_tokens) or contestant_tokens.issubset(correct_tokens):
        return True

    # Use difflib to check similarity
    similarity_ratio = difflib.SequenceMatcher(None, contestant_answer, correct_answer).ratio()
    if similarity_ratio > 0.8:  # Adjust the threshold as needed
        return True

    return False

# Function to start the quiz
def start_quiz(jeopardy_data):
    episode = select_random_episode(jeopardy_data)
    available_questions = initialize_available_questions(episode)
    categories = list(available_questions.keys())
    contestant_score = 0
    
    print(f"Let's get started with the categories in the first round: {', '.join(categories)}")
    selected_category = input('Please select a category from the list: ').upper()
    
    while available_questions:
        if selected_category not in available_questions:
            selected_category = input(f"{selected_category} is not available. Please select a valid category: ").upper()
            continue
        
        values = available_questions[selected_category]
        print(f"Here are the available values for {selected_category}: {', '.join(values)}")
        select_a_value = input('Please select a value from the list: ')
        clean_value = re.sub(r'\D', '', select_a_value)
        value_int = int(clean_value)
        selected_value = f'${value_int}'
        
        if selected_value not in values:
            print(f"{selected_value} is not available. Please select a valid value.")
            continue
  
        # Retrieve and present the question based on selected category and value.
        question_row = episode[(episode['category'] == selected_category) & (episode['value'] == selected_value)].iloc[0]
        question = question_row['question']
        print(f"Your question is: {question}")
        answer = input('Who or what is: ')
        contestant_answer = answer.lower().strip()
        correct_answer = question_row['answer'].lower().strip()
    
        if is_answer_correct(contestant_answer, correct_answer):
            contestant_score += value_int
            print(f'Correct! You have earned {value_int}. Your total score is now {contestant_score}')
        else:
            contestant_score -= value_int
            print(f'Sorry, the correct answer is {correct_answer}. You have lost {value_int}. Your score is now {contestant_score}')
        
        # Update the available questions
        values.remove(selected_value)
        if not values:
            del available_questions[selected_category]
        
        if not available_questions:
            print("All questions have been answered. The game is over.")
            break

        print(f"Available categories: {', '.join(available_questions.keys())}")  # Reminder of available categories
        selected_category = input('Please select another category from the list: ').upper()

# Main program   
start_quiz_input = input('Welcome to Jeopardy! I am your host Ken. Would you like to play a full round of Jeopardy today? (yes/no): ')
if start_quiz_input.lower() == 'yes':
    start_quiz(jeopardy_data)
else:
    print("Have a wonderful day!")



    

    