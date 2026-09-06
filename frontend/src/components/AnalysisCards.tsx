import type { ReactNode } from 'react'
import { Flame, Zap, Thermometer, Sun, Moon, MapPin } from 'lucide-react'
import type { PredictResponse } from '../types'
import CountUp from './fx/CountUp'
import SpotlightCard from './fx/SpotlightCard'
import Reveal from './fx/Reveal'

function StatTile({ icon, label, value, suffix = '' }: { icon: ReactNode; label: string; value: number; suffix?: string }) {
  return (
    <SpotlightCard className="p-5">
      <div className="mb-3 flex items-center gap-2 text-fog">
        {icon}
        <span className="text-[13px] font-semibold tracking-[-0.02em]">{label}</span>
      </div>
      <div className="font-display text-[28px] text-paper-white">
        <CountUp to={value} decimals={2} suffix={suffix} duration={1} />
      </div>
    </SpotlightCard>
  )
}

function AnalysisCard({ title, message }: { title: string; message: string }) {
  return (
    <SpotlightCard className="p-6">
      <h3 className="text-[18px] font-semibold text-bone">{title}</h3>
      <p className="mt-2 text-[15px] leading-[1.5] text-mist">{message}</p>
    </SpotlightCard>
  )
}

export default function AnalysisCards({ result, latitude, longitude }: { result: PredictResponse; latitude: number; longitude: number }) {
  return (
    <div className="space-y-8">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Reveal delay={0}>
          <StatTile icon={<Flame size={16} strokeWidth={1.5} aria-hidden="true" />} label="Brightness" value={result.brightness} />
        </Reveal>
        <Reveal delay={0.05}>
          <StatTile icon={<Zap size={16} strokeWidth={1.5} aria-hidden="true" />} label="FRP" value={result.frp} />
        </Reveal>
        <Reveal delay={0.1}>
          <StatTile icon={<Thermometer size={16} strokeWidth={1.5} aria-hidden="true" />} label="Brightness Difference" value={result.brightness_difference} />
        </Reveal>
        <Reveal delay={0.15}>
          <SpotlightCard className="p-5">
            <div className="mb-3 flex items-center gap-2 text-fog">
              {result.daynight === 'D' ? (
                <Sun size={16} strokeWidth={1.5} aria-hidden="true" />
              ) : (
                <Moon size={16} strokeWidth={1.5} aria-hidden="true" />
              )}
              <span className="text-[13px] font-semibold tracking-[-0.02em]">Day / Night</span>
            </div>
            <div className="font-display text-[28px] text-paper-white">{result.daynight === 'D' ? 'Day' : 'Night'}</div>
          </SpotlightCard>
        </Reveal>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Reveal>
          <AnalysisCard title={`Fire Intensity — ${result.intensity}`} message={result.intensity_message} />
        </Reveal>
        <Reveal delay={0.05}>
          <AnalysisCard title={result.thermal_status} message={result.thermal_message} />
        </Reveal>
        <Reveal delay={0.1}>
          <AnalysisCard
            title={`Observation Period — ${result.daynight === 'D' ? 'Daytime' : 'Nighttime'}`}
            message={
              result.daynight === 'D'
                ? 'Daytime satellite observations may be affected by solar and surface conditions.'
                : 'Nighttime thermal observations can provide useful hotspot information.'
            }
          />
        </Reveal>
        <Reveal delay={0.15}>
          <SpotlightCard className="p-6">
            <div className="mb-1 flex items-center gap-2 text-bone">
              <MapPin size={16} strokeWidth={1.5} className="text-copper" aria-hidden="true" />
              <h3 className="text-[18px] font-semibold">Hotspot Location</h3>
            </div>
            <p className="text-[15px] leading-[1.6] text-mist">
              Latitude: <span className="text-bone">{latitude.toFixed(6)}</span>
              <br />
              Longitude: <span className="text-bone">{longitude.toFixed(6)}</span>
              <br />
              Observation Season: <span className="text-bone capitalize">{result.season}</span>
            </p>
          </SpotlightCard>
        </Reveal>
      </div>
    </div>
  )
}
