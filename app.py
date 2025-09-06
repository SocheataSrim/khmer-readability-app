import streamlit as st
import pandas as pd
import time
from datetime import datetime
import base64
import os

st.set_page_config(page_title="Readability Survey", layout="centered")

# ---------------------------
# Initialize session state
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 0

# ---------------------------
# Passages
# ---------------------------
plain_text = """ប្រាសាទព្រះវិហារ ជាប្រាសាទដ៏ពិសិដ្ឋរបស់កម្ពុជាមានទីតាំងលាតសន្ធឹងនៅលើខ្ពង់រាបនៃជួរភ្នំដងរែក 
ដែលមានរយៈកម្ពស់ ៦២៥ម៉ែត្រ ធៀបនឹងកម្ពស់ទឹកសមុទ្រ និងមានផ្ទៃក្រឡា២៨២៨.៩ហិកតា ស្ថិតក្នុងស្រុកជាំក្សាន្ត ខេត្តព្រះវិហារ ។ 
ប្រាសាទដ៏ចំណាស់មួយនេះ បានចាប់ផ្តើមកសាងក្នុង រជ្ជកាលព្រះបាទយសោវរ្ម័នទី១ (៨៨៩-៩១០គ.ស) 
និងបញ្ចប់ក្នុងរជ្ជកាលព្រះបាទសូរ្យវរ្ម័នទី២ (១១១៣-១១៥០គ.ស) ដើម្បីឧទ្ទិសដល់អាទិទេព ព្រះឥសូរក្នុងសាសនាហិណ្ឌូ 
ក្នុងទម្រង់ជាទេពភ្នំសិខរេស្វរ និងភដ្រេស្វរ។ 
ប្រាសាទព្រះវិហារត្រូវបានពិភពលោកទទួលស្គាល់ថាស្ថិតក្នុងបូរណភាពដែនដីនៃព្រះរាជាណាចក្រកម្ពុជាយ៉ាងពិតប្រាកដ​ 
ក្រោយតុលារការយុត្តិធម៌អន្ដរជាតិ បានប្រកាសសាលក្រមជាផ្លូវការនៅថ្ងៃទី១៥ ខែមិថុនា ឆ្នាំ១៩៦២ 
ក្រោមព្រះរាជបូជនីយកិច្ចដ៏ឧត្តុងឧត្តមរបស់ព្រះបរមរតនកោដ្ឋ នរោត្តម សីហនុ។ 
លើសពីនោះថែមទៀត កាលនៅថ្ងៃទី០៧​ ខែកក្កដា​ ឆ្នាំ២០០៨ អង្គការយូណេស្កូ បានសម្រេចដាក់ប្រាសាទព្រះវិហារក្នុងបញ្ជីសម្បត្តិបេតិកភណ្ឌនៃមនុស្សជាតិ 
ក្នុងកិច្ចប្រជុំលើកទី៣២ នៅទីក្រុងកេបិចប្រទេសកាណាដា។ 
ដែលជាភាពជោគជ័យ​និងមោទកភាពសម្រាប់កូនខ្មែរគ្រប់ៗរូបចងចាំមិនអាចបំភ្លេចបាន​​ ក្រោមការដឹកនាំរបស់សម្តេចតេជោ ហ៊ុន សែន 
អតីតនាយករដ្ឋមន្ត្រី និងបច្ចុប្បន្នជាប្រធានព្រឹទ្ធសភាកម្ពុជា។"""

styled_text = """ចំណុចសំខាន់ៗទាក់ទងនឹងប្រាសាទអង្គរវត្ត៖  
**១. ប្រាសាទអង្គរវត្ត** ចូលជាសម្បត្តិបេតិកភណ្ឌពិភពលោកនៅថ្ងៃទី **១៤ ខែធ្នូ ១៩៩២** នាទីក្រុងសាន់តាហ្វេ សហរដ្ឋអាមេរិក។  
**២. រៀងរាល់ថ្ងៃទី ២១ ដល់ ២២ ខែមិនា និង ថ្ងៃទី ២២ ដល់ ២៣ ខែកញ្ញា** គឺព្រះអាទិត្យរះ និងលិចចំកណ្ដាលកំពូល **ប្រាសាទអង្គរវត្ត** ដែលចែករយៈពេលយប់ និងថ្ងៃស្មើគ្នា(សមរាត្រី)។  
**៣. ប្រាសាទ** ប្រើប្រាស់ថ្មក្នុងការសាងសង់ប្រមាណ **១០ លានតោន**។  
**៤. ប្រាសាទ** ប្រើកម្លាំងពលករសាងសង់ **១០ ម៉ឺននាក់** និងសត្វដំរីជាង **៦,០០០ ក្បាល**។  
**៥. ប្រាសាទ** មានផ្ទៃក្រឡាប្រមាណ **២០០ ហិចតា**។  
**៦. កម្ពស់របស់ប្រាសាទអង្គរវត្ត** គឺ **៦៥ ម៉ែត្រ**។  
**៧. កំពូលប្រាសាទអង្គរវត្ត** មានចំនួន **៥** និងបែរមុខទៅទិសខាងលិច។  
**៨. ប្រាសាទ** មានទីតាំងស្ថិតនៅខាងជើងនៃក្រុងសៀមរាប ខេត្តសៀមរាប ដែលមានចម្ងាយ **៧ គីឡូម៉ែត្រ** ពីទីរួមខេត្តសៀមរាប។  
**៩. ឈ្មោះមួយទៀត** របស់ប្រាសាទអង្គរវត្តគឺ **ប្រាសាទអង្គរតូច**។  
**១០. ប្រាសាទអង្គរវត្ត** មានឈ្មោះដើមថា **បរមវិស្ណុលោក**។  
**១១. ប្រាសាទ** តំណាងអោយព្រះសុមេរុ។  
**១២. គេសាងសង់ដើម្បីឧទ្ទិសថ្វាយ** ព្រះវិស្ណុក្នុងព្រហ្មញ្ញសាសនា។  
**១៣. ប្រាសាទអង្គរវត្ត** សាងសង់ដោយ **ព្រះបាទសូរ្យវរ្ម័នទី២** នៅសវទី **១២**។"""

