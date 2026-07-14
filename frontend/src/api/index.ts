import axios from 'axios'
import type { ApiResponse, MatchResult, ResumeAnalysis, ResumeRecord } from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 60000,
})

export async function uploadResume(file: File): Promise<ApiResponse<ResumeRecord>> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/api/resume/upload', form)
  return data
}

export async function analyzeResume(resumeId: string): Promise<ApiResponse<ResumeAnalysis>> {
  const { data } = await api.post(`/api/resume/${resumeId}/analyze`)
  return data
}

export async function getResume(resumeId: string): Promise<ApiResponse<ResumeRecord>> {
  const { data } = await api.get(`/api/resume/${resumeId}`)
  return data
}

export async function matchResume(resumeId: string, jobDescription: string): Promise<ApiResponse<MatchResult>> {
  const { data } = await api.post('/api/match', { resume_id: resumeId, job_description: jobDescription })
  return data
}
