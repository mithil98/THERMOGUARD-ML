import { useRef, type ReactNode } from 'react'
import { motion, useMotionValue, useAnimationFrame, useTransform, useReducedMotion } from 'motion/react'

// Adapted from reactbits.dev's GradientText (TS+Tailwind variant), retuned to
// the Dashboard_Design.md gilded-gradient palette instead of the stock purple/pink.

interface GradientTextProps {
  children: ReactNode
  className?: string
  colors?: string[]
  animationSpeed?: number
  direction?: 'horizontal' | 'vertical' | 'diagonal'
}

export default function GradientText({
  children,
  className = '',
  colors = ['#ae9357', '#fff0cc', '#ae9357', '#cc9166'],
  animationSpeed = 6,
  direction = 'horizontal',
}: GradientTextProps) {
  const progress = useMotionValue(0)
  const elapsedRef = useRef(0)
  const lastTimeRef = useRef<number | null>(null)
  const reduceMotion = useReducedMotion()

  const animationDuration = animationSpeed * 1000

  useAnimationFrame((time) => {
    if (reduceMotion) return
    if (lastTimeRef.current === null) {
      lastTimeRef.current = time
      return
    }
    const deltaTime = time - lastTimeRef.current
    lastTimeRef.current = time
    elapsedRef.current += deltaTime

    const fullCycle = animationDuration * 2
    const cycleTime = elapsedRef.current % fullCycle

    if (cycleTime < animationDuration) {
      progress.set((cycleTime / animationDuration) * 100)
    } else {
      progress.set(100 - ((cycleTime - animationDuration) / animationDuration) * 100)
    }
  })

  const backgroundPosition = useTransform(progress, (p) =>
    direction === 'vertical' ? `50% ${p}%` : `${p}% 50%`,
  )

  const gradientAngle = direction === 'vertical' ? 'to bottom' : direction === 'diagonal' ? 'to bottom right' : 'to right'
  const gradientColors = [...colors, colors[0]].join(', ')

  return (
    <motion.span
      className={`inline-block bg-clip-text text-transparent ${className}`}
      style={{
        backgroundImage: `linear-gradient(${gradientAngle}, ${gradientColors})`,
        backgroundSize: '300% 100%',
        backgroundPosition,
        WebkitBackgroundClip: 'text',
      }}
    >
      {children}
    </motion.span>
  )
}
