import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: process.env.port || 3000,
    host: true,
  },
  plugins: [react()],
});