# ---------------------------
# Quiz questions (your version)
# ---------------------------
plain_quiz = [
    {"q": "តើប្រាសាទនេះចាប់ផ្ដើមកសាងដោយស្ដេចអង្គណា?",
     "options": ["ព្រះបាទជ័យវរ្ម័នទី៧", "ព្រះបាទជ័យវរ្ម័នទី២", "ព្រះបាទសូរ្យវរ្ម័នទី២", "ព្រះបាទយសោវរ្ម័នទី១"],
     "answer": "ព្រះបាទយសោវរ្ម័នទី១"},
    {"q": "តើប្រាសាទនេះឧទ្ទិសដល់អទិទេពណា?",
     "options": ["ព្រះឥសូរ", "ព្រះព្រហ្ម", "ព្រះវិស្ណុ", "ព្រះពុទ្ធ"],
     "answer": "ព្រះឥសូរ"},
    {"q": "តើប្រាសាទនេះចូលក្នុងបញ្ជីបេតិកភណ្ឌពិភពលោកនៅឆ្នាំណា?",
     "options": ["៧ កក្កដា ២០០៨", "១៥ មិថុនា ១៩៦២", "៧ សីហា ២០០៨", "១៥ កក្កដា ១៩៦២"],
     "answer": "៧ កក្កដា ២០០៨"},
    {"q": "តើប្រាសាទនេះចូលក្នុងបញ្ជីបេតិកភណ្ឌនៅទីក្រុងណា?",
     "options": ["ញូវយ៉ក", "សាន់តាហ្វេ", "ហ្សឺណេវ", "កេបិច"],
     "answer": "កេបិច"},
    {"q": "តើរជ្ជកាលរបស់ព្រះបាទសូរ្យវរ្ម័នទី២នៅចន្លោះពីឆ្នាំណាដល់ឆ្នាំណា?",
     "options": ["1100-1130", "1130-1150", "1113-1150", "1200-1300"],
     "answer": "1113-1150"}
]

styled_quiz = [
    {"q": "តើប្រាសាទនេះចាប់ផ្ដើមកសាងដោយស្ដេចអង្គណា?",
     "options": ["ព្រះបាទជ័យវរ្ម័នទី៧", "ព្រះបាទជ័យវរ្ម័នទី២", "ព្រះបាទសូរ្យវរ្ម័នទី២", "ព្រះបាទយសោវរ្ម័នទី១"],
     "answer": "ព្រះបាទសូរ្យវរ្ម័នទី២"},
    {"q": "តើប្រាសាទនេះឧទ្ទិសដល់អទិទេពណា?",
     "options": ["ព្រះឥសូរ", "ព្រះព្រហ្ម", "ព្រះវិស្ណុ", "ព្រះពុទ្ធ"],
     "answer": "ព្រះវិស្ណុ"},
    {"q": "តើប្រាសាទនេះចូលក្នុងបញ្ជីបេតិកភណ្ឌពិភពលោកនៅឆ្នាំណា?",
     "options": ["៧ កក្កដា ២០០៨", "១៥ មិថុនា ១៩៦២", "១៥ ធ្នូ ១៩៩២", "១៤ ធ្នូ ១៩៩២"],
     "answer": "១៤ ធ្នូ ១៩៩២"},
    {"q": "តើប្រាសាទនេះចូលក្នុងបញ្ជីបេតិកភណ្ឌនៅទីក្រុងណា?",
     "options": ["ញូវយ៉ក", "សាន់តាហ្វេ", "ហ្សឺណេវ", "កេបិច"],
     "answer": "សាន់តាហ្វេ"},
    {"q": "សមរាត្រីនៅខែណា?",
     "options": ["មិនា និង កញ្ញា", "ឧសភា និង កញ្ញា", "កុម្ភៈ និង សីហា", "តុលា និង ធ្នូ"],
     "answer": "មិនា និង កញ្ញា"},
    {"q": "តើការសាងសង់បានប្រើប្រាស់ដំរីប៉ុន្មានក្បាល?",
     "options": ["៦០០០", "៣០០០", "១៥០០", "៥០០០"],
     "answer": "៦០០០"},
    {"q": "ឈ្មោះដើមរបស់ប្រាសាទ?",
     "options": ["បុទុមគិរី", "បរមវិស្ណុលោក", "អង្គរធំ", "បរមអង្គរ"],
     "answer": "បរមវិស្ណុលោក"}
]


