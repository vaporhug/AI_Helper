运行命令如下，在AI_Helper这个目录下：<br>
flask --app app run --debug


我使用本地的请求进行测试的时候输入的命令如下：<br>
curl http://localhost:5000/register -d '{"email": "example@example.com", "gender": "male","username": "username","age":"age","role":"role"}' -H "Content-Type: application/json" -X POST
