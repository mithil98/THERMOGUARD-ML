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
    </section>
  )
}
