---
hide:
  - navigation
  - toc
  - title
---

<style>
/* Suppress the auto-injected page title on the home page */
.md-content__inner > h1:first-child { display: none !important; }
</style>

<div class="hero-section">
  <div class="hero-logo-col">
    <img class="hero-logo-full hero-logo--dark"  src="assets/img/logo-horizontal.svg"       alt="DataHub.local">
    <img class="hero-logo-full hero-logo--light" src="assets/img/logo-horizontal-light.svg" alt="DataHub.local">
  </div>
  <div class="hero-content-col">
    <p class="hero-tagline">Enterprise-grade data platform running on homelab Kubernetes. Built for learning, experimentation, and real-world results.</p>
    <div class="hero-badges">
      <a href="https://github.com/datahub-local"><img src="https://img.shields.io/badge/GitHub-datahub--local-181717?logo=github&logoColor=white" alt="GitHub Org"></a>
      <a href="https://github.com/datahub-local/datahub-local/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
      <a href="services/core/"><img src="https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo&logoColor=white" alt="GitOps"></a>
      <a href="https://datahub-local.alvsanand.com"><img src="https://img.shields.io/badge/Docs-datahub--local.alvsanand.com-00BCD4" alt="Docs"></a>
    </div>
    <a href="architecture/overview/" class="md-button md-button--primary">Explore Architecture</a>
    <a href="https://github.com/datahub-local" class="md-button">View on GitHub</a>
  </div>
</div>

<div class="stats-row">
  <div class="stat-item">
    <div class="stat-number">7</div>
    <div class="stat-label">Cluster Nodes</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">25+</div>
    <div class="stat-label">Running Services</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">44</div>
    <div class="stat-label">CPU Cores</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">100 GB</div>
    <div class="stat-label">Total RAM</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">~4 TB</div>
    <div class="stat-label">Total Storage</div>
  </div>
</div>

---

## What is DataHub.local?

**DataHub.local** is a personal homelab project that runs a complete, enterprise-grade data platform on hardware.
Think of it as a personal Snowflake/Databricks — running at home, on a Kubernetes cluster made of OrangePi boards, a NAS, and a laptop.

It is simultaneously a **portfolio project**, a **learning environment**, and a **real working platform** used daily for data workflows, media, AI inference, and home automation.

---

## Goals

<div class="grid cards goals-grid" markdown>

- :fontawesome-solid-server: **Infrastructure as Code**

    Deploy and maintain a production-grade Kubernetes cluster using GitOps, Ansible, and Helm — fully reproducible from a git repository.

- :fontawesome-solid-chart-line: **Data Platform**

    Design and run a scalable data lakehouse: ingestion → streaming → storage → transformation → visualization.

- :fontawesome-solid-robot: **AI & Automation**

    Self-host LLMs for inference, build AI-powered workflows in n8n, and run autonomous agents for SRE/DevOps tasks.

- :fontawesome-solid-shield-halved: **Security & Observability**

    Full-stack monitoring (metrics, logs, alerts), zero-trust networking with Tailscale, and OIDC-based SSO for all services.

- :fontawesome-solid-graduation-cap: **Portfolio & Learning**

    Every component here is a hands-on experiment — from kernel-level GPIO fan control to Iceberg table formats and LLM pipelines.

</div>

---

## About the Author

<div class="authors-grid">
  <div class="author-card">
    <img class="author-photo" src="https://avatars.githubusercontent.com/alvsanand" alt="Alvaro Santos Andres">
    <div class="author-info">
      <h3 class="author-name">Alvaro Santos Andres</h3>
      <p class="author-bio">
        Data &amp; AI engineer building production-grade platforms on open-source tech.
        DataHub.local is a real, running homelab — from Kubernetes on ARM64 to LLM pipelines and GitOps, built and improved in the open.
      </p>
      <div class="author-links">
        <a href="https://www.linkedin.com/in/alvsanand/" class="author-link author-link--linkedin" target="_blank" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          LinkedIn
        </a>
        <a href="https://github.com/alvsanand" class="author-link author-link--github" target="_blank" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
          GitHub
        </a>
      </div>
    </div>
  </div>
</div>
