import { useState } from 'react'
import './App.css'

// 定义 API 返回的结构，增强类型安全
interface StreamData {
  token: string;
}

function App() {
  const [sqlResult, setSqlResult] = useState<string>("")
  const [isProcessing, setIsProcessing] = useState<boolean>(false)

  const handleFixSql = async () => {
    // 1. 初始化状态
    setSqlResult("")
    setIsProcessing(true)

    try {
      /** * 🚀 这里的路径使用了 '/api' 前缀
       * Vite 会根据 vite.config.ts 将其转发至 http://localhost:8000/stream
       */
      const response = await fetch('/api/stream')

      if (!response.ok) throw new Error('网络响应错误')

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) return

      // 2. 循环读取流数据
      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        // 解析 SSE 格式数据 (data: {"token": "..."}\n\n)
        const lines = chunk.split('\n\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.replace('data: ', '')
              const data: StreamData = JSON.parse(jsonStr)
              // 使用函数式更新，确保拿到最新的 state
              setSqlResult((prev) => prev + data.token)
            } catch (e) {
              console.error("解析 JSON 出错:", e)
            }
          }
        }
      }
    } catch (error) {
      console.error('修复 SQL 失败:', error)
      setSqlResult("Error: 无法连接到后端，请检查 FastAPI 服务。")
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="container">
      <h1>AI SQL Fixer</h1>

      <div className="editor-section">
        <button
          onClick={handleFixSql}
          disabled={isProcessing}
          className={isProcessing ? 'loading' : ''}
        >
          {isProcessing ? 'AI 正在思考...' : '执行 AI 修复'}
        </button>
      </div>

      <div className="output-panel">
        <h3>修复结果：</h3>
        <pre className="code-block">
          <code>{sqlResult || "等待指令..."}</code>
          {isProcessing && <span className="typing-cursor">|</span>}
        </pre>
      </div>
    </div>
  )
}

export default App