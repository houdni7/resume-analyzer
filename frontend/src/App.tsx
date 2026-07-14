import React, { useState } from 'react'
import Uploader from './components/Uploader'
import ResultCard from './components/ResultCard'
import Matcher from './components/Matcher'
import { uploadResume, analyzeResume } from './api'
import type { ResumeAnalysis } from './types'

const App: React.FC = () => {
  const [resumeId, setResumeId] = useState<string | null>(null)
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null)
  const [uploading, setUploading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<'result' | 'match'>('result')

  const handleUpload = async (file: File) => {
    setUploading(true)
    setError('')
    setAnalysis(null)
    try {
      const res = await uploadResume(file)
      if (res.code === 0 && res.data) {
        const id = res.data.resume_id
        setResumeId(id)

        setAnalyzing(true)
        const analyzeRes = await analyzeResume(id)
        if (analyzeRes.code === 0 && analyzeRes.data) {
          setAnalysis(analyzeRes.data)
        } else {
          setError(analyzeRes.message || 'AI 分析失败')
        }
        setAnalyzing(false)
      } else {
        setError(res.message || '上传失败')
      }
    } catch {
      setError('上传请求失败，请检查后端服务')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <header className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">📊</span>
            <h1 className="text-xl font-bold text-gray-800">AI 智能简历分析系统</h1>
          </div>
          {analysis && (
            <div className="flex gap-2">
              <button
                onClick={() => setTab('result')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  tab === 'result' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                简历详情
              </button>
              <button
                onClick={() => setTab('match')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  tab === 'match' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                岗位匹配
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {!analysis && (
          <div className="mb-8">
            <p className="text-center text-gray-500 mb-6">
              上传一份 PDF 简历，AI 将自动提取关键信息并进行智能分析
            </p>
            <Uploader onUpload={handleUpload} uploading={uploading} />
            {error && (
              <div className="mt-4 bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">
                {error}
              </div>
            )}
          </div>
        )}

        {uploading && (
          <div className="text-center py-12">
            <div className="animate-spin inline-block w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full mb-4" />
            <p className="text-gray-600">正在解析简历...</p>
          </div>
        )}

        {analyzing && (
          <div className="text-center py-12">
            <div className="animate-spin inline-block w-10 h-10 border-4 border-purple-200 border-t-purple-600 rounded-full mb-4" />
            <p className="text-gray-600">AI 正在分析简历内容...</p>
          </div>
        )}

        {analysis && !uploading && !analyzing && (
          <>
            {tab === 'result' && <ResultCard analysis={analysis} />}
            {tab === 'match' && resumeId && <Matcher resumeId={resumeId} />}
          </>
        )}
      </main>

      <footer className="text-center py-6 text-sm text-gray-400 border-t border-gray-100 mt-12">
        AI Resume Analyzer · Powered by 通义千问
      </footer>
    </div>
  )
}

export default App
