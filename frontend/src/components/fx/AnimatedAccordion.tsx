import { AnimatePresence, motion } from 'motion/react'
import { ChevronDown } from 'lucide-react'
import { useId, useState, type ReactNode } from 'react'

interface AnimatedAccordionProps {
  title: string
  children: ReactNode
  defaultOpen?: boolean
}

export default function AnimatedAccordion({ title, children, defaultOpen = false }: AnimatedAccordionProps) {
  const [open, setOpen] = useState(defaultOpen)
  const panelId = useId()

  return (
    <div className="overflow-hidden rounded-[10px] border border-graphite bg-onyx">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={panelId}
        className="flex w-full items-center justify-between px-6 py-5 text-left outline-none focus-visible:ring-2 focus-visible:ring-copper focus-visible:ring-inset"
      >
        <span className="text-[18px] font-medium text-bone">{title}</span>
        <motion.span animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.3 }}>
          <ChevronDown size={18} strokeWidth={1.5} className="text-steel" aria-hidden="true" />
        </motion.span>
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            id={panelId}
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
            className="overflow-hidden"
          >
            <div className="border-t border-graphite px-6 py-5">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
