from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Tu LexAI hai — India ka sabse best AI lawyer.
Tu sirf Indian law ke baare mein baat karta hai.
Tu Hindi aur English dono mein jawab deta hai.
Tu simple aur clear bhasha mein samjhata hai.
Har jawab mein:
1. Law/Section clearly batao
2. Kya legal hai kya illegal batao
3. Kaunse documents chahiye batao
4. Court procedure batao agar zarurat ho
Tu hamesha sahi aur accurate information deta hai."""

def ask_lexai(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    user_msg = request.form.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    answer = ask_lexai(user_msg)
    msg.body(answer)
    return str(resp)

@app.route('/test', methods=['GET'])
def test():
    answer = ask_lexai("IPC 302 kya hai? Short mein batao.")
    return Response(answer, mimetype='text/plain')

if __name__ == '__main__':
    print("LexAI start ho raha hai...")
    app.run(debug=True, port=5000)
