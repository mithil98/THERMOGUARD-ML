export function riskTone(risk: string): { border: string; text: string; bg: string; dot: string } {
  const r = risk.toLowerCase()
  if (r === 'high') {
    return { border: 'border-[#c47768]/50', text: 'text-[#e8a898]', bg: 'bg-[#c47768]/10', dot: 'bg-[#c47768]' }
  }
  if (r === 'medium') {
    return { border: 'border-[#c9974f]/50', text: 'text-[#e6b878]', bg: 'bg-[#c9974f]/10', dot: 'bg-[#c9974f]' }
  }
  return { border: 'border-[#7fae8e]/50', text: 'text-[#9fcaac]', bg: 'bg-[#7fae8e]/10', dot: 'bg-[#7fae8e]' }
}
