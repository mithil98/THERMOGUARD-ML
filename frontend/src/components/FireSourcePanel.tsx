import { Trees, MapPinned, Waves, HelpCircle, AlertOctagon } from 'lucide-react'
import CountUp from './fx/CountUp'
import SpotlightCard from './fx/SpotlightCard'

const SOURCE_INFO: Record<string, { icon: typeof Trees; message: string; tone: 'sage' | 'amber' | 'neutral' }> = {
  'Vegetation Fire': {
    icon: Trees,
    tone: 'sage',
    message:
      'Vegetation-related hotspot. May involve forest, grassland or agricultural vegetation — the current dataset does not separate these categories.',
  },
  'Other Land Source': {
    icon: MapPinned,
    tone: 'amber',
    message:
      'Land-based hotspot. Must NOT be treated as confirmed industrial fire — the dataset has no direct Industrial label.',
  },
  Offshore: {
    icon: Waves,
    tone: 'neutral',
    message: 'Offshore or water-related hotspot. Geographic verification is recommended.',
  },
  Unknown: {
    icon: HelpCircle,
    tone: 'amber',
    message: 'Source could not be determined confidently. Additional satellite or geographic data is required.',
  },
}

const TONE_CLASS: Record<string, string> = {
  sage: 'text-[#9fcaac]',
  amber: 'text-[#e6b878]',
  neutral: 'text-fog',
}

export default function FireSourcePanel({ source, confidence }: { source: string; confidence: number }) {
  const info = SOURCE_INFO[source] ?? {
    icon: AlertOctagon,
    tone: 'neutral' as const,
    message: 'Fire source classification completed.',
  }
  const Icon = info.icon

  return (
    <SpotlightCard className="p-6">
      <div className="grid gap-6 sm:grid-cols-2">
        <div className="flex items-start gap-3">
          <Icon size={24} strokeWidth={1.5} className={TONE_CLASS[info.tone]} aria-hidden="true" />
          <div>
            <div className="text-[13px] font-semibold tracking-[-0.02em] text-fog">DETECTED FIRE SOURCE</div>
            <div className="font-display text-[28px] text-paper-white">{source}</div>
          </div>
        </div>
        <div>
          <div className="text-[13px] font-semibold tracking-[-0.02em] text-fog">SOURCE CONFIDENCE</div>
          <div className="font-display text-[28px] text-paper-white">
            <CountUp to={confidence} decimals={2} suffix="%" duration={1} />
          </div>
        </div>
      </div>
      <p className="mt-5 border-t border-graphite pt-5 text-[15px] leading-[1.5] text-mist">{info.message}</p>
    </SpotlightCard>
  )
}
