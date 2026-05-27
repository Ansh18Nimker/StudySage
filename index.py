from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.instance_path = "/tmp"

# ---------------- CONFIG ----------------
app.config['SECRET_KEY'] = 'studysage_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/studysage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- GOOGLE OAUTH ----------------
import os

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# ---------------- USER MODEL ----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


RESOURCES = [

    {
        "title": "Artificial Intelligence & Machine Learning",
        "description": "Learn AI, neural networks, deep learning, NLP, and modern ML algorithms with hands-on Python projects.",
        "article": "https://www.coursera.org/articles/artificial-intelligence",
        "course": "https://www.coursera.org/specializations/machine-learning-introduction",
        "youtube": "https://www.youtube.com/playlist?list=PLKnIA16_RmvY5eP91BGPa0vXUYmIdtfPQ",
        "type": "AI/ML",
        "source": "Coursera"
    },

    {
        "title": "Cybersecurity & Ethical Hacking",
        "description": "Master ethical hacking, penetration testing, network security, malware analysis, and cyber defense systems.",
        "article": "https://www.ibm.com/topics/cybersecurity",
        "course": "https://www.coursera.org/professional-certificates/google-cybersecurity",
        "youtube": "https://www.youtube.com/playlist?list=PLBf0hzazHTGOepimcP15eS6Y-aR4m6ql3",
        "type": "Cybersecurity",
        "source": "Google"
    },

    {
        "title": "Full Stack Web Development",
        "description": "Learn HTML, CSS, JavaScript, React, Node.js, Flask, APIs, and deployment for complete web apps.",
        "article": "https://developer.mozilla.org/en-US/docs/Learn",
        "course": "https://www.theodinproject.com/",
        "youtube": "https://www.youtube.com/playlist?list=PLjVLYmrlmjGcNM5WrJNgF4d2FA2bIWJ1x",
        "type": "Web Development",
        "source": "MDN"
    },

    {
        "title": "Data Science & Analytics",
        "description": "Work with datasets, visualization, Pandas, NumPy, statistics, and predictive modeling techniques.",
        "article": "https://www.ibm.com/topics/data-science",
        "course": "https://www.coursera.org/professional-certificates/ibm-data-science",
        "youtube": "https://www.youtube.com/playlist?list=PLZoTAELRMXVPS-dOaVbAux22vzqdgoGhG",
        "type": "Data Science",
        "source": "IBM"
    },

    {
        "title": "Cloud Computing & AWS",
        "description": "Learn cloud infrastructure, EC2, S3, deployment, virtualization, Docker, and scalable systems.",
        "article": "https://aws.amazon.com/what-is-cloud-computing/",
        "course": "https://www.coursera.org/learn/aws-fundamentals-going-cloud-native",
        "youtube": "https://www.youtube.com/playlist?list=PLBf0hzazHTGN31ZPTzBbk70bohTYT7HSm",
        "type": "Cloud Computing",
        "source": "AWS"
    },

    {
        "title": "DevOps & Docker",
        "description": "Understand CI/CD pipelines, Docker containers, Kubernetes, Jenkins, and deployment automation.",
        "article": "https://www.redhat.com/en/topics/devops",
        "course": "https://www.udemy.com/course/devops-training/",
        "youtube": "https://www.youtube.com/playlist?list=PLdpzxOOAlwvIKMhk8WhzN1pYoJ1YU8Csa",
        "type": "DevOps",
        "source": "RedHat"
    },

    {
        "title": "Blockchain Development",
        "description": "Build decentralized apps, understand Ethereum, smart contracts, Solidity, and Web3 ecosystems.",
        "article": "https://ethereum.org/en/developers/docs/",
        "course": "https://www.coursera.org/specializations/blockchain",
        "youtube": "https://www.youtube.com/playlist?list=PLS5SEs8ZftgXlCGbzWt2mRyErxp5yGJEN",
        "type": "Blockchain",
        "source": "Ethereum"
    },

    {
        "title": "Internet of Things (IoT)",
        "description": "Explore smart devices, Raspberry Pi, Arduino, sensors, MQTT protocols, and IoT architecture.",
        "article": "https://aws.amazon.com/iot/what-is-the-internet-of-things/",
        "course": "https://www.coursera.org/specializations/internet-of-things",
        "youtube": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRhqzJT87LsdQKYZBC93ezDo",
        "type": "IoT",
        "source": "AWS"
    },

    {
        "title": "Data Structures & Algorithms",
        "description": "Master arrays, linked lists, trees, graphs, recursion, DP, and coding interview preparation.",
        "article": "https://www.geeksforgeeks.org/data-structures/",
        "course": "https://www.coursera.org/specializations/data-structures-algorithms",
        "youtube": "https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA",
        "type": "DSA",
        "source": "GeeksforGeeks"
    },

    {
        "title": "Java Programming",
        "description": "Learn Java syntax, OOP, collections, multithreading, JDBC, and backend development concepts.",
        "article": "https://www.w3schools.com/java/",
        "course": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
        "youtube": "https://www.youtube.com/playlist?list=PLu0W_9lII9agS67Uits0UnJyrYiXhDS6q",
        "type": "Programming",
        "source": "Udemy"
    },

    {
        "title": "Python Programming",
        "description": "Master Python basics to advanced topics including automation, APIs, Flask, and data analysis.",
        "article": "https://docs.python.org/3/tutorial/",
        "course": "https://www.coursera.org/specializations/python",
        "youtube": "https://www.youtube.com/playlist?list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3",
        "type": "Programming",
        "source": "Python"
    },

    {
        "title": "Operating Systems",
        "description": "Understand processes, threads, scheduling, paging, deadlocks, memory management, and file systems.",
        "article": "https://www.geeksforgeeks.org/operating-systems/",
        "course": "https://www.udemy.com/course/operating-system-course/",
        "youtube": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRgLLlzdgiTUKULKJPYc0A4q",
        "type": "CS Core",
        "source": "GeeksforGeeks"
    },

    {
        "title": "Database Management Systems",
        "description": "Learn SQL, normalization, ER models, transactions, indexing, and relational databases.",
        "article": "https://www.geeksforgeeks.org/dbms/",
        "course": "https://www.coursera.org/learn/database-management",
        "youtube": "https://www.youtube.com/playlist?list=PL08903FB7ACA1C2FB",
        "type": "DBMS",
        "source": "Coursera"
    },

    {
        "title": "Computer Networks",
        "description": "Study TCP/IP, routing, OSI model, DNS, HTTP, and network security fundamentals.",
        "article": "https://www.cloudflare.com/learning/network-layer/what-is-a-computer-network/",
        "course": "https://www.coursera.org/learn/computer-networking",
        "youtube": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRjX6r2uhhlubuF5QextdCSM",
        "type": "Networking",
        "source": "Cloudflare"
    },

    {
        "title": "Mobile App Development",
        "description": "Build Android and cross-platform apps using Flutter, Firebase, APIs, and modern UI design.",
        "article": "https://developer.android.com/guide",
        "course": "https://www.udemy.com/course/flutter-bootcamp-with-dart/",
        "youtube": "https://www.youtube.com/playlist?list=PLjxrf2q8roU1ai7WYXQKa2w9BKW7XHgx2",
        "type": "Mobile Development",
        "source": "Android"
    },

    {
        "title": "Generative AI & LLMs",
        "description": "Learn ChatGPT, transformers, prompt engineering, fine-tuning, embeddings, and GenAI applications.",
        "article": "https://platform.openai.com/docs",
        "course": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "youtube": "https://www.youtube.com/playlist?list=PLZoTAELRMXVONhVxA0L06hio4S2_1S6Mc",
        "type": "Generative AI",
        "source": "OpenAI"
    }

]



