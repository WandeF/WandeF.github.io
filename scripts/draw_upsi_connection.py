#!/usr/bin/env python3
"""Render a vector UPSI detail figure using the manuscript architecture palette.
Requires CairoSVG and Times New Roman. Not required by the website build.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import argparse
import cairosvg

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets')
dest = parser.parse_args().output
dest.mkdir(parents=True, exist_ok=True)
W, H = 1680, 1110
parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>UPSI, adapters and physical simulators</title>
<desc>One adapter connects one selected physical simulator to UPSI. Red arrows return measurements, blue arrows carry commands, and dashed black arrows indicate stepping calls. Three rows show alternative backends, not simultaneous coupling.</desc>
<defs>''']
for name, color in [('measurement','#ff4775'),('command','#5287e8'),('step','#222222')]:
    parts.append(f'<marker id="{name}" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L9,3.5 L0,7 Z" fill="{color}"/></marker>')
parts.append('</defs><rect width="1680" height="1110" fill="white"/>')

def box(x,y,w,h,fill,stroke,rx=12):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def text(x,y,words,size=25,bold=False,anchor='middle'):
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Times New Roman" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="black">{escape(words)}</text>')
def line(x1,y1,x2,y2,kind):
    color={'measurement':'#ff4775','command':'#5287e8','step':'#222222'}[kind]
    dash=' stroke-dasharray="9 6"' if kind=='step' else ''
    parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="2.5"{dash} marker-end="url(#{kind})"/>')

def icon(x,y,kind):
    # Small monochrome outline symbols echo the manuscript's component icons.
    parts.append(f'<g transform="translate({x} {y})" fill="none" stroke="#333" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">')
    if kind=='database':
        parts.append('<ellipse cx="15" cy="5" rx="13" ry="5"/><path d="M2,5 V29 C2,36 28,36 28,29 V5 M2,13 C2,20 28,20 28,13 M2,21 C2,28 28,28 28,21"/>')
    elif kind=='adapter':
        parts.append('<path d="M3,2 H21 L29,10 V34 H3 Z M21,2 V10 H29 M9,15 H23 M9,21 H23 M9,27 H19"/>')
    elif kind=='water':
        parts.append('<path d="M16,1 C12,9 5,16 5,22 A11,11 0 0 0 27,22 C27,16 20,9 16,1 Z M2,35 Q9,30 16,35 T30,35"/>')
    elif kind=='power':
        parts.append('<path d="M19,1 L4,21 H15 L11,36 L29,14 H17 Z"/>')
    elif kind=='thermal':
        parts.append('<path d="M10,4 A5,5 0 0 1 20,4 V23 A9,9 0 1 1 10,23 Z M15,10 V28 M23,8 H29 M23,15 H29"/>')
    elif kind=='control':
        parts.append('<rect x="1" y="1" width="30" height="22"/><path d="M9,29 H24 M16,23 V29 M7,7 V17 M13,7 V17 M19,7 V17 M25,7 V17"/>')
    parts.append('</g>')

# Shared control loop above the physical layer.
box(40,28,450,150,'#edf4e9','#9eab97')
icon(62,56,'control')
text(286,65,'Control & SCADA Layer',29,True)
text(265,107,'PLC / SCADA / Network',25)
text(265,147,'Shared control and communication loop',22)
text(1080,68,'UPSI and Physical Simulator Integration',33,True)
text(1080,112,'Unified operations, simulator-specific adapters',25)
text(1080,151,'Select one backend per scene',24)

# Original physical-layer colors, rounded panels and serif typography.
box(25,266,1630,685,'#fef7e9','#d9bc8a')
text(840,306,'Physical Layer',32,True)
line(156,342,156,178,'measurement')
text(142,229,'Measurements',22,anchor='end')
line(355,178,355,342,'command')
text(369,229,'Commands',22,anchor='start')
box(55,342,405,563,'#fdf9ed','#d9bc8a')
icon(83,370,'database')
text(275,401,'1) UPSI',32,True)
text(257,449,'Unified Physical Simulation Interface',23)
text(257,497,'Signals, units & physical time',25)
parts.append('<path d="M85,525 H430" stroke="#d9bc8a" stroke-width="1.5"/>')
for y, main, sub in [(573,'describe()','Ports, types and capabilities'),(657,'initialize()','Model settings and initial state'),(741,'advance(until_s, inputs)','Control inputs and target time'),(825,'close()','Release model resources')]:
    text(257,y,main,26,True);text(257,y+33,sub,22)
text(802,342,'2) Simulator-specific Adapters',28,True)
text(1390,342,'3) Physical Simulators',28,True)

rows=[(370,'EPANET adapter','Water-network variables','EPANET','Levels / pressures / flows','water'),
      (550,'pandapower adapter','Power-system variables','pandapower','Voltages / currents / power','power'),
      (730,'Thermal-box adapter','Thermal-model variables','Thermal model','Temperature / heater state','thermal')]
for y, adapter, description, model, variables, kind in rows:
    box(630,y,345,155,'#fdf9ed','#d9bc8a',8)
    icon(647,y+18,'adapter')
    text(819,y+40,adapter,27,True)
    text(802,y+85,description,23)
    text(802,y+125,'Native API calls & result mapping',21)
    box(1190,y,420,155,'#fdf9ed','#d9bc8a',8)
    icon(1208,y+18,kind)
    text(1420,y+40,model,28,True)
    text(1400,y+85,variables,23)
    text(1400,y+125,'Model equations & numerical solver',22)
    # Measurements travel toward UPSI; commands and stepping travel to the solver.
    for left,right in [(460,630),(975,1190)]:
        line(right,y+32,left,y+32,'measurement')
        line(left,y+78,right,y+78,'command')
        line(left,y+122,right,y+122,'step')

# Legend mirrors the manuscript arrow key, with explicit directions and payloads.
box(40,978,1600,104,'#fff','#9eab97',8)
for x, kind, title, payload in [(68,'measurement','Measurements / results','outputs, time_s, status'),(610,'command','Control inputs','pump / switch / heater commands'),(1160,'step','Stepping calls','advance(until_s, inputs)')]:
    line(x,1008,x+80,1008,kind)
    text(x+95,1016,title,24,anchor='start')
    text(x+95,1054,payload,21,anchor='start')
parts.append('</svg>')
svg='\n'.join(parts).encode()
path=dest/'upsi_physical_connections.svg'
path.write_bytes(svg)
cairosvg.svg2png(bytestring=svg,write_to=str(path.with_suffix('.png')))
cairosvg.svg2pdf(bytestring=svg,write_to=str(path.with_suffix('.pdf')))
print(path)
