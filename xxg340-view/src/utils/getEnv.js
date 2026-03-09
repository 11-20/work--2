import fs from 'fs'
import path from 'path'
import dotenv from 'dotenv'

export function isDevFn(mode) {
	return mode === 'development'
}

export function isProdFn(mode) {
	return mode === 'production'
}

/**
 * 是否生成预览包
 */
export function isReportMode() {
	return process.env.VITE_REPORT === 'true'
}

// 将所有环境变量配置文件读取到process.env
export function wrapperEnv(envConf) {
	const ret = {}
	for (const envName of Object.keys(envConf)) {
		let realName = envConf[envName].replace(/\\n/g, '\n')
		realName = realName === 'true' ? true : realName === 'false' ? false : realName

		if (envName === 'VITE_PORT') {
			realName = Number(realName)
		}
		if (envName === 'VITE_PROXY') {
			try {
				realName = JSON.parse(realName)
			} catch (error) {}
		}
		ret[envName] = realName
		process.env[envName] = realName
	}
	return ret
}

/**
 * 获取以指定前缀开头的环境变量
 * @param match 前缀
 * @param confFiles 配置文件
 */
export function getEnvConfig(match = 'VITE_GLOB_', confFiles = ['.env', '.env.production']) {
	let envConfig = {}
	confFiles.forEach(item => {
		try {
			const env = dotenv.parse(fs.readFileSync(path.resolve(process.cwd(), item)))
			envConfig = { ...envConfig, ...env }
		} catch (error) {
			console.error(`Error in parsing ${item}`, error)
		}
	})

	Object.keys(envConfig).forEach(key => {
		const reg = new RegExp(`^(${match})`)
		if (!reg.test(key)) {
			Reflect.deleteProperty(envConfig, key)
		}
	})
	return envConfig
}

/**
 * 获取用户根目录
 * @param dir file path
 */
export function getRootPath(...dir) {
	return path.resolve(process.cwd(), ...dir)
}
