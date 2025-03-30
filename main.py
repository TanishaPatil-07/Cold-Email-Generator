import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Email Generator")

    # Allow multiple URLs separated by commas
    url_input = st.text_area("Enter URLs (comma-separated):",
                             value="https://www.amazon.jobs/en/jobs/2940549/sde-ii-alexa-customer-journeys, https://job-boards.greenhouse.io/razorpaysoftwareprivatelimited/jobs/4535839005")

    submit_button = st.button("Submit")

    if submit_button:
        urls = [url.strip() for url in url_input.split(",") if url.strip()]  # Split URLs and remove spaces

        if not urls:
            st.error("Please enter at least one valid URL.")
            return

        for url in urls:
            st.subheader(f"Cold Email for: {url}")  # Show which email belongs to which URL
            try:
                loader = WebBaseLoader([url])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language="markdown")  # Display email

            except Exception as e:
                st.error(f"An Error Occurred for {url}: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
