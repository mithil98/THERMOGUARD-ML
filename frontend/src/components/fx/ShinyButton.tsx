import { motion } from 'motion/react'
import type { ButtonHTMLAttributes, ReactNode } from 'react'

interface ShinyButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode
  variant?: 'primary' | 'ghost'
}

// Primary Action Button / Ghost Outline Button from Dashboard_Design.md,
// with a reactbits-style diagonal sheen sweep on hover.

export default function ShinyButton({ children, variant = 'primary', className = '', ...props }: ShinyButtonProps) {
  const base =
    'relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-full px-6 py-3 text-[14px] font-medium transition-transform active:scale-[0.98] disabled:opacity-40 disabled:pointer-events-none outline-none focus-visible:ring-2 focus-visible:ring-copper focus-visible:ring-offset-2 focus-visible:ring-offset-obsidian'

  const variantClass =
    variant === 'primary'
      ? 'bg-paper-white text-black'
      : 'border border-white/70 text-bone bg-transparent'

  return (
    <motion.button
      whileHover={{ scale: 1.015 }}
      whileTap={{ scale: 0.98 }}
      className={`${base} ${variantClass} ${className}`}
      {...(props as any)}
    >
      <span className="relative z-10 flex items-center gap-2">{children}</span>
      <motion.span
        aria-hidden
        className="pointer-events-none absolute inset-0"
        initial={{ x: '-120%' }}
        whileHover={{ x: '120%' }}
        transition={{ duration: 0.7, ease: 'easeInOut' }}
        style={{
          background:
            variant === 'primary'
              ? 'linear-gradient(115deg, transparent 30%, rgba(0,0,0,0.12) 50%, transparent 70%)'
              : 'linear-gradient(115deg, transparent 30%, rgba(255,255,255,0.16) 50%, transparent 70%)',
        }}
      />
    </motion.button>
  )
}
