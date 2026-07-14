export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

export interface ResumeRecord {
  resume_id: string
  filename: string
  status: string
  raw_text: string
  structured: {
    sections: string[]
  }
  analysis?: ResumeAnalysis
}

export interface BasicInfo {
  name: string
  phone: string
  email: string
  address: string
}

export interface JobIntention {
  target_position: string
  expected_salary: string
}

export interface EducationItem {
  degree: string
  school: string
  major: string
  year: string
}

export interface ProjectItem {
  name: string
  role: string
  description: string
}

export interface WorkItem {
  company: string
  position: string
  duration: string
  description: string
}

export interface Background {
  work_years: number
  education: EducationItem[]
  projects: ProjectItem[]
  work_experience: WorkItem[]
  skills: string[]
}

export interface ResumeAnalysis {
  resume_id: string
  basic_info: BasicInfo
  job_intention: JobIntention
  background: Background
}

export interface DimensionScores {
  skill_match_rate: number
  experience_relevance: number
  education_match: number
  project_alignment: number
}

export interface MatchResult {
  resume_id: string
  overall_score: number
  dimensions: DimensionScores
  matched_skills: string[]
  missing_skills: string[]
  ai_comment: string
  job_keywords: string[]
  resume_keywords: string[]
}
