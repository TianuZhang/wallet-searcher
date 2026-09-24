# Web3 AI Agent MVP

一个面向学习的 Python MVP：读取 Ethereum 钱包的 ETH 余额，并使用 OpenAI API 用中文解释该余额。

## 架构

```text
钱包地址
  ↓
Infura / Ethereum RPC（读取公开链上数据）
  ↓
Python 数据层（wallet_reader.py）
  ↓
OpenAI API 分析层（ai_analyzer.py）
```

本项目只读取公开数据：不需要、也绝不应输入私钥或助记词。

## 项目文件

- `wallet_reader.py`：校验地址并读取原生 ETH 余额。
- `ai_analyzer.py`：获取余额后，请 OpenAI 用中文解释结果。
- `token_reader.py`：读取标准 ERC-20 代币余额。
- `agent.py`：由 OpenAI 选择并调用只读 ETH、ERC-20 余额工具。
- `requirements.txt`：Python 依赖。
- `.env.example`：环境变量名称示例，不包含真实密钥。

## 环境要求

- Python 3.10+
- Ethereum Mainnet RPC URL（例如 Infura）
- OpenAI API Key（仅运行 AI 分析脚本时需要）

## 安装

在 PowerShell 中进入项目目录：

```powershell
cd "D:\文档\ChatGPT\ai web3"
python -m pip install -r requirements.txt
```

## 配置密钥

在当前 PowerShell 会话设置环境变量：

```powershell
$env:ETH_RPC_URL="https://mainnet.infura.io/v3/你的_INFURA_PROJECT_ID"
$env:OPENAI_API_KEY="你的_OPENAI_API_KEY"
```

请勿把真实 RPC URL 或 API Key 提交到 GitHub。

## 运行

只查询 ETH 余额：

```powershell
python wallet_reader.py
```

查询余额并由 AI 解释：

```powershell
python ai_analyzer.py
```

以自然语言查询 ETH 或 ERC-20 余额（在问题中包含地址）：

```powershell
python agent.py
```

示例问题：

```text
请查询 0x... 的 ETH 余额，并用中文解释。
```

查询 ERC-20 时，必须同时提供钱包地址和代币合约地址：

```text
查询钱包 0x... 持有的代币合约 0x... 的余额。
```

读取 ERC-20 代币余额（需要输入钱包地址和代币合约地址）：

```powershell
python token_reader.py
```

## 当前范围与下一步

当前 MVP 仅支持 Ethereum 主网的原生 ETH 余额。后续计划：

1. 读取 ERC-20 代币余额。
2. 查询交易历史。
3. 将余额、交易和风险检查封装为可供模型调用的工具。
4. 使用 LangGraph 编排多步钱包风险分析。
