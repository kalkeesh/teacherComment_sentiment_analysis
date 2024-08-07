import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

global df

st.set_page_config(page_title="teach vibe", page_icon = "🚀", layout = "centered", initial_sidebar_state = "auto")

df = pd.read_csv("feedbackData.csv")
st.title('LECTURER SENTIMENT ANALYSIS')

def display_pie_chart(data):
    sentiment_counts = data['sentiment'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, hole=0.3)])
    fig.update_layout(title=f'Sentiment Analysis for {selected_empname}', height=550, width=700)
    st.plotly_chart(fig, use_container_width=True)

def display_bar_chart(data):
    emp_sentiment_counts = data[data['sentiment'] == 'positive']['empname'].value_counts(normalize=True).mul(100)
    colors = px.colors.qualitative.Set1  
    colors = colors * (len(emp_sentiment_counts) // len(colors)) + colors[:len(emp_sentiment_counts) % len(colors)] 
    fig = go.Figure(data=go.Bar(x=emp_sentiment_counts.index, 
                                 y=emp_sentiment_counts.values, 
                                 marker_color=colors))
    fig.update_layout(title='Positive Sentiment Percentage for All Employees', xaxis_title='Employee Name', yaxis_title='Positive Sentiment Percentage')
    st.plotly_chart(fig, use_container_width=True)

def display_sample_data(data):
    data = data.drop(columns=[ "question", "student_name", "campus_name", "course_name", "section_name"])
    with st.expander("Unique Comments by Sentiment", expanded=False):
        st.markdown("""
            <style>
            .scroll-table {
                max-height: auto;
                overflow: auto;
            }
            </style>
        """, unsafe_allow_html=True)
        st.write(data.sample(5).to_html(classes=['scroll-table'], escape=False), unsafe_allow_html=True)

def display_presentation():
    st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:800px;">
        <iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSS9ty8udh3_qGB5OEFKafsCXBfAQPdnsgj24j0yuktRIICd4VRECTQ6QSeKIoSzyNpztxc2as_F37A/embed?start=false&loop=false&delayms=3000" 
        width="1000" height="450"></iframe>
    </div>
    """, unsafe_allow_html=True)

# st.sidebar.title('ABOUT❓')
show_presentation = False
if st.sidebar.button("❓"):
    show_presentation = not show_presentation
if show_presentation:
    display_presentation()
else:
    chart_type = st.radio("Select Chart Type:", ('Comment-Analysis', 'Employee-Positive-Sentiment'))

    if chart_type == 'Comment-Analysis':
        st.sidebar.title('Filters')
        selected_empname = st.sidebar.selectbox('Select Employee Name:', df['empname'].unique())
        dept_code_options = df[df['empname'] == selected_empname]['department_code'].unique()
        selected_dept_code = st.sidebar.selectbox('Select Department Code:', dept_code_options)
        section_options = df[(df['empname'] == selected_empname) & (df['department_code'] == selected_dept_code)]['course_name'].unique()
        selected_course = st.sidebar.selectbox('Select section :', section_options)

        filtered_df = df[(df['empname'] == selected_empname) & 
                        (df['department_code'] == selected_dept_code) & 
                        (df['course_name'] == selected_course)]

        display_pie_chart(filtered_df)
        display_sample_data(filtered_df)
        st.subheader("About Creator")
        with st.expander("kalkeesh jami"):
            st.image("mepic.jpg", use_column_width=True)  
            st.write("""
            Hello! I'm KALKEESH JAMI #AKA Kalki, a passionate developer exploring the world of AI and programming.
            
            - I love building applications that make life easier.
            - I'm good at Python and data analysis.
            - Don't misunderstand me as a nerd; I'm socially adept too! 😄
            - Thank you for checking out my app!
            
            Do check out my [LinkedIn](https://www.linkedin.com/in/kalkeesh-jami-42891b260/) and [GitHub](https://github.com/kalkeesh/).
            """)

    elif chart_type == 'Employee-Positive-Sentiment':
        display_bar_chart(df)

