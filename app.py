from flask import Flask, render_template, request, jsonify
import ollama
import markdown 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "No message received"}), 400

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful and professional AI medical assistant. "
                        "Provide medically accurate, empathetic, and informative responses. "
                        "You can explain medical conditions, symptoms, treatments, and wellness tips, "
                        "but do not give direct diagnoses. Always recommend seeing a healthcare provider "
                        "for urgent or serious concerns."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        markdown_text = response['message']['content'].strip()
        html_response = markdown.markdown(markdown_text) 
        return jsonify({"response": html_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
