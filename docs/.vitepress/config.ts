import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Hybrid Infrastructure Toolkit',
  description: 'Configurable, repeatable hybrid infrastructure labs and reference environments.',
  base: '/hybrid-infra-toolkit/',
  cleanUrls: true,
  lastUpdated: true,

  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Demos', link: '/demos/' },
      { text: 'Design', link: '/design/deployment-and-implementation' },
      { text: 'Project', link: '/project/about' },
    ],

    sidebar: [
      {
        text: 'Demos',
        items: [
          { text: 'Overview', link: '/demos/' },
          {
            text: 'Hyper-V Cluster Lab',
            collapsed: true,
            items: [
              { text: '1. Architecture overview', link: '/demos/hyperv-cluster-lab/01-architecture-overview' },
              { text: '2. Prerequisites', link: '/demos/hyperv-cluster-lab/02-prerequisites' },
              { text: '3. Host VM sizing', link: '/demos/hyperv-cluster-lab/03-host-vm-sizing' },
              { text: '4. Networking', link: '/demos/hyperv-cluster-lab/04-networking' },
              { text: '5. Active Directory', link: '/demos/hyperv-cluster-lab/05-active-directory' },
              { text: '6. iSCSI storage', link: '/demos/hyperv-cluster-lab/06-iscsi-storage' },
              { text: '7. Hyper-V cluster', link: '/demos/hyperv-cluster-lab/07-hyper-v-cluster' },
              { text: '8. Cloud witness', link: '/demos/hyperv-cluster-lab/08-cloud-witness' },
              { text: '9. WAC virtualization mode', link: '/demos/hyperv-cluster-lab/09-wac-virtualization-mode' },
              { text: '10. SCVMM setup', link: '/demos/hyperv-cluster-lab/10-scvmm-setup' },
              { text: '11. BGP routing', link: '/demos/hyperv-cluster-lab/11-bgp-routing-connectivity' },
              { text: '12. Deployment workflow', link: '/demos/hyperv-cluster-lab/12-deployment-workflow' },
              { text: '13. Demo day guide', link: '/demos/hyperv-cluster-lab/13-demo-day-guide' },
              { text: '14. Platform roadmap', link: '/demos/hyperv-cluster-lab/14-platform-roadmap' },
            ],
          },
        ],
      },
      {
        text: 'Project',
        items: [
          { text: 'About', link: '/project/about' },
          { text: 'Roadmap', link: '/project/roadmap' },
          { text: 'Changelog', link: '/project/changelog' },
          { text: 'Open source', link: '/project/open-source' },
          { text: 'Contributing', link: '/project/contributing' },
        ],
      },
      {
        text: 'Standards',
        items: [
          { text: 'Engineering standards', link: '/standards/engineering-standards' },
        ],
      },
      {
        text: 'Design',
        items: [
          { text: 'Deployment and implementation', link: '/design/deployment-and-implementation' },
          { text: 'CI/CD automation', link: '/design/ci-cd-automation' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/Hybrid-Solutions-Cloud/hybrid-infra-toolkit' },
    ],

    search: { provider: 'local' },

    editLink: {
      pattern: 'https://github.com/Hybrid-Solutions-Cloud/hybrid-infra-toolkit/edit/main/docs/:path',
      text: 'Edit this page on GitHub',
    },

    footer: {
      message: 'A Hybrid Solutions Cloud lab project.',
      copyright: 'Hybrid Solutions Cloud',
    },
  },

  markdown: {
    lineNumbers: true,
  },
})
