import { useId } from 'react'

interface SliderProps {
  label: string
  value: number
  min: number
  max: number
  step?: number
  unit?: string
  onChange: (v: number) => void
}

export default function Slider({ label, value, min, max, step = 1, unit = '', onChange }: SliderProps) {
  const id = useId()
  const pct = ((value - min) / (max - min)) * 100

  return (
    <div>
      <div className="mb-2 flex items-baseline justify-between">
        <label htmlFor={id} className="text-[13px] font-semibold tracking-[-0.02em] text-fog">
          {label}
        </label>
        <span className="text-[15px] font-medium text-bone" aria-hidden="true">
          {value.toFixed(step < 1 ? 1 : 0)}
          {unit}
        </span>
      </div>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        aria-valuetext={`${value.toFixed(step < 1 ? 1 : 0)}${unit}`}
        onChange={(e) => onChange(e.target.valueAsNumber)}
        className="h-[3px] w-full cursor-pointer appearance-none rounded-full bg-graphite accent-copper touch-manipulation focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-copper"
        style={{
          background: `linear-gradient(to right, #cc9166 ${pct}%, #1c1d22 ${pct}%)`,
        }}
      />
    </div>
  )
}
