import { useEffect, useState } from 'react'
import { Radio } from 'lucide-react'
import type { PredictRequest, PredictResponse } from '../types'
import { predict } from '../lib/api'
import { useDebouncedValue } from '../lib/useDebouncedValue'
import Slider from './ui/Slider'
import { SelectField } from './ui/fields'
import RiskCard from './RiskCard'
import RiskProbabilityChart from './RiskProbabilityChart'
import FireDetectionCard from './FireDetectionCard'
import Reveal from './fx/Reveal'
import SectionTitle from './ui/SectionTitle'
import SpotlightCard from './fx/SpotlightCard'

interface LiveInteractionProps {
  baseForm: PredictRequest
}

export default function LiveInteraction({ baseForm }: LiveInteractionProps) {
  const [liveBrightness, setLiveBrightness] = useState(() => clamp(baseForm.brightness, 250, 450))
  const [liveFrp, setLiveFrp] = useState(() => clamp(baseForm.frp, 0, 100))
  const [liveBrightT31, setLiveBrightT31] = useState(() => clamp(baseForm.bright_t31, 250, 400))
  const [liveConfidence, setLiveConfidence] = useState<PredictRequest['confidence']>('h')

  const [result, setResult] = useState<PredictResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const liveRequest = useDebouncedValue(
    {
      ...baseForm,
      brightness: liveBrightness,
      frp: liveFrp,
      bright_t31: liveBrightT31,
      confidence: liveConfidence,
    },
    200,
  )

  useEffect(() => {
    const controller = new AbortController()
    predict(liveRequest, controller.signal)
      .then((res) => {
        setResult(res)
        setError(null)
      })
      .catch((e) => {
        if (e.name !== 'AbortError') setError(String(e.message ?? e))
      })
    return () => controller.abort()
  }, [liveRequest])

  return (
    <section className="mx-auto max-w-[1216px] px-6 py-16">
      <SectionTitle eyebrow="Step 02" title="Live Fire Risk Interaction" icon={<Radio size={26} strokeWidth={1.5} className="text-copper" aria-hidden="true" />} />

      <div className="grid gap-6 lg:grid-cols-2">
        <Reveal>
          <SpotlightCard className="h-full p-6">
            <h3 className="mb-6 text-[16px] font-semibold text-silver">Adjust satellite parameters</h3>
            <div className="space-y-6">
              <Slider label="Brightness" value={liveBrightness} min={250} max={450} onChange={setLiveBrightness} />
              <Slider label="FRP" value={liveFrp} min={0} max={100} step={0.5} onChange={setLiveFrp} />
              <Slider label="Brightness T31" value={liveBrightT31} min={250} max={400} onChange={setLiveBrightT31} />
              <SelectField
                label="Satellite Confidence"
                value={liveConfidence}
                onChange={setLiveConfidence}
                options={[
                  { label: 'High (h)', value: 'h' },
                  { label: 'Low (l)', value: 'l' },
                  { label: 'Nominal (n)', value: 'n' },
                ]}
              />
            </div>
          </SpotlightCard>
        </Reveal>

        <Reveal delay={0.1} className="flex flex-col gap-6">
          {result ? (
            <>
              <RiskCard label="LIVE RISK" risk={result.predicted_risk} confidence={result.confidence_score} message="Recalculated instantly as you move the sliders." />
              <SpotlightCard className="p-6">
                <RiskProbabilityChart data={result.prediction_proba} compact />
              </SpotlightCard>
              <FireDetectionCard detected={result.fire_detected} brightnessDifference={result.brightness_difference} frp={result.frp} />
            </>
          ) : (
            <div className="flex h-full items-center justify-center rounded-[10px] border border-graphite p-8 text-[14px] text-steel">
              {error ? `Live prediction unavailable: ${error}` : 'Calculating live risk…'}
            </div>
          )}
        </Reveal>
      </div>
    </section>
  )
}

function clamp(v: number, min: number, max: number) {
  return Math.min(max, Math.max(min, v))
}
