# DD-TO-WX 钉钉消息转发微信服务

一个自动化工具，用于将钉钉群聊消息识别并转发到微信。通过截图、AI识别和UI自动化技术，实现钉钉到微信的消息同步。

## 🚀 项目特色

- **智能截图监控**: 自动监控钉钉群聊界面变化
- **AI内容识别**: 使用阿里通义千问VL多模态模型识别截图中的文字内容
- **结构化提取**: 智能提取发言人、时间、内容等结构化信息
- **自动转发**: 通过UI自动化将消息转发到微信群聊
- **差异检测**: 只在群聊内容发生变化时才进行处理，避免重复操作

## 📋 核心功能

### 1. 定时截图与差异检测

- 定时对指定的钉钉群聊窗口进行截图
- 通过哈希值比较检测内容变化
- 只有在检测到新消息时才进行后续处理

### 2. 多模态内容识别

- 使用Qwen2.5-VL-72B-Instruct模型识别截图内容
- 智能提取群聊对话信息：
  - 发言时间
  - 发言人昵称
  - 消息内容
  - 媒体类型识别（图片、视频等）

### 3. 结构化数据输出

识别结果输出为标准JSON格式：

```json
{
    "records": [
        {
            "time": "14:30",
            "speaker": "张三",
            "content": "今天的会议记录已经整理完毕"
        }
    ]
}
```

### 4. 微信自动转发

- 通过HTTP接口将识别结果发送到微信端
- 支持批量消息发送
- 可配置目标微信群聊或联系人

## 🛠️ 技术架构

### 依赖组件

- **UI自动化**: `uiautomation` - 基于Windows UI Automation的屏幕截图和控件操作
- **多模态AI**: 阿里云ModelScope平台的Qwen2.5-VL模型
- **HTTP服务**: 微信消息发送接口服务
- **图像处理**: PIL/base64 图像编码处理

### 参考项目

- [wxauto](https://github.com/cluic/wxauto) - 微信UI自动化控制库

## 📦 安装配置

### 环境要求

- Python >= 3.11
- Windows系统（uiautomation依赖）
- ModelScope Access Token

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境变量配置

创建 `.env` 文件并配置：

```env
MODELSCOPE_ACCESS_TOKEN=your_modelscope_token_here
```

### 微信接口服务

确保微信消息发送服务在 `http://127.0.0.1:10010` 运行。

## 🚀 使用方法

### 1. 启动定时截图监控

```bash
python timed_capture.py
```

### 2. 操作步骤

1. 运行脚本后，将鼠标放在要监控的钉钉群聊窗口上
2. 等待3秒让程序识别控件
3. 程序开始每10秒截图一次，监控内容变化
4. 检测到新消息时自动：
   - 保存截图到 `capture_diff/` 目录
   - 调用AI模型识别内容
   - 生成JSON格式的结构化数据
   - 发送到微信接口

### 3. 单独测试AI识别

```bash
python vl.py  # 测试图像识别功能
python qwen-vl.py  # 使用qwen_vl_recognize函数
```

## 📁 项目结构

```text
dd-to-wx/
├── main.py              # 项目入口文件
├── timed_capture.py     # 定时截图与监控主程序
├── qwen-vl.py          # Qwen-VL模型调用封装
├── vl.py               # 视觉语言模型测试脚本
├── requirements.txt     # 项目依赖
├── pyproject.toml      # 项目配置文件
├── capture_diff/       # 截图差异保存目录（自动创建）
├── demo.png            # 测试图片样本
└── README.md           # 项目文档
```

## ⚙️ 配置参数

### 截图监控参数

- `interval`: 截图间隔时间（默认10秒）
- `save_folder`: 差异图片保存目录（默认 `capture_diff`）

### AI模型配置

- API推理介绍：`https://www.modelscope.cn/docs/model-service/API-Inference/intro`
- 模型: `Qwen/Qwen2.5-VL-72B-Instruct`
- API基址: `https://api-inference.modelscope.cn/v1`
- 支持图片格式: PNG, JPEG等常见格式

### 微信接口配置

- 接口地址: `http://127.0.0.1:10010/text`
- 请求格式: JSON POST
- 参数: `msg`(消息内容), `receiver`(接收人)

## 🎯 应用场景

- **工作协同**: 将重要的钉钉工作群消息同步到微信
- **消息备份**: 自动备份和归档群聊记录
- **跨平台通知**: 在不同即时通讯平台间建立消息桥梁
- **内容监控**: 监控特定群聊的重要消息更新

## 🔧 故障排除

### 常见问题

1. **截图失败**: 确保钉钉窗口在前台且可见
2. **识别错误**: 检查ModelScope Token是否正确配置
3. **转发失败**: 确认微信接口服务正常运行
4. **权限问题**: Windows可能需要管理员权限运行

### 调试建议

- 查看 `capture_diff/` 目录中保存的截图和JSON文件
- 检查控制台输出的错误信息
- 验证环境变量配置是否正确

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📞 联系

如有问题或建议，请通过GitHub Issue联系。
