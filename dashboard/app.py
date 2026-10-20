import streamlit as st
import pickle
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="EduPrediction",
    page_icon="🎓",
    layout="centered"
)

# -------------------------
# LOAD MODEL
# -------------------------

model = pickle.load(
    open(
        "models/risk_model.pkl",
        "rb"
    )
)

# -------------------------
# BEAUTIFUL UI
# -------------------------

st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(
        135deg,
        #EEF4FF 0%,
        #FFFFFF 100%
    );
}

/* Headings */
.main-title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:#1E3A8A;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#475569;
}

.hero-card{
    background:white;
    padding:35px;
    border-radius:25px;
    box-shadow:
        0px 8px 25px rgba(0,0,0,0.08);
    margin-top:20px;
}

.result-card{
    background:white;
    padding:30px;
    border-radius:25px;
    box-shadow:
        0px 8px 25px rgba(0,0,0,0.08);
}

.stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border-radius:12px;
    height:55px;
    border:none;
    font-size:18px;
    font-weight:600;
}

.stButton>button:hover{
    background:#1D4ED8;
}

[data-testid="stProgressBar"]{
    padding-top:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATE
# -------------------------

if "step" not in st.session_state:
    st.session_state.step = 0

# -------------------------
# SCREEN 1
# -------------------------

if st.session_state.step == 0:

    st.markdown(
        '<div class="main-title">🎓 EduPrediction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI Student Risk Prediction System</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        """
        This system predicts whether a student is:

        ✅ Low Risk

        ⚠️ Medium Risk

        🚨 High Risk

        Click Start to begin.
        """
    )

    if st.button("🚀 Start Assessment"):
        st.session_state.step = 1
        st.rerun()

# -------------------------
# QUESTION 1
# -------------------------

elif st.session_state.step == 1:

    st.progress(10)

    st.header("Question 1")

    age = st.number_input(
        "How old is the student?",
        15,
        22
    )

    if st.button("Next"):
        st.session_state.age = age
        st.session_state.step = 2
        st.rerun()

# -------------------------
# QUESTION 2
# -------------------------

elif st.session_state.step == 2:

    st.progress(20)

    sex = st.radio(
        "What is the student's gender?",
        ["Female", "Male"]
    )

    if st.button("Next"):
        st.session_state.sex = sex
        st.session_state.step = 3
        st.rerun()

# -------------------------
# QUESTION 3
# -------------------------

elif st.session_state.step == 3:

    st.progress(30)

    study = st.radio(
        "How much time does the student study?",
        [
            "Less than 2 Hours",
            "2 to 5 Hours",
            "5 to 10 Hours",
            "More than 10 Hours"
        ]
    )

    if st.button("Next"):
        st.session_state.study = study
        st.session_state.step = 4
        st.rerun()

# -------------------------
# QUESTION 4
# -------------------------

elif st.session_state.step == 4:

    st.progress(40)

    failures = st.selectbox(
        "Previous Failures",
        [0,1,2,3]
    )

    if st.button("Next"):
        st.session_state.failures = failures
        st.session_state.step = 5
        st.rerun()

# -------------------------
# QUESTION 5
# -------------------------

elif st.session_state.step == 5:

    st.progress(50)

    absences = st.number_input(
        "Number of Absences",
        0,
        50
    )

    if st.button("Next"):
        st.session_state.absences = absences
        st.session_state.step = 6
        st.rerun()

# -------------------------
# QUESTION 6
# -------------------------

elif st.session_state.step == 6:

    st.progress(60)

    g1 = st.number_input(
        "First Grade (G1)",
        0,
        20
    )

    if st.button("Next"):
        st.session_state.g1 = g1
        st.session_state.step = 7
        st.rerun()

# -------------------------
# QUESTION 7
# -------------------------

elif st.session_state.step == 7:

    st.progress(70)

    g2 = st.number_input(
        "Second Grade (G2)",
        0,
        20
    )

    if st.button("Analyse Student"):
        st.session_state.g2 = g2
        st.session_state.step = 8
        st.rerun()

# -------------------------
# RESULT SCREEN
# -------------------------

elif st.session_state.step == 8:

    sex_value = 0 if st.session_state.sex == "Female" else 1

    study_value = {
        "Less than 2 Hours":1,
        "2 to 5 Hours":2,
        "5 to 10 Hours":3,
        "More than 10 Hours":4
    }[st.session_state.study]

    student_data = pd.DataFrame(
        [[
            st.session_state.age,
            sex_value,
            study_value,
            st.session_state.failures,
            st.session_state.absences,
            1,
            1,
            1,
            4,
            4,
            st.session_state.g1,
            st.session_state.g2
        ]],
        columns=[
            "age",
            "sex",
            "studytime",
            "failures",
            "absences",
            "schoolsup",
            "famsup",
            "internet",
            "Medu",
            "Fedu",
            "G1",
            "G2"
        ]
    )

    prediction = model.predict(student_data)

    st.balloons()

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True
    )

    if prediction[0] == "High Risk":

        st.error("🚨 HIGH RISK")

        st.write("""
        Recommendation

        • Increase study time

        • Improve attendance

        • Request academic support
        """)

    elif prediction[0] == "Medium Risk":

        st.warning("⚠️ MEDIUM RISK")

        st.write("""
        Recommendation

        • Monitor progress

        • Attend classes regularly
        """)

    else:

        st.success("✅ LOW RISK")

        st.write("""
        Recommendation

        • Continue current study habits

        • Maintain attendance

        • Keep academic performance high
        """)

    if st.button("🔄 New Assessment"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()