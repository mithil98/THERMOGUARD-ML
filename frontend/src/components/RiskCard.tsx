import { AnimatePresence, motion } from 'motion/react'
import { AlertTriangle, ShieldCheck, ShieldAlert } from 'lucide-react'
import { riskTone } from '../lib/risk'
import CountUp from './fx/CountUp'

interface RiskCardProps {
  label: string
  risk: string
  confidence: number
  message: string
}

const ICONS: Record<string, typeof ShieldCheck> = {
  high: ShieldAlert,
  medium: AlertTriangle,
  low: ShieldCheck,
}

export default function RiskCard({ label, risk, confidence, message }: RiskCardProps) {
  const tone = riskTone(risk)
  const Icon = ICONS[risk.toLowerCase()] ?? ShieldCheck

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={risk}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.35 }}
        className={`rounded-[10px] border ${tone.border} ${tone.bg} p-8 text-center`}
      >
        <div className="mb-4 flex items-center justify-center gap-2">
          <Icon size={20} strokeWidth={1.5} className={tone.text} aria-hidden="true" />
          <span className={`text-[13px] font-semibold tracking-[-0.02em] ${tone.text}`}>{label}</span>
        </div>
        <div className="font-display text-[44px] text-paper-white sm:text-[52px]">{risk}</div>
        <p className="mt-3 text-[16px] text-mist">{message}</p>
        <div className="mt-5 inline-flex items-center gap-2 rounded-full border border-slate px-4 py-1.5">
          <span className="text-[13px] text-fog">AI Confidence</span>
          <span className="text-[15px] font-medium text-bone">
            <CountUp to={confidence} decimals={2} suffix="%" duration={1} />
          </span>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
