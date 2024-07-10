from flask import Flask, request, render_template_string
from openai import OpenAI

client = OpenAI()


app = Flask(__name__)


# HTML-Vorlage für die Hauptseite
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chatbot mit OpenAI</title>
</head>
<body>
    <h1>Chatbot mit OpenAI GPT</h1>
    <form action="/" method="post">
      <textarea name="user_input" cols="40" rows="5" placeholder="Deine Frage..."></textarea><br>
      <input type="submit" value="Frage senden">
    </form>
    {% if answer %}
        <h2>Antwort:</h2>
        <p>{{ answer }}</p>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def chatbot():
    answer = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        answer = generate_response(user_input)
    return render_template_string(HTML_TEMPLATE, answer=answer)


def generate_response(user_input):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
