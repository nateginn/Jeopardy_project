import pandas as pd

# Read the CSV file
jeopardy_data = pd.read_csv('jeopardy.csv')
# Rename columns for ease of use
jeopardy_data.columns = ['show_number', 'air_date', 'round', 'category', 'value', 'question', 'answer']

# Count total questions in the dataset
total_questions = len(jeopardy_data)
print(f'There are a total of \033[1m{total_questions}\033[0m questions in this dataset.')

# Get date range of the dataset
date_range_min = jeopardy_data['air_date'].min()
date_range_max = jeopardy_data['air_date'].max()
print(f'Earliest air date: {date_range_min} and most recent air date: {date_range_max}')

# Convert 'air_date' column to datetime format
jeopardy_data['air_date'] = pd.to_datetime(jeopardy_data['air_date'])

# Date ranges for different decades
start_80 = '1980-01-01'
end_80 = '1989-12-31'
start_90 = '1990-01-01'
end_90 = '1999-12-31'
start_00 = '2000-01-01'
end_00 = '2009-12-31'
start_10 = '2010-01-01'
end_10 = '2019-12-31'

# Function to convert value strings to float
def convert_value(val):
    if val in ['None', 'no value', '']:
        return 0.0
    else:
        try:
            return float(val.replace('$', '').replace(',', ''))
        except ValueError:
            return 0.0

# Apply the function to the value column to create val_float
jeopardy_data['val_float'] = jeopardy_data['value'].apply(convert_value)

# Input words for search
word1 = input('Search for the following word in Jeopardy Questions: ').lower()
word2 = input('Search for the additional word (may leave blank) in Jeopardy Questions: ').lower()

# Find questions containing the search words
if word2:
    find_words = jeopardy_data['question'].apply(lambda x: word1 in x.lower() and word2 in x.lower())
else:
    find_words = jeopardy_data['question'].apply(lambda x: word1 in x.lower())

# Print the number of questions that contain the search words
total_questions_with_words = find_words.sum()
print(f'There are a total of  \033[1m{total_questions_with_words}\033[0m questions with the word(s) you chose.')
percent_of_total = float(total_questions_with_words / total_questions)
find_words_questions = jeopardy_data[find_words]

# Calculate the average value for questions containing the search words
average_val_words = find_words_questions['val_float'].mean()
print(f'The average value for questions containing "{word1}" {"and " + word2 if word2 else ""} is: \033[1m ${average_val_words:.2f}\033[0m')

# Count the top answers for questions containing the search words
answer_counts = find_words_questions['answer'].value_counts()
print(f'Top 5 answers of all time: {answer_counts.head()}')
print(f'Questions with these key word(s) represent {percent_of_total:.5f}% of all questions in the database.')

# Filter data by decades
data_80s = (jeopardy_data['air_date'] >= start_80) & (jeopardy_data['air_date'] <= end_80)
data_90s = (jeopardy_data['air_date'] >= start_90) & (jeopardy_data['air_date'] <= end_90)
data_00s = (jeopardy_data['air_date'] >= start_00) & (jeopardy_data['air_date'] <= end_00)
data_10s = (jeopardy_data['air_date'] >= start_10) & (jeopardy_data['air_date'] <= end_10)

# Apply combined filters
combined_filter_80s = data_80s & find_words
answers_80 = jeopardy_data[combined_filter_80s]
answer_counts_80 = answers_80['answer'].value_counts()
print(f"Total answers in the 1980s: {answer_counts_80.sum()}")
print(f"Top 3 answers in the 1980s: {answer_counts_80.head(3)}")

combined_filter_90s = data_90s & find_words
answers_90 = jeopardy_data[combined_filter_90s]
answer_counts_90 = answers_90['answer'].value_counts()
print(f"Total answers in the 1990s: {answer_counts_90.sum()}")
print(f"Top 3 answers in the 1990s: {answer_counts_90.head(3)}")

combined_filter_00s = data_00s & find_words
answers_00 = jeopardy_data[combined_filter_00s]
answer_counts_00 = answers_00['answer'].value_counts()
print(f"Total answers in the 2000s: {answer_counts_00.sum()}")
print(f"Top 3 answers in the 2000s: {answer_counts_00.head(3)}")

combined_filter_10s = data_10s & find_words
answers_10 = jeopardy_data[combined_filter_10s]
answer_counts_10 = answers_10['answer'].value_counts()
print(f"Total answers in the 2010s: {answer_counts_10.sum()}")
print(f"Top 3 answers in the 2010s: {answer_counts_10.head(3)}")


