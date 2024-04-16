import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

global df
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

elif chart_type == 'Employee-Positive-Sentiment':
    display_bar_chart(df)

