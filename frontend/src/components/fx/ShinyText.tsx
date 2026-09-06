import React from 'react'
import { motion, useMotionValue, useAnimationFrame, useTransform, useReducedMotion } from 'motion/react'
import { useRef, useEffect } from 'react'

// Adapted from reactbits.dev's ShinyText, recolored to Fog -> Bone
// (the style guide's "workhorse gray" sweeping to the high-emphasis white).

interface ShinyTextProps {
  text: string
  speed?: number
  className?: string
  color?: string
  shineColor?: string
}

const ShinyText: React.FC<ShinyTextProps> = ({
  text,
  speed = 2.5,
  className = '',
  color = '#9194a1',
  shineColor = '#ffffff',
}) => {
  const progress = useMotionValue(0)
  const elapsedRef = useRef(0)
  const lastTimeRef = useRef<number | null>(null)
  const animationDuration = speed * 1000
  const reduceMotion = useReducedMotion()

  useAnimationFrame((time) => {
    if (reduceMotion) return
    if (lastTimeRef.current === null) {
      lastTimeRef.current = time
      return
    }
    const deltaTime = time - lastTimeRef.current
    lastTimeRef.current = time
    elapsedRef.current += deltaTime

    const cycleTime = elapsedRef.current % (animationDuration + 1500)
    if (cycleTime < animationDuration) {
      progress.set((cycleTime / animationDuration) * 100)
    } else {
      progress.set(100)
    }
  })

  useEffect(() => {
    elapsedRef.current = 0
  }, [])

  const backgroundPosition = useTransform(progress, (p) => `${150 - p * 2}% center`)

  return (
    <motion.span
      className={`inline-block ${className}`}
      style={{
        backgroundImage: `linear-gradient(120deg, ${color} 0%, ${color} 35%, ${shineColor} 50%, ${color} 65%, ${color} 100%)`,
        backgroundSize: '200% auto',
        WebkitBackgroundClip: 'text',
        backgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundPosition,
      }}
    >
      {text}
    </motion.span>
  )
}

export default ShinyText
