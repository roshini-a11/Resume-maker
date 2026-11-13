from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "resume_builder_secret"


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- LOGIN PAGE ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Temporary login
        if email and password:
            flash("Login Successful!", "success")
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# ---------------- REGISTER PAGE ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        password = request.form["password"]
        flash("Registration Successful!", "success")
            
        return redirect(url_for("login"))

        return render_template("register.html")


# ---------------- RESUME INPUT PAGE ----------------

@app.route("/resume")
def resume():
    flash("Resume Generated Successfully!", "success")

    return render_template("resume_form.html")


# ---------------- GENERATE RESUME ----------------

@app.route("/generate", methods=["POST"])
def generate():

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    linkedin = request.form["linkedin"]
    address = request.form["address"]
    about = request.form["about"]
    education = request.form["education"]
    skills = request.form["skills"]
    experience = request.form["experience"]
    projects = request.form["projects"]
    certificates = request.form["certificates"]
    declaration = request.form["declaration"]

    return render_template(
        "resume.html",
        name=name,
        phone=phone,
        email=email,
        linkedin=linkedin,
        address=address,
        about=about,
        education=education,
        skills=skills,
        experience=experience,
        projects=projects,
        certificates=certificates,
        declaration=declaration
    )


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")

# ---------------- ATS CHECKER ----------------


@app.route("/ats", methods=["GET", "POST"])
def ats():

    if request.method == "POST":

        resume_skills = request.form.get(
            "resume_skills", ""
        )

        job_skills = request.form.get(
            "job_skills", ""
        )

        # Convert both inputs to lowercase
        resume_skills = resume_skills.lower()
        job_skills = job_skills.lower()

        # Split skills using commas
        resume_list = [
            skill.strip()
            for skill in resume_skills.split(",")
            if skill.strip()
        ]

        job_list = [
            skill.strip()
            for skill in job_skills.split(",")
            if skill.strip()
        ]

        # Find matching skills
        matching_skills = []

        for skill in job_list:

            if skill in resume_list:

                matching_skills.append(skill)

        # Calculate ATS score
        if len(job_list) > 0:

            ats_score = (
                len(matching_skills)
                / len(job_list)
            ) * 100

        else:

            ats_score = 0

        return render_template(
            "ats_result.html",
            ats_score=round(ats_score, 2),
            matching_skills=matching_skills
        )

    return render_template("ats.html")


# ---------------- COVER LETTER ----------------

@app.route("/coverletter", methods=["GET", "POST"])
def coverletter():

    if request.method == "POST":

        name = request.form.get("name", "")
        job_role = request.form.get("job_role", "")
        company = request.form.get("company", "")
        skills = request.form.get("skills", "")

        return render_template(
            "coverletter_result.html",
            name=name,
            job_role=job_role,
            company=company,
            skills=skills
        )

    return render_template("coverletter.html")


# ---------------- SAVED RESUME DATA ----------------

resumes = [
    {
        "id": 1,
        "name": "Roshini",
        "skills": "Python,Java,C,C++",
        "experience": "Fresher",
        "projects": "AI Resume Maker"
    }
]


# ---------------- SAVED RESUMES ----------------

@app.route("/saved")
def saved_resume():

    return render_template(
        "saved_resume.html",
        resumes=resumes
    )


# ---------------- EDIT RESUME ----------------

@app.route("/edit/<int:resume_id>", methods=["GET", "POST"])
def edit_resume(resume_id):

    resume = next(
        (
            item for item in resumes
            if item["id"] == resume_id
        ),
        None
    )

    if resume is None:
        return "Resume not found"

    if request.method == "POST":

        resume["name"] = request.form["name"]
        resume["skills"] = request.form["skills"]
        resume["experience"] = request.form["experience"]
        resume["projects"] = request.form["projects"]

        return redirect(
            url_for("saved_resume")
        )

    return render_template(
        "edit_resume.html",
        resume=resume
    )


# ---------------- DELETE RESUME ----------------

@app.route("/delete/<int:resume_id>")
def delete_resume(resume_id):

    global resumes

    resumes = [
        resume
        for resume in resumes
        if resume["id"] != resume_id
    ]

    return redirect(
        url_for("saved_resume")
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    return redirect(
        url_for("login")
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)