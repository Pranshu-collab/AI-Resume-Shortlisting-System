import time
import streamlit as st

from resume_parser import ResumeManager
from job_desc_parser import JobDescriptionManager
from scores_calculation import extract,exact_score,similarity_score,ownership_score,achievement_score

st.set_page_config(page_title="AI Resume & JD Parser", layout="wide")
st.title("AI Resume & Job Description Parser")
col1, col2 = st.columns(2)
with col1:
        st.subheader("Upload Resume")
        resume_file = st.file_uploader(
            "Upload Resume PDF",
            type="pdf",
            key="resume_uploader"
        )

with col2:
        st.subheader("Upload Job Description")
        jd_file = st.file_uploader(
            "Upload JD PDF",
            type="pdf",
            key="jd_uploader"
        )

process_btn = st.button("Process Files")

if process_btn:
        if not resume_file or not jd_file:
            st.error("Please upload both Resume and Job Description.")

        with st.spinner("Processing..."):
            start_time = time.time()

            resume_parser = ResumeManager(resume_file, extension=".pdf")
            resume_output = resume_parser.parse()

            jd_parser = JobDescriptionManager(jd_file, extension=".pdf")
            jd_output = jd_parser.parse()
            
            r_out,jd_out=extract(resume_output,jd_output)
            exact=exact_score(r_out,jd_out)
            similarity=similarity_score(r_out,jd_out)
            ownership=ownership_score(r_out)
            achievement=achievement_score(r_out)
            final_score=(
                0.4*exact+
                0.3*similarity+
                0.15*ownership+
                0.15*achievement
            )
            end_time = time.time()
            seconds = end_time - start_time
            m, s = divmod(seconds, 60)

        st.success("Processing Complete!")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Parsed Resume Output")
            st.json(resume_output)

        with col2:
            st.subheader("Parsed Job Description Output")
            st.json(jd_output)

        st.divider()
        st.subheader("Candidate Evaluation Scores")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Exact Match", f"{exact:.2f}")
        col2.metric("Semantic Similarity", f"{similarity:.2f}")
        col3.metric("Ownership Score", f"{ownership:.2f}")
        col4.metric("Achievement Score", f"{achievement:.2f}")

        st.divider()

        st.subheader("Final Match Score")
        st.metric("Overall Score", f"{final_score:.2f} / 100")

        st.progress(min(int(final_score), 100))

        st.write(f"Total time: {int(m)} min {int(s)} seconds")
