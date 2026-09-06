import { motion } from 'motion/react'
import GradientText from './fx/GradientText'
import ShinyText from './fx/ShinyText'

export default function Hero() {
  return (
    <section className="mx-auto max-w-[1216px] px-6 pt-20 pb-16 text-center">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
      >
        <span className="mb-6 inline-block rounded-full border border-slate px-3 py-1.5 text-[13px] font-semibold tracking-[-0.02em] text-copper">
          SATELLITE HOTSPOT INTELLIGENCE
        </span>

        <h1 className="font-display text-balance text-[44px] leading-[1.13] text-paper-white sm:text-[64px] lg:text-[88px]">
          Wildfire risk,{' '}
          <GradientText className="font-display">read in real time</GradientText>
        </h1>

        <p className="mx-auto mt-6 max-w-[640px] text-[18px] leading-[1.5] text-mist sm:text-[20px]">
          <ShinyText text="AI-based wildfire risk prediction and fire source analysis" speed={3.5} />
          <br />
          built on NASA satellite hotspot telemetry.
        </p>
      </motion.div>
    </section>
  )
}
