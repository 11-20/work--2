import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
import viteCompression from 'vite-plugin-compression'
import { wrapperEnv } from "./src/utils/getEnv";
import { resolve } from "path";
export default defineConfig((mode) => {
	const env = loadEnv(mode, process.cwd())
	const viteEnv = wrapperEnv(env)
	return {
		base: "./",
		resolve: {
			alias: {
				"@": resolve(__dirname, "./src")
			}
		},
		css: {
			preprocessorOptions: {
				scss: {
					// 全局公共scss
					additionalData: `@import "@/styles/var.scss";`
				}
			}
		},
		server: {
			// 服务器主机名，如果允许外部访问，可设置为 "0.0.0.0"
			host: "0.0.0.0",
			port: 3301,
			// 方案一：直接指定具体页面（硬编码）
			open: "#/login",  // 例如打开登录页
		
			cors: true,
			proxy: {
				"/api": {
					target: "http://127.0.0.1:8080", // easymock：https://mock.mengxuegu.com/ 生成假数据
					changeOrigin: true,
					rewrite: path => path.replace(/^\/api/, "")
				}
			}
		},
		plugins: [
			vue(),
			// * EsLint 报错信息显示在浏览器界面上
			// eslintPlugin(),
			// * vite 可以使用 jsx/tsx 语法
			vueJsx(),
			// * 组件的 name 可以写在 script 标签上
			VueSetupExtend(),
			// * 是否生成包预览(分析依赖包大小,方便做优化处理)
			viteEnv.VITE_REPORT && visualizer(),
			// * gzip compress
			viteEnv.VITE_BUILD_GZIP &&
			viteCompression({
				verbose: true,
				disable: false,
				threshold: 10240,
				algorithm: "gzip",
				ext: ".gz"
			}),
		],
	
		build: {
			outDir: "dist",
			minify: "esbuild",
			// esbuild 打包更快，但是不能去除 console.log，terser打包慢，但能去除 console.log
			// minify: "terser",
			// terserOptions: {
			// 	compress: {
			// 		drop_console: viteEnv.VITE_DROP_CONSOLE,
			// 		drop_debugger: true
			// 	}
			// },
			chunkSizeWarningLimit: 1500,
			rollupOptions: {
				output: {
					// Static resource classification and packaging
					chunkFileNames: "assets/js/[name]-[hash].js",
					entryFileNames: "assets/js/[name]-[hash].js",
					assetFileNames: "assets/[ext]/[name]-[hash].[ext]"
				}
			}
		}
	}
})