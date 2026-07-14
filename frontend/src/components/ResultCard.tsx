import React from 'react'
import type { ResumeAnalysis } from '../types'

interface Props {
  analysis: ResumeAnalysis
}

const ResultCard: React.FC<Props> = ({ analysis }) => {
  const { basic_info, job_intention, background } = analysis

  return (
    <div className="space-y-6">
      {/* Basic Info Card */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">基本信息</h3>
        <div className="grid grid-cols-2 gap-4">
          {basic_info.name && (
            <div>
              <span className="text-sm text-gray-500">姓名</span>
              <p className="font-medium text-gray-800">{basic_info.name}</p>
            </div>
          )}
          {basic_info.phone && (
            <div>
              <span className="text-sm text-gray-500">电话</span>
              <p className="font-medium text-gray-800">{basic_info.phone}</p>
            </div>
          )}
          {basic_info.email && (
            <div>
              <span className="text-sm text-gray-500">邮箱</span>
              <p className="font-medium text-gray-800">{basic_info.email}</p>
            </div>
          )}
          {basic_info.address && (
            <div>
              <span className="text-sm text-gray-500">地址</span>
              <p className="font-medium text-gray-800">{basic_info.address}</p>
            </div>
          )}
        </div>
        {job_intention.target_position && (
          <div className="mt-4 flex gap-4">
            <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm">
              期望职位: {job_intention.target_position}
            </div>
            {job_intention.expected_salary && (
              <div className="bg-green-50 text-green-700 px-3 py-1 rounded-full text-sm">
                期望薪资: {job_intention.expected_salary}
              </div>
            )}
            <div className="bg-purple-50 text-purple-700 px-3 py-1 rounded-full text-sm">
              工作年限: {background.work_years}年
            </div>
          </div>
        )}
      </div>

      {/* Education */}
      {background.education.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">教育经历</h3>
          <div className="space-y-3">
            {background.education.map((edu, i) => (
              <div key={i} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <span className="text-xl">🎓</span>
                <div>
                  <p className="font-medium text-gray-800">{edu.school}</p>
                  <p className="text-sm text-gray-600">{edu.degree} · {edu.major} · {edu.year}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Work Experience */}
      {background.work_experience.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">工作经历</h3>
          <div className="space-y-4">
            {background.work_experience.map((w, i) => (
              <div key={i} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-800">{w.company}</p>
                    <p className="text-sm text-blue-600">{w.position}</p>
                  </div>
                  <span className="text-sm text-gray-500">{w.duration}</span>
                </div>
                {w.description && <p className="text-sm text-gray-600 mt-2">{w.description}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Projects */}
      {background.projects.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">项目经历</h3>
          <div className="space-y-4">
            {background.projects.map((p, i) => (
              <div key={i} className="p-3 bg-gray-50 rounded-lg">
                <p className="font-medium text-gray-800">{p.name}</p>
                <p className="text-sm text-blue-600">{p.role}</p>
                {p.description && <p className="text-sm text-gray-600 mt-1">{p.description}</p>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Skills */}
      {background.skills.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">技能</h3>
          <div className="flex flex-wrap gap-2">
            {background.skills.map((s, i) => (
              <span key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                {s}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultCard
