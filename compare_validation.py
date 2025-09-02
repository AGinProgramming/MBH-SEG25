import pandas as pd

teacher_csv = "/root/autodl-tmp/MBH_Validation_Preds/evaluation_summary.csv"
student_csv = "/root/autodl-tmp/MBH_Validation_Preds_student/evaluation_summary_student.csv"

df_teacher = pd.read_csv(teacher_csv)
df_teacher['model'] = 'Teacher'

df_student = pd.read_csv(student_csv)
df_student['model'] = 'Student'

df_all = pd.concat([df_teacher, df_student], ignore_index=True)

# 按模型统计平均 Dice、GED
summary = df_all.groupby("model").mean(numeric_only=True)
print(summary)

summary.to_csv("/root/autodl-tmp/teacher_student_comparison.csv", index=True)
