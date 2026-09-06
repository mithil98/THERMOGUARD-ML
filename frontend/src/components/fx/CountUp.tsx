import { useInView, useMotionValue, useSpring } from 'motion/react'
import { useCallback, useEffect, useRef } from 'react'

// Ported near-verbatim from reactbits.dev's CountUp (TS+Tailwind variant).

interface CountUpProps {
  to: number
  from?: number
  duration?: number
  className?: string
  decimals?: number
  suffix?: string
}

export default function CountUp({ to, from = 0, duration = 1.2, className = '', decimals, suffix = '' }: CountUpProps) {
  const ref = useRef<HTMLSpanElement>(null)
  const motionValue = useMotionValue(from)

  const damping = 20 + 40 * (1 / duration)
  const stiffness = 100 * (1 / duration)

  const springValue = useSpring(motionValue, { damping, stiffness })
  const isInView = useInView(ref, { once: true, margin: '0px' })

  const formatValue = useCallback(
    (latest: number) => {
      const d = decimals ?? (Number.isInteger(to) ? 0 : 2)
      return latest.toFixed(d) + suffix
    },
    [decimals, to, suffix],
  )

  useEffect(() => {
    if (ref.current) ref.current.textContent = formatValue(from)
  }, [from, formatValue])

  useEffect(() => {
    if (isInView) motionValue.set(to)
  }, [isInView, motionValue, to])

  useEffect(() => {
    const unsubscribe = springValue.on('change', (latest) => {
      if (ref.current) ref.current.textContent = formatValue(latest)
    })
    return () => unsubscribe()
  }, [springValue, formatValue])

  return <span className={className} ref={ref} />
}