# ---------------------------
# Timer function
# ---------------------------
def run_timer(seconds):
    st.session_state.timer_start = time.time()
    placeholder = st.empty()
    for i in range(seconds, -1, -1):
        mins, secs = divmod(i, 60)
        placeholder.markdown(f"⏱ Time Remaining: {mins:02d}:{secs:02d}")
        time.sleep(1)
    st.session_state.step += 1
    st.rerun()

# ---------------------------
# Step 0: Reader info
# ---------------------------
if st.session_state.step == 0:
    st.title("Readability Survey")
    st.write("សូមបំពេញព័ត៌មានផ្ទាល់ខ្លួន")
    gender = st.radio("ភេទ", ["ប្រុស", "ស្រី", "ផ្សេងទៀត"])
    age = st.number_input("អាយុ", 10, 100, 18)
    habit = st.selectbox("អត្រាការអាន", ["រាល់ថ្ងៃ", "ម្តងម្កាល", "កម្រណាស់", "មិនអាន"])
    if st.button("ចាប់ផ្តើម"):
        st.session_state.answers["gender"] = gender
        st.session_state.answers["age"] = age
        st.session_state.answers["habit"] = habit
        st.session_state.step = 1
        st.rerun()

# ---------------------------
# Step 1: Plain text reading
# ---------------------------
elif st.session_state.step == 1:
    st.header("អត្ថបទទី១ (Plain Text)")
    st.text_area("អានអត្ថបទនេះ", plain_text, height=250)
    if st.button("Start Reading"):
        run_timer(70)  # 1 min 10 sec

# ---------------------------
# Step 2: Plain text quiz
# ---------------------------
elif st.session_state.step == 2:
    st.header("Quiz for Plain Text")
    answers = {}
    for i, q in enumerate(plain_quiz):
        answers[i] = st.radio(q["q"], q["options"], key=f"plain_{i}")
    if st.button("Submit Quiz"):
        st.session_state.answers["plain_quiz"] = answers
        st.session_state.step = 3
        st.rerun()

# ---------------------------
# Step 3: Styled text reading
# ---------------------------
elif st.session_state.step == 3:
    st.header("អត្ថបទទី២ (Styled Text)")
    st.markdown(styled_text)
    if st.button("Start Reading"):
        run_timer(70)

# ---------------------------
# Step 4: Styled text quiz
# ---------------------------
elif st.session_state.step == 4:
    st.header("Quiz for Styled Text")
    answers = {}
    for i, q in enumerate(styled_quiz):
        answers[i] = st.radio(q["q"], q["options"], key=f"styled_{i}")
    if st.button("Submit Quiz"):
        st.session_state.answers["styled_quiz"] = answers
        st.session_state.step = 5
        st.rerun()

# ---------------------------
# Step 5: Preference & Results
# ---------------------------
elif st.session_state.step == 5:
    st.header("សូមជ្រើសរើសអត្ថបទដែលអ្នកយល់បានលឿនជាង")
    choice = st.radio("", ["Plain Text", "Styled Text"])
    if st.button("Finish Survey"):
        st.session_state.answers["preference"] = choice

        # Calculate scores
        score_plain = 0
        for i, q in enumerate(plain_quiz):
            if st.session_state.answers["plain_quiz"][i] == q["answer"]:
                score_plain += 1
        score_styled = 0
        for i, q in enumerate(styled_quiz):
            if st.session_state.answers["styled_quiz"][i] == q["answer"]:
                score_styled += 1
        st.session_state.answers["score_plain"] = score_plain
        st.session_state.answers["score_styled"] = score_styled
        st.session_state.answers["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to CSV
        df = pd.DataFrame([st.session_state.answers])
        if os.path.exists("results.csv"):
            df.to_csv("results.csv", mode="a", header=False, index=False, encoding="utf-8-sig")
        else:
            df.to_csv("results.csv", index=False, encoding="utf-8-sig")

        # Show results
        st.success("✅ សូមអរគុណចំពោះការចូលរួម!")
        st.subheader("Correct Answers")
        for q in plain_quiz + styled_quiz:
            st.write(f"{q['q']}: ✅ {q['answer']}")
        st.subheader("Your Scores")
        st.write(f"Plain Text Score: {score_plain}/{len(plain_quiz)}")
        st.write(f"Styled Text Score: {score_styled}/{len(styled_quiz)}")

# ---------------------------
# Download CSV
# ---------------------------
if os.path.exists("results.csv"):
    st.subheader("📥 Download All Participants' Results")
    with open("results.csv", "r", encoding="utf-8") as f:
        csv = f.read()
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="results.csv">Download Results CSV</a>',
        unsafe_allow_html=True
    )
