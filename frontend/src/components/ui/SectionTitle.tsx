import type { ReactNode } from 'react'
import Reveal from '../fx/Reveal'

export default function SectionTitle({
  eyebrow,
  title,
  icon,
}: {
  eyebrow?: string
  title: string
  icon?: ReactNode
}) {
  return (
    <Reveal className="mb-8">
      {eyebrow && (
        <span className="mb-2 block text-[13px] font-semibold tracking-[-0.02em] text-copper">{eyebrow}</span>
      )}
      <h2 className="font-display flex items-center gap-3 text-balance text-[28px] text-paper-white sm:text-[36px]">
        {icon}
        {title}
      </h2>
    </Reveal>
  )
}
