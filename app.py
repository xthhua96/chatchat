from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

# 创建 Flask 应用实例
app = Flask(__name__)

# 设置密钥用于安全用途
app.config["SECRET_KEY"] = "secretkey"

# 配置数据库 URI，这里使用 SQLite 数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

# 创建 SQLAlchemy 实例
db = SQLAlchemy(app)

# 创建 Flask-Login 实例
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # 设置登录视图


# 创建用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# 用户加载回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 创建注册表单
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=150)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=150)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Register")

    # 验证用户名是否已存在
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


# 创建登录表单
class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=150)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=150)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


# 主页路由
@app.route("/")
def home():
    return render_template("index.html")


# 注册路由
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method="sha256"
        )  # 密码哈希
        new_user = User(
            username=form.username.data, password=hashed_password
        )  # 创建新用户
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))  # 重定向到登录页面
    return render_template("register.html", form=form)


# 登录路由
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):  # 验证密码
                login_user(user)  # 登录用户
                return redirect(url_for("dashboard"))  # 重定向到仪表板
    return render_template("login.html", form=form)


# 仪表板路由（需要登录）
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hello, {current_user.username}!"


# 注销路由
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()  # 注销用户
    return redirect(url_for("login"))  # 重定向到登录页面


# 聊天路由
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})


# 模拟响应函数
def get_response(user_input):
    # 这里可以实现与大模型的连接或其他逻辑
    return f"你说了：{user_input}"


# 主函数
if __name__ == "__main__":
    db.create_all()  # 创建数据库
    app.run(debug=True)
