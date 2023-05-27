from datetime import datetime
import pandas as pd
from fjutils.sheets.google_sheet import GoogleSheet
from course import Course
from typing import List
import training_emails
import training_sheet

def is_completed(value):
    """add styling for positive class"""
    value = "Completed"
    return '<div class="positive"><body style="color:green;">{}</body></div>'.format(value)

def is_red(value):
    return '<div class="positive"><body style="color:red;">{}</body></div>'.format(value)
   

def table_style():
    """
    format function applied to all elements of column c
    """
    return """<style> .tb { border-collapse: collapse; }
    .tb th, .tb td { padding: 5px; border: solid 1px #777; }
    .tb th { background-color: lightblue; }
    </style>"""


def format_column_c(value):
    """
    format function applied to all elements of column c
    """
    result = str(value)
    if value == 'CnQ' or value =="C":
        result = is_completed(result)
    elif value == 'I':
        result=is_red("Incomplete course")
    elif value ==  'QNT':
        result=is_red("Quiz not taken")
    elif value == 'FNG':
        result = "Feedback pending"
    elif value == 'RI' or value == 'RF':
        result = "Rescheduled"
    elif value == 'TC':
        result = "Taking course"
    elif value == 'F':
        result = is_red("Failed")
    elif value == 'PC':
        result = "Taking course"
    elif value == 'QF':
        result = is_red("Quiz failed")
        

    return result

def main():
    tracker_sheet = GoogleSheet("Online Training Course Repository", "reportcardtracker")
    courses: List[Course] = training_sheet.get_courses(tracker_sheet)
    assert len(courses) > 1, "Didn't get all of the courses"
    course: Course

    st=0
    ed: int
    print(len(courses))
    course_temp=[]
    df=pd.DataFrame(columns=['Course','End Date','Present State', 'Quiz Result'])
    for i in range(len(courses)-1):
        sheet_row = i + 2
        course_temp.append(courses[i])
        print(f"sheet_row: {sheet_row}")
        
        if i==len(courses)-1 or courses[i].taker.name != courses[i+1].taker.name:
            
            for j in range(len(course_temp)):
                
                # df=df.append(pd.DataFrame([course_temp[j].name,course_temp[j].start_date,course_temp[j].end_date,course_temp[j].final_state]),ignore_index=True)
                df.loc[len(df)] = [course_temp[j].name,course_temp[j].end_date, course_temp[j].final_state,course_temp[j].quiz_result]
            df['End Date'] = pd.to_datetime(df['End Date']).apply(lambda x: x.date())  
            df=df[df['End Date']<datetime.today().date()]
            df=df.sort_values('End Date')                         
            # print(df.iloc[1,1],type(df.iloc[1,1]))  
            
            training_emails.send_weekly_report_email(course_temp[0],df.to_html(index=False,justify='center',border=2,formatters={"Present State":format_column_c},escape=False))
            course_temp=[]
            print(df)
            df=pd.DataFrame(columns=['Course','End Date','Present State', 'Quiz Result'])
           
            


if __name__ == "__main__":
    main()