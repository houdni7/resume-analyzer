import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'

interface Props {
  onUpload: (file: File) => void
  uploading: boolean
}

const Uploader: React.FC<Props> = ({ onUpload, uploading }) => {
  const [file, setFile] = useState<File | null>(null)

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted.length > 0) {
      setFile(accepted[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: uploading,
  })

  const handleUpload = () => {
    if (file) onUpload(file)
  }

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 bg-white'}
          ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="text-5xl mb-4">📄</div>
        <p className="text-gray-600 text-lg">
          {isDragActive ? '松开鼠标上传文件' : '拖拽 PDF 简历到此处，或点击选择文件'}
        </p>
        <p className="text-gray-400 text-sm mt-2">仅支持 .pdf 格式</p>
      </div>

      {file && (
        <div className="mt-4 flex items-center justify-between bg-white rounded-lg p-4 shadow-sm">
          <div className="flex items-center gap-3">
            <span className="text-2xl">📎</span>
            <div>
              <p className="font-medium text-gray-800">{file.name}</p>
              <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <button
            onClick={handleUpload}
            disabled={uploading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {uploading ? '解析中...' : '上传解析'}
          </button>
        </div>
      )}

      {uploading && (
        <div className="mt-4 w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div className="bg-blue-600 h-full rounded-full animate-pulse w-2/3" />
        </div>
      )}
    </div>
  )
}

export default Uploader
