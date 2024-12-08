from flask import Flask, render_template, request

app = Flask(__name__)

# Load dictionary
def load_dictionary():
    filepath = "dico.txt"
    try:
        with open(filepath, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return []

dictionary = load_dictionary()

# Sequence Alignment Algorithm
def calculate_penalty(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i * 2  # Gap penalty
    for j in range(m + 1):
        dp[0][j] = j * 2  # Gap penalty

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = 0 if word1[i - 1] == word2[j - 1] else (
                1 if (word1[i - 1] in "aeiou" and word2[j - 1] in "aeiou") or 
                     (word1[i - 1] not in "aeiou" and word2[j - 1] not in "aeiou") 
                else 3
            )
            dp[i][j] = min(dp[i - 1][j - 1] + match,  # Match/mismatch
                           dp[i - 1][j] + 2,          # Gap in word2
                           dp[i][j - 1] + 2)          # Gap in word1

    return dp[n][m]

# Find top 10 suggestions with penalties
def get_suggestions(input_word):
    scores = [(word, calculate_penalty(input_word, word)) for word in dictionary]
    scores.sort(key=lambda x: x[1])  # Sort by penalty score
    return scores[:10]  # Return top 10 suggestions with their penalties

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    input_word = request.form.get('word')
    suggestions = get_suggestions(input_word)
    return render_template('index.html', word=input_word, suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
