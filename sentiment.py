import pandas as pd
import pymongo
from textblob import TextBlob
# import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["feedback"]
collection = db["comments"]

question_list = []
student_name_list = []
section_name_list = []
course_name_list = []
campus_name_list = []
department_code_list = []
empname_list = []
comment_list = [] 
sentiment_list = []

for doc in collection.find():
    feedback_data = doc.get("feedbackdata", [])
    for feedback_obj in feedback_data:
        question = feedback_obj.get("question", "")
        student_name = feedback_obj.get("student_name", "")
        section_name = feedback_obj.get("section_name", "")
        course_name = feedback_obj.get("course_name", "")
        campus_name = feedback_obj.get("campus_name", "")
        department_code = feedback_obj.get("departmentcode", "")
        empname = feedback_obj.get("empname", "")
        comment = feedback_obj.get("comment", "")  # Extract comment
        
        blob = TextBlob(comment)
        sentiment_polarity = blob.sentiment.polarity
        if sentiment_polarity > 0:
            sentiment_label = "positive"
        elif sentiment_polarity < 0:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        question_list.append(question)
        student_name_list.append(student_name)
        section_name_list.append(section_name)
        course_name_list.append(course_name)
        campus_name_list.append(campus_name)
        department_code_list.append(department_code)
        empname_list.append(empname)
        comment_list.append(comment)  
        sentiment_list.append(sentiment_label) 

data = {
    "question": question_list,
    "student_name": student_name_list,
    "section_name": section_name_list,
    "course_name": course_name_list,
    "campus_name": campus_name_list,
    "department_code": department_code_list,
    "empname": empname_list,
    "comment": comment_list, 
    "sentiment": sentiment_list
}

df = pd.DataFrame(data)
# def is_valid_comment(comment):
#     return len(comment) >= 3 and not bool(re.search(r'[^a-zA-Z0-9\s]', comment))
# df = df[df['comment'].apply(is_valid_comment)]
df.to_csv('feedbackData.csv', index=False)

print("DataFrame saved as 'feedbackData.csv'.")
