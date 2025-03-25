# exam_generator.py
import json, re, time
from datetime import datetime
from tqdm import tqdm
from docx import Document
from concurrent.futures import ThreadPoolExecutor

from deepseek_client import DeepSeekClient
from document_utils import setup_document_style, add_answer_section
from conf.config import DEEPSEEK_API_KEY

class EnhancedInterviewGenerator:
    def __init__(self, tech_direction="JAVA"):
        self.tech_direction = tech_direction
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com"
        self.doc = Document()
        # 存放所有题目的答案与解析信息，后续用于生成参考答案与解析部分
        self.answer_sheet = []  
        # 用于记录所有题目的编号（全局递增）
        self.question_count = 0  
        # 存放各题型生成的题目数据，结构：{ "单选题": [q1, q2, ...], "多选题": [...], ... }
        self.generated_questions = {}  
        self.deepseek_client = DeepSeekClient(api_key=self.api_key, base_url=self.base_url, tech_direction=self.tech_direction)

    def _get_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"{self.tech_direction}_Interview_{timestamp}.docx"
    
    def _generate_batch_questions(self, question_type, num=15):
        """
        调用 API 生成一批题目，并对生成的题目进行格式校验（多选题单个题目错误则剔除）
        若遇到部分题目错误，则仅剔除错误题目，返回格式正确的题目列表。
        """
        # 定义各题型要求
        type_requirements = {
            "单选题": "每个问题必须包含四个中文选项，用大写字母A. B. C. D. 标记，答案只能有一个正确选项",
            "多选题": "每个问题必须包含5-7个中文选项，用大写字母A. B. C. D. E. F...标记，答案应有2-7个正确选项。问题内容必须明确列出所有选项，每个选项用大写字母开头（例如：A. 选项内容）",
            "填空题": "问题中用___________表示空白，答案填具体内容",
            "判断题": "答案只能是'正确'或'错误'",
            "问答题": "问题必须是不含任何选项的开放式技术问题，答案为简明扼要的文字描述"
        }
        # 定义示例文本，注意问答题的示例避免包含多余引号或选项
        question_examples = {
            "单选题": '"问题内容（示例：\'Java中的final关键字作用？\\nA. 继承\\nB. 重写\\nC. 常量\\nD. 多态\'）"',
            "多选题": '"问题内容（示例：\'哪些是Java集合接口？\\nA. List\\nB. Set\\nC. Map\\nD. Array\'）"',
            "问答题": '问题内容（示例："请详细解释C#中垃圾回收机制及其优化方法"）'
        }
        
        # 针对问答题，单独构造 prompt，确保题目不包含选项，并严格返回 JSON 格式
        if question_type == "问答题":
            prompt = f"""请生成{num}道{self.tech_direction}高级开发工程师面试{question_type}，
                要求：
                1. {type_requirements[question_type]}。
                2. 所有问题和解析必须使用中文（专有名称和术语除外）。
                3. 使用严格的JSON格式，仅返回JSON，不包含任何其他文本，格式如下：
                {{
                    "questions": [
                        {{
                            "question": "请详细解释{self.tech_direction}中某个关键技术原理",
                            "short_answer": "最简答案",
                            "detailed_analysis": "300字技术解析",
                            "keywords": ["关键词"],
                            "difficulty": "1-5"
                        }}
                    ]
                }}
                4. 请确保生成的题目各不相同，不要包含任何选项。
            """
        else:
            prompt = f"""请生成{num}道{self.tech_direction}高级开发工程师面试{question_type}，要求：
                1. {type_requirements[question_type]}
                2. 所有问题、选项和解析必须使用中文（专有名称和术语除外）
                3. {"多选题答案字母按升序排列（如ABE）" if question_type == "多选题" else ""}
                4. 使用严格JSON格式：
                {{
                    "questions": [
                        {{
                            "question": {question_examples.get(question_type, '"问题内容"')},
                            "short_answer": "最简答案",
                            "detailed_analysis": "300字技术解析",
                            "keywords": ["关键词"],
                            "difficulty": "1-5"
                        }}
                    ]
                }}
                5. 不要包含多余文本
                6. 请确保生成的题目各不相同
            """
        
        result = self.deepseek_client.call(prompt)
        if not result:
            return []
        # 清理可能存在的代码块标记
        result = re.sub(r'```json|```', '', result).strip()
        try:
            data = json.loads(result)
            questions = data.get("questions", [])[:num]
            valid_questions = []
            if question_type == "单选题":
                for q in questions:
                    valid = True
                    answer = q.get("short_answer", "")
                    if len(answer) != 1 or not answer.isalpha():
                        print(f"单选题答案格式错误: {answer}，已剔除该题")
                        valid = False
                    options = re.findall(r'\b[A-Z]\.\s', q.get("question", ""))
                    if len(options) != 4:
                        print(f"单选题选项数量不为4: {q.get('question','')}，已剔除该题")
                        valid = False
                    if valid:
                        valid_questions.append(q)
            elif question_type == "多选题":
                for q in questions:
                    valid = True
                    answer = q.get("short_answer", "")
                    if len(answer) < 2 or not answer.isalpha() or answer != ''.join(sorted(answer)):
                        print(f"多选题答案格式错误: {answer}，已剔除该题")
                        valid = False
                    if not re.search(r'\b[A-Z]\.\s', q.get("question", "")):
                        print(f"多选题选项缺失: {q.get('question','')}，已剔除该题")
                        valid = False
                    if valid:
                        valid_questions.append(q)
            elif question_type == "问答题":
                for q in questions:
                    if re.search(r'\b[A-Z]\.\s', q.get("question", "")):
                        print(f"问答题包含选项: {q.get('question','')}，已剔除该题")
                    else:
                        valid_questions.append(q)
            else:
                # 填空题、判断题等直接返回
                valid_questions = questions
            return valid_questions
        except Exception as e:
            print(f"解析失败: {str(e)}")
            print("原始内容:", result)
            return []
    
    def _write_question_sections(self, generated_questions):
        """
        根据生成的题目数据写入文档，按照题型分组
        """
        for q_type in generated_questions:
            questions = generated_questions[q_type]
            self.doc.add_heading(f"{q_type}（共{len(questions)}题）", level=2)
            for q in questions:
                if "number" in q:
                    self.doc.add_paragraph(
                        f"{q['number']}. {q['question']}（难度：{q['difficulty']}/5）",
                        style='Normal'
                    )
                else:
                    self.doc.add_paragraph(q.get('question', '无题'), style='Normal')
            self.doc.add_page_break()
    
    def _add_knowledge_points_summary(self):
        """
        根据所有生成的题目（包括判断题），调用 API 生成一份涉及主要知识点的总结，
        现修改为生成更详细的知识点总结，每个知识点包括详细的原理、实际应用、优缺点及注意事项，
        以便于深入学习。输出要求为适合 docx 排版的纯文本格式（不使用 Markdown 语法），
        并确保所有试题的知识点均被覆盖。
        """
        import re
        # 遍历所有题型，将所有题目拼接起来，确保覆盖所有试题
        all_questions = []
        for q_type, questions in self.generated_questions.items():
            all_questions.extend(questions)
        all_questions.sort(key=lambda x: x['number'])
        questions_text = "\n".join([f"{item['number']}. {item['question']}" for item in all_questions])
        prompt = (
            f"请根据以下{self.tech_direction}高级开发面试题目，生成一份详细的知识点总结。\n"
            "请按照以下模板格式生成，每个知识点块之间用 '====' 分隔，模板如下：\n"
            "【知识点名称】：\n"
            "【原理】：\n"
            "【实际应用】：\n"
            "【优点】：\n"
            "【缺点】：\n"
            "【注意事项】：\n"
            "请确保所有试题的知识点均被覆盖，并输出为纯文本格式，避免使用 Markdown 语法。\n"
            "题目如下：\n"
            f"{questions_text}"
        )
        knowledge_start = time.time()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.deepseek_client.call, prompt)
            print("生成详细知识点总结中，请稍候...")
            knowledge_points = future.result()
        knowledge_end = time.time()
        print(f"详细知识点总结生成完成，耗时 {knowledge_end - knowledge_start:.2f} 秒")
        if knowledge_points:
            knowledge_points = re.sub(r'```.+?```', '', knowledge_points).strip()
            return knowledge_points
        else:
            print("生成详细知识点总结失败")
            return None
    
    def generate_exam_paper(self, question_types):
        overall_start = time.time()
        from document_utils import add_knowledge_summary_section_template
        setup_document_style(self.doc)
        self.doc.add_heading(f"{self.tech_direction}高级开发面试题库", level=0)
        self.doc.add_paragraph("\n考生姓名：__________\n考试时间：120分钟\n\n")
        
        # 存储各题型生成的题目数据
        self.generated_questions = {}
        
        # 先生成各类题目，但不直接写入文档
        for q_type, total in question_types:
            generated = []
            remaining = total
            seen_questions = set()
            attempts = 0
            max_attempts = 5
            pbar = tqdm(total=total, desc=f"生成 {q_type}", ncols=80)
            while remaining > 0 and attempts < max_attempts:
                batch_num = remaining if remaining < 10 else 10
                questions = self._generate_batch_questions(q_type, batch_num)
                if questions is None:
                    print(f"{q_type}生成失败，请检查API设置")
                    break
                unique_questions = []
                for q in questions:
                    if q["question"] not in seen_questions:
                        seen_questions.add(q["question"])
                        self.question_count += 1
                        q_with_num = q.copy()
                        q_with_num["number"] = self.question_count
                        q_with_num["type"] = q_type  # 添加题型信息
                        q_with_num["answer"] = q.get("short_answer", "")
                        q_with_num["analysis"] = q.get("detailed_analysis", "")
                        unique_questions.append(q_with_num)
                        self.answer_sheet.append(q_with_num)
                    else:
                        print(f"检测到重复题目，已跳过: {q['question']}")
                if len(unique_questions) == 0:
                    attempts += 1
                    print(f"当前批次{q_type}重复或格式错误较多，尝试补充次数：{attempts}")
                else:
                    attempts = 0
                generated.extend(unique_questions)
                pbar.update(len(unique_questions))
                remaining = total - len(generated)
            pbar.close()
            if remaining > 0:
                print(f"警告：{q_type}最终未生成足够题目，期望{total}题，实际获得{len(generated)}题")
            self.generated_questions[q_type] = generated
        
        # 所有题目生成完成后，根据题目生成知识点总结，并插入到考生信息之后
        knowledge_points = self._add_knowledge_points_summary()
        if knowledge_points:
            add_knowledge_summary_section_template(self.doc, knowledge_points)
            self.doc.add_page_break()
            print("知识点总结添加成功")
        else:
            print("未生成知识点总结")
        
        # 将各题型题目写入文档
        self._write_question_sections(self.generated_questions)
        
        overall_end = time.time()
        add_answer_section(self.doc, self.answer_sheet)
        filename = self._get_filename()
        self.doc.save(filename)
        print(f"生成成功！文件已保存为 {filename}, 共{self.question_count}题")
        print(f"总耗时: {overall_end - overall_start:.2f}秒")
