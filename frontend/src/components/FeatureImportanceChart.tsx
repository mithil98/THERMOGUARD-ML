import { motion } from 'motion/react'
import type { FeatureImportance } from '../types'

export default function FeatureImportanceChart({ data }: { data: FeatureImportance[] }) {
  const top = data.slice(0, 15)
  const max = Math.max(...top.map((d) => d.importance), 0.0001)

  return (
    <div className="space-y-3">
      {top.map((row, i) => (
        <div key={row.feature} className="flex items-center gap-3">
          <span className="w-[140px] shrink-0 truncate text-[13px] text-fog">{row.feature}</span>
          <div className="h-[8px] flex-1 overflow-hidden rounded-full bg-graphite/60">
            <motion.div
              className="h-full rounded-full"
              style={{ background: 'linear-gradient(90deg, #ae9357, #fff0cc)' }}
              initial={{ width: 0 }}
              whileInView={{ width: `${(row.importance / max) * 100}%` }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: i * 0.03 }}
            />
          </div>
          <span className="w-[60px] shrink-0 text-right text-[13px] text-bone">{row.importance.toFixed(4)}</span>
        </div>
      ))}
    </div>
  )
}
