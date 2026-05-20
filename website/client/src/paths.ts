const rawBase = import.meta.env.BASE_URL || '/'
const basePath = rawBase === '/' ? '' : rawBase.replace(/\/+$/, '')

export function appPath(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`
  return `${basePath}${normalized}`
}

export function stripBasePath(pathname: string): string {
  if (!basePath) return pathname
  if (pathname === basePath) return '/'
  if (pathname.startsWith(`${basePath}/`)) {
    return pathname.slice(basePath.length) || '/'
  }
  return pathname
}
