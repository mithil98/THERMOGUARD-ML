import type { PredictRequest } from '../types'

export default function InputSummaryTable({ form, season }: { form: PredictRequest; season: string }) {
  const rows: [string, string][] = [
    ['Latitude', form.latitude.toFixed(6)],
    ['Longitude', form.longitude.toFixed(6)],
    ['Brightness', form.brightness.toFixed(2)],
    ['Scan', form.scan.toFixed(2)],
    ['Track', form.track.toFixed(2)],
    ['Acquisition Time', String(form.acq_time)],
    ['Brightness T31', form.bright_t31.toFixed(2)],
    ['FRP', form.frp.toFixed(2)],
    ['Confidence', form.confidence],
    ['Day / Night', form.daynight],
    ['Hotspot Type', String(form.fire_type)],
    ['Satellite Version', form.version],
    ['Observation Date', form.observation_date],
    ['Observation Time', form.observation_time],
    ['Season', season],
  ]

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-[15px]">
        <thead>
          <tr className="border-b border-graphite">
            <th className="py-3 text-left font-medium text-fog">Parameter</th>
            <th className="py-3 text-right font-medium text-fog">Value</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([k, v]) => (
            <tr key={k} className="border-b border-graphite">
              <td className="py-3 text-bone">{k}</td>
              <td className="py-3 text-right text-bone">{v}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
