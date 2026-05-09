import pandas as pd

courses = pd.read_csv('dataset/courses.csv')

def recommend_courses(interest):

    matched = courses[
        courses['category'].str.lower() == interest.lower()
    ]

    recommendations = []

    for index, row in matched.iterrows():

        recommendations.append({
            'course': row['course_name'],
            'category': row['category']
        })

    return recommendations