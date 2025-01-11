import streamlit as st

from crew import BaCrewConcept1
#from CustomVectorDBSource import CustomVectorDBSource

# Streamlit UI
st.title("Streamlit + CrewAI Integration")

# Initialize session state for conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display conversation
for message in st.session_state.conversation:
    st.chat_message(message["role"], message["content"])

# Input for the Crew
user_input = st.text_input("You:", placeholder="Enter your message here...")

#uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Submit button
if st.button("Send"):
    if user_input:
        # Add user message to conversation
        st.session_state.conversation.append({"role": "user", "content": user_input})

        file_path = "uploaded/temp.pdf"
        file_type = "pdf"
        with st.spinner("The Crew is working on your request..."):
            # if uploaded_file:
            #     # Save the uploaded file to a temporary location
            #     with open(file_path, "wb") as f:
            #         f.write(uploaded_file.getbuffer())

            #     #vector_db_source = CustomVectorDBSource()
            #     #initialize_before_crew(file_path, file_type)

            #     # Upload the file to the vector database source
            #     #vector_db_source.load("temp.pdf", "pdf")
            #     #vector_db_source.add(file_path, file_type)

            crew = BaCrewConcept1().crew()  # Initialize Crew
            #crew.llm_provider = 'openai/gpt-4o'

            # results = crew.kickoff(inputs={"topic": user_input,
                                        #    "file_path": file_path,
                                        #    "file_type": file_type})
            results = crew.kickoff(inputs={"topic": user_input})

            # Add Crew response to conversation
            st.session_state.conversation.append({"role": "crew", "content": "Crew has completed the tasks!"})
            for task_result in results:
                task_name, task_output = task_result  # Unpack the tuple
                st.session_state.conversation.append({"role": "crew", "content": f"**{task_name}**: {task_output}"})
    else:
        st.warning("Please enter a message to proceed.")