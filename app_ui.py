import streamlit as st
from graph_app import app

st.set_page_config(page_title="AI Research Agent", page_icon="🤖")

st.title("🤖 AI Autonomous Research Agent")
st.caption("Running on Llama 3.2 (1B) for maximum performance")

query = st.text_input("What would you like me to research?", placeholder="e.g. Compare Tesla vs Rivian")

if st.button("Run Research"):
    if query:
        with st.spinner("Agent is thinking... (Planning, Researching, and Analyzing)"):
            try:
                # Running the graph
                result = app.invoke({"query": query})
                
                st.subheader("Final Analysis")
                st.write(result.get("final", "No analysis was generated."))
                
                # Optional: Show the research steps
                with st.expander("View Research Process"):
                    st.markdown("**Research Plan:**")
                    st.info(result.get("plan"))
                    st.markdown("**Raw Research Data:**")
                    st.secondary(result.get("research"))
                    
            except Exception as e:
                st.error(f"Memory or Model Error: {str(e)}")
                st.warning("Tip: Try restarting the Ollama service to free up RAM.")
    else:
        st.warning("Please enter a query first!")