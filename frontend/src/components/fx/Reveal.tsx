import { motion } from 'motion/react'
import type { ReactNode } from 'react'

// A lightweight, motion/react-native scroll-reveal, in the spirit of
// reactbits.dev's AnimatedContent/ScrollReveal but without pulling in gsap
// as a second animation runtime.

interface RevealProps {
  children: ReactNode
  className?: string
  delay?: number
  y?: number
}

export default function Reveal({ children, className = '', delay = 0, y = 24 }: RevealProps) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  )
}
