import React, { useState } from 'react'
import type { MatchResult } from '../types'
import { matchResume } from '../api'

interface Props {
  resumeId: string
}

const DIM_LABELS: Record<string, string> = {
  skill_match_rate: '技能匹配',
  experience_relevance: '经验相关',
  education_match: '学历匹配',
  project_alignment: '项目契合',
}

const Matcher: React.FC<Props> = ({ resumeId }) => {
  const [jd, setJd] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MatchResult | null>(null)
  const [error, setError] = useState('')

  const handleMatch = async () => {
    if (!jd.trim()) return
    setLoading(true)
    setError('')
    try {
      const res = await matchResume(resumeId, jd)
      if (res.code === 0) {
        setResult(res.data)
      } else {
        setError(res.message)
      }
    } catch {
      setError('匹配请求失败，请检查后端服务')
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = (s: number) => {
    if (s >= 80) return 'text-green-500'
    if (s >= 60) return 'text-yellow-500'
    return 'text-red-500'
  }

  const ringOffset = (percent: number) => {
    const c = 2 * Math.PI * 48
    return c - (percent / 100) * c
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">岗位匹配度分析</h3>
        <textarea
          className="w-full h-36 border border-gray-300 rounded-lg p-4 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
          placeholder="请输入岗位描述（JD），例如：招聘 Java 后端工程师，5年以上经验，熟悉 Spring Boot、MySQL、Redis..."
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />
        <button
          onClick={handleMatch}
          disabled={loading || !jd.trim()}
          className="mt-4 bg-blue-600 text-white px-8 py-2.5 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? '分析中...' : '开始匹配分析'}
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>

      {result && (
        <div className="space-y-6">
          {/* Overall Score Ring */}
          <div className="bg-white rounded-xl shadow-sm p-6 flex flex-col items-center">
            <h3 className="text-lg font-semibold text-gray-800 mb-6">综合评分</h3>
            <div className="relative w-32 h-32">
              <svg className="w-32 h-32 -rotate-90" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="48" fill="none" stroke="#e5e7eb" strokeWidth="10" />
                <circle
                  cx="60" cy="60" r="48"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="10"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 48}`}
                  strokeDashoffset={ringOffset(result.overall_score)}
                  className={scoreColor(result.overall_score)}
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className={`text-3xl font-bold ${scoreColor(result.overall_score)}`}>
                  {result.overall_score}
                </span>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2">百分制综合评价</p>

            {result.ai_comment && (
              <p className="mt-4 text-gray-700 text-center bg-blue-50 rounded-lg p-4 max-w-lg">
                💡 {result.ai_comment}
              </p>
            )}
          </div>

          {/* Dimension Scores */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">各维度评分</h3>
            <div className="space-y-4">
              {Object.entries(result.dimensions).map(([key, val]) => (
                <div key={key} className="flex items-center gap-4">
                  <span className="w-24 text-sm text-gray-600">{DIM_LABELS[key] || key}</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${Math.round(val * 100)}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-700 w-12 text-right">
                    {Math.round(val * 100)}%
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Skills Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h4 className="font-semibold text-green-700 mb-3">✅ 匹配技能</h4>
              <div className="flex flex-wrap gap-2">
                {result.matched_skills.map((s, i) => (
                  <span key={i} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">{s}</span>
                ))}
                {result.matched_skills.length === 0 && <span className="text-gray-400 text-sm">无</span>}
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h4 className="font-semibold text-red-700 mb-3">❌ 缺失技能</h4>
              <div className="flex flex-wrap gap-2">
                {result.missing_skills.map((s, i) => (
                  <span key={i} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">{s}</span>
                ))}
                {result.missing_skills.length === 0 && <span className="text-gray-400 text-sm">无</span>}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Matcher
