/** Local replacement for the Tailwind Play CDN (was <script src="https://cdn.tailwindcss.com">).
 *  Build with:  npx tailwindcss@3 -i assets/tw-input.css -o assets/tw.css --minify
 */
module.exports = {
  content: [
    "./index.html",
    "./articles/**/*.html",
    "./encyclopedia/**/*.html",
    "./assets/**/*.js",
  ],
  theme: { extend: {} },
  plugins: [],
};
