<div class="hero">
<div class="hero-kicker">CPS² Lab · Water CPS Security</div>
<h1>Hydro-CPS-Sim</h1>
<p>A co-simulation platform for the security research of water distribution cyber-physical systems. It connects hydraulic dynamics, PLC control, SCADA communications, and network simulation to support attack-impact evaluation and cross-layer analysis.</p>
<div class="hero-buttons"><a href="quickstart.html">Get started →</a><a href="architecture.html" class="outline">Explore architecture</a><a class="outline" href="https://github.com/WandeF/hydro-cps-sim" target="_blank" rel="noopener">GitHub ↗</a></div>
</div>

<span class="eyebrow">Project Overview</span>

## What can the platform do?

<div class="feature-grid">
<div class="feature"><span class="glyph">▤</span><strong>Cross-layer co-simulation</strong><p>Link hydraulic models, control logic, and communication processes to study how cyber events affect the physical network.</p></div>
<div class="feature"><span class="glyph">⌁</span><strong>Attack-impact evaluation</strong><p>Support research into MITM, DoS, and PLC logic modification scenarios. Runnable cases depend on the published code and configurations.</p></div>
<div class="feature"><span class="glyph">▦</span><strong>Reproducible workflows</strong><p>Organize experiments through configuration files and scripts, and export logs and CSV results for analysis.</p></div>
<div class="feature"><span class="glyph">◇</span><strong>Research extensibility</strong><p>Investigate control, network, and hydraulic effects within a modular experiment framework.</p></div>
</div>

## From network events to physical responses

<div class="layers"><div class="layer">Attack<small>MITM / DoS / Logic</small></div><div class="layer">Network<small>ns-3 + Namespace</small></div><div class="layer">SCADA / PLC<small>Data &amp; Control</small></div><div class="layer">Hydraulics<small>DHALSIM-epynet</small></div><div class="layer">Evidence<small>Logs / CSV</small></div></div>

The key research question is: **How do cyberattacks propagate through sensing, control decisions, and actuation into physical water-system behavior?**

## Start here

1. Read the [introduction](introduction.html).
2. Review [installation requirements](installation.html).
3. Follow the [quick-start guide](quickstart.html).
4. Explore the [experiment design](experiments.html).

> **Documentation status:** This is the deployed working draft of the research software documentation. Unverified configuration keys, publication details, and experiment claims are deliberately left as follow-up work.
