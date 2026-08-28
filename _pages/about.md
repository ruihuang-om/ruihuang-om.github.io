---
layout: site
title: "Home"
permalink: /
nav_key: home
---

<section class="profile-hero">
  <div class="profile-hero__media">
    <img src="{{ '/images/rui_profile.jpg' | relative_url }}" alt="Portrait of Rui Huang">
    <div class="profile-links" aria-label="Academic profiles">
      <a href="mailto:{{ site.author.email }}">Email</a>
      <a href="{{ site.author.googlescholar }}" target="_blank" rel="noopener">Google Scholar</a>
      <a href="{{ site.author.orcid }}" target="_blank" rel="noopener">ORCID</a>
      <a href="https://github.com/{{ site.author.github }}" target="_blank" rel="noopener">GitHub</a>
      <a href="{{ '/files/Rui_CV_2026_0827_V2.pdf' | relative_url }}" target="_blank" rel="noopener">CV</a>
    </div>
  </div>

  <div class="profile-hero__copy">
    <p class="eyebrow">Welcome</p>
    <h1>Hi! I'm Rui (Grace) Huang</h1>
    <p>I am a Ph.D. candidate in Management Science and Engineering at the University of Science and Technology of China.</p>
    <p>My research focuses on sustainable operations, electricity markets, energy-efficiency investment, and supply chain contracting.</p>
    <p>I am currently a joint Ph.D. student in Operations Management at Ivey Business School, Western University.</p>
  </div>
</section>

<section class="content-section research-interests">
  <h2>Research Interests</h2>
  <p><strong>Topics:</strong> Sustainable Operations, Energy and Electricity Markets, Energy-Efficiency Investment, and Supply Chain Contracting.</p>
  <p><strong>Methods:</strong> Game Theory, Optimization, and Econometric Analysis.</p>
</section>

<section class="content-section selected-research">
  <h2>Selected Research</h2>
  {% assign selected = site.publications | where: "selected", true | sort: "order" %}
  <ol class="research-list">
    {% for post in selected limit:3 %}
      {% include research-entry.html post=post %}
    {% endfor %}
  </ol>
  <p class="section-link"><a href="{{ '/research/' | relative_url }}">View all research &rarr;</a></p>
</section>
