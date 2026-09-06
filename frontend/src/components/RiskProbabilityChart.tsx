import { motion } from 'motion/react'
import type { RiskProbability } from '../types'

const ORDER = ['Low', 'Medium', 'High']

export default function RiskProbabilityChart({ data, compact = false }: { data: RiskProbability[]; compact?: boolean }) {
  const sorted = [...data].sort((a, b) => ORDER.indexOf(a.risk_level) - ORDER.indexOf(b.risk_level))
  const height = compact ? 120 : 200

  return (
    <div className="w-full">
      <svg width="0" height="0">
        <defs>
          <linearGradient id="gilded" x1="0" y1="1" x2="0" y2="0">
            <stop offset="0%" stopColor="#ae9357" />
            <stop offset="45%" stopColor="#fff0cc" />
            <stop offset="100%" stopColor="#ae9357" />
          </linearGradient>
        </defs>
      </svg>

      <div className="flex items-end justify-between gap-4" style={{ height }}>
        {sorted.map((row, i) => (
          <div key={row.risk_level} className="flex flex-1 flex-col items-center gap-2">
            <span className="text-[13px] font-medium text-bone">{row.probability.toFixed(1)}%</span>
            <div className="flex w-full flex-1 items-end overflow-hidden rounded-t-[4px] bg-graphite/60">
              <motion.div
                className="w-full rounded-t-[4px]"
                style={{ background: 'linear-gradient(180deg, #fff0cc, #ae9357)' }}
                initial={{ height: 0 }}
                whileInView={{ height: `${Math.max(row.probability, 2)}%` }}
                viewport={{ once: true }}
                transition={{ duration: 0.7, delay: i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <span className="text-[13px] text-fog">{row.risk_level}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
