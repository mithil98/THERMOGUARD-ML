import { Flame } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-graphite py-16 text-center">
      <div className="mx-auto flex max-w-[1216px] flex-col items-center gap-3 px-6">
        <div className="flex items-center gap-2">
          <Flame size={18} strokeWidth={1.5} className="text-copper" aria-hidden="true" />
          <span className="font-display text-[20px] text-paper-white">ThermoGuard AI</span>
        </div>
        <p className="text-[16px] text-fog">AI-Based Wildfire Risk Prediction System</p>
        <p className="text-[13px] text-ash">
          Satellite Hotspot → Fire Detection → Source Analysis → Risk Assessment → Alert → Report
        </p>
      </div>
    </footer>
  )
}
