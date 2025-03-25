
<h1 align="center" style="color:rgb(0, 15, 22); text-shadow: 2px 2px 4px rgba(0,0,0,0.2); font-size: 2.5em; margin-bottom: 20px;">🔥 高级开发面试题库自动生成工具</h1>

<div align="center">
  
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-4DA1F7?logo=open-source-initiative&logoColor=white&style=for-the-badge)](LICENSE)
[![Downloads](https://img.shields.io/badge/Downloads-1k%2Fweek-27AE60?logo=github&logoColor=white&style=for-the-badge)](https://github.com/saeran-chang/auto-exam-generator)
[![Build Status](https://img.shields.io/badge/CI/CD-Passing-8E44AD?logo=github-actions&logoColor=white&style=for-the-badge)](https://github.com/saeran-chang/auto-exam-generator/actions)

</div>

<div align="center">
  
🎯 **智能组卷** | 🚄 **快速生成** | 🧠 **AI赋能** | 🛡️ **质量保障**

</div>

---

<div align="center">
  
✨ [![Saeran Chang](https://img.shields.io/badge/Author-@Saeran_Chang-FF6B6B?logo=github&style=flat-square)](https://github.com/saeran-chang) 匠心打造 | 💡 欢迎提交 [![Issues](https://img.shields.io/badge/-Issue-2ECC71?logo=git&style=flat-square)](issues) & [![PR](https://img.shields.io/badge/-PR-3498DB?logo=git&style=flat-square)](pulls) ✨

</div>

---

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 🌟 项目简介

<div align="center">
  
![Workflow](https://s1.aigei.com/src/img/gif/ac/ac2fb391bf1148efa2e3186d82e51f43.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:20WvawD1vFFrzxJVfYSXev7dAyQ=)

</div>

本项目是一款**高级自动化试卷生成工具**，主要用于生成针对高级开发面试的题库。通过调用 DeepSeek API，项目可以自动生成单选题、多选题、填空题、判断题和问答题，同时生成对应的参考答案与详细解析。为了帮助考生复习，本项目在试卷前还自动生成一份涵盖关键知识点的基础知识总结。

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 🎯 主要特性

- **🚀 自动化题目生成**  
  利用 DeepSeek API 自动生成各类型面试题，涵盖多种题型，满足不同面试需求。

- **🔍 严格格式校验**  
  对生成的题目进行严格验证，确保题目、选项及答案格式规范，剔除错误题目。

- **📚 基础知识补充**  
  在试卷前添加基础知识部分，内容涵盖语法、面向对象、内存管理、垃圾回收、并发编程、设计模式、数据结构与算法等关键知识点。

- **⏱️ 实时进度与计时显示**  
  使用 `tqdm` 库展示生成进度，同时记录生成过程耗时，直观了解生成情况。

- **🧩 模块化设计**  
  项目采用模块化结构，将配置、API调用、文档生成与核心逻辑分离，便于扩展与维护。

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## ⚙️ 安装要求

- **Python 版本**：Python 3.10 及以上  
- **依赖库**：

使用以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 📂 项目结构

``` plaintext
.
├── conf/config.py             # 配置文件，存放 API 密钥等信息
├── deepseek_client.py         # DeepSeek API 封装调用
├── document_utils.py          # Word 文档生成与样式设置工具函数
├── exam_generator.py          # 自动生成试卷的核心逻辑
└── main.py                    # 项目入口，执行试卷生成任务
```

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 🚦 使用说明

- **配置 API 密钥**

```python
# Deepseek API配置
DEEPSEEK_API_KEY = "**-*******************************"
```

在 conf/config.py 中设置你的 DeepSeek API 密钥。

- **模型选择**

```python
# deepseek-chat是deepseek-v3, deepseek-reasoner是deepseek-r1
MODEL = ["deepseek-chat", "deepseek-reasoner"][1]
```

- **运行项目**

执行以下命令生成试卷：

```bash
python main.py
```

输入要生成的试卷方向

```bash
请输入考试技术方向（默认JAVA）：Java-后端开发-Mybatis # 多个方向请用"-"隔开
```

- 生成的试卷将保存为 .docx 文件，文件名格式为 技术方向_Interview_时间戳.docx。

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 🚀 高级功能

- **🎛️ 自定义题目数量与题型**  
  根据需求定制各类型题目的数量，灵活生成试卷。

- **📈 动态基础知识生成**  
  自动生成与后续试题相关的基础知识总结，帮助考生在考试前快速温习重点内容。

- **❌ 错误题目自动剔除**  
  生成过程中自动剔除格式错误或重复的题目，确保试卷质量。

</div>

<div style="background: rgba(248, 249, 250, 0.8); padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); backdrop-filter: blur(8px); margin: 2rem 0;">

## 💖 致谢

<div align="center">
  
![Validation](https://s1.aigei.com/src/img/gif/48/48ba6f7287da4c0fad35df3f8f369ef9.gif?imageMogr2/auto-orient/thumbnail/!282x240r/gravity/Center/crop/282x240/quality/85/%7CimageView2/2/w/282&e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:F7G3bNauSCXqc4Qham6SYVQn53w=)

</div>

感谢 DeepSeek API 提供强大的自然语言生成能力，同时感谢所有开源项目为本项目的发展贡献力量。

> **注意**：本项目仅供学习和研究用途，请勿用于商业目的。如有疑问，请联系项目维护者。

**Happy Coding!** 🚀  
<sub>✨ 用代码改变世界，用技术创造未来 ✨</sub>

</div>
