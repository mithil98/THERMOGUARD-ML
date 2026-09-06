import { motion, AnimatePresence } from 'motion/react'
import { Flame, ShieldCheck } from 'lucide-react'

export default function FireDetectionCard({
  detected,
  brightnessDifference,
  frp,
}: {
  detected: boolean
  brightnessDifference: number
  frp: number
}) {
  const tone = detected
    ? { border: 'border-[#c47768]/50', bg: 'bg-[#c47768]/10', text: 'text-[#e8a898]' }
    : { border: 'border-[#7fae8e]/50', bg: 'bg-[#7fae8e]/10', text: 'text-[#9fcaac]' }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={String(detected)}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.3 }}
        className={`rounded-[10px] border ${tone.border} ${tone.bg} p-6`}
      >
        <div className="flex items-center gap-3">
          {detected ? (
            <Flame size={22} strokeWidth={1.5} className={tone.text} aria-hidden="true" />
          ) : (
            <ShieldCheck size={22} strokeWidth={1.5} className={tone.text} aria-hidden="true" />
          )}
          <div>
            <div className={`text-[18px] font-semibold ${tone.text}`}>
              Fire Detected: {detected ? 'YES' : 'NO'}
            </div>
            <p className="text-[14px] text-mist">
              FRP {frp.toFixed(2)} · Brightness Difference {brightnessDifference.toFixed(2)} — preliminary
              rule-based thermal screening (FRP ≥ 2.40 and ΔT ≥ 15), not a trained binary classifier.
            </p>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
