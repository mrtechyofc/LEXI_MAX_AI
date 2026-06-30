import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        lexi: {
          bg: "#05070d",
          panel: "#0b1018",
          accent: "#5eead4",
          accent2: "#60a5fa",
          text: "#e5e7eb",
          muted: "#9ca3af",
          danger: "#f87171",
        },
      },
      fontFamily: { mono: ["ui-monospace", "SFMono-Regular", "monospace"] },
    },
  },
  plugins: [],
};
export default config;
