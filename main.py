from exam_generator import EnhancedInterviewGenerator

if __name__ == "__main__":
    tech_direction = input("请输入考试技术方向（默认JAVA）：") or "JAVA"
    generator = EnhancedInterviewGenerator(tech_direction=tech_direction)
    generator.generate_exam_paper([
        ("单选题", 30),
        ("多选题", 30),
        ("填空题", 10),
        ("判断题", 10),
        ("问答题", 10)
    ])
