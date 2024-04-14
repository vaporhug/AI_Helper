
```markdown
# AI_Helper

AI_Helper 是一个使用 Python 编写的项目，主要用于处理和生成对话、问题、笔记等。
其前端的代码仓库为
(https://github.com/LouisLou2/LawExamPal/blob/master/README_EN.md)


## 运行项目

在 AI_Helper 目录下，使用以下命令运行项目：

```bash
flask --app app run --debug
```

## 测试

使用以下命令进行本地测试：

```bash
curl http://localhost:5000/register -d '{"email": "example@example.com", "gender": "male","username": "username","age":"age","role":"role"}' -H "Content-Type: application/json" -X POST
```

## 邮件服务

项目中的邮件服务需要 SMTP 服务器地址。以下是一些常见的电子邮件服务提供商的 SMTP 服务器地址：

- Gmail: smtp.gmail.com
- Outlook/Hotmail: smtp-mail.outlook.com
- Yahoo Mail: smtp.mail.yahoo.com
- AOL: smtp.aol.com
- Office365: smtp.office365.com
- QQ Mail: smtp.qq.com
- 163 Mail: smtp.163.com

## Markdown 转 PDF

在 Python 中，你可以使用 `pandoc` 和 `pypandoc` 库将 Markdown 文件转换为 PDF 文件。首先，你需要安装 `pypandoc` 和 `pandoc`：

```bash
pip install pypandoc
brew install pandoc
```

然后，你可以使用以下 Python 代码将 Markdown 文件转换为 PDF：

```python
import pypandoc

output = pypandoc.convert_file('input.md', 'pdf', outputfile="output.pdf")
assert output == ""
```

注意：这个过程需要 LaTeX 环境，因为 Pandoc 使用 LaTeX 来生成 PDF。如果你的系统上没有安装 LaTeX，你可能需要安装一个。在 macOS 上，你可以使用 MacTeX：

```bash
brew install --cask mactex-no-gui
```

## 环境配置

运行本项目还需要添加一些环境变量，具体如下：  
首先是关于用来发送验证码的邮箱的配置  
EMAIL_PASSWORD：邮箱密码   
EMAIL_ACCOUNT：邮箱账号   
EMAIL_TYPE: 邮箱类型   
然后是用来和前端交互的本地服务器主机号和端口的配置和用来和远程服务器交流的模型的服务器主机号的配置   
MODEL_BASE_URL：模型服务器的主机号   
LOCAL_HOST：本地服务器的主机号   
然后是用来进行文件格式转换的pdflatex的本地地址   
PDFLATEX_LOCATION：pdflatex的本地地址（参考：--pdf-engine=/usr/local/texlive/2024/bin/universal-darwin/pdflatex）

```
