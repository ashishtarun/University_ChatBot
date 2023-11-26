from flask import Flask, render_template, request, jsonify
import openai
import json
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = 'API KEY'

# Load the dataset from a JSON file
with open('bot_dataset.json', 'r') as json_file:
    dataset = json.load(json_file)

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the user message from the POST request
    user_message = request.json.get("message")
    response = {"role": "assistant", "content": ""}

    # Iterate through the intents to find a match
    for intent in dataset["intents"]:
        for pattern in intent["patterns"]:
            similarity_score = fuzz.ratio(user_message.lower(), pattern.lower())
            if similarity_score > 60:
                print(similarity_score)
                response["content"] = intent["responses"][0]

                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": "Rephrase the sentence"+response["content"]}
                    ]
                )
                response = completion.choices[0].message
                response["content"] = response["content"].replace(". ", "<br>").replace(": ", "<br>").replace(", ", "<br>")
                print(response)
                return response
    print(similarity_score)


    if not response["content"]:
        # If no intent match is found, you can use OpenAI or provide a default response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        response = completion.choices[0].message

    # Return the response
    print(response)
    return response

if __name__ == '__main__':
    app.run()