# ---------------- ROUTES ----------------

# HOME
@app.route("/")
def index():
    return render_template("index.html")


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


# GOOGLE LOGIN
@app.route("/google-login")
def google_login():

    redirect_uri = url_for('auth_callback', _external=True)

    return google.authorize_redirect(redirect_uri)


# GOOGLE CALLBACK
@app.route("/auth/callback")
def auth_callback():

    token = google.authorize_access_token()

    user_info = token['userinfo']

    email = user_info['email']
    name = user_info['name']

    # Check existing user
    user = User.query.filter_by(email=email).first()

    # Create account if user doesn't exist
    if not user:

        random_password = bcrypt.generate_password_hash(
            "google_oauth_user"
        ).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password=random_password
        )

        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for("dashboard"))


# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ---------------- SEARCH ----------------

# SEARCH PAGE
@app.route("/search-page")
@login_required
def search_page():
    return render_template("search.html")


# SEARCH LOGIC
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    if request.method == "GET":
        return redirect(url_for("search_page"))

    query = request.form.get("query")

    if not query:
        return redirect(url_for("search_page"))

    query = query.lower()

    filtered_results = []

    for r in RESOURCES:

        if (
            query in r["title"].lower()
            or query in r["description"].lower()
        ):
            filtered_results.append(r)

    return render_template(
        "search-results.html",
        query=query,
        results=filtered_results
    )


# ---------------- OTHER PAGES ----------------

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")


@app.route("/bookmarks")
@login_required
def bookmarks():
    return render_template("bookmarks.html")


# LOGOUT
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("index"))


# ---------------- RUN ----------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)