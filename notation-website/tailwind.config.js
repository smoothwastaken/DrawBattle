module.exports = {
  // mode: "jit",
  purge: ["./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      sans: ["ui-sans-serif", "system-ui"],
      serif: ["ui-serif", "Georgia"],
      mono: ["ui-monospace", "SFMono-Regular"],
      title: ["Gilroy"],
      display: ["SofiaPro"],
      body: ["SofiaPro"],
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
