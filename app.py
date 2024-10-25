from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 用于模拟响应的简单函数
def get_response(user_input):
    # 这里可以实现与大模型的连接或其他逻辑
    return f"你说了：{user_input}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
