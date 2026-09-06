import { useState } from 'react'
import { FileDown, Loader2 } from 'lucide-react'
import type { PredictRequest } from '../types'
import { downloadReport } from '../lib/api'
import ShinyButton from './fx/ShinyButton'

export default function ReportButton({ form }: { form: PredictRequest }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleClick = async () => {
    setLoading(true)
    setError(null)
    try {
      await downloadReport(form)
    } catch (e: any) {
      setError(String(e.message ?? e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center gap-2">
      <ShinyButton onClick={handleClick} disabled={loading} className="w-full sm:w-auto">
        {loading ? (
          <Loader2 size={16} className="animate-spin" aria-hidden="true" />
        ) : (
          <FileDown size={16} strokeWidth={1.5} aria-hidden="true" />
        )}
        {loading ? 'Generating report…' : 'Download PDF Report'}
      </ShinyButton>
      {error && <p className="text-[13px] text-[#e8a898]">{error}</p>}
    </div>
  )
}
