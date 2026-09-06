import { TriangleAlert } from 'lucide-react'
import type { MetaResponse } from '../types'
import CountUp from './fx/CountUp'
import Reveal from './fx/Reveal'
import SectionTitle from './ui/SectionTitle'
import SpotlightCard from './fx/SpotlightCard'

export default function PerformanceStats({ meta }: { meta: MetaResponse }) {
  const stats = [
    { label: 'Model', value: meta.performance.model, isNumber: false },
    { label: 'Features', value: meta.performance.features, isNumber: true },
    { label: 'Test Samples', value: meta.performance.test_samples, isNumber: true },
    { label: 'Reported Accuracy', value: meta.performance.accuracy, isNumber: true, suffix: '%' },
  ]

  return (
    <section className="mx-auto max-w-[1216px] px-6 py-16">
      <SectionTitle eyebrow="Model" title="Model Performance" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s, i) => (
          <Reveal key={s.label} delay={i * 0.05}>
            <SpotlightCard className="p-6 text-center">
              <div className="font-display text-[44px] text-paper-white">
                {s.isNumber ? <CountUp to={s.value as number} suffix={s.suffix} duration={1.2} /> : (s.value as string)}
              </div>
              <div className="mt-2 text-[14px] text-fog">{s.label}</div>
            </SpotlightCard>
          </Reveal>
        ))}
      </div>

      {!meta.performance.verified && (
        <Reveal delay={0.2}>
          <div className="mt-4 flex items-start gap-3 rounded-[10px] border border-[#c9974f]/50 bg-[#c9974f]/10 p-5">
            <TriangleAlert size={18} strokeWidth={1.5} className="mt-0.5 shrink-0 text-[#e6b878]" aria-hidden="true" />
            <p className="text-[14px] leading-[1.5] text-mist">
              <b className="text-bone">Unverified:</b> {meta.performance.caveat}
            </p>
          </div>
        </Reveal>
      )}
    </section>
  )
}
