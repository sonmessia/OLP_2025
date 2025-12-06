// Copyright (c) 2025 Green Wave Team
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: "GreenWave",
  tagline: "GreenWave get your way to a better environment",
  favicon: "../assets/docusaurus/logo.png",

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: "https://sonmessia.github.io",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.BASE_URL || "/GreenWave/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "sonmessia", // Usually your GitHub org/user name.
  projectName: "GreenWave", // Usually your repo name.

  onBrokenLinks: "throw",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en", "vi"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/sonmessia/GreenWave.git",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: "../assets/docusaurus/its.jpg",
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "GreenWave",
      logo: {
        alt: "GreenWave Logo",
        src: "/img/logo.png",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Tutorial",
        },
        { to: "/docs/installation", label: "Installation", position: "left" },
        {
          href: "https://github.com/sonmessia/GreenWave.git",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Tutorial",
              to: "/docs/intro",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "Discord",
              href: "https://discord.gg/taTcryge",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "Installation",
              to: "/docs/installation",
            },
            {
              label: "GitHub",
              href: "https://github.com/sonmessia/GreenWave.git",
            },
          ],
        },
      ],
      logo: {
        alt: "Hutech Logo",
        src: "/img/hutech_logo.png",
        href: "https://www.hutech.edu.vn/",
        height: 75,
      },
      copyright: `Copyright © ${new Date().getFullYear()} GreenWave, Inc. All rights reserved`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
