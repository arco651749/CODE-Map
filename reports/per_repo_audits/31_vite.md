# 🔬 CODE-Map 基準審查獨立驗證報告: `vite`
> **技術生態**: `TypeScript (現代前端打包管線 / HMR 廣播)`  
> **本地倉庫路徑**: `test_repos/vite`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 25 Files  
> **報告生成時間**: 2026-10-20 21:44:16  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `8` / `25` | `32.0%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `17` / `25` | `68.0%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `0` / `25` | `0.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`25` / `25`** | **`100.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `25` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `15c85dda`
- **完整 Hash**: `15c85ddae2bbbc3808d96a223a5a18a800883252`
- **說明 (Ground Truth)**: fix(create-vite): use typescript v6 for now (#23841)
- **變更檔案數**: 1

#### 📄 檔案: `packages/create-vite/src/index.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:53, E:38, A:0) ➔ After(N:53, E:38, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupEslint()`
- **變更前簽章 (Before)**: `function setupEslint(root: string, isTs: boolean)` (L879~L1053)
- **變更後簽章 (After)**: `function setupEslint(root: string, isTs: boolean)` (L879~L1050)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setupEslint(root: string, isTs: boolean) {
  // renovate: datasource=npm depName=@eslint/js
  const eslintJsVersion = '10.0.1'
  // renovate: datasource=npm depName=eslint
  const eslintVersion = '10.13.0'
  // renovate: datasource=npm depName=eslint-plugin-react-hooks
  const eslintPluginReactHooksVersion = '7.1.1'
  // renovate: datasource=npm depName=eslint-plugin-react-refresh
  const eslintPluginReactRefreshVersion = '0.5.7'
  // renovate: datasource=npm depName=globals
  const globalsVersion = '17.13.0'
  // renovate: datasource=npm depName=typescript-eslint
  const typescriptEslintVersion = '8.71.2'

  const eslintConfigForTS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
  },
])
`
  const eslintConfigForJS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
`

  fs.rmSync(path.resolve(root, '.oxlintrc.json'))

  const eslintConfig = isTs ? eslintConfigForTS : eslintConfigForJS
  fs.writeFileSync(path.resolve(root, 'eslint.config.js'), eslintConfig)

  editFile(path.resolve(root, 'package.json'), (content) => {
    const asObject = JSON.parse(content)
    const devDepsEntries = Object.entries(asObject.devDependencies).filter(
      ([name]) => name !== 'oxlint',
    )
    devDepsEntries.push(
      ['@eslint/js', `^${eslintJsVersion}`],
      ['eslint', `^${eslintVersion}`],
      ['eslint-plugin-react-hooks', `^${eslintPluginReactHooksVersion}`],
      ['eslint-plugin-react-refresh', `^${eslintPluginReactRefreshVersion}`],
      ['globals', `^${globalsVersion}`],
    )
    if (isTs) {
      devDepsEntries.push(['typescript-eslint', `^${typescriptEslintVersion}`])
      // Keep TypeScript 6 until typescript-eslint supports TypeScript 7.
      // https://github.com/typescript-eslint/typescript-eslint/issues/10940
      asObject.devDependencies.typescript = '~6.0.3'
    }
    devDepsEntries.sort()
    asObject.devDependencies = Object.fromEntries(devDepsEntries)
    asObject.scripts.lint = 'eslint .'
    return JSON.stringify(asObject, null, 2) + '\n'
  })

  editFile(path.resolve(root, 'README.md'), (content) => {
    content = content.replace(
      'with HMR and some Oxlint rules',
      'with HMR and some ESLint rules',
    )
    const headingIndex = content.indexOf(
      '## Expanding the Oxlint configuration',
    )
    if (headingIndex === -1) {
      console.warn('Could not update Oxlint section in README.md')
      return content
    }
    const eslintTypeAwareConfig = /* js */ `export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`
    const eslintReactConfig = /* js */ `// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`

    const eslintSection = isTs
      ? `## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

\`\`\`js
${eslintTypeAwareConfig}
\`\`\`

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

\`\`\`js
${eslintReactConfig}
\`\`\`
`
      : `## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [\`typescript-eslint\`](https://typescript-eslint.io) in your project.
`
    return content.slice(0, headingIndex) + eslintSection
  })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setupEslint(root: string, isTs: boolean) {
  // renovate: datasource=npm depName=@eslint/js
  const eslintJsVersion = '10.0.1'
  // renovate: datasource=npm depName=eslint
  const eslintVersion = '10.13.0'
  // renovate: datasource=npm depName=eslint-plugin-react-hooks
  const eslintPluginReactHooksVersion = '7.1.1'
  // renovate: datasource=npm depName=eslint-plugin-react-refresh
  const eslintPluginReactRefreshVersion = '0.5.7'
  // renovate: datasource=npm depName=globals
  const globalsVersion = '17.13.0'
  // renovate: datasource=npm depName=typescript-eslint
  const typescriptEslintVersion = '8.71.2'

  const eslintConfigForTS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
  },
])
`
  const eslintConfigForJS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
`

  fs.rmSync(path.resolve(root, '.oxlintrc.json'))

  const eslintConfig = isTs ? eslintConfigForTS : eslintConfigForJS
  fs.writeFileSync(path.resolve(root, 'eslint.config.js'), eslintConfig)

  editFile(path.resolve(root, 'package.json'), (content) => {
    const asObject = JSON.parse(content)
    const devDepsEntries = Object.entries(asObject.devDependencies).filter(
      ([name]) => name !== 'oxlint',
    )
    devDepsEntries.push(
      ['@eslint/js', `^${eslintJsVersion}`],
      ['eslint', `^${eslintVersion}`],
      ['eslint-plugin-react-hooks', `^${eslintPluginReactHooksVersion}`],
      ['eslint-plugin-react-refresh', `^${eslintPluginReactRefreshVersion}`],
      ['globals', `^${globalsVersion}`],
    )
    if (isTs) {
      devDepsEntries.push(['typescript-eslint', `^${typescriptEslintVersion}`])
    }
    devDepsEntries.sort()
    asObject.devDependencies = Object.fromEntries(devDepsEntries)
    asObject.scripts.lint = 'eslint .'
    return JSON.stringify(asObject, null, 2) + '\n'
  })

  editFile(path.resolve(root, 'README.md'), (content) => {
    content = content.replace(
      'with HMR and some Oxlint rules',
      'with HMR and some ESLint rules',
    )
    const headingIndex = content.indexOf(
      '## Expanding the Oxlint configuration',
    )
    if (headingIndex === -1) {
      console.warn('Could not update Oxlint section in README.md')
      return content
    }
    const eslintTypeAwareConfig = /* js */ `export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`
    const eslintReactConfig = /* js */ `// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`

    const eslintSection = isTs
      ? `## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

\`\`\`js
${eslintTypeAwareConfig}
\`\`\`

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

\`\`\`js
${eslintReactConfig}
\`\`\`
`
      : `## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [\`typescript-eslint\`](https://typescript-eslint.io) in your project.
`
    return content.slice(0, headingIndex) + eslintSection
  })
}
```


---

### 🔹 Commit #02: `467f7ac3`
- **完整 Hash**: `467f7ac3b8c7cca0b33290e7fd86f3fc79ce92cb`
- **說明 (Ground Truth)**: fix(create-vite): use Vite for TanStack projects (#23838)
- **變更檔案數**: 1

#### 📄 檔案: `packages/create-vite/src/index.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:53, E:38, A:0) ➔ After(N:53, E:38, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `FRAMEWORKS()`
- **變更前簽章 (Before)**: `[Module State] FRAMEWORKS` (L81~L404)
- **變更後簽章 (After)**: `[Module State] FRAMEWORKS` (L81~L404)

#### ◀️ 變更前實作碼 (Before Implementation):
```
FRAMEWORKS: Framework[] = [
  {
    name: 'vanilla',
    display: 'Vanilla',
    color: yellow,
    variants: [
      {
        name: 'vanilla-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'vanilla',
        display: 'JavaScript',
        color: yellow,
      },
    ],
  },
  {
    name: 'vue',
    display: 'Vue',
    color: green,
    variants: [
      {
        name: 'vue-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'vue',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-create-vue',
        display: 'Official Vue Starter ↗',
        color: green,
        customCommand: 'npm create vue@latest TARGET_DIR',
      },
      {
        name: 'custom-nuxt',
        display: 'Nuxt ↗',
        link: 'https://nuxt.com',
        color: greenBright,
        customCommand: 'npm exec nuxi init TARGET_DIR',
      },
      {
        name: 'custom-vike-vue',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: greenBright,
        customCommand: 'npm create -- vike@latest --vue TARGET_DIR',
      },
    ],
  },
  {
    name: 'react',
    display: 'React',
    color: cyan,
    variants: [
      {
        name: 'react-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'react-compiler-ts',
        display: 'TypeScript + React Compiler',
        color: blue,
      },
      {
        name: 'react',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'react-compiler',
        display: 'JavaScript + React Compiler',
        color: yellow,
      },
      {
        name: 'rsc',
        display: 'RSC',
        color: magenta,
        customCommand:
          'npm exec tiged vitejs/vite-plugin-react/packages/plugin-rsc/examples/starter TARGET_DIR',
      },
      {
        name: 'custom-react-router',
        display: 'React Router v7 ↗',
        link: 'https://reactrouter.com',
        color: cyan,
        customCommand: 'npm create react-router@latest TARGET_DIR',
      },
      {
        name: 'custom-tanstack-start-react',
        display: 'TanStack Start ↗',
        link: 'https://tanstack.com/start',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework react --interactive',
      },
      {
        name: 'custom-tanstack-router-react',
        display: 'TanStack Router ↗',
        link: 'https://tanstack.com/router',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework react --router-only --interactive',
      },
      {
        name: 'redwoodsdk-standard',
        display: 'RedwoodSDK ↗',
        link: 'https://rwsdk.com',
        color: cyan,
        customCommand: 'npm create rwsdk@latest TARGET_DIR',
      },
      {
        name: 'custom-vike-react',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: cyan,
        customCommand: 'npm create -- vike@latest --react TARGET_DIR',
      },
    ],
  },
  {
    name: 'preact',
    display: 'Preact',
    color: magenta,
    variants: [
      {
        name: 'preact-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'preact',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-create-preact',
        display: 'Official Preact Starter ↗',
        color: magenta,
        customCommand: 'npm create preact@latest TARGET_DIR',
      },
    ],
  },
  {
    name: 'lit',
    display: 'Lit',
    color: redBright,
    variants: [
      {
        name: 'lit-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'lit',
        display: 'JavaScript',
        color: yellow,
      },
    ],
  },
  {
    name: 'svelte',
    display: 'Svelte',
    color: red,
    variants: [
      {
        name: 'svelte-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'svelte',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-svelte-kit',
        display: 'SvelteKit ↗',
        color: red,
        customCommand: 'npm exec sv create TARGET_DIR',
      },
    ],
  },
  {
    name: 'solid',
    display: 'Solid',
    color: blue,
    variants: [
      {
        name: 'solid-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'solid',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-tanstack-start-solid',
        display: 'TanStack Start ↗',
        link: 'https://tanstack.com/start',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework solid --interactive',
      },
      {
        name: 'custom-tanstack-router-solid',
        display: 'TanStack Router ↗',
        link: 'https://tanstack.com/router',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework solid --router-only --interactive',
      },
      {
        name: 'custom-vike-solid',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: cyan,
        customCommand: 'npm create -- vike@latest --solid TARGET_DIR',
      },
    ],
  },
  {
    name: 'ember',
    display: 'Ember',
    color: redBright,
    variants: [
      {
        name: 'ember-app-ts',
        display: 'TypeScript ↗',
        color: blueBright,
        customCommand:
          'npm exec -- ember-cli@latest new TARGET_DIR --typescript',
      },
      {
        name: 'ember-app',
        display: 'JavaScript ↗',
        color: redBright,
        customCommand: 'npm exec -- ember-cli@latest new TARGET_DIR',
      },
    ],
  },
  {
    name: 'qwik',
    display: 'Qwik',
    color: blueBright,
    variants: [
      {
        name: 'qwik-ts',
        display: 'TypeScript',
        color: blueBright,
      },
      {
        name: 'qwik',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-qwik-city',
        display: 'QwikCity ↗',
        color: blueBright,
        customCommand: 'npm create qwik@latest empty TARGET_DIR',
      },
    ],
  },
  {
    name: 'angular',
    display: 'Angular',
    color: red,
    variants: [
      {
        name: 'custom-angular',
        display: 'Angular ↗',
        color: red,
        customCommand: 'npm exec @angular/cli@latest new TARGET_DIR',
      },
      {
        name: 'custom-analog',
        display: 'Analog ↗',
        color: yellow,
        customCommand: 'npm create analog@latest TARGET_DIR',
      },
    ],
  },
  {
    name: 'marko',
    display: 'Marko',
    color: magenta,
    variants: [
      {
        name: 'marko-run',
        display: 'Marko Run ↗',
        color: magenta,
        customCommand: 'npm create -- marko@latest --name TARGET_DIR',
      },
    ],
  },
  {
    name: 'others',
    display: 'Others',
    color: reset,
    variants: [
      {
        name: 'create-vite-extra',
        display: 'Extra Vite Starters ↗',
        color: reset,
        customCommand: 'npm create vite-extra@latest TARGET_DIR',
      },
      {
        name: 'create-electron-vite',
        display: 'Electron ↗',
        color: reset,
        customCommand: 'npm create electron-vite@latest TARGET_DIR',
      },
    ],
  },
]
```

#### ▶️ 變更後實作碼 (After Implementation):
```
FRAMEWORKS: Framework[] = [
  {
    name: 'vanilla',
    display: 'Vanilla',
    color: yellow,
    variants: [
      {
        name: 'vanilla-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'vanilla',
        display: 'JavaScript',
        color: yellow,
      },
    ],
  },
  {
    name: 'vue',
    display: 'Vue',
    color: green,
    variants: [
      {
        name: 'vue-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'vue',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-create-vue',
        display: 'Official Vue Starter ↗',
        color: green,
        customCommand: 'npm create vue@latest TARGET_DIR',
      },
      {
        name: 'custom-nuxt',
        display: 'Nuxt ↗',
        link: 'https://nuxt.com',
        color: greenBright,
        customCommand: 'npm exec nuxi init TARGET_DIR',
      },
      {
        name: 'custom-vike-vue',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: greenBright,
        customCommand: 'npm create -- vike@latest --vue TARGET_DIR',
      },
    ],
  },
  {
    name: 'react',
    display: 'React',
    color: cyan,
    variants: [
      {
        name: 'react-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'react-compiler-ts',
        display: 'TypeScript + React Compiler',
        color: blue,
      },
      {
        name: 'react',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'react-compiler',
        display: 'JavaScript + React Compiler',
        color: yellow,
      },
      {
        name: 'rsc',
        display: 'RSC',
        color: magenta,
        customCommand:
          'npm exec tiged vitejs/vite-plugin-react/packages/plugin-rsc/examples/starter TARGET_DIR',
      },
      {
        name: 'custom-react-router',
        display: 'React Router v7 ↗',
        link: 'https://reactrouter.com',
        color: cyan,
        customCommand: 'npm create react-router@latest TARGET_DIR',
      },
      {
        name: 'custom-tanstack-start-react',
        display: 'TanStack Start ↗',
        link: 'https://tanstack.com/start',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework react --build-tool vite --interactive',
      },
      {
        name: 'custom-tanstack-router-react',
        display: 'TanStack Router ↗',
        link: 'https://tanstack.com/router',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework react --build-tool vite --router-only --interactive',
      },
      {
        name: 'redwoodsdk-standard',
        display: 'RedwoodSDK ↗',
        link: 'https://rwsdk.com',
        color: cyan,
        customCommand: 'npm create rwsdk@latest TARGET_DIR',
      },
      {
        name: 'custom-vike-react',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: cyan,
        customCommand: 'npm create -- vike@latest --react TARGET_DIR',
      },
    ],
  },
  {
    name: 'preact',
    display: 'Preact',
    color: magenta,
    variants: [
      {
        name: 'preact-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'preact',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-create-preact',
        display: 'Official Preact Starter ↗',
        color: magenta,
        customCommand: 'npm create preact@latest TARGET_DIR',
      },
    ],
  },
  {
    name: 'lit',
    display: 'Lit',
    color: redBright,
    variants: [
      {
        name: 'lit-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'lit',
        display: 'JavaScript',
        color: yellow,
      },
    ],
  },
  {
    name: 'svelte',
    display: 'Svelte',
    color: red,
    variants: [
      {
        name: 'svelte-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'svelte',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-svelte-kit',
        display: 'SvelteKit ↗',
        color: red,
        customCommand: 'npm exec sv create TARGET_DIR',
      },
    ],
  },
  {
    name: 'solid',
    display: 'Solid',
    color: blue,
    variants: [
      {
        name: 'solid-ts',
        display: 'TypeScript',
        color: blue,
      },
      {
        name: 'solid',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-tanstack-start-solid',
        display: 'TanStack Start ↗',
        link: 'https://tanstack.com/start',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework solid --build-tool vite --interactive',
      },
      {
        name: 'custom-tanstack-router-solid',
        display: 'TanStack Router ↗',
        link: 'https://tanstack.com/router',
        color: cyan,
        customCommand:
          'npm exec -- @tanstack/cli@latest create TARGET_DIR --framework solid --build-tool vite --router-only --interactive',
      },
      {
        name: 'custom-vike-solid',
        display: 'Vike ↗',
        link: 'https://vike.dev',
        color: cyan,
        customCommand: 'npm create -- vike@latest --solid TARGET_DIR',
      },
    ],
  },
  {
    name: 'ember',
    display: 'Ember',
    color: redBright,
    variants: [
      {
        name: 'ember-app-ts',
        display: 'TypeScript ↗',
        color: blueBright,
        customCommand:
          'npm exec -- ember-cli@latest new TARGET_DIR --typescript',
      },
      {
        name: 'ember-app',
        display: 'JavaScript ↗',
        color: redBright,
        customCommand: 'npm exec -- ember-cli@latest new TARGET_DIR',
      },
    ],
  },
  {
    name: 'qwik',
    display: 'Qwik',
    color: blueBright,
    variants: [
      {
        name: 'qwik-ts',
        display: 'TypeScript',
        color: blueBright,
      },
      {
        name: 'qwik',
        display: 'JavaScript',
        color: yellow,
      },
      {
        name: 'custom-qwik-city',
        display: 'QwikCity ↗',
        color: blueBright,
        customCommand: 'npm create qwik@latest empty TARGET_DIR',
      },
    ],
  },
  {
    name: 'angular',
    display: 'Angular',
    color: red,
    variants: [
      {
        name: 'custom-angular',
        display: 'Angular ↗',
        color: red,
        customCommand: 'npm exec @angular/cli@latest new TARGET_DIR',
      },
      {
        name: 'custom-analog',
        display: 'Analog ↗',
        color: yellow,
        customCommand: 'npm create analog@latest TARGET_DIR',
      },
    ],
  },
  {
    name: 'marko',
    display: 'Marko',
    color: magenta,
    variants: [
      {
        name: 'marko-run',
        display: 'Marko Run ↗',
        color: magenta,
        customCommand: 'npm create -- marko@latest --name TARGET_DIR',
      },
    ],
  },
  {
    name: 'others',
    display: 'Others',
    color: reset,
    variants: [
      {
        name: 'create-vite-extra',
        display: 'Extra Vite Starters ↗',
        color: reset,
        customCommand: 'npm create vite-extra@latest TARGET_DIR',
      },
      {
        name: 'create-electron-vite',
        display: 'Electron ↗',
        color: reset,
        customCommand: 'npm create electron-vite@latest TARGET_DIR',
      },
    ],
  },
]
```


---

### 🔹 Commit #03: `77d83735`
- **完整 Hash**: `77d8373510da1b26ce057eb2248e570b7f63fde9`
- **說明 (Ground Truth)**: fix(deps): update all non-major dependencies (#23826)
- **變更檔案數**: 1

#### 📄 檔案: `packages/create-vite/src/index.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:53, E:38, A:0) ➔ After(N:53, E:38, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `setupEslint()`
- **變更前簽章 (Before)**: `function setupEslint(root: string, isTs: boolean)` (L879~L1053)
- **變更後簽章 (After)**: `function setupEslint(root: string, isTs: boolean)` (L879~L1053)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function setupEslint(root: string, isTs: boolean) {
  // renovate: datasource=npm depName=@eslint/js
  const eslintJsVersion = '10.0.1'
  // renovate: datasource=npm depName=eslint
  const eslintVersion = '10.12.0'
  // renovate: datasource=npm depName=eslint-plugin-react-hooks
  const eslintPluginReactHooksVersion = '7.1.1'
  // renovate: datasource=npm depName=eslint-plugin-react-refresh
  const eslintPluginReactRefreshVersion = '0.5.7'
  // renovate: datasource=npm depName=globals
  const globalsVersion = '17.13.0'
  // renovate: datasource=npm depName=typescript-eslint
  const typescriptEslintVersion = '8.71.1'

  const eslintConfigForTS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
  },
])
`
  const eslintConfigForJS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
`

  fs.rmSync(path.resolve(root, '.oxlintrc.json'))

  const eslintConfig = isTs ? eslintConfigForTS : eslintConfigForJS
  fs.writeFileSync(path.resolve(root, 'eslint.config.js'), eslintConfig)

  editFile(path.resolve(root, 'package.json'), (content) => {
    const asObject = JSON.parse(content)
    const devDepsEntries = Object.entries(asObject.devDependencies).filter(
      ([name]) => name !== 'oxlint',
    )
    devDepsEntries.push(
      ['@eslint/js', `^${eslintJsVersion}`],
      ['eslint', `^${eslintVersion}`],
      ['eslint-plugin-react-hooks', `^${eslintPluginReactHooksVersion}`],
      ['eslint-plugin-react-refresh', `^${eslintPluginReactRefreshVersion}`],
      ['globals', `^${globalsVersion}`],
    )
    if (isTs) {
      devDepsEntries.push(['typescript-eslint', `^${typescriptEslintVersion}`])
      // Keep TypeScript 6 until typescript-eslint supports TypeScript 7.
      // https://github.com/typescript-eslint/typescript-eslint/issues/10940
      asObject.devDependencies.typescript = '~6.0.3'
    }
    devDepsEntries.sort()
    asObject.devDependencies = Object.fromEntries(devDepsEntries)
    asObject.scripts.lint = 'eslint .'
    return JSON.stringify(asObject, null, 2) + '\n'
  })

  editFile(path.resolve(root, 'README.md'), (content) => {
    content = content.replace(
      'with HMR and some Oxlint rules',
      'with HMR and some ESLint rules',
    )
    const headingIndex = content.indexOf(
      '## Expanding the Oxlint configuration',
    )
    if (headingIndex === -1) {
      console.warn('Could not update Oxlint section in README.md')
      return content
    }
    const eslintTypeAwareConfig = /* js */ `export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`
    const eslintReactConfig = /* js */ `// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`

    const eslintSection = isTs
      ? `## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

\`\`\`js
${eslintTypeAwareConfig}
\`\`\`

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

\`\`\`js
${eslintReactConfig}
\`\`\`
`
      : `## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [\`typescript-eslint\`](https://typescript-eslint.io) in your project.
`
    return content.slice(0, headingIndex) + eslintSection
  })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function setupEslint(root: string, isTs: boolean) {
  // renovate: datasource=npm depName=@eslint/js
  const eslintJsVersion = '10.0.1'
  // renovate: datasource=npm depName=eslint
  const eslintVersion = '10.13.0'
  // renovate: datasource=npm depName=eslint-plugin-react-hooks
  const eslintPluginReactHooksVersion = '7.1.1'
  // renovate: datasource=npm depName=eslint-plugin-react-refresh
  const eslintPluginReactRefreshVersion = '0.5.7'
  // renovate: datasource=npm depName=globals
  const globalsVersion = '17.13.0'
  // renovate: datasource=npm depName=typescript-eslint
  const typescriptEslintVersion = '8.71.2'

  const eslintConfigForTS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
  },
])
`
  const eslintConfigForJS = /* js */ `import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
  },
])
`

  fs.rmSync(path.resolve(root, '.oxlintrc.json'))

  const eslintConfig = isTs ? eslintConfigForTS : eslintConfigForJS
  fs.writeFileSync(path.resolve(root, 'eslint.config.js'), eslintConfig)

  editFile(path.resolve(root, 'package.json'), (content) => {
    const asObject = JSON.parse(content)
    const devDepsEntries = Object.entries(asObject.devDependencies).filter(
      ([name]) => name !== 'oxlint',
    )
    devDepsEntries.push(
      ['@eslint/js', `^${eslintJsVersion}`],
      ['eslint', `^${eslintVersion}`],
      ['eslint-plugin-react-hooks', `^${eslintPluginReactHooksVersion}`],
      ['eslint-plugin-react-refresh', `^${eslintPluginReactRefreshVersion}`],
      ['globals', `^${globalsVersion}`],
    )
    if (isTs) {
      devDepsEntries.push(['typescript-eslint', `^${typescriptEslintVersion}`])
      // Keep TypeScript 6 until typescript-eslint supports TypeScript 7.
      // https://github.com/typescript-eslint/typescript-eslint/issues/10940
      asObject.devDependencies.typescript = '~6.0.3'
    }
    devDepsEntries.sort()
    asObject.devDependencies = Object.fromEntries(devDepsEntries)
    asObject.scripts.lint = 'eslint .'
    return JSON.stringify(asObject, null, 2) + '\n'
  })

  editFile(path.resolve(root, 'README.md'), (content) => {
    content = content.replace(
      'with HMR and some Oxlint rules',
      'with HMR and some ESLint rules',
    )
    const headingIndex = content.indexOf(
      '## Expanding the Oxlint configuration',
    )
    if (headingIndex === -1) {
      console.warn('Could not update Oxlint section in README.md')
      return content
    }
    const eslintTypeAwareConfig = /* js */ `export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`
    const eslintReactConfig = /* js */ `// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
`

    const eslintSection = isTs
      ? `## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

\`\`\`js
${eslintTypeAwareConfig}
\`\`\`

You can also install [eslint-plugin-react-x](https://npmx.dev/package/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://npmx.dev/package/eslint-plugin-react-dom) for React-specific lint rules:

\`\`\`js
${eslintReactConfig}
\`\`\`
`
      : `## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [\`typescript-eslint\`](https://typescript-eslint.io) in your project.
`
    return content.slice(0, headingIndex) + eslintSection
  })
}
```


---

### 🔹 Commit #04: `8d7623d9`
- **完整 Hash**: `8d7623d9b5647714a5b20cbd787a5401ca846229`
- **說明 (Ground Truth)**: fix(build): handle missing chunk import maps (#23777)
- **變更檔案數**: 3

#### 📄 檔案: `packages/vite/src/node/plugins/css.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:248, E:213, A:1) ➔ After(N:248, E:213, A:1)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#injectCode** `(Control)`
    └── 🎯 [CALLS] `createCachedImport()`
        └── 🎯 [CALLS] `imp (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'urlResolver' 被深鎖在內部閉包 (scope:handler@after/packages/vite/src/node/plugins/css.ts:L392C7)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `cssPostPlugin()`
- **變更前簽章 (Before)**: `function cssPostPlugin(config: ResolvedConfig): Plugin` (L483~L1222)
- **變更後簽章 (After)**: `function cssPostPlugin(config: ResolvedConfig): Plugin` (L483~L1218)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function cssPostPlugin(config: ResolvedConfig): Plugin {
  // styles initialization in buildStart causes a styling loss in watch
  const styles = new Map<string, string>()
  // queue to emit css serially to guarantee the files are emitted in a deterministic order
  let codeSplitEmitQueue = createSerialPromiseQueue<string>()
  const urlEmitQueue = createSerialPromiseQueue<unknown>()
  let pureCssChunks: Set<RenderedChunk>
  let chunkCssReferences: Map<string, string>

  // when there are multiple rollup outputs and extracting CSS, only emit once,
  // since output formats have no effect on the generated CSS.
  let hasEmitted = false
  let chunkCSSMap: Map<string, string>

  const rolldownOptionsOutput = config.build.rolldownOptions.output
  const assetFileNames = (
    Array.isArray(rolldownOptionsOutput)
      ? rolldownOptionsOutput[0]
      : rolldownOptionsOutput
  )?.assetFileNames
  const getCssAssetDirname = (
    cssAssetName: string,
    originalFileName?: string,
  ) => {
    const cssAssetNameDir = path.dirname(cssAssetName)
    if (!assetFileNames) {
      return path.join(config.build.assetsDir, cssAssetNameDir)
    } else if (typeof assetFileNames === 'string') {
      return path.join(path.dirname(assetFileNames), cssAssetNameDir)
    } else {
      return path.dirname(
        assetFileNames({
          type: 'asset',
          name: cssAssetName,
          names: [cssAssetName],
          originalFileName,
          originalFileNames: originalFileName ? [originalFileName] : [],
          source: '/* vite internal call, ignore */',
        }),
      )
    }
  }

  function getCssBundleName() {
    const cached = cssBundleNameCache.get(config)
    if (cached) return cached

    const cssBundleName = config.build.lib
      ? resolveLibCssFilename(
          config.build.lib,
          config.root,
          config.packageCache,
        )
      : defaultCssBundleName
    cssBundleNameCache.set(config, cssBundleName)
    return cssBundleName
  }

  return {
    name: 'vite:css-post',

    renderStart() {
      // Ensure new caches for every build (i.e. rebuilding in watch mode)
      pureCssChunks = new Set<RenderedChunk>()
      chunkCssReferences = new Map<string, string>()
      hasEmitted = false
      chunkCSSMap = new Map()
      codeSplitEmitQueue = createSerialPromiseQueue()
    },

    transform: {
      filter: {
        id: {
          include: CSS_LANGS_RE,
          exclude: [commonjsProxyRE, SPECIAL_QUERY_RE],
        },
      },
      async handler(css, id) {
        css = stripBomTag(css)

        // cache css compile result to map
        // and then use the cache replace inline-style-flag
        // when `generateBundle` in vite:build-html plugin and devHtmlHook
        const inlineCSS = inlineCSSRE.test(id)
        const isHTMLProxy = htmlProxyRE.test(id)
        if (inlineCSS && isHTMLProxy) {
          if (styleAttrRE.test(id)) {
            css = css.replace(/"/g, '&quot;')
          } else {
            if (config.command !== 'serve' && config.build.cssMinify) {
              css = await minifyCSS(css, config, true, id)
            }
            css = css.replace(styleTagCloseRE, '<\\/style')
          }
          const index = htmlProxyIndexRE.exec(id)?.[1]
          if (index == null) {
            throw new Error(`HTML proxy index in "${id}" not found`)
          }
          addToHTMLProxyTransformResult(
            `${getHash(cleanUrl(id))}_${Number.parseInt(index)}`,
            css,
          )
          return {
            code: `export default ''`,
            map: { mappings: '' },
          }
        }

        const inlined = inlineRE.test(id)
        const modules = cssModulesCache.get(config)!.get(id)

        // #6984, #7552
        // `foo.module.css` => modulesCode
        // `foo.module.css?inline` => cssContent
        const modulesCode =
          modules &&
          !inlined &&
          dataToEsm(modules, { namedExports: true, preferConst: true })

        if (config.command === 'serve') {
          const getContentWithSourcemap = async (content: string) => {
            if (config.css.devSourcemap) {
              const sourcemap = this.getCombinedSourcemap()
              if (sourcemap.mappings) {
                await injectSourcesContent(
                  sourcemap,
                  cleanUrl(id),
                  config.logger,
                )
              }
              return getCodeWithSourcemap('css', content, sourcemap)
            }
            return content
          }

          if (isDirectCSSRequest(id)) {
            return null
          }
          if (inlined) {
            return `export default ${JSON.stringify(css)}`
          }
          if (this.environment.config.consumer === 'server') {
            return modulesCode || 'export {}'
          }

          const cssContent = await getContentWithSourcemap(css)
          const code = [
            `import { updateStyle as __vite__updateStyle, removeStyle as __vite__removeStyle } from ${JSON.stringify(
              path.posix.join(config.base, CLIENT_PUBLIC_PATH),
            )}`,
            `const __vite__id = ${JSON.stringify(id)}`,
            `const __vite__css = ${JSON.stringify(cssContent)}`,
            `__vite__updateStyle(__vite__id, __vite__css)`,
            // css modules exports change on edit so it can't self accept
            `${modulesCode || 'import.meta.hot.accept()'}`,
            `import.meta.hot.prune(() => __vite__removeStyle(__vite__id))`,
          ].join('\n')
          return { code, map: { mappings: '' }, moduleType: 'js' }
        }

        // build CSS handling ----------------------------------------------------

        // record css
        if (!inlined) {
          styles.set(id, css)
        }

        let code: string
        if (modulesCode) {
          code = modulesCode
        } else if (inlined) {
          let content = css
          if (config.build.cssMinify) {
            content = await minifyCSS(content, config, true, id)
          }
          code = `export default ${JSON.stringify(content)}`
        } else {
          // empty module when it's not a CSS module nor `?inline`
          code = ''
        }

        return {
          code,
          map: { mappings: '' },
          // avoid the css module from being tree-shaken so that we can retrieve
          // it in renderChunk()
          moduleSideEffects: modulesCode || inlined ? false : 'no-treeshake',
          moduleType: 'js',
        }
      },
    },

    ...(config.command === 'build'
      ? {
          async renderChunk(code, chunk, opts, meta) {
            let chunkCSS: string | undefined
            const renderedModules = new Proxy(
              {} as Record<string, RenderedModule | undefined>,
              {
                get(_target, p) {
                  for (const name in meta.chunks) {
                    const modules = meta.chunks[name].modules
                    const module = modules[p as string]
                    if (module) {
                      return module
                    }
                  }
                },
              },
            )
            // the chunk is empty if it's a dynamic entry chunk that only contains a CSS import
            const isJsChunkEmpty = code === '' && !chunk.isEntry
            let isPureCssChunk = chunk.exports.length === 0
            const ids = Object.keys(chunk.modules)
            for (const id of ids) {
              if (styles.has(id)) {
                // ?transform-only is used for ?url and shouldn't be included in normal CSS chunks
                if (transformOnlyRE.test(id)) {
                  continue
                }

                // If this CSS is scoped to its importers exports, check if those importers exports
                // are rendered in the chunks. If they are not, we can skip bundling this CSS.
                const cssScopeTo =
                  this.getModuleInfo(id)?.meta?.vite?.cssScopeTo
                if (
                  cssScopeTo &&
                  !isCssScopeToRendered(cssScopeTo, renderedModules)
                ) {
                  continue
                }

                // a css module contains JS, so it makes this not a pure css chunk
                if (cssModuleRE.test(id)) {
                  isPureCssChunk = false
                }

                chunkCSS = (chunkCSS || '') + styles.get(id)
              } else if (!isJsChunkEmpty) {
                // if the module does not have a style, then it's not a pure css chunk.
                // this is true because in the `transform` hook above, only modules
                // that are css gets added to the `styles` map.
                isPureCssChunk = false
              }
            }

            const publicAssetUrlMap = publicAssetUrlCache.get(config)!

            // resolve asset URL placeholders to their built file URLs
            const resolveAssetUrlsInCss = (
              chunkCSS: string,
              cssAssetName: string,
              originalFileName?: string,
            ) => {
              const encodedPublicUrls = encodePublicUrlsInCSS(config)

              const relative = config.base === './' || config.base === ''
              const cssAssetDirname =
                encodedPublicUrls || relative
                  ? slash(getCssAssetDirname(cssAssetName, originalFileName))
                  : undefined

              const toRelative = (filename: string) => {
                // relative base + extracted CSS
                const relativePath = normalizePath(
                  path.relative(cssAssetDirname!, filename),
                )
                return relativePath[0] === '.'
                  ? relativePath
                  : './' + relativePath
              }

              // replace asset url references with resolved url.
              chunkCSS = chunkCSS.replace(assetUrlRE, (_, fileHash, urlId) => {
                const filename =
                  this.getFileName(fileHash) +
                  getAssetUrlPostfix(this.environment, urlId)
                chunk.viteMetadata!.importedAssets.add(cleanUrl(filename))
                return encodeURIPath(
                  toOutputFilePathInCss(
                    filename,
                    'asset',
                    cssAssetName,
                    'css',
                    config,
                    toRelative,
                  ),
                )
              })
              // resolve public URL from CSS paths
              if (encodedPublicUrls) {
                const relativePathToPublicFromCSS = normalizePath(
                  path.relative(cssAssetDirname!, ''),
                )
                chunkCSS = chunkCSS.replace(publicAssetUrlRE, (_, hash) => {
                  const publicUrl = publicAssetUrlMap.get(hash)!.slice(1)
                  return encodeURIPath(
                    toOutputFilePathInCss(
                      publicUrl,
                      'public',
                      cssAssetName,
                      'css',
                      config,
                      () => `${relativePathToPublicFromCSS}/${publicUrl}`,
                    ),
                  )
                })
              }
              return chunkCSS
            }

            function ensureFileExt(name: string, ext: string) {
              return normalizePath(
                path.format({ ...path.parse(name), base: undefined, ext }),
              )
            }

            let s: MagicString | undefined
            const urlEmitTasks: Array<{
              cssAssetName: string
              originalFileName: string
              content: string
              start: number
              end: number
            }> = []

            if (code.includes('__VITE_CSS_URL__')) {
              let match: RegExpExecArray | null
              cssUrlAssetRE.lastIndex = 0
              while ((match = cssUrlAssetRE.exec(code))) {
                const [full, idHex] = match
                const id = Buffer.from(idHex, 'hex').toString()
                const originalFileName = cleanUrl(id)
                const cssAssetName = ensureFileExt(
                  path.basename(originalFileName),
                  '.css',
                )
                if (!styles.has(id)) {
                  throw new Error(
                    `css content for ${JSON.stringify(id)} was not found`,
                  )
                }

                let cssContent = styles.get(id)!

                cssContent = resolveAssetUrlsInCss(
                  cssContent,
                  cssAssetName,
                  originalFileName,
                )

                urlEmitTasks.push({
                  cssAssetName,
                  originalFileName,
                  content: cssContent,
                  start: match.index,
                  end: match.index + full.length,
                })
              }
            }

            // should await even if this chunk does not include __VITE_CSS_URL__
            // so that code after this line runs in the same order
            await urlEmitQueue.run(async () =>
              Promise.all(
                urlEmitTasks.map(async (info) => {
                  info.content = await finalizeCss(info.content, config)
                }),
              ),
            )
            if (urlEmitTasks.length > 0) {
              const toRelativeRuntime =
                createToImportMetaURLBasedRelativeRuntime(
                  opts.format,
                  config.isWorker,
                )
              s ||= new MagicString(code)

              for (const {
                cssAssetName,
                originalFileName,
                content,
                start,
                end,
              } of urlEmitTasks) {
                const referenceId = this.emitFile({
                  type: 'asset',
                  name: cssAssetName,
                  originalFileName,
                  source: content,
                })

                const filename = this.getFileName(referenceId)
                chunk.viteMetadata!.importedAssets.add(cleanUrl(filename))
                const replacement = toOutputFilePathInJS(
                  this.environment,
                  filename,
                  'asset',
                  chunk.fileName,
                  'js',
                  toRelativeRuntime,
                )
                const replacementString =
                  typeof replacement === 'string'
                    ? JSON.stringify(encodeURIPath(replacement)).slice(1, -1)
                    : `"+${replacement.runtime}+"`
                s.update(start, end, replacementString)
              }
            }

            if (chunkCSS !== undefined) {
              if (
                isPureCssChunk &&
                (opts.format === 'es' || opts.format === 'cjs')
              ) {
                // this is a shared CSS-only chunk that is empty.
                pureCssChunks.add(chunk)
              }

              if (this.environment.config.build.cssCodeSplit) {
                if (
                  (opts.format === 'es' || opts.format === 'cjs') &&
                  !chunk.fileName.includes('-legacy')
                ) {
                  const isEntry = chunk.isEntry && isPureCssChunk
                  const cssFullAssetName = ensureFileExt(chunk.name, '.css')
                  // if facadeModuleId doesn't exist or doesn't have a CSS extension,
                  // that means a JS entry file imports a CSS file.
                  // in this case, only use the filename for the CSS chunk name like JS chunks.
                  const cssAssetName =
                    chunk.isEntry &&
                    (!chunk.facadeModuleId ||
                      !isCSSRequest(chunk.facadeModuleId))
                      ? path.basename(cssFullAssetName)
                      : cssFullAssetName
                  const originalFileName = getChunkOriginalFileName(
                    chunk,
                    config.root,
                    this.environment.config.isOutputOptionsForLegacyChunks?.(
                      opts,
                    ) ?? false,
                  )

                  chunkCSS = resolveAssetUrlsInCss(
                    chunkCSS,
                    cssAssetName,
                    originalFileName,
                  )

                  // wait for previous tasks as well
                  chunkCSS = await codeSplitEmitQueue.run(async () => {
                    return finalizeCss(chunkCSS!, config)
                  })

                  // emit corresponding css file
                  const referenceId = this.emitFile({
                    type: 'asset',
                    name: cssAssetName,
                    originalFileName,
                    source: chunkCSS,
                  })
                  chunkCssReferences.set(chunk.fileName, referenceId)
                  if (isEntry) {
                    cssEntriesMap
                      .get(this.environment)!
                      .set(chunk.fileName, { referenceId, name: chunk.name })
                  }
                  chunk.viteMetadata!.importedCss.add(
                    this.getFileName(referenceId),
                  )
                } else if (this.environment.config.consumer === 'client') {
                  // legacy build and inline css

                  // Entry chunk CSS will be collected into `chunk.viteMetadata.importedCss`
                  // and injected later by the `'vite:build-html'` plugin into the `index.html`
                  // so it will be duplicated. (https://github.com/vitejs/vite/issues/2062#issuecomment-782388010)
                  // But because entry chunk can be imported by dynamic import,
                  // we shouldn't remove the inlined CSS. (#10285)

                  chunkCSS = await finalizeCss(chunkCSS, config)
                  let cssString = JSON.stringify(chunkCSS)
                  cssString =
                    renderAssetUrlInJS(
                      this,
                      chunk,
                      opts,
                      cssString,
                    )?.toString() || cssString
                  const style = `__vite_style__`
                  const injectCode =
                    `var ${style} = document.createElement('style');` +
                    `${style}.textContent = ${cssString};` +
                    `document.head.appendChild(${style});`

                  s ||= new MagicString(code)
                  injectInlinedCSS(s, this, code, opts.format, injectCode)
                }
              } else {
                // resolve public URL from CSS paths, we need to use absolute paths
                chunkCSS = resolveAssetUrlsInCss(
                  chunkCSS,
                  getCssBundleName(),
                  defaultCssBundleName,
                )
                // finalizeCss is called for the aggregated chunk in generateBundle

                chunkCSSMap.set(chunk.fileName, chunkCSS)
              }
            }

            if (s) {
              if (config.build.sourcemap) {
                return {
                  code: s.toString(),
                  map: s.generateMap({ hires: 'boundary' }),
                }
              } else {
                return { code: s.toString() }
              }
            }
            return null
          },

          augmentChunkHash(chunk) {
            if (chunk.viteMetadata?.importedCss.size) {
              let hash = ''
              for (const id of chunk.viteMetadata.importedCss) {
                hash += id
              }
              return hash
            }
          },
        }
      : {}),

    async generateBundle(opts, bundle) {
      // to avoid emitting duplicate assets for modern build and legacy build
      if (this.environment.config.isOutputOptionsForLegacyChunks?.(opts)) {
        return
      }

      // vite:asset cleans up earlier assets of 'renderChunk',
      // but with cssCodeSplit=false we may still emit CSS here.
      // So is our responsibility to respect emitAssets
      const canEmitAssets =
        config.command !== 'build' || this.environment.config.build.emitAssets

      // extract as single css bundle if no codesplit
      if (
        canEmitAssets &&
        !this.environment.config.build.cssCodeSplit &&
        !hasEmitted
      ) {
        let extractedCss = ''
        const collected = new Set<OutputChunk>()
        // will be populated in order they are used by entry points
        const dynamicImports = new Set<string>()

        function collect(chunk: OutputChunk | OutputAsset | undefined) {
          if (!chunk || chunk.type !== 'chunk' || collected.has(chunk)) return
          collected.add(chunk)

          // First collect all styles from the synchronous imports (lowest priority)
          chunk.imports.forEach((importName) => collect(bundle[importName]))
          // Save dynamic imports in deterministic order to add the styles later (to have the highest priority)
          chunk.dynamicImports.forEach((importName) =>
            dynamicImports.add(importName),
          )
          // Then collect the styles of the current chunk (might overwrite some styles from previous imports)
          extractedCss += chunkCSSMap.get(chunk.preliminaryFileName) ?? ''
        }

        // The bundle is guaranteed to be deterministic, if not then we have a bug in rollup.
        // So we use it to ensure a deterministic order of styles
        for (const chunk of Object.values(bundle)) {
          if (chunk.type === 'chunk' && chunk.isEntry) {
            collect(chunk)
          }
        }
        // Now collect the dynamic chunks, this is done last to have the styles overwrite the previous ones
        for (const chunkName of dynamicImports) {
          collect(bundle[chunkName])
        }

        // Finally, if there's any extracted CSS, we emit the asset
        if (extractedCss) {
          hasEmitted = true
          extractedCss = await finalizeCss(extractedCss, config)
          this.emitFile({
            name: getCssBundleName(),
            type: 'asset',
            source: extractedCss,
            // this file is an implicit entry point, use defaultCssBundleName as the original file name
            // this name is also used as a key in the manifest
            originalFileName: defaultCssBundleName,
          })
        }
      }

      // With `cssCodeSplit: false`, CSS is emitted as a single stylesheet in the HTML,
      // so this per-chunk import map handling is irrelevant.
      if (
        this.environment.config.build.chunkImportMap &&
        chunkCssReferences.size
      ) {
        // The import map hash identifies the JS chunk independently of its content.
        // Since each chunk has at most one extracted CSS sidecar, we can reuse that
        // stable identity with a `.css` extension while mapping it to the CSS content hash.
        const importMap = getImportMap(bundle, this.environment.config)!
        const importMapReverseMapping = Object.fromEntries(
          Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
        )
        const chunksByPreliminaryFileName = new Map(
          Object.values(bundle)
            .filter((output): output is OutputChunk => output.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk]),
        )

        for (const [chunkFileName, referenceId] of chunkCssReferences) {
          const chunk = chunksByPreliminaryFileName.get(chunkFileName)
          if (!chunk) continue

          const stableChunkFileName =
            importMapReverseMapping[chunk.fileName] ?? chunk.fileName
          const extension = path.posix.extname(stableChunkFileName)
          const stableCssFileName = `${stableChunkFileName.slice(
            0,
            extension ? -extension.length : undefined,
          )}.css`
          importMap.content.imports[config.base + stableCssFileName] =
            config.base + this.getFileName(referenceId)
        }
        importMap.asset.source = JSON.stringify(importMap.content)
      }

      // remove empty css chunks and their imports
      if (pureCssChunks.size) {
        // map each pure css chunk (rendered chunk) to it's corresponding bundle
        // chunk. we check that by `preliminaryFileName` as they have different
        // `filename`s (rendered chunk has the !~{XXX}~ placeholder)
        const prelimaryNameToChunkMap = Object.fromEntries(
          Object.values(bundle)
            .filter((chunk): chunk is OutputChunk => chunk.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk.fileName]),
        )

        // When running in watch mode the generateBundle is called once per output format
        // in this case the `bundle` is not populated with the other output files
        // but they are still in `pureCssChunks`.
        // So we need to filter the names and only use those who are defined
        const pureCssChunkNames = [...pureCssChunks]
          .map((pureCssChunk) => prelimaryNameToChunkMap[pureCssChunk.fileName])
          .filter(Boolean)
        const pureCssChunkNameSet = new Set(pureCssChunkNames)

        let importMapReverseMapping: Record<string, string> | undefined
        if (this.environment.config.build.chunkImportMap) {
          const importMap = getImportMap(bundle, this.environment.config)!
          importMapReverseMapping = Object.fromEntries(
            Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
          )
        }
        const pureCssChunkNamesInCode = importMapReverseMapping
          ? pureCssChunkNames.map(
              (name) => importMapReverseMapping![name] ?? name,
            )
          : pureCssChunkNames

        const replaceEmptyChunk = getEmptyChunkReplacer(
          pureCssChunkNamesInCode,
          opts.format,
        )

        for (const file in bundle) {
          const chunk = bundle[file]
          if (chunk.type === 'chunk') {
            let chunkImportsPureCssChunk = false
            // remove pure css chunk from other chunk's imports,
            // and also register the emitted CSS files under the importer
            // chunks instead.
            chunk.imports = chunk.imports.filter((file) => {
              if (pureCssChunkNameSet.has(file)) {
                const { importedCss, importedAssets } = (
                  bundle[file] as OutputChunk
                ).viteMetadata!
                importedCss.forEach((file) =>
                  chunk.viteMetadata!.importedCss.add(file),
                )
                importedAssets.forEach((file) =>
                  chunk.viteMetadata!.importedAssets.add(file),
                )
                chunkImportsPureCssChunk = true
                return false
              }
              return true
            })
            if (chunkImportsPureCssChunk) {
              chunk.code = replaceEmptyChunk(chunk.code)
            }
          }
        }

        const removedPureCssFiles = removedPureCssFilesCache.get(config)!
        pureCssChunkNames.forEach((fileName) => {
          const emptyJsPlaceholder = bundle[fileName] as OutputChunk
          if (emptyJsPlaceholder.isEntry) {
            const { importedAssets, importedCss } =
              emptyJsPlaceholder.viteMetadata!
            const cssReferenceId = cssEntriesMap
              .get(this.environment)!
              .get(emptyJsPlaceholder.preliminaryFileName)!.referenceId
            const realCssEntryName = this.getFileName(cssReferenceId)
            const realCssEntry = bundle[realCssEntryName]!
            importedCss.delete(realCssEntryName)
            if (importedAssets.size) {
              realCssEntry.viteMetadata!.importedAssets = importedAssets
            }
            if (importedCss.size) {
              realCssEntry.viteMetadata!.importedCss = importedCss
            }
          }

          removedPureCssFiles.set(fileName, emptyJsPlaceholder)
          delete bundle[fileName]
          delete bundle[`${fileName}.map`]
        })
      }

      const cssAssets = Object.values(bundle).filter(
        (asset): asset is OutputAsset =>
          asset.type === 'asset' && asset.fileName.endsWith('.css'),
      )
      for (const cssAsset of cssAssets) {
        if (typeof cssAsset.source === 'string') {
          cssAsset.source = cssAsset.source.replace(viteHashUpdateMarkerRE, '')
        }
      }
    },
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function cssPostPlugin(config: ResolvedConfig): Plugin {
  // styles initialization in buildStart causes a styling loss in watch
  const styles = new Map<string, string>()
  // queue to emit css serially to guarantee the files are emitted in a deterministic order
  let codeSplitEmitQueue = createSerialPromiseQueue<string>()
  const urlEmitQueue = createSerialPromiseQueue<unknown>()
  let pureCssChunks: Set<RenderedChunk>
  let chunkCssReferences: Map<string, string>

  // when there are multiple rollup outputs and extracting CSS, only emit once,
  // since output formats have no effect on the generated CSS.
  let hasEmitted = false
  let chunkCSSMap: Map<string, string>

  const rolldownOptionsOutput = config.build.rolldownOptions.output
  const assetFileNames = (
    Array.isArray(rolldownOptionsOutput)
      ? rolldownOptionsOutput[0]
      : rolldownOptionsOutput
  )?.assetFileNames
  const getCssAssetDirname = (
    cssAssetName: string,
    originalFileName?: string,
  ) => {
    const cssAssetNameDir = path.dirname(cssAssetName)
    if (!assetFileNames) {
      return path.join(config.build.assetsDir, cssAssetNameDir)
    } else if (typeof assetFileNames === 'string') {
      return path.join(path.dirname(assetFileNames), cssAssetNameDir)
    } else {
      return path.dirname(
        assetFileNames({
          type: 'asset',
          name: cssAssetName,
          names: [cssAssetName],
          originalFileName,
          originalFileNames: originalFileName ? [originalFileName] : [],
          source: '/* vite internal call, ignore */',
        }),
      )
    }
  }

  function getCssBundleName() {
    const cached = cssBundleNameCache.get(config)
    if (cached) return cached

    const cssBundleName = config.build.lib
      ? resolveLibCssFilename(
          config.build.lib,
          config.root,
          config.packageCache,
        )
      : defaultCssBundleName
    cssBundleNameCache.set(config, cssBundleName)
    return cssBundleName
  }

  return {
    name: 'vite:css-post',

    renderStart() {
      // Ensure new caches for every build (i.e. rebuilding in watch mode)
      pureCssChunks = new Set<RenderedChunk>()
      chunkCssReferences = new Map<string, string>()
      hasEmitted = false
      chunkCSSMap = new Map()
      codeSplitEmitQueue = createSerialPromiseQueue()
    },

    transform: {
      filter: {
        id: {
          include: CSS_LANGS_RE,
          exclude: [commonjsProxyRE, SPECIAL_QUERY_RE],
        },
      },
      async handler(css, id) {
        css = stripBomTag(css)

        // cache css compile result to map
        // and then use the cache replace inline-style-flag
        // when `generateBundle` in vite:build-html plugin and devHtmlHook
        const inlineCSS = inlineCSSRE.test(id)
        const isHTMLProxy = htmlProxyRE.test(id)
        if (inlineCSS && isHTMLProxy) {
          if (styleAttrRE.test(id)) {
            css = css.replace(/"/g, '&quot;')
          } else {
            if (config.command !== 'serve' && config.build.cssMinify) {
              css = await minifyCSS(css, config, true, id)
            }
            css = css.replace(styleTagCloseRE, '<\\/style')
          }
          const index = htmlProxyIndexRE.exec(id)?.[1]
          if (index == null) {
            throw new Error(`HTML proxy index in "${id}" not found`)
          }
          addToHTMLProxyTransformResult(
            `${getHash(cleanUrl(id))}_${Number.parseInt(index)}`,
            css,
          )
          return {
            code: `export default ''`,
            map: { mappings: '' },
          }
        }

        const inlined = inlineRE.test(id)
        const modules = cssModulesCache.get(config)!.get(id)

        // #6984, #7552
        // `foo.module.css` => modulesCode
        // `foo.module.css?inline` => cssContent
        const modulesCode =
          modules &&
          !inlined &&
          dataToEsm(modules, { namedExports: true, preferConst: true })

        if (config.command === 'serve') {
          const getContentWithSourcemap = async (content: string) => {
            if (config.css.devSourcemap) {
              const sourcemap = this.getCombinedSourcemap()
              if (sourcemap.mappings) {
                await injectSourcesContent(
                  sourcemap,
                  cleanUrl(id),
                  config.logger,
                )
              }
              return getCodeWithSourcemap('css', content, sourcemap)
            }
            return content
          }

          if (isDirectCSSRequest(id)) {
            return null
          }
          if (inlined) {
            return `export default ${JSON.stringify(css)}`
          }
          if (this.environment.config.consumer === 'server') {
            return modulesCode || 'export {}'
          }

          const cssContent = await getContentWithSourcemap(css)
          const code = [
            `import { updateStyle as __vite__updateStyle, removeStyle as __vite__removeStyle } from ${JSON.stringify(
              path.posix.join(config.base, CLIENT_PUBLIC_PATH),
            )}`,
            `const __vite__id = ${JSON.stringify(id)}`,
            `const __vite__css = ${JSON.stringify(cssContent)}`,
            `__vite__updateStyle(__vite__id, __vite__css)`,
            // css modules exports change on edit so it can't self accept
            `${modulesCode || 'import.meta.hot.accept()'}`,
            `import.meta.hot.prune(() => __vite__removeStyle(__vite__id))`,
          ].join('\n')
          return { code, map: { mappings: '' }, moduleType: 'js' }
        }

        // build CSS handling ----------------------------------------------------

        // record css
        if (!inlined) {
          styles.set(id, css)
        }

        let code: string
        if (modulesCode) {
          code = modulesCode
        } else if (inlined) {
          let content = css
          if (config.build.cssMinify) {
            content = await minifyCSS(content, config, true, id)
          }
          code = `export default ${JSON.stringify(content)}`
        } else {
          // empty module when it's not a CSS module nor `?inline`
          code = ''
        }

        return {
          code,
          map: { mappings: '' },
          // avoid the css module from being tree-shaken so that we can retrieve
          // it in renderChunk()
          moduleSideEffects: modulesCode || inlined ? false : 'no-treeshake',
          moduleType: 'js',
        }
      },
    },

    ...(config.command === 'build'
      ? {
          async renderChunk(code, chunk, opts, meta) {
            let chunkCSS: string | undefined
            const renderedModules = new Proxy(
              {} as Record<string, RenderedModule | undefined>,
              {
                get(_target, p) {
                  for (const name in meta.chunks) {
                    const modules = meta.chunks[name].modules
                    const module = modules[p as string]
                    if (module) {
                      return module
                    }
                  }
                },
              },
            )
            // the chunk is empty if it's a dynamic entry chunk that only contains a CSS import
            const isJsChunkEmpty = code === '' && !chunk.isEntry
            let isPureCssChunk = chunk.exports.length === 0
            const ids = Object.keys(chunk.modules)
            for (const id of ids) {
              if (styles.has(id)) {
                // ?transform-only is used for ?url and shouldn't be included in normal CSS chunks
                if (transformOnlyRE.test(id)) {
                  continue
                }

                // If this CSS is scoped to its importers exports, check if those importers exports
                // are rendered in the chunks. If they are not, we can skip bundling this CSS.
                const cssScopeTo =
                  this.getModuleInfo(id)?.meta?.vite?.cssScopeTo
                if (
                  cssScopeTo &&
                  !isCssScopeToRendered(cssScopeTo, renderedModules)
                ) {
                  continue
                }

                // a css module contains JS, so it makes this not a pure css chunk
                if (cssModuleRE.test(id)) {
                  isPureCssChunk = false
                }

                chunkCSS = (chunkCSS || '') + styles.get(id)
              } else if (!isJsChunkEmpty) {
                // if the module does not have a style, then it's not a pure css chunk.
                // this is true because in the `transform` hook above, only modules
                // that are css gets added to the `styles` map.
                isPureCssChunk = false
              }
            }

            const publicAssetUrlMap = publicAssetUrlCache.get(config)!

            // resolve asset URL placeholders to their built file URLs
            const resolveAssetUrlsInCss = (
              chunkCSS: string,
              cssAssetName: string,
              originalFileName?: string,
            ) => {
              const encodedPublicUrls = encodePublicUrlsInCSS(config)

              const relative = config.base === './' || config.base === ''
              const cssAssetDirname =
                encodedPublicUrls || relative
                  ? slash(getCssAssetDirname(cssAssetName, originalFileName))
                  : undefined

              const toRelative = (filename: string) => {
                // relative base + extracted CSS
                const relativePath = normalizePath(
                  path.relative(cssAssetDirname!, filename),
                )
                return relativePath[0] === '.'
                  ? relativePath
                  : './' + relativePath
              }

              // replace asset url references with resolved url.
              chunkCSS = chunkCSS.replace(assetUrlRE, (_, fileHash, urlId) => {
                const filename =
                  this.getFileName(fileHash) +
                  getAssetUrlPostfix(this.environment, urlId)
                chunk.viteMetadata!.importedAssets.add(cleanUrl(filename))
                return encodeURIPath(
                  toOutputFilePathInCss(
                    filename,
                    'asset',
                    cssAssetName,
                    'css',
                    config,
                    toRelative,
                  ),
                )
              })
              // resolve public URL from CSS paths
              if (encodedPublicUrls) {
                const relativePathToPublicFromCSS = normalizePath(
                  path.relative(cssAssetDirname!, ''),
                )
                chunkCSS = chunkCSS.replace(publicAssetUrlRE, (_, hash) => {
                  const publicUrl = publicAssetUrlMap.get(hash)!.slice(1)
                  return encodeURIPath(
                    toOutputFilePathInCss(
                      publicUrl,
                      'public',
                      cssAssetName,
                      'css',
                      config,
                      () => `${relativePathToPublicFromCSS}/${publicUrl}`,
                    ),
                  )
                })
              }
              return chunkCSS
            }

            function ensureFileExt(name: string, ext: string) {
              return normalizePath(
                path.format({ ...path.parse(name), base: undefined, ext }),
              )
            }

            let s: MagicString | undefined
            const urlEmitTasks: Array<{
              cssAssetName: string
              originalFileName: string
              content: string
              start: number
              end: number
            }> = []

            if (code.includes('__VITE_CSS_URL__')) {
              let match: RegExpExecArray | null
              cssUrlAssetRE.lastIndex = 0
              while ((match = cssUrlAssetRE.exec(code))) {
                const [full, idHex] = match
                const id = Buffer.from(idHex, 'hex').toString()
                const originalFileName = cleanUrl(id)
                const cssAssetName = ensureFileExt(
                  path.basename(originalFileName),
                  '.css',
                )
                if (!styles.has(id)) {
                  throw new Error(
                    `css content for ${JSON.stringify(id)} was not found`,
                  )
                }

                let cssContent = styles.get(id)!

                cssContent = resolveAssetUrlsInCss(
                  cssContent,
                  cssAssetName,
                  originalFileName,
                )

                urlEmitTasks.push({
                  cssAssetName,
                  originalFileName,
                  content: cssContent,
                  start: match.index,
                  end: match.index + full.length,
                })
              }
            }

            // should await even if this chunk does not include __VITE_CSS_URL__
            // so that code after this line runs in the same order
            await urlEmitQueue.run(async () =>
              Promise.all(
                urlEmitTasks.map(async (info) => {
                  info.content = await finalizeCss(info.content, config)
                }),
              ),
            )
            if (urlEmitTasks.length > 0) {
              const toRelativeRuntime =
                createToImportMetaURLBasedRelativeRuntime(
                  opts.format,
                  config.isWorker,
                )
              s ||= new MagicString(code)

              for (const {
                cssAssetName,
                originalFileName,
                content,
                start,
                end,
              } of urlEmitTasks) {
                const referenceId = this.emitFile({
                  type: 'asset',
                  name: cssAssetName,
                  originalFileName,
                  source: content,
                })

                const filename = this.getFileName(referenceId)
                chunk.viteMetadata!.importedAssets.add(cleanUrl(filename))
                const replacement = toOutputFilePathInJS(
                  this.environment,
                  filename,
                  'asset',
                  chunk.fileName,
                  'js',
                  toRelativeRuntime,
                )
                const replacementString =
                  typeof replacement === 'string'
                    ? JSON.stringify(encodeURIPath(replacement)).slice(1, -1)
                    : `"+${replacement.runtime}+"`
                s.update(start, end, replacementString)
              }
            }

            if (chunkCSS !== undefined) {
              if (
                isPureCssChunk &&
                (opts.format === 'es' || opts.format === 'cjs')
              ) {
                // this is a shared CSS-only chunk that is empty.
                pureCssChunks.add(chunk)
              }

              if (this.environment.config.build.cssCodeSplit) {
                if (
                  (opts.format === 'es' || opts.format === 'cjs') &&
                  !chunk.fileName.includes('-legacy')
                ) {
                  const isEntry = chunk.isEntry && isPureCssChunk
                  const cssFullAssetName = ensureFileExt(chunk.name, '.css')
                  // if facadeModuleId doesn't exist or doesn't have a CSS extension,
                  // that means a JS entry file imports a CSS file.
                  // in this case, only use the filename for the CSS chunk name like JS chunks.
                  const cssAssetName =
                    chunk.isEntry &&
                    (!chunk.facadeModuleId ||
                      !isCSSRequest(chunk.facadeModuleId))
                      ? path.basename(cssFullAssetName)
                      : cssFullAssetName
                  const originalFileName = getChunkOriginalFileName(
                    chunk,
                    config.root,
                    this.environment.config.isOutputOptionsForLegacyChunks?.(
                      opts,
                    ) ?? false,
                  )

                  chunkCSS = resolveAssetUrlsInCss(
                    chunkCSS,
                    cssAssetName,
                    originalFileName,
                  )

                  // wait for previous tasks as well
                  chunkCSS = await codeSplitEmitQueue.run(async () => {
                    return finalizeCss(chunkCSS!, config)
                  })

                  // emit corresponding css file
                  const referenceId = this.emitFile({
                    type: 'asset',
                    name: cssAssetName,
                    originalFileName,
                    source: chunkCSS,
                  })
                  chunkCssReferences.set(chunk.fileName, referenceId)
                  if (isEntry) {
                    cssEntriesMap
                      .get(this.environment)!
                      .set(chunk.fileName, { referenceId, name: chunk.name })
                  }
                  chunk.viteMetadata!.importedCss.add(
                    this.getFileName(referenceId),
                  )
                } else if (this.environment.config.consumer === 'client') {
                  // legacy build and inline css

                  // Entry chunk CSS will be collected into `chunk.viteMetadata.importedCss`
                  // and injected later by the `'vite:build-html'` plugin into the `index.html`
                  // so it will be duplicated. (https://github.com/vitejs/vite/issues/2062#issuecomment-782388010)
                  // But because entry chunk can be imported by dynamic import,
                  // we shouldn't remove the inlined CSS. (#10285)

                  chunkCSS = await finalizeCss(chunkCSS, config)
                  let cssString = JSON.stringify(chunkCSS)
                  cssString =
                    renderAssetUrlInJS(
                      this,
                      chunk,
                      opts,
                      cssString,
                    )?.toString() || cssString
                  const style = `__vite_style__`
                  const injectCode =
                    `var ${style} = document.createElement('style');` +
                    `${style}.textContent = ${cssString};` +
                    `document.head.appendChild(${style});`

                  s ||= new MagicString(code)
                  injectInlinedCSS(s, this, code, opts.format, injectCode)
                }
              } else {
                // resolve public URL from CSS paths, we need to use absolute paths
                chunkCSS = resolveAssetUrlsInCss(
                  chunkCSS,
                  getCssBundleName(),
                  defaultCssBundleName,
                )
                // finalizeCss is called for the aggregated chunk in generateBundle

                chunkCSSMap.set(chunk.fileName, chunkCSS)
              }
            }

            if (s) {
              if (config.build.sourcemap) {
                return {
                  code: s.toString(),
                  map: s.generateMap({ hires: 'boundary' }),
                }
              } else {
                return { code: s.toString() }
              }
            }
            return null
          },

          augmentChunkHash(chunk) {
            if (chunk.viteMetadata?.importedCss.size) {
              let hash = ''
              for (const id of chunk.viteMetadata.importedCss) {
                hash += id
              }
              return hash
            }
          },
        }
      : {}),

    async generateBundle(opts, bundle) {
      // to avoid emitting duplicate assets for modern build and legacy build
      if (this.environment.config.isOutputOptionsForLegacyChunks?.(opts)) {
        return
      }

      // vite:asset cleans up earlier assets of 'renderChunk',
      // but with cssCodeSplit=false we may still emit CSS here.
      // So is our responsibility to respect emitAssets
      const canEmitAssets =
        config.command !== 'build' || this.environment.config.build.emitAssets

      // extract as single css bundle if no codesplit
      if (
        canEmitAssets &&
        !this.environment.config.build.cssCodeSplit &&
        !hasEmitted
      ) {
        let extractedCss = ''
        const collected = new Set<OutputChunk>()
        // will be populated in order they are used by entry points
        const dynamicImports = new Set<string>()

        function collect(chunk: OutputChunk | OutputAsset | undefined) {
          if (!chunk || chunk.type !== 'chunk' || collected.has(chunk)) return
          collected.add(chunk)

          // First collect all styles from the synchronous imports (lowest priority)
          chunk.imports.forEach((importName) => collect(bundle[importName]))
          // Save dynamic imports in deterministic order to add the styles later (to have the highest priority)
          chunk.dynamicImports.forEach((importName) =>
            dynamicImports.add(importName),
          )
          // Then collect the styles of the current chunk (might overwrite some styles from previous imports)
          extractedCss += chunkCSSMap.get(chunk.preliminaryFileName) ?? ''
        }

        // The bundle is guaranteed to be deterministic, if not then we have a bug in rollup.
        // So we use it to ensure a deterministic order of styles
        for (const chunk of Object.values(bundle)) {
          if (chunk.type === 'chunk' && chunk.isEntry) {
            collect(chunk)
          }
        }
        // Now collect the dynamic chunks, this is done last to have the styles overwrite the previous ones
        for (const chunkName of dynamicImports) {
          collect(bundle[chunkName])
        }

        // Finally, if there's any extracted CSS, we emit the asset
        if (extractedCss) {
          hasEmitted = true
          extractedCss = await finalizeCss(extractedCss, config)
          this.emitFile({
            name: getCssBundleName(),
            type: 'asset',
            source: extractedCss,
            // this file is an implicit entry point, use defaultCssBundleName as the original file name
            // this name is also used as a key in the manifest
            originalFileName: defaultCssBundleName,
          })
        }
      }

      // With `cssCodeSplit: false`, CSS is emitted as a single stylesheet in the HTML,
      // so this per-chunk import map handling is irrelevant.
      const importMap = getImportMap(bundle, this.environment.config)
      if (importMap && chunkCssReferences.size) {
        // The import map hash identifies the JS chunk independently of its content.
        // Since each chunk has at most one extracted CSS sidecar, we can reuse that
        // stable identity with a `.css` extension while mapping it to the CSS content hash.
        const importMapReverseMapping = Object.fromEntries(
          Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
        )
        const chunksByPreliminaryFileName = new Map(
          Object.values(bundle)
            .filter((output): output is OutputChunk => output.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk]),
        )

        for (const [chunkFileName, referenceId] of chunkCssReferences) {
          const chunk = chunksByPreliminaryFileName.get(chunkFileName)
          if (!chunk) continue

          const stableChunkFileName =
            importMapReverseMapping[chunk.fileName] ?? chunk.fileName
          const extension = path.posix.extname(stableChunkFileName)
          const stableCssFileName = `${stableChunkFileName.slice(
            0,
            extension ? -extension.length : undefined,
          )}.css`
          importMap.content.imports[config.base + stableCssFileName] =
            config.base + this.getFileName(referenceId)
        }
        importMap.asset.source = JSON.stringify(importMap.content)
      }

      // remove empty css chunks and their imports
      if (pureCssChunks.size) {
        // map each pure css chunk (rendered chunk) to it's corresponding bundle
        // chunk. we check that by `preliminaryFileName` as they have different
        // `filename`s (rendered chunk has the !~{XXX}~ placeholder)
        const prelimaryNameToChunkMap = Object.fromEntries(
          Object.values(bundle)
            .filter((chunk): chunk is OutputChunk => chunk.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk.fileName]),
        )

        // When running in watch mode the generateBundle is called once per output format
        // in this case the `bundle` is not populated with the other output files
        // but they are still in `pureCssChunks`.
        // So we need to filter the names and only use those who are defined
        const pureCssChunkNames = [...pureCssChunks]
          .map((pureCssChunk) => prelimaryNameToChunkMap[pureCssChunk.fileName])
          .filter(Boolean)
        const pureCssChunkNameSet = new Set(pureCssChunkNames)

        let importMapReverseMapping: Record<string, string> | undefined
        if (importMap) {
          importMapReverseMapping = Object.fromEntries(
            Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
          )
        }
        const pureCssChunkNamesInCode = importMapReverseMapping
          ? pureCssChunkNames.map(
              (name) => importMapReverseMapping![name] ?? name,
            )
          : pureCssChunkNames

        const replaceEmptyChunk = getEmptyChunkReplacer(
          pureCssChunkNamesInCode,
          opts.format,
        )

        for (const file in bundle) {
          const chunk = bundle[file]
          if (chunk.type === 'chunk') {
            let chunkImportsPureCssChunk = false
            // remove pure css chunk from other chunk's imports,
            // and also register the emitted CSS files under the importer
            // chunks instead.
            chunk.imports = chunk.imports.filter((file) => {
              if (pureCssChunkNameSet.has(file)) {
                const { importedCss, importedAssets } = (
                  bundle[file] as OutputChunk
                ).viteMetadata!
                importedCss.forEach((file) =>
                  chunk.viteMetadata!.importedCss.add(file),
                )
                importedAssets.forEach((file) =>
                  chunk.viteMetadata!.importedAssets.add(file),
                )
                chunkImportsPureCssChunk = true
                return false
              }
              return true
            })
            if (chunkImportsPureCssChunk) {
              chunk.code = replaceEmptyChunk(chunk.code)
            }
          }
        }

        const removedPureCssFiles = removedPureCssFilesCache.get(config)!
        pureCssChunkNames.forEach((fileName) => {
          const emptyJsPlaceholder = bundle[fileName] as OutputChunk
          if (emptyJsPlaceholder.isEntry) {
            const { importedAssets, importedCss } =
              emptyJsPlaceholder.viteMetadata!
            const cssReferenceId = cssEntriesMap
              .get(this.environment)!
              .get(emptyJsPlaceholder.preliminaryFileName)!.referenceId
            const realCssEntryName = this.getFileName(cssReferenceId)
            const realCssEntry = bundle[realCssEntryName]!
            importedCss.delete(realCssEntryName)
            if (importedAssets.size) {
              realCssEntry.viteMetadata!.importedAssets = importedAssets
            }
            if (importedCss.size) {
              realCssEntry.viteMetadata!.importedCss = importedCss
            }
          }

          removedPureCssFiles.set(fileName, emptyJsPlaceholder)
          delete bundle[fileName]
          delete bundle[`${fileName}.map`]
        })
      }

      const cssAssets = Object.values(bundle).filter(
        (asset): asset is OutputAsset =>
          asset.type === 'asset' && asset.fileName.endsWith('.css'),
      )
      for (const cssAsset of cssAssets) {
        if (typeof cssAsset.source === 'string') {
          cssAsset.source = cssAsset.source.replace(viteHashUpdateMarkerRE, '')
        }
      }
    },
  }
}
```

### 🔹 函式: `generateBundle()`
- **變更前簽章 (Before)**: `generateBundle(opts, bundle)` (L1018~L1220)
- **變更後簽章 (After)**: `generateBundle(opts, bundle)` (L1018~L1216)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async generateBundle(opts, bundle) {
      // to avoid emitting duplicate assets for modern build and legacy build
      if (this.environment.config.isOutputOptionsForLegacyChunks?.(opts)) {
        return
      }

      // vite:asset cleans up earlier assets of 'renderChunk',
      // but with cssCodeSplit=false we may still emit CSS here.
      // So is our responsibility to respect emitAssets
      const canEmitAssets =
        config.command !== 'build' || this.environment.config.build.emitAssets

      // extract as single css bundle if no codesplit
      if (
        canEmitAssets &&
        !this.environment.config.build.cssCodeSplit &&
        !hasEmitted
      ) {
        let extractedCss = ''
        const collected = new Set<OutputChunk>()
        // will be populated in order they are used by entry points
        const dynamicImports = new Set<string>()

        function collect(chunk: OutputChunk | OutputAsset | undefined) {
          if (!chunk || chunk.type !== 'chunk' || collected.has(chunk)) return
          collected.add(chunk)

          // First collect all styles from the synchronous imports (lowest priority)
          chunk.imports.forEach((importName) => collect(bundle[importName]))
          // Save dynamic imports in deterministic order to add the styles later (to have the highest priority)
          chunk.dynamicImports.forEach((importName) =>
            dynamicImports.add(importName),
          )
          // Then collect the styles of the current chunk (might overwrite some styles from previous imports)
          extractedCss += chunkCSSMap.get(chunk.preliminaryFileName) ?? ''
        }

        // The bundle is guaranteed to be deterministic, if not then we have a bug in rollup.
        // So we use it to ensure a deterministic order of styles
        for (const chunk of Object.values(bundle)) {
          if (chunk.type === 'chunk' && chunk.isEntry) {
            collect(chunk)
          }
        }
        // Now collect the dynamic chunks, this is done last to have the styles overwrite the previous ones
        for (const chunkName of dynamicImports) {
          collect(bundle[chunkName])
        }

        // Finally, if there's any extracted CSS, we emit the asset
        if (extractedCss) {
          hasEmitted = true
          extractedCss = await finalizeCss(extractedCss, config)
          this.emitFile({
            name: getCssBundleName(),
            type: 'asset',
            source: extractedCss,
            // this file is an implicit entry point, use defaultCssBundleName as the original file name
            // this name is also used as a key in the manifest
            originalFileName: defaultCssBundleName,
          })
        }
      }

      // With `cssCodeSplit: false`, CSS is emitted as a single stylesheet in the HTML,
      // so this per-chunk import map handling is irrelevant.
      if (
        this.environment.config.build.chunkImportMap &&
        chunkCssReferences.size
      ) {
        // The import map hash identifies the JS chunk independently of its content.
        // Since each chunk has at most one extracted CSS sidecar, we can reuse that
        // stable identity with a `.css` extension while mapping it to the CSS content hash.
        const importMap = getImportMap(bundle, this.environment.config)!
        const importMapReverseMapping = Object.fromEntries(
          Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
        )
        const chunksByPreliminaryFileName = new Map(
          Object.values(bundle)
            .filter((output): output is OutputChunk => output.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk]),
        )

        for (const [chunkFileName, referenceId] of chunkCssReferences) {
          const chunk = chunksByPreliminaryFileName.get(chunkFileName)
          if (!chunk) continue

          const stableChunkFileName =
            importMapReverseMapping[chunk.fileName] ?? chunk.fileName
          const extension = path.posix.extname(stableChunkFileName)
          const stableCssFileName = `${stableChunkFileName.slice(
            0,
            extension ? -extension.length : undefined,
          )}.css`
          importMap.content.imports[config.base + stableCssFileName] =
            config.base + this.getFileName(referenceId)
        }
        importMap.asset.source = JSON.stringify(importMap.content)
      }

      // remove empty css chunks and their imports
      if (pureCssChunks.size) {
        // map each pure css chunk (rendered chunk) to it's corresponding bundle
        // chunk. we check that by `preliminaryFileName` as they have different
        // `filename`s (rendered chunk has the !~{XXX}~ placeholder)
        const prelimaryNameToChunkMap = Object.fromEntries(
          Object.values(bundle)
            .filter((chunk): chunk is OutputChunk => chunk.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk.fileName]),
        )

        // When running in watch mode the generateBundle is called once per output format
        // in this case the `bundle` is not populated with the other output files
        // but they are still in `pureCssChunks`.
        // So we need to filter the names and only use those who are defined
        const pureCssChunkNames = [...pureCssChunks]
          .map((pureCssChunk) => prelimaryNameToChunkMap[pureCssChunk.fileName])
          .filter(Boolean)
        const pureCssChunkNameSet = new Set(pureCssChunkNames)

        let importMapReverseMapping: Record<string, string> | undefined
        if (this.environment.config.build.chunkImportMap) {
          const importMap = getImportMap(bundle, this.environment.config)!
          importMapReverseMapping = Object.fromEntries(
            Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
          )
        }
        const pureCssChunkNamesInCode = importMapReverseMapping
          ? pureCssChunkNames.map(
              (name) => importMapReverseMapping![name] ?? name,
            )
          : pureCssChunkNames

        const replaceEmptyChunk = getEmptyChunkReplacer(
          pureCssChunkNamesInCode,
          opts.format,
        )

        for (const file in bundle) {
          const chunk = bundle[file]
          if (chunk.type === 'chunk') {
            let chunkImportsPureCssChunk = false
            // remove pure css chunk from other chunk's imports,
            // and also register the emitted CSS files under the importer
            // chunks instead.
            chunk.imports = chunk.imports.filter((file) => {
              if (pureCssChunkNameSet.has(file)) {
                const { importedCss, importedAssets } = (
                  bundle[file] as OutputChunk
                ).viteMetadata!
                importedCss.forEach((file) =>
                  chunk.viteMetadata!.importedCss.add(file),
                )
                importedAssets.forEach((file) =>
                  chunk.viteMetadata!.importedAssets.add(file),
                )
                chunkImportsPureCssChunk = true
                return false
              }
              return true
            })
            if (chunkImportsPureCssChunk) {
              chunk.code = replaceEmptyChunk(chunk.code)
            }
          }
        }

        const removedPureCssFiles = removedPureCssFilesCache.get(config)!
        pureCssChunkNames.forEach((fileName) => {
          const emptyJsPlaceholder = bundle[fileName] as OutputChunk
          if (emptyJsPlaceholder.isEntry) {
            const { importedAssets, importedCss } =
              emptyJsPlaceholder.viteMetadata!
            const cssReferenceId = cssEntriesMap
              .get(this.environment)!
              .get(emptyJsPlaceholder.preliminaryFileName)!.referenceId
            const realCssEntryName = this.getFileName(cssReferenceId)
            const realCssEntry = bundle[realCssEntryName]!
            importedCss.delete(realCssEntryName)
            if (importedAssets.size) {
              realCssEntry.viteMetadata!.importedAssets = importedAssets
            }
            if (importedCss.size) {
              realCssEntry.viteMetadata!.importedCss = importedCss
            }
          }

          removedPureCssFiles.set(fileName, emptyJsPlaceholder)
          delete bundle[fileName]
          delete bundle[`${fileName}.map`]
        })
      }

      const cssAssets = Object.values(bundle).filter(
        (asset): asset is OutputAsset =>
          asset.type === 'asset' && asset.fileName.endsWith('.css'),
      )
      for (const cssAsset of cssAssets) {
        if (typeof cssAsset.source === 'string') {
          cssAsset.source = cssAsset.source.replace(viteHashUpdateMarkerRE, '')
        }
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async generateBundle(opts, bundle) {
      // to avoid emitting duplicate assets for modern build and legacy build
      if (this.environment.config.isOutputOptionsForLegacyChunks?.(opts)) {
        return
      }

      // vite:asset cleans up earlier assets of 'renderChunk',
      // but with cssCodeSplit=false we may still emit CSS here.
      // So is our responsibility to respect emitAssets
      const canEmitAssets =
        config.command !== 'build' || this.environment.config.build.emitAssets

      // extract as single css bundle if no codesplit
      if (
        canEmitAssets &&
        !this.environment.config.build.cssCodeSplit &&
        !hasEmitted
      ) {
        let extractedCss = ''
        const collected = new Set<OutputChunk>()
        // will be populated in order they are used by entry points
        const dynamicImports = new Set<string>()

        function collect(chunk: OutputChunk | OutputAsset | undefined) {
          if (!chunk || chunk.type !== 'chunk' || collected.has(chunk)) return
          collected.add(chunk)

          // First collect all styles from the synchronous imports (lowest priority)
          chunk.imports.forEach((importName) => collect(bundle[importName]))
          // Save dynamic imports in deterministic order to add the styles later (to have the highest priority)
          chunk.dynamicImports.forEach((importName) =>
            dynamicImports.add(importName),
          )
          // Then collect the styles of the current chunk (might overwrite some styles from previous imports)
          extractedCss += chunkCSSMap.get(chunk.preliminaryFileName) ?? ''
        }

        // The bundle is guaranteed to be deterministic, if not then we have a bug in rollup.
        // So we use it to ensure a deterministic order of styles
        for (const chunk of Object.values(bundle)) {
          if (chunk.type === 'chunk' && chunk.isEntry) {
            collect(chunk)
          }
        }
        // Now collect the dynamic chunks, this is done last to have the styles overwrite the previous ones
        for (const chunkName of dynamicImports) {
          collect(bundle[chunkName])
        }

        // Finally, if there's any extracted CSS, we emit the asset
        if (extractedCss) {
          hasEmitted = true
          extractedCss = await finalizeCss(extractedCss, config)
          this.emitFile({
            name: getCssBundleName(),
            type: 'asset',
            source: extractedCss,
            // this file is an implicit entry point, use defaultCssBundleName as the original file name
            // this name is also used as a key in the manifest
            originalFileName: defaultCssBundleName,
          })
        }
      }

      // With `cssCodeSplit: false`, CSS is emitted as a single stylesheet in the HTML,
      // so this per-chunk import map handling is irrelevant.
      const importMap = getImportMap(bundle, this.environment.config)
      if (importMap && chunkCssReferences.size) {
        // The import map hash identifies the JS chunk independently of its content.
        // Since each chunk has at most one extracted CSS sidecar, we can reuse that
        // stable identity with a `.css` extension while mapping it to the CSS content hash.
        const importMapReverseMapping = Object.fromEntries(
          Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
        )
        const chunksByPreliminaryFileName = new Map(
          Object.values(bundle)
            .filter((output): output is OutputChunk => output.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk]),
        )

        for (const [chunkFileName, referenceId] of chunkCssReferences) {
          const chunk = chunksByPreliminaryFileName.get(chunkFileName)
          if (!chunk) continue

          const stableChunkFileName =
            importMapReverseMapping[chunk.fileName] ?? chunk.fileName
          const extension = path.posix.extname(stableChunkFileName)
          const stableCssFileName = `${stableChunkFileName.slice(
            0,
            extension ? -extension.length : undefined,
          )}.css`
          importMap.content.imports[config.base + stableCssFileName] =
            config.base + this.getFileName(referenceId)
        }
        importMap.asset.source = JSON.stringify(importMap.content)
      }

      // remove empty css chunks and their imports
      if (pureCssChunks.size) {
        // map each pure css chunk (rendered chunk) to it's corresponding bundle
        // chunk. we check that by `preliminaryFileName` as they have different
        // `filename`s (rendered chunk has the !~{XXX}~ placeholder)
        const prelimaryNameToChunkMap = Object.fromEntries(
          Object.values(bundle)
            .filter((chunk): chunk is OutputChunk => chunk.type === 'chunk')
            .map((chunk) => [chunk.preliminaryFileName, chunk.fileName]),
        )

        // When running in watch mode the generateBundle is called once per output format
        // in this case the `bundle` is not populated with the other output files
        // but they are still in `pureCssChunks`.
        // So we need to filter the names and only use those who are defined
        const pureCssChunkNames = [...pureCssChunks]
          .map((pureCssChunk) => prelimaryNameToChunkMap[pureCssChunk.fileName])
          .filter(Boolean)
        const pureCssChunkNameSet = new Set(pureCssChunkNames)

        let importMapReverseMapping: Record<string, string> | undefined
        if (importMap) {
          importMapReverseMapping = Object.fromEntries(
            Object.entries(importMap.mapping).map(([k, v]) => [v, k]),
          )
        }
        const pureCssChunkNamesInCode = importMapReverseMapping
          ? pureCssChunkNames.map(
              (name) => importMapReverseMapping![name] ?? name,
            )
          : pureCssChunkNames

        const replaceEmptyChunk = getEmptyChunkReplacer(
          pureCssChunkNamesInCode,
          opts.format,
        )

        for (const file in bundle) {
          const chunk = bundle[file]
          if (chunk.type === 'chunk') {
            let chunkImportsPureCssChunk = false
            // remove pure css chunk from other chunk's imports,
            // and also register the emitted CSS files under the importer
            // chunks instead.
            chunk.imports = chunk.imports.filter((file) => {
              if (pureCssChunkNameSet.has(file)) {
                const { importedCss, importedAssets } = (
                  bundle[file] as OutputChunk
                ).viteMetadata!
                importedCss.forEach((file) =>
                  chunk.viteMetadata!.importedCss.add(file),
                )
                importedAssets.forEach((file) =>
                  chunk.viteMetadata!.importedAssets.add(file),
                )
                chunkImportsPureCssChunk = true
                return false
              }
              return true
            })
            if (chunkImportsPureCssChunk) {
              chunk.code = replaceEmptyChunk(chunk.code)
            }
          }
        }

        const removedPureCssFiles = removedPureCssFilesCache.get(config)!
        pureCssChunkNames.forEach((fileName) => {
          const emptyJsPlaceholder = bundle[fileName] as OutputChunk
          if (emptyJsPlaceholder.isEntry) {
            const { importedAssets, importedCss } =
              emptyJsPlaceholder.viteMetadata!
            const cssReferenceId = cssEntriesMap
              .get(this.environment)!
              .get(emptyJsPlaceholder.preliminaryFileName)!.referenceId
            const realCssEntryName = this.getFileName(cssReferenceId)
            const realCssEntry = bundle[realCssEntryName]!
            importedCss.delete(realCssEntryName)
            if (importedAssets.size) {
              realCssEntry.viteMetadata!.importedAssets = importedAssets
            }
            if (importedCss.size) {
              realCssEntry.viteMetadata!.importedCss = importedCss
            }
          }

          removedPureCssFiles.set(fileName, emptyJsPlaceholder)
          delete bundle[fileName]
          delete bundle[`${fileName}.map`]
        })
      }

      const cssAssets = Object.values(bundle).filter(
        (asset): asset is OutputAsset =>
          asset.type === 'asset' && asset.fileName.endsWith('.css'),
      )
      for (const cssAsset of cssAssets) {
        if (typeof cssAsset.source === 'string') {
          cssAsset.source = cssAsset.source.replace(viteHashUpdateMarkerRE, '')
        }
      }
    }
```


#### 📄 檔案: `packages/vite/src/node/plugins/html.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:123, E:112, A:0) ➔ After(N:123, E:112, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getImportMap()`
- **變更前簽章 (Before)**: `function getImportMap(
  bundle: OutputBundle,
  options: ResolvedEnvironmentOptions & ResolvedConfig,
):
  |` (L1735~L1762)
- **變更後簽章 (After)**: `function getImportMap(
  bundle: OutputBundle,
  options: ResolvedEnvironmentOptions & ResolvedConfig,
):
  |` (L1735~L1764)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getImportMap(
  bundle: OutputBundle,
  options: ResolvedEnvironmentOptions & ResolvedConfig,
):
  | {
      asset: OutputAsset
      content: { imports: Record<string, string> }
      /** import map entries with the base stripped (placeholder name -> real name) */
      mapping: Record<string, string>
    }
  | undefined {
  const asset = bundle[getImportMapFilename(options)] as OutputAsset | undefined
  if (!asset) return undefined

  const content: { imports: Record<string, string> } = JSON.parse(
    typeof asset.source === 'string'
      ? asset.source
      : new TextDecoder().decode(asset.source),
  )
  const baseUrl = getImportMapBaseUrl(options)
  const mapping = Object.fromEntries(
    Object.entries(content.imports).map(([k, v]) => [
      k.slice(baseUrl.length),
      v.slice(baseUrl.length),
    ]),
  )
  return { asset, content, mapping }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getImportMap(
  bundle: OutputBundle,
  options: ResolvedEnvironmentOptions & ResolvedConfig,
):
  | {
      asset: OutputAsset
      content: { imports: Record<string, string> }
      /** import map entries with the base stripped (placeholder name -> real name) */
      mapping: Record<string, string>
    }
  | undefined {
  if (!options.build.chunkImportMap) return undefined

  const asset = bundle[getImportMapFilename(options)] as OutputAsset | undefined
  if (!asset) return undefined

  const content: { imports: Record<string, string> } = JSON.parse(
    typeof asset.source === 'string'
      ? asset.source
      : new TextDecoder().decode(asset.source),
  )
  const baseUrl = getImportMapBaseUrl(options)
  const mapping = Object.fromEntries(
    Object.entries(content.imports).map(([k, v]) => [
      k.slice(baseUrl.length),
      v.slice(baseUrl.length),
    ]),
  )
  return { asset, content, mapping }
}
```


#### 📄 檔案: `packages/vite/src/node/plugins/importAnalysisBuild.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:53, E:36, A:3) ➔ After(N:53, E:36, A:3)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#cspNonceMeta** `(Control)`
  🌲 **#link** `(Control)`
    └── ⚡ **on('error')**
        └── 🎯 [CALLS] `rej (External/Unresolved)()`
    └── ⚡ **on('load')**
        └── 🎯 [TRIGGERS] `res (External/Unresolved)()`
  🌲 **#relList** `(Control)`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `generateBundle()`
- **變更前簽章 (Before)**: `generateBundle(opts, bundle)` (L333~L687)
- **變更後簽章 (After)**: `generateBundle(opts, bundle)` (L333~L687)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async generateBundle(opts, bundle) {
      const { format } = opts
      if (format !== 'es') {
        return
      }

      await init

      // If preload is not enabled, we parse through each imports and remove any imports to pure CSS chunks
      // as they are removed from the bundle
      if (!getInsertPreload(this.environment)) {
        const removedPureCssFiles = removedPureCssFilesCache.get(config)
        if (removedPureCssFiles && removedPureCssFiles.size > 0) {
          for (const file in bundle) {
            const chunk = bundle[file]
            if (chunk.type === 'chunk' && chunk.code.includes('import')) {
              const code = chunk.code
              let imports!: ImportSpecifier[]
              try {
                imports = parseImports(code)[0].filter((i) => i.d > -1)
              } catch (e: any) {
                const loc = numberToPos(code, e.idx)
                this.error({
                  name: e.name,
                  message: e.message,
                  stack: e.stack,
                  cause: e.cause,
                  pos: e.idx,
                  loc: { ...loc, file: chunk.fileName },
                  frame: generateCodeFrame(code, loc),
                })
              }

              for (const imp of imports) {
                const {
                  n: name,
                  s: start,
                  e: end,
                  ss: expStart,
                  se: expEnd,
                } = imp
                let url = name
                if (!url) {
                  const rawUrl = code.slice(start, end)
                  if (
                    (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                    (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                  )
                    url = rawUrl.slice(1, -1)
                }
                if (!url) continue

                const normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )
                if (removedPureCssFiles.has(normalizedFile)) {
                  // remove with Promise.resolve({}) while preserving source map location
                  chunk.code =
                    chunk.code.slice(0, expStart) +
                    `Promise.resolve({${''.padEnd(expEnd - expStart - 19, ' ')}})` +
                    chunk.code.slice(expEnd)
                }
              }
            }
          }
        }
        return
      }
      const buildSourcemap = this.environment.config.build.sourcemap
      const { modulePreload } = this.environment.config.build

      let importMapMapping: Record<string, string> | undefined
      let importMapReverseMapping: Record<string, string> | undefined
      if (this.environment.config.build.chunkImportMap) {
        const importMap = getImportMap(bundle, this.environment.config)!
        importMapMapping = importMap.mapping
        importMapReverseMapping = Object.fromEntries(
          Object.entries(importMapMapping).map(([k, v]) => [v, k]),
        )

        if (config.isOutputOptionsForLegacyChunks?.(opts)) {
          this.emitFile({
            type: 'asset',
            fileName: 'importmap.legacy.json',
            source: importMap.asset.source,
          })
          delete bundle[getImportMapFilename(this.environment.config)]
        }
      }

      for (const file in bundle) {
        const chunk = bundle[file]
        // can't use chunk.dynamicImports.length here since some modules e.g.
        // dynamic import to constant json may get inlined.
        if (chunk.type === 'chunk' && chunk.code.includes(preloadMarker)) {
          const code = chunk.code
          let imports!: ImportSpecifier[]
          try {
            imports = parseImports(code)[0].filter((i) => i.d > -1)
          } catch (e: any) {
            const loc = numberToPos(code, e.idx)
            this.error({
              name: e.name,
              message: e.message,
              stack: e.stack,
              cause: e.cause,
              pos: e.idx,
              loc: { ...loc, file: chunk.fileName },
              frame: generateCodeFrame(code, loc),
            })
          }

          const s = new MagicString(code)
          const rewroteMarkerStartPos = new Set() // position of the leading double quote

          const fileDeps: FileDep[] = []
          const addFileDep = (
            url: string,
            runtime: boolean = false,
          ): number => {
            const index = fileDeps.findIndex((dep) => dep.url === url)
            if (index === -1) {
              return fileDeps.push({ url, runtime }) - 1
            } else {
              return index
            }
          }

          if (imports.length) {
            const importMarkerPos = matchImportsToPreloadMarkers(code, imports)

            for (let index = 0; index < imports.length; index++) {
              // To handle escape sequences in specifier strings, the .n field will be provided where possible.
              const {
                n: name,
                s: start,
                e: end,
                ss: expStart,
                se: expEnd,
              } = imports[index]
              // check the chunk being imported
              let url = name
              if (!url) {
                const rawUrl = code.slice(start, end)
                if (
                  (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                  (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                )
                  url = rawUrl.slice(1, -1)
              }
              const deps = new Set<string>()
              let hasRemovedPureCssChunk = false

              let normalizedFile: string | undefined = undefined

              if (url) {
                normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )

                const ownerFilename = chunk.fileName
                // literal import - trace direct imports and add to deps
                const analyzed: Set<string> = new Set<string>()
                const addDeps = (rawFilename: string) => {
                  const filename =
                    importMapMapping?.[rawFilename] ?? rawFilename
                  if (filename === ownerFilename) return
                  if (analyzed.has(filename)) return
                  analyzed.add(filename)
                  const chunk = bundle[filename]
                  if (chunk) {
                    deps.add(chunk.fileName)
                    if (chunk.type === 'chunk') {
                      chunk.imports.forEach(addDeps)
                      // Ensure that the css imported by current chunk is loaded after the dependencies.
                      // So the style of current chunk won't be overwritten unexpectedly.
                      chunk.viteMetadata!.importedCss.forEach((file) => {
                        deps.add(file)
                      })
                    }
                  } else {
                    const removedPureCssFiles =
                      removedPureCssFilesCache.get(config)!
                    const chunk = removedPureCssFiles.get(filename)
                    if (chunk) {
                      if (chunk.viteMetadata!.importedCss.size) {
                        chunk.viteMetadata!.importedCss.forEach((file) => {
                          deps.add(file)
                        })
                        hasRemovedPureCssChunk = true
                      }

                      s.update(expStart, expEnd, 'Promise.resolve({})')
                    }
                  }
                }
                addDeps(normalizedFile)
              }

              const markerStartPos = importMarkerPos[index]

              if (markerStartPos > 0) {
                // the dep list includes the main chunk, so only need to reload when there are actual other deps.
                let depsArray =
                  deps.size > 1 ||
                  // main chunk is removed
                  (hasRemovedPureCssChunk && deps.size > 0)
                    ? modulePreload === false
                      ? // CSS deps use the same mechanism as module preloads, so even if disabled,
                        // we still need to pass these deps to the preload helper in dynamic imports.
                        [...deps].filter((d) => d.endsWith('.css'))
                      : [...deps]
                    : []

                const resolveDependencies = modulePreload
                  ? modulePreload.resolveDependencies
                  : undefined
                if (resolveDependencies && normalizedFile) {
                  // We can't let the user remove css deps as these aren't really preloads, they are just using
                  // the same mechanism as module preloads for this chunk
                  const cssDeps: string[] = []
                  const otherDeps: string[] = []
                  for (const dep of depsArray) {
                    ;(dep.endsWith('.css') ? cssDeps : otherDeps).push(dep)
                  }
                  depsArray = [
                    // NOTE: deps are URLs, not specifiers using the import map mapping
                    ...resolveDependencies(normalizedFile, otherDeps, {
                      hostId: file,
                      hostType: 'js',
                    }),
                    ...cssDeps,
                  ]
                }

                depsArray = depsArray.map(
                  (dep) => importMapReverseMapping?.[dep] ?? dep,
                )

                let renderedDeps: number[]
                if (renderBuiltUrl) {
                  renderedDeps = depsArray.map((dep) => {
                    const replacement = toOutputFilePathInJS(
                      this.environment,
                      dep,
                      'asset',
                      chunk.fileName,
                      'js',
                      toRelativePath,
                    )

                    if (typeof replacement === 'string') {
                      return addFileDep(replacement)
                    }

                    return addFileDep(replacement.runtime, true)
                  })
                } else {
                  renderedDeps = depsArray.map((d) =>
                    // Don't include the assets dir if the default asset file names
                    // are used, the path will be reconstructed by the import preload helper
                    isRelativeBase
                      ? addFileDep(toRelativePath(d, file))
                      : addFileDep(d),
                  )
                }

                s.update(
                  markerStartPos,
                  markerStartPos + preloadMarker.length,
                  renderedDeps.length > 0
                    ? `__vite__mapDeps([${renderedDeps.join(',')}])`
                    : `[]`,
                )
                rewroteMarkerStartPos.add(markerStartPos)
              }
            }
          }

          if (fileDeps.length > 0) {
            const fileDepsCode = `[${fileDeps
              .map((fileDep) =>
                fileDep.runtime ? fileDep.url : JSON.stringify(fileDep.url),
              )
              .join(',')}]`

            const mapDepsCode = `const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=${fileDepsCode})))=>i.map(i=>d[i]);\n`

            // inject extra code at the top or next line of hashbang
            if (code.startsWith('#!')) {
              s.prependLeft(getFileStartIndex(code), mapDepsCode)
            } else {
              s.prepend(mapDepsCode)
            }
          }

          // there may still be markers due to inlined dynamic imports, remove
          // all the markers regardless
          let markerStartPos = findPreloadMarker(code)
          while (markerStartPos >= 0) {
            if (!rewroteMarkerStartPos.has(markerStartPos)) {
              s.update(
                markerStartPos,
                markerStartPos + preloadMarker.length,
                'void 0',
              )
            }
            markerStartPos = findPreloadMarker(
              code,
              markerStartPos + preloadMarker.length,
            )
          }

          if (s.hasChanged()) {
            chunk.code = s.toString()
            if (buildSourcemap && chunk.map) {
              const nextMap = s.generateDecodedMap({
                source: chunk.fileName,
                hires: 'boundary',
              })
              const originalFile = chunk.map.file
              const map = combineSourcemaps(chunk.fileName, [
                nextMap as DecodedSourceMap,
                chunk.map as RawSourceMap,
              ]) as SourceMap
              map.toUrl = () => genSourceMapUrl(map)
              if (originalFile) {
                map.file = originalFile
              }

              const originalDebugId = chunk.map.debugId
              chunk.map = map

              if (buildSourcemap === 'inline') {
                chunk.code = chunk.code.replace(
                  convertSourceMap.mapFileCommentRegex,
                  '',
                )
                chunk.code += `\n//# sourceMappingURL=${genSourceMapUrl(map)}`
              } else {
                if (originalDebugId) {
                  map.debugId = originalDebugId
                }
                const mapAsset = bundle[chunk.fileName + '.map']
                if (mapAsset && mapAsset.type === 'asset') {
                  mapAsset.source = map.toString()
                }
              }
            }
          }
        }
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async generateBundle(opts, bundle) {
      const { format } = opts
      if (format !== 'es') {
        return
      }

      await init

      // If preload is not enabled, we parse through each imports and remove any imports to pure CSS chunks
      // as they are removed from the bundle
      if (!getInsertPreload(this.environment)) {
        const removedPureCssFiles = removedPureCssFilesCache.get(config)
        if (removedPureCssFiles && removedPureCssFiles.size > 0) {
          for (const file in bundle) {
            const chunk = bundle[file]
            if (chunk.type === 'chunk' && chunk.code.includes('import')) {
              const code = chunk.code
              let imports!: ImportSpecifier[]
              try {
                imports = parseImports(code)[0].filter((i) => i.d > -1)
              } catch (e: any) {
                const loc = numberToPos(code, e.idx)
                this.error({
                  name: e.name,
                  message: e.message,
                  stack: e.stack,
                  cause: e.cause,
                  pos: e.idx,
                  loc: { ...loc, file: chunk.fileName },
                  frame: generateCodeFrame(code, loc),
                })
              }

              for (const imp of imports) {
                const {
                  n: name,
                  s: start,
                  e: end,
                  ss: expStart,
                  se: expEnd,
                } = imp
                let url = name
                if (!url) {
                  const rawUrl = code.slice(start, end)
                  if (
                    (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                    (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                  )
                    url = rawUrl.slice(1, -1)
                }
                if (!url) continue

                const normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )
                if (removedPureCssFiles.has(normalizedFile)) {
                  // remove with Promise.resolve({}) while preserving source map location
                  chunk.code =
                    chunk.code.slice(0, expStart) +
                    `Promise.resolve({${''.padEnd(expEnd - expStart - 19, ' ')}})` +
                    chunk.code.slice(expEnd)
                }
              }
            }
          }
        }
        return
      }
      const buildSourcemap = this.environment.config.build.sourcemap
      const { modulePreload } = this.environment.config.build

      let importMapMapping: Record<string, string> | undefined
      let importMapReverseMapping: Record<string, string> | undefined
      const importMap = getImportMap(bundle, this.environment.config)
      if (importMap) {
        importMapMapping = importMap.mapping
        importMapReverseMapping = Object.fromEntries(
          Object.entries(importMapMapping).map(([k, v]) => [v, k]),
        )

        if (config.isOutputOptionsForLegacyChunks?.(opts)) {
          this.emitFile({
            type: 'asset',
            fileName: 'importmap.legacy.json',
            source: importMap.asset.source,
          })
          delete bundle[getImportMapFilename(this.environment.config)]
        }
      }

      for (const file in bundle) {
        const chunk = bundle[file]
        // can't use chunk.dynamicImports.length here since some modules e.g.
        // dynamic import to constant json may get inlined.
        if (chunk.type === 'chunk' && chunk.code.includes(preloadMarker)) {
          const code = chunk.code
          let imports!: ImportSpecifier[]
          try {
            imports = parseImports(code)[0].filter((i) => i.d > -1)
          } catch (e: any) {
            const loc = numberToPos(code, e.idx)
            this.error({
              name: e.name,
              message: e.message,
              stack: e.stack,
              cause: e.cause,
              pos: e.idx,
              loc: { ...loc, file: chunk.fileName },
              frame: generateCodeFrame(code, loc),
            })
          }

          const s = new MagicString(code)
          const rewroteMarkerStartPos = new Set() // position of the leading double quote

          const fileDeps: FileDep[] = []
          const addFileDep = (
            url: string,
            runtime: boolean = false,
          ): number => {
            const index = fileDeps.findIndex((dep) => dep.url === url)
            if (index === -1) {
              return fileDeps.push({ url, runtime }) - 1
            } else {
              return index
            }
          }

          if (imports.length) {
            const importMarkerPos = matchImportsToPreloadMarkers(code, imports)

            for (let index = 0; index < imports.length; index++) {
              // To handle escape sequences in specifier strings, the .n field will be provided where possible.
              const {
                n: name,
                s: start,
                e: end,
                ss: expStart,
                se: expEnd,
              } = imports[index]
              // check the chunk being imported
              let url = name
              if (!url) {
                const rawUrl = code.slice(start, end)
                if (
                  (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                  (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                )
                  url = rawUrl.slice(1, -1)
              }
              const deps = new Set<string>()
              let hasRemovedPureCssChunk = false

              let normalizedFile: string | undefined = undefined

              if (url) {
                normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )

                const ownerFilename = chunk.fileName
                // literal import - trace direct imports and add to deps
                const analyzed: Set<string> = new Set<string>()
                const addDeps = (rawFilename: string) => {
                  const filename =
                    importMapMapping?.[rawFilename] ?? rawFilename
                  if (filename === ownerFilename) return
                  if (analyzed.has(filename)) return
                  analyzed.add(filename)
                  const chunk = bundle[filename]
                  if (chunk) {
                    deps.add(chunk.fileName)
                    if (chunk.type === 'chunk') {
                      chunk.imports.forEach(addDeps)
                      // Ensure that the css imported by current chunk is loaded after the dependencies.
                      // So the style of current chunk won't be overwritten unexpectedly.
                      chunk.viteMetadata!.importedCss.forEach((file) => {
                        deps.add(file)
                      })
                    }
                  } else {
                    const removedPureCssFiles =
                      removedPureCssFilesCache.get(config)!
                    const chunk = removedPureCssFiles.get(filename)
                    if (chunk) {
                      if (chunk.viteMetadata!.importedCss.size) {
                        chunk.viteMetadata!.importedCss.forEach((file) => {
                          deps.add(file)
                        })
                        hasRemovedPureCssChunk = true
                      }

                      s.update(expStart, expEnd, 'Promise.resolve({})')
                    }
                  }
                }
                addDeps(normalizedFile)
              }

              const markerStartPos = importMarkerPos[index]

              if (markerStartPos > 0) {
                // the dep list includes the main chunk, so only need to reload when there are actual other deps.
                let depsArray =
                  deps.size > 1 ||
                  // main chunk is removed
                  (hasRemovedPureCssChunk && deps.size > 0)
                    ? modulePreload === false
                      ? // CSS deps use the same mechanism as module preloads, so even if disabled,
                        // we still need to pass these deps to the preload helper in dynamic imports.
                        [...deps].filter((d) => d.endsWith('.css'))
                      : [...deps]
                    : []

                const resolveDependencies = modulePreload
                  ? modulePreload.resolveDependencies
                  : undefined
                if (resolveDependencies && normalizedFile) {
                  // We can't let the user remove css deps as these aren't really preloads, they are just using
                  // the same mechanism as module preloads for this chunk
                  const cssDeps: string[] = []
                  const otherDeps: string[] = []
                  for (const dep of depsArray) {
                    ;(dep.endsWith('.css') ? cssDeps : otherDeps).push(dep)
                  }
                  depsArray = [
                    // NOTE: deps are URLs, not specifiers using the import map mapping
                    ...resolveDependencies(normalizedFile, otherDeps, {
                      hostId: file,
                      hostType: 'js',
                    }),
                    ...cssDeps,
                  ]
                }

                depsArray = depsArray.map(
                  (dep) => importMapReverseMapping?.[dep] ?? dep,
                )

                let renderedDeps: number[]
                if (renderBuiltUrl) {
                  renderedDeps = depsArray.map((dep) => {
                    const replacement = toOutputFilePathInJS(
                      this.environment,
                      dep,
                      'asset',
                      chunk.fileName,
                      'js',
                      toRelativePath,
                    )

                    if (typeof replacement === 'string') {
                      return addFileDep(replacement)
                    }

                    return addFileDep(replacement.runtime, true)
                  })
                } else {
                  renderedDeps = depsArray.map((d) =>
                    // Don't include the assets dir if the default asset file names
                    // are used, the path will be reconstructed by the import preload helper
                    isRelativeBase
                      ? addFileDep(toRelativePath(d, file))
                      : addFileDep(d),
                  )
                }

                s.update(
                  markerStartPos,
                  markerStartPos + preloadMarker.length,
                  renderedDeps.length > 0
                    ? `__vite__mapDeps([${renderedDeps.join(',')}])`
                    : `[]`,
                )
                rewroteMarkerStartPos.add(markerStartPos)
              }
            }
          }

          if (fileDeps.length > 0) {
            const fileDepsCode = `[${fileDeps
              .map((fileDep) =>
                fileDep.runtime ? fileDep.url : JSON.stringify(fileDep.url),
              )
              .join(',')}]`

            const mapDepsCode = `const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=${fileDepsCode})))=>i.map(i=>d[i]);\n`

            // inject extra code at the top or next line of hashbang
            if (code.startsWith('#!')) {
              s.prependLeft(getFileStartIndex(code), mapDepsCode)
            } else {
              s.prepend(mapDepsCode)
            }
          }

          // there may still be markers due to inlined dynamic imports, remove
          // all the markers regardless
          let markerStartPos = findPreloadMarker(code)
          while (markerStartPos >= 0) {
            if (!rewroteMarkerStartPos.has(markerStartPos)) {
              s.update(
                markerStartPos,
                markerStartPos + preloadMarker.length,
                'void 0',
              )
            }
            markerStartPos = findPreloadMarker(
              code,
              markerStartPos + preloadMarker.length,
            )
          }

          if (s.hasChanged()) {
            chunk.code = s.toString()
            if (buildSourcemap && chunk.map) {
              const nextMap = s.generateDecodedMap({
                source: chunk.fileName,
                hires: 'boundary',
              })
              const originalFile = chunk.map.file
              const map = combineSourcemaps(chunk.fileName, [
                nextMap as DecodedSourceMap,
                chunk.map as RawSourceMap,
              ]) as SourceMap
              map.toUrl = () => genSourceMapUrl(map)
              if (originalFile) {
                map.file = originalFile
              }

              const originalDebugId = chunk.map.debugId
              chunk.map = map

              if (buildSourcemap === 'inline') {
                chunk.code = chunk.code.replace(
                  convertSourceMap.mapFileCommentRegex,
                  '',
                )
                chunk.code += `\n//# sourceMappingURL=${genSourceMapUrl(map)}`
              } else {
                if (originalDebugId) {
                  map.debugId = originalDebugId
                }
                const mapAsset = bundle[chunk.fileName + '.map']
                if (mapAsset && mapAsset.type === 'asset') {
                  mapAsset.source = map.toString()
                }
              }
            }
          }
        }
      }
    }
```

### 🔹 函式: `buildImportAnalysisPlugin()`
- **變更前簽章 (Before)**: `function buildImportAnalysisPlugin(config: ResolvedConfig): Plugin[]` (L306~L708)
- **變更後簽章 (After)**: `function buildImportAnalysisPlugin(config: ResolvedConfig): Plugin[]` (L306~L708)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function buildImportAnalysisPlugin(config: ResolvedConfig): Plugin[] {
  const getInsertPreload = (environment: PartialEnvironment) =>
    environment.config.consumer === 'client' &&
    !config.isWorker &&
    !config.build.lib

  const renderBuiltUrl = config.experimental.renderBuiltUrl
  const isRelativeBase = config.base === './' || config.base === ''

  const plugin: Plugin = {
    name: 'vite:build-import-analysis',

    renderChunk(code, _, { format }) {
      // make sure we only perform the preload logic in modern builds.
      if (code.includes(isModernFlag)) {
        const re = new RegExp(isModernFlag, 'g')
        const isModern = String(format === 'es')
        const isModernWithPadding =
          isModern + ' '.repeat(isModernFlag.length - isModern.length)
        return {
          code: code.replace(re, isModernWithPadding),
          map: null,
        }
      }
      return null
    },

    async generateBundle(opts, bundle) {
      const { format } = opts
      if (format !== 'es') {
        return
      }

      await init

      // If preload is not enabled, we parse through each imports and remove any imports to pure CSS chunks
      // as they are removed from the bundle
      if (!getInsertPreload(this.environment)) {
        const removedPureCssFiles = removedPureCssFilesCache.get(config)
        if (removedPureCssFiles && removedPureCssFiles.size > 0) {
          for (const file in bundle) {
            const chunk = bundle[file]
            if (chunk.type === 'chunk' && chunk.code.includes('import')) {
              const code = chunk.code
              let imports!: ImportSpecifier[]
              try {
                imports = parseImports(code)[0].filter((i) => i.d > -1)
              } catch (e: any) {
                const loc = numberToPos(code, e.idx)
                this.error({
                  name: e.name,
                  message: e.message,
                  stack: e.stack,
                  cause: e.cause,
                  pos: e.idx,
                  loc: { ...loc, file: chunk.fileName },
                  frame: generateCodeFrame(code, loc),
                })
              }

              for (const imp of imports) {
                const {
                  n: name,
                  s: start,
                  e: end,
                  ss: expStart,
                  se: expEnd,
                } = imp
                let url = name
                if (!url) {
                  const rawUrl = code.slice(start, end)
                  if (
                    (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                    (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                  )
                    url = rawUrl.slice(1, -1)
                }
                if (!url) continue

                const normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )
                if (removedPureCssFiles.has(normalizedFile)) {
                  // remove with Promise.resolve({}) while preserving source map location
                  chunk.code =
                    chunk.code.slice(0, expStart) +
                    `Promise.resolve({${''.padEnd(expEnd - expStart - 19, ' ')}})` +
                    chunk.code.slice(expEnd)
                }
              }
            }
          }
        }
        return
      }
      const buildSourcemap = this.environment.config.build.sourcemap
      const { modulePreload } = this.environment.config.build

      let importMapMapping: Record<string, string> | undefined
      let importMapReverseMapping: Record<string, string> | undefined
      if (this.environment.config.build.chunkImportMap) {
        const importMap = getImportMap(bundle, this.environment.config)!
        importMapMapping = importMap.mapping
        importMapReverseMapping = Object.fromEntries(
          Object.entries(importMapMapping).map(([k, v]) => [v, k]),
        )

        if (config.isOutputOptionsForLegacyChunks?.(opts)) {
          this.emitFile({
            type: 'asset',
            fileName: 'importmap.legacy.json',
            source: importMap.asset.source,
          })
          delete bundle[getImportMapFilename(this.environment.config)]
        }
      }

      for (const file in bundle) {
        const chunk = bundle[file]
        // can't use chunk.dynamicImports.length here since some modules e.g.
        // dynamic import to constant json may get inlined.
        if (chunk.type === 'chunk' && chunk.code.includes(preloadMarker)) {
          const code = chunk.code
          let imports!: ImportSpecifier[]
          try {
            imports = parseImports(code)[0].filter((i) => i.d > -1)
          } catch (e: any) {
            const loc = numberToPos(code, e.idx)
            this.error({
              name: e.name,
              message: e.message,
              stack: e.stack,
              cause: e.cause,
              pos: e.idx,
              loc: { ...loc, file: chunk.fileName },
              frame: generateCodeFrame(code, loc),
            })
          }

          const s = new MagicString(code)
          const rewroteMarkerStartPos = new Set() // position of the leading double quote

          const fileDeps: FileDep[] = []
          const addFileDep = (
            url: string,
            runtime: boolean = false,
          ): number => {
            const index = fileDeps.findIndex((dep) => dep.url === url)
            if (index === -1) {
              return fileDeps.push({ url, runtime }) - 1
            } else {
              return index
            }
          }

          if (imports.length) {
            const importMarkerPos = matchImportsToPreloadMarkers(code, imports)

            for (let index = 0; index < imports.length; index++) {
              // To handle escape sequences in specifier strings, the .n field will be provided where possible.
              const {
                n: name,
                s: start,
                e: end,
                ss: expStart,
                se: expEnd,
              } = imports[index]
              // check the chunk being imported
              let url = name
              if (!url) {
                const rawUrl = code.slice(start, end)
                if (
                  (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                  (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                )
                  url = rawUrl.slice(1, -1)
              }
              const deps = new Set<string>()
              let hasRemovedPureCssChunk = false

              let normalizedFile: string | undefined = undefined

              if (url) {
                normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )

                const ownerFilename = chunk.fileName
                // literal import - trace direct imports and add to deps
                const analyzed: Set<string> = new Set<string>()
                const addDeps = (rawFilename: string) => {
                  const filename =
                    importMapMapping?.[rawFilename] ?? rawFilename
                  if (filename === ownerFilename) return
                  if (analyzed.has(filename)) return
                  analyzed.add(filename)
                  const chunk = bundle[filename]
                  if (chunk) {
                    deps.add(chunk.fileName)
                    if (chunk.type === 'chunk') {
                      chunk.imports.forEach(addDeps)
                      // Ensure that the css imported by current chunk is loaded after the dependencies.
                      // So the style of current chunk won't be overwritten unexpectedly.
                      chunk.viteMetadata!.importedCss.forEach((file) => {
                        deps.add(file)
                      })
                    }
                  } else {
                    const removedPureCssFiles =
                      removedPureCssFilesCache.get(config)!
                    const chunk = removedPureCssFiles.get(filename)
                    if (chunk) {
                      if (chunk.viteMetadata!.importedCss.size) {
                        chunk.viteMetadata!.importedCss.forEach((file) => {
                          deps.add(file)
                        })
                        hasRemovedPureCssChunk = true
                      }

                      s.update(expStart, expEnd, 'Promise.resolve({})')
                    }
                  }
                }
                addDeps(normalizedFile)
              }

              const markerStartPos = importMarkerPos[index]

              if (markerStartPos > 0) {
                // the dep list includes the main chunk, so only need to reload when there are actual other deps.
                let depsArray =
                  deps.size > 1 ||
                  // main chunk is removed
                  (hasRemovedPureCssChunk && deps.size > 0)
                    ? modulePreload === false
                      ? // CSS deps use the same mechanism as module preloads, so even if disabled,
                        // we still need to pass these deps to the preload helper in dynamic imports.
                        [...deps].filter((d) => d.endsWith('.css'))
                      : [...deps]
                    : []

                const resolveDependencies = modulePreload
                  ? modulePreload.resolveDependencies
                  : undefined
                if (resolveDependencies && normalizedFile) {
                  // We can't let the user remove css deps as these aren't really preloads, they are just using
                  // the same mechanism as module preloads for this chunk
                  const cssDeps: string[] = []
                  const otherDeps: string[] = []
                  for (const dep of depsArray) {
                    ;(dep.endsWith('.css') ? cssDeps : otherDeps).push(dep)
                  }
                  depsArray = [
                    // NOTE: deps are URLs, not specifiers using the import map mapping
                    ...resolveDependencies(normalizedFile, otherDeps, {
                      hostId: file,
                      hostType: 'js',
                    }),
                    ...cssDeps,
                  ]
                }

                depsArray = depsArray.map(
                  (dep) => importMapReverseMapping?.[dep] ?? dep,
                )

                let renderedDeps: number[]
                if (renderBuiltUrl) {
                  renderedDeps = depsArray.map((dep) => {
                    const replacement = toOutputFilePathInJS(
                      this.environment,
                      dep,
                      'asset',
                      chunk.fileName,
                      'js',
                      toRelativePath,
                    )

                    if (typeof replacement === 'string') {
                      return addFileDep(replacement)
                    }

                    return addFileDep(replacement.runtime, true)
                  })
                } else {
                  renderedDeps = depsArray.map((d) =>
                    // Don't include the assets dir if the default asset file names
                    // are used, the path will be reconstructed by the import preload helper
                    isRelativeBase
                      ? addFileDep(toRelativePath(d, file))
                      : addFileDep(d),
                  )
                }

                s.update(
                  markerStartPos,
                  markerStartPos + preloadMarker.length,
                  renderedDeps.length > 0
                    ? `__vite__mapDeps([${renderedDeps.join(',')}])`
                    : `[]`,
                )
                rewroteMarkerStartPos.add(markerStartPos)
              }
            }
          }

          if (fileDeps.length > 0) {
            const fileDepsCode = `[${fileDeps
              .map((fileDep) =>
                fileDep.runtime ? fileDep.url : JSON.stringify(fileDep.url),
              )
              .join(',')}]`

            const mapDepsCode = `const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=${fileDepsCode})))=>i.map(i=>d[i]);\n`

            // inject extra code at the top or next line of hashbang
            if (code.startsWith('#!')) {
              s.prependLeft(getFileStartIndex(code), mapDepsCode)
            } else {
              s.prepend(mapDepsCode)
            }
          }

          // there may still be markers due to inlined dynamic imports, remove
          // all the markers regardless
          let markerStartPos = findPreloadMarker(code)
          while (markerStartPos >= 0) {
            if (!rewroteMarkerStartPos.has(markerStartPos)) {
              s.update(
                markerStartPos,
                markerStartPos + preloadMarker.length,
                'void 0',
              )
            }
            markerStartPos = findPreloadMarker(
              code,
              markerStartPos + preloadMarker.length,
            )
          }

          if (s.hasChanged()) {
            chunk.code = s.toString()
            if (buildSourcemap && chunk.map) {
              const nextMap = s.generateDecodedMap({
                source: chunk.fileName,
                hires: 'boundary',
              })
              const originalFile = chunk.map.file
              const map = combineSourcemaps(chunk.fileName, [
                nextMap as DecodedSourceMap,
                chunk.map as RawSourceMap,
              ]) as SourceMap
              map.toUrl = () => genSourceMapUrl(map)
              if (originalFile) {
                map.file = originalFile
              }

              const originalDebugId = chunk.map.debugId
              chunk.map = map

              if (buildSourcemap === 'inline') {
                chunk.code = chunk.code.replace(
                  convertSourceMap.mapFileCommentRegex,
                  '',
                )
                chunk.code += `\n//# sourceMappingURL=${genSourceMapUrl(map)}`
              } else {
                if (originalDebugId) {
                  map.debugId = originalDebugId
                }
                const mapAsset = bundle[chunk.fileName + '.map']
                if (mapAsset && mapAsset.type === 'asset') {
                  mapAsset.source = map.toString()
                }
              }
            }
          }
        }
      }
    },
  }

  return [
    plugin,
    perEnvironmentPlugin('native:import-analysis-build', (environment) => {
      const preloadCode = getPreloadCode(
        environment,
        !!renderBuiltUrl,
        isRelativeBase,
      )
      return nativeBuildImportAnalysisPlugin({
        preloadCode,
        insertPreload: getInsertPreload(environment),
        // this field looks redundant, put a dummy value for now
        optimizeModulePreloadRelativePaths: false,
        renderBuiltUrl: !!renderBuiltUrl,
        isRelativeBase,
      })
    }),
  ]
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function buildImportAnalysisPlugin(config: ResolvedConfig): Plugin[] {
  const getInsertPreload = (environment: PartialEnvironment) =>
    environment.config.consumer === 'client' &&
    !config.isWorker &&
    !config.build.lib

  const renderBuiltUrl = config.experimental.renderBuiltUrl
  const isRelativeBase = config.base === './' || config.base === ''

  const plugin: Plugin = {
    name: 'vite:build-import-analysis',

    renderChunk(code, _, { format }) {
      // make sure we only perform the preload logic in modern builds.
      if (code.includes(isModernFlag)) {
        const re = new RegExp(isModernFlag, 'g')
        const isModern = String(format === 'es')
        const isModernWithPadding =
          isModern + ' '.repeat(isModernFlag.length - isModern.length)
        return {
          code: code.replace(re, isModernWithPadding),
          map: null,
        }
      }
      return null
    },

    async generateBundle(opts, bundle) {
      const { format } = opts
      if (format !== 'es') {
        return
      }

      await init

      // If preload is not enabled, we parse through each imports and remove any imports to pure CSS chunks
      // as they are removed from the bundle
      if (!getInsertPreload(this.environment)) {
        const removedPureCssFiles = removedPureCssFilesCache.get(config)
        if (removedPureCssFiles && removedPureCssFiles.size > 0) {
          for (const file in bundle) {
            const chunk = bundle[file]
            if (chunk.type === 'chunk' && chunk.code.includes('import')) {
              const code = chunk.code
              let imports!: ImportSpecifier[]
              try {
                imports = parseImports(code)[0].filter((i) => i.d > -1)
              } catch (e: any) {
                const loc = numberToPos(code, e.idx)
                this.error({
                  name: e.name,
                  message: e.message,
                  stack: e.stack,
                  cause: e.cause,
                  pos: e.idx,
                  loc: { ...loc, file: chunk.fileName },
                  frame: generateCodeFrame(code, loc),
                })
              }

              for (const imp of imports) {
                const {
                  n: name,
                  s: start,
                  e: end,
                  ss: expStart,
                  se: expEnd,
                } = imp
                let url = name
                if (!url) {
                  const rawUrl = code.slice(start, end)
                  if (
                    (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                    (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                  )
                    url = rawUrl.slice(1, -1)
                }
                if (!url) continue

                const normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )
                if (removedPureCssFiles.has(normalizedFile)) {
                  // remove with Promise.resolve({}) while preserving source map location
                  chunk.code =
                    chunk.code.slice(0, expStart) +
                    `Promise.resolve({${''.padEnd(expEnd - expStart - 19, ' ')}})` +
                    chunk.code.slice(expEnd)
                }
              }
            }
          }
        }
        return
      }
      const buildSourcemap = this.environment.config.build.sourcemap
      const { modulePreload } = this.environment.config.build

      let importMapMapping: Record<string, string> | undefined
      let importMapReverseMapping: Record<string, string> | undefined
      const importMap = getImportMap(bundle, this.environment.config)
      if (importMap) {
        importMapMapping = importMap.mapping
        importMapReverseMapping = Object.fromEntries(
          Object.entries(importMapMapping).map(([k, v]) => [v, k]),
        )

        if (config.isOutputOptionsForLegacyChunks?.(opts)) {
          this.emitFile({
            type: 'asset',
            fileName: 'importmap.legacy.json',
            source: importMap.asset.source,
          })
          delete bundle[getImportMapFilename(this.environment.config)]
        }
      }

      for (const file in bundle) {
        const chunk = bundle[file]
        // can't use chunk.dynamicImports.length here since some modules e.g.
        // dynamic import to constant json may get inlined.
        if (chunk.type === 'chunk' && chunk.code.includes(preloadMarker)) {
          const code = chunk.code
          let imports!: ImportSpecifier[]
          try {
            imports = parseImports(code)[0].filter((i) => i.d > -1)
          } catch (e: any) {
            const loc = numberToPos(code, e.idx)
            this.error({
              name: e.name,
              message: e.message,
              stack: e.stack,
              cause: e.cause,
              pos: e.idx,
              loc: { ...loc, file: chunk.fileName },
              frame: generateCodeFrame(code, loc),
            })
          }

          const s = new MagicString(code)
          const rewroteMarkerStartPos = new Set() // position of the leading double quote

          const fileDeps: FileDep[] = []
          const addFileDep = (
            url: string,
            runtime: boolean = false,
          ): number => {
            const index = fileDeps.findIndex((dep) => dep.url === url)
            if (index === -1) {
              return fileDeps.push({ url, runtime }) - 1
            } else {
              return index
            }
          }

          if (imports.length) {
            const importMarkerPos = matchImportsToPreloadMarkers(code, imports)

            for (let index = 0; index < imports.length; index++) {
              // To handle escape sequences in specifier strings, the .n field will be provided where possible.
              const {
                n: name,
                s: start,
                e: end,
                ss: expStart,
                se: expEnd,
              } = imports[index]
              // check the chunk being imported
              let url = name
              if (!url) {
                const rawUrl = code.slice(start, end)
                if (
                  (rawUrl[0] === `"` && rawUrl.at(-1) === `"`) ||
                  (rawUrl[0] === '`' && rawUrl.at(-1) === '`')
                )
                  url = rawUrl.slice(1, -1)
              }
              const deps = new Set<string>()
              let hasRemovedPureCssChunk = false

              let normalizedFile: string | undefined = undefined

              if (url) {
                normalizedFile = path.posix.join(
                  path.posix.dirname(chunk.fileName),
                  url,
                )

                const ownerFilename = chunk.fileName
                // literal import - trace direct imports and add to deps
                const analyzed: Set<string> = new Set<string>()
                const addDeps = (rawFilename: string) => {
                  const filename =
                    importMapMapping?.[rawFilename] ?? rawFilename
                  if (filename === ownerFilename) return
                  if (analyzed.has(filename)) return
                  analyzed.add(filename)
                  const chunk = bundle[filename]
                  if (chunk) {
                    deps.add(chunk.fileName)
                    if (chunk.type === 'chunk') {
                      chunk.imports.forEach(addDeps)
                      // Ensure that the css imported by current chunk is loaded after the dependencies.
                      // So the style of current chunk won't be overwritten unexpectedly.
                      chunk.viteMetadata!.importedCss.forEach((file) => {
                        deps.add(file)
                      })
                    }
                  } else {
                    const removedPureCssFiles =
                      removedPureCssFilesCache.get(config)!
                    const chunk = removedPureCssFiles.get(filename)
                    if (chunk) {
                      if (chunk.viteMetadata!.importedCss.size) {
                        chunk.viteMetadata!.importedCss.forEach((file) => {
                          deps.add(file)
                        })
                        hasRemovedPureCssChunk = true
                      }

                      s.update(expStart, expEnd, 'Promise.resolve({})')
                    }
                  }
                }
                addDeps(normalizedFile)
              }

              const markerStartPos = importMarkerPos[index]

              if (markerStartPos > 0) {
                // the dep list includes the main chunk, so only need to reload when there are actual other deps.
                let depsArray =
                  deps.size > 1 ||
                  // main chunk is removed
                  (hasRemovedPureCssChunk && deps.size > 0)
                    ? modulePreload === false
                      ? // CSS deps use the same mechanism as module preloads, so even if disabled,
                        // we still need to pass these deps to the preload helper in dynamic imports.
                        [...deps].filter((d) => d.endsWith('.css'))
                      : [...deps]
                    : []

                const resolveDependencies = modulePreload
                  ? modulePreload.resolveDependencies
                  : undefined
                if (resolveDependencies && normalizedFile) {
                  // We can't let the user remove css deps as these aren't really preloads, they are just using
                  // the same mechanism as module preloads for this chunk
                  const cssDeps: string[] = []
                  const otherDeps: string[] = []
                  for (const dep of depsArray) {
                    ;(dep.endsWith('.css') ? cssDeps : otherDeps).push(dep)
                  }
                  depsArray = [
                    // NOTE: deps are URLs, not specifiers using the import map mapping
                    ...resolveDependencies(normalizedFile, otherDeps, {
                      hostId: file,
                      hostType: 'js',
                    }),
                    ...cssDeps,
                  ]
                }

                depsArray = depsArray.map(
                  (dep) => importMapReverseMapping?.[dep] ?? dep,
                )

                let renderedDeps: number[]
                if (renderBuiltUrl) {
                  renderedDeps = depsArray.map((dep) => {
                    const replacement = toOutputFilePathInJS(
                      this.environment,
                      dep,
                      'asset',
                      chunk.fileName,
                      'js',
                      toRelativePath,
                    )

                    if (typeof replacement === 'string') {
                      return addFileDep(replacement)
                    }

                    return addFileDep(replacement.runtime, true)
                  })
                } else {
                  renderedDeps = depsArray.map((d) =>
                    // Don't include the assets dir if the default asset file names
                    // are used, the path will be reconstructed by the import preload helper
                    isRelativeBase
                      ? addFileDep(toRelativePath(d, file))
                      : addFileDep(d),
                  )
                }

                s.update(
                  markerStartPos,
                  markerStartPos + preloadMarker.length,
                  renderedDeps.length > 0
                    ? `__vite__mapDeps([${renderedDeps.join(',')}])`
                    : `[]`,
                )
                rewroteMarkerStartPos.add(markerStartPos)
              }
            }
          }

          if (fileDeps.length > 0) {
            const fileDepsCode = `[${fileDeps
              .map((fileDep) =>
                fileDep.runtime ? fileDep.url : JSON.stringify(fileDep.url),
              )
              .join(',')}]`

            const mapDepsCode = `const __vite__mapDeps=(i,m=__vite__mapDeps,d=(m.f||(m.f=${fileDepsCode})))=>i.map(i=>d[i]);\n`

            // inject extra code at the top or next line of hashbang
            if (code.startsWith('#!')) {
              s.prependLeft(getFileStartIndex(code), mapDepsCode)
            } else {
              s.prepend(mapDepsCode)
            }
          }

          // there may still be markers due to inlined dynamic imports, remove
          // all the markers regardless
          let markerStartPos = findPreloadMarker(code)
          while (markerStartPos >= 0) {
            if (!rewroteMarkerStartPos.has(markerStartPos)) {
              s.update(
                markerStartPos,
                markerStartPos + preloadMarker.length,
                'void 0',
              )
            }
            markerStartPos = findPreloadMarker(
              code,
              markerStartPos + preloadMarker.length,
            )
          }

          if (s.hasChanged()) {
            chunk.code = s.toString()
            if (buildSourcemap && chunk.map) {
              const nextMap = s.generateDecodedMap({
                source: chunk.fileName,
                hires: 'boundary',
              })
              const originalFile = chunk.map.file
              const map = combineSourcemaps(chunk.fileName, [
                nextMap as DecodedSourceMap,
                chunk.map as RawSourceMap,
              ]) as SourceMap
              map.toUrl = () => genSourceMapUrl(map)
              if (originalFile) {
                map.file = originalFile
              }

              const originalDebugId = chunk.map.debugId
              chunk.map = map

              if (buildSourcemap === 'inline') {
                chunk.code = chunk.code.replace(
                  convertSourceMap.mapFileCommentRegex,
                  '',
                )
                chunk.code += `\n//# sourceMappingURL=${genSourceMapUrl(map)}`
              } else {
                if (originalDebugId) {
                  map.debugId = originalDebugId
                }
                const mapAsset = bundle[chunk.fileName + '.map']
                if (mapAsset && mapAsset.type === 'asset') {
                  mapAsset.source = map.toString()
                }
              }
            }
          }
        }
      }
    },
  }

  return [
    plugin,
    perEnvironmentPlugin('native:import-analysis-build', (environment) => {
      const preloadCode = getPreloadCode(
        environment,
        !!renderBuiltUrl,
        isRelativeBase,
      )
      return nativeBuildImportAnalysisPlugin({
        preloadCode,
        insertPreload: getInsertPreload(environment),
        // this field looks redundant, put a dummy value for now
        optimizeModulePreloadRelativePaths: false,
        renderBuiltUrl: !!renderBuiltUrl,
        isRelativeBase,
      })
    }),
  ]
}
```


---

### 🔹 Commit #05: `50b382d3`
- **完整 Hash**: `50b382d31835b8b4bc8b6964738ac03146e44261`
- **說明 (Ground Truth)**: fix(css): don't fail on a literal `%` in `url()` (#23676)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/plugins/css.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:248, E:213, A:1) ➔ After(N:248, E:213, A:1)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#injectCode** `(Control)`
    └── 🎯 [CALLS] `createCachedImport()`
        └── 🎯 [CALLS] `imp (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `decodeURIIfPossible (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `decodeURI (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `urlResolver` ──[CALLS]──> `decodeURIIfPossible (External/Unresolved)`
  • - [移除呼叫邊] `urlResolver` ──[CALLS]──> `decodeURI (External/Unresolved)`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'urlResolver' 被深鎖在內部閉包 (scope:handler@after/packages/vite/src/node/plugins/css.ts:L392C7)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `handler()`
- **變更前簽章 (Before)**: `handler(raw, id)` (L391~L472)
- **變更後簽章 (After)**: `handler(raw, id)` (L392~L475)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async handler(raw, id) {
        const { environment } = this
        const resolveUrl = (url: string, importer?: string) =>
          idResolver(environment, url, importer)

        const urlResolver: CssUrlResolver = async (url, importer) => {
          const decodedUrl = decodeURI(url)
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }

        const {
          code: css,
          modules,
          deps,
          map,
        } = await compileCSS(
          environment,
          id,
          raw,
          preprocessorWorkerController!,
          urlResolver,
        )
        if (modules) {
          moduleCache.set(id, modules)
        }

        if (deps) {
          for (const file of deps) {
            this.addWatchFile(file)
          }
        }

        return {
          code: css,
          map,
        }
      }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async handler(raw, id) {
        const { environment } = this
        const resolveUrl = (url: string, importer?: string) =>
          idResolver(environment, url, importer)

        const urlResolver: CssUrlResolver = async (url, importer) => {
          // a `%` that doesn't start an escape sequence (e.g. `url(100%.png)`)
          // is kept as is, like browsers do
          const decodedUrl = decodeURIIfPossible(url) ?? url
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }

        const {
          code: css,
          modules,
          deps,
          map,
        } = await compileCSS(
          environment,
          id,
          raw,
          preprocessorWorkerController!,
          urlResolver,
        )
        if (modules) {
          moduleCache.set(id, modules)
        }

        if (deps) {
          for (const file of deps) {
            this.addWatchFile(file)
          }
        }

        return {
          code: css,
          map,
        }
      }
```

### 🔹 函式: `urlResolver()`
- **變更前簽章 (Before)**: `urlResolver(url, importer)` (L396~L444)
- **變更後簽章 (After)**: `urlResolver(url, importer)` (L397~L447)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async (url, importer) => {
          const decodedUrl = decodeURI(url)
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async (url, importer) => {
          // a `%` that doesn't start an escape sequence (e.g. `url(100%.png)`)
          // is kept as is, like browsers do
          const decodedUrl = decodeURIIfPossible(url) ?? url
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }
```

### 🔹 函式: `cssPlugin()`
- **變更前簽章 (Before)**: `function cssPlugin(config: ResolvedConfig): Plugin` (L314~L475)
- **變更後簽章 (After)**: `function cssPlugin(config: ResolvedConfig): Plugin` (L315~L478)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function cssPlugin(config: ResolvedConfig): Plugin {
  const isBuild = config.command === 'build'
  let moduleCache: Map<string, Record<string, string>>

  const idResolver = createBackCompatIdResolver(config, {
    preferRelative: true,
    tryIndex: false,
    extensions: [],
  })

  let preprocessorWorkerController: PreprocessorWorkerController | undefined

  // warm up cache for resolved postcss config
  if (config.css.transformer !== 'lightningcss') {
    resolvePostcssConfig(config).catch(() => {
      /* will be handled later */
    })
  }

  return {
    name: 'vite:css',

    buildStart() {
      // Ensure a new cache for every build (i.e. rebuilding in watch mode)
      moduleCache = new Map<string, Record<string, string>>()
      cssModulesCache.set(config, moduleCache)

      removedPureCssFilesCache.set(config, new Map<string, RenderedChunk>())

      preprocessorWorkerController = createPreprocessorWorkerController(
        normalizeMaxWorkers(config.css.preprocessorMaxWorkers),
      )
      preprocessorWorkerControllerCache.set(
        config,
        preprocessorWorkerController,
      )
    },

    async buildEnd() {
      await preprocessorWorkerController?.close()
    },

    load: {
      filter: {
        id: CSS_LANGS_RE,
      },
      handler(id) {
        if (urlRE.test(id)) {
          if (isModuleCSSRequest(id)) {
            throw new Error(
              `?url is not supported with CSS modules. (tried to import ${JSON.stringify(
                id,
              )})`,
            )
          }

          // *.css?url
          // in dev, it's handled by assets plugin.
          if (isBuild) {
            id = injectQuery(removeUrlQuery(id), 'transform-only')
            return (
              `import ${JSON.stringify(id)};` +
              `export default "__VITE_CSS_URL__${Buffer.from(id).toString(
                'hex',
              )}__"`
            )
          }
        }
      },
    },
    transform: {
      filter: {
        id: {
          include: CSS_LANGS_RE,
          exclude: [commonjsProxyRE, SPECIAL_QUERY_RE],
        },
      },
      async handler(raw, id) {
        const { environment } = this
        const resolveUrl = (url: string, importer?: string) =>
          idResolver(environment, url, importer)

        const urlResolver: CssUrlResolver = async (url, importer) => {
          const decodedUrl = decodeURI(url)
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }

        const {
          code: css,
          modules,
          deps,
          map,
        } = await compileCSS(
          environment,
          id,
          raw,
          preprocessorWorkerController!,
          urlResolver,
        )
        if (modules) {
          moduleCache.set(id, modules)
        }

        if (deps) {
          for (const file of deps) {
            this.addWatchFile(file)
          }
        }

        return {
          code: css,
          map,
        }
      },
    },
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function cssPlugin(config: ResolvedConfig): Plugin {
  const isBuild = config.command === 'build'
  let moduleCache: Map<string, Record<string, string>>

  const idResolver = createBackCompatIdResolver(config, {
    preferRelative: true,
    tryIndex: false,
    extensions: [],
  })

  let preprocessorWorkerController: PreprocessorWorkerController | undefined

  // warm up cache for resolved postcss config
  if (config.css.transformer !== 'lightningcss') {
    resolvePostcssConfig(config).catch(() => {
      /* will be handled later */
    })
  }

  return {
    name: 'vite:css',

    buildStart() {
      // Ensure a new cache for every build (i.e. rebuilding in watch mode)
      moduleCache = new Map<string, Record<string, string>>()
      cssModulesCache.set(config, moduleCache)

      removedPureCssFilesCache.set(config, new Map<string, RenderedChunk>())

      preprocessorWorkerController = createPreprocessorWorkerController(
        normalizeMaxWorkers(config.css.preprocessorMaxWorkers),
      )
      preprocessorWorkerControllerCache.set(
        config,
        preprocessorWorkerController,
      )
    },

    async buildEnd() {
      await preprocessorWorkerController?.close()
    },

    load: {
      filter: {
        id: CSS_LANGS_RE,
      },
      handler(id) {
        if (urlRE.test(id)) {
          if (isModuleCSSRequest(id)) {
            throw new Error(
              `?url is not supported with CSS modules. (tried to import ${JSON.stringify(
                id,
              )})`,
            )
          }

          // *.css?url
          // in dev, it's handled by assets plugin.
          if (isBuild) {
            id = injectQuery(removeUrlQuery(id), 'transform-only')
            return (
              `import ${JSON.stringify(id)};` +
              `export default "__VITE_CSS_URL__${Buffer.from(id).toString(
                'hex',
              )}__"`
            )
          }
        }
      },
    },
    transform: {
      filter: {
        id: {
          include: CSS_LANGS_RE,
          exclude: [commonjsProxyRE, SPECIAL_QUERY_RE],
        },
      },
      async handler(raw, id) {
        const { environment } = this
        const resolveUrl = (url: string, importer?: string) =>
          idResolver(environment, url, importer)

        const urlResolver: CssUrlResolver = async (url, importer) => {
          // a `%` that doesn't start an escape sequence (e.g. `url(100%.png)`)
          // is kept as is, like browsers do
          const decodedUrl = decodeURIIfPossible(url) ?? url
          if (checkPublicFile(decodedUrl, config)) {
            if (encodePublicUrlsInCSS(config)) {
              return [publicFileToBuiltUrl(decodedUrl, config), undefined]
            } else {
              const base = joinUrlSegments(
                config.server.origin ?? '',
                config.base,
              )
              return [joinUrlSegments(base, decodedUrl), undefined]
            }
          }
          const [id, fragment] = decodedUrl.split('#')
          let resolved = await resolveUrl(id, importer)
          if (resolved) {
            if (fragment) resolved += '#' + fragment
            let url = await fileToUrl(this, resolved, 'string')
            // Inherit HMR timestamp if this asset was invalidated
            if (!url.startsWith('data:') && this.environment.mode === 'dev') {
              const mod = [
                ...(this.environment.moduleGraph.getModulesByFile(resolved) ??
                  []),
              ].find((mod) => mod.type === 'asset')
              if (mod?.lastHMRTimestamp) {
                url = injectQuery(url, `t=${mod.lastHMRTimestamp}`)
              }
            }
            return [url, cleanUrl(resolved)]
          }
          if (config.command === 'build') {
            const isExternal = config.build.rolldownOptions.external
              ? resolveUserExternal(
                  config.build.rolldownOptions.external,
                  decodedUrl, // use URL as id since id could not be resolved
                  id,
                  false,
                )
              : false

            if (!isExternal) {
              // #9800 If we cannot resolve the css url, leave a warning.
              config.logger.warnOnce(
                `\n${decodedUrl} referenced in ${id} didn't resolve at build time, it will remain unchanged to be resolved at runtime`,
              )
            }
          }
          return [url, undefined]
        }

        const {
          code: css,
          modules,
          deps,
          map,
        } = await compileCSS(
          environment,
          id,
          raw,
          preprocessorWorkerController!,
          urlResolver,
        )
        if (modules) {
          moduleCache.set(id, modules)
        }

        if (deps) {
          for (const file of deps) {
            this.addWatchFile(file)
          }
        }

        return {
          code: css,
          map,
        }
      },
    },
  }
}
```


---

### 🔹 Commit #06: `a7d56967`
- **完整 Hash**: `a7d56967ef0050a09c0507e63a18164bc7a0d486`
- **說明 (Ground Truth)**: fix(optimizer): skip patches dir hash for nub lockfile (#23761)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/optimizer/index.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:93, E:106, A:0) ➔ After(N:93, E:106, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'cleanUp' 被深鎖在內部閉包 (scope:runOptimizeDeps@after/packages/vite/src/node/optimizer/index.ts:L523C8)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `lockfileFormats()`
- **變更前簽章 (Before)**: `[Module State] lockfileFormats` (L1234~L1301)
- **變更後簽章 (After)**: `[Module State] lockfileFormats` (L1234~L1302)

#### ◀️ 變更前實作碼 (Before Implementation):
```
lockfileFormats = [
  {
    path: 'node_modules/.pnpm/lock.yaml',
    // Included in lockfile
    checkPatchesDir: false,
    manager: 'pnpm',
  },
  {
    path: 'node_modules/.package-lock.json',
    checkPatchesDir: 'patches',
    manager: 'npm',
  },
  {
    // Yarn non-PnP
    path: 'node_modules/.yarn-state.yml',
    checkPatchesDir: false,
    manager: 'yarn',
  },
  {
    path: 'bun.lock',
    checkPatchesDir: 'patches',
    manager: 'bun',
  },
  {
    path: '.rush/temp/shrinkwrap-deps.json',
    // Included in lockfile
    checkPatchesDir: false,
    manager: 'pnpm',
  },
  {
    path: 'aube-lock.yaml',
    checkPatchesDir: false,
    manager: 'aube',
  },
  {
    path: 'nub.lock',
    checkPatchesDir: 'patches',
    manager: 'nub',
  },

  // discouraged package manager lockfiles
  // or deprecated lockfiles
  {
    // Yarn v3+ PnP
    path: '.pnp.cjs',
    checkPatchesDir: '.yarn/patches',
    manager: 'yarn',
  },
  {
    // Yarn v2 PnP
    path: '.pnp.js',
    checkPatchesDir: '.yarn/patches',
    manager: 'yarn',
  },
  {
    // yarn 1
    path: 'node_modules/.yarn-integrity',
    checkPatchesDir: 'patches',
    manager: 'yarn',
  },
  {
    path: 'bun.lockb',
    checkPatchesDir: 'patches',
    manager: 'bun',
  },
].sort((_, { manager }) => {
  return process.env.npm_config_user_agent?.startsWith(manager) ? 1 : -1
})
```

#### ▶️ 變更後實作碼 (After Implementation):
```
lockfileFormats = [
  {
    path: 'node_modules/.pnpm/lock.yaml',
    // Included in lockfile
    checkPatchesDir: false,
    manager: 'pnpm',
  },
  {
    path: 'node_modules/.package-lock.json',
    checkPatchesDir: 'patches',
    manager: 'npm',
  },
  {
    // Yarn non-PnP
    path: 'node_modules/.yarn-state.yml',
    checkPatchesDir: false,
    manager: 'yarn',
  },
  {
    path: 'bun.lock',
    checkPatchesDir: 'patches',
    manager: 'bun',
  },
  {
    path: '.rush/temp/shrinkwrap-deps.json',
    // Included in lockfile
    checkPatchesDir: false,
    manager: 'pnpm',
  },
  {
    path: 'aube-lock.yaml',
    checkPatchesDir: false,
    manager: 'aube',
  },
  {
    path: 'nub.lock',
    // Included in lockfile (`patchedDependencies` has patch hashes)
    checkPatchesDir: false,
    manager: 'nub',
  },

  // discouraged package manager lockfiles
  // or deprecated lockfiles
  {
    // Yarn v3+ PnP
    path: '.pnp.cjs',
    checkPatchesDir: '.yarn/patches',
    manager: 'yarn',
  },
  {
    // Yarn v2 PnP
    path: '.pnp.js',
    checkPatchesDir: '.yarn/patches',
    manager: 'yarn',
  },
  {
    // yarn 1
    path: 'node_modules/.yarn-integrity',
    checkPatchesDir: 'patches',
    manager: 'yarn',
  },
  {
    path: 'bun.lockb',
    checkPatchesDir: 'patches',
    manager: 'bun',
  },
].sort((_, { manager }) => {
  return process.env.npm_config_user_agent?.startsWith(manager) ? 1 : -1
})
```


---

### 🔹 Commit #07: `11fe1e46`
- **完整 Hash**: `11fe1e46ff0c136cb90fbe263ba03993bc94df18`
- **說明 (Ground Truth)**: fix(bundled-dev): map forwarded error stacks through the bundle source maps (#23741)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/plugins/forwardConsole.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:6, A:0) ➔ After(N:15, E:12, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 6, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `readFile` (FUNCTION_DEF)
  • + [新增節點] `getBundledDevSourceMap` (FUNCTION_DEF)
  • + [新增節點] `getBundledDevChunkPath` (FUNCTION_DEF)
  • + [新增節點] `getBundledDevOutDir` (FUNCTION_DEF)
  • + [新增節點] `cleanUrl (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `configureServer` ──[CALLS [guarded]]──> `getBundledDevOutDir`
  • + [新增呼叫邊] `getUrlId` ──[CALLS [guard: (memoryFiles)]]──> `getBundledDevChunkPath`
  • + [新增呼叫邊] `getSourceMap` ──[CALLS [guard: (memoryFiles)]]──> `getBundledDevSourceMap`
  • + [新增呼叫邊] `getBundledDevOutDir` ──[CALLS]──> `normalizePath (External/Unresolved)`
  • + [新增呼叫邊] `getBundledDevChunkPath` ──[CALLS]──> `cleanUrl (External/Unresolved)`
  • + [新增呼叫邊] `getBundledDevSourceMap` ──[CALLS]──> `readFile`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `forwardConsolePlugin()`
- **變更前簽章 (Before)**: `function forwardConsolePlugin(pluginOpts:` (L11~L52)
- **變更後簽章 (After)**: `function forwardConsolePlugin(pluginOpts:` (L14~L61)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function forwardConsolePlugin(pluginOpts: {
  environments: string[]
}): Plugin {
  const sourceMapCache = new Map<string, any>()

  return {
    name: 'vite:forward-console',
    apply: 'serve',
    configureServer(server) {
      for (const name of pluginOpts.environments) {
        const environment = server.environments[name]
        environment.hot.on('vite:forward-console', (payload) => {
          if (
            payload.type === 'error' ||
            payload.type === 'unhandled-rejection'
          ) {
            const output = formatError(payload, environment, sourceMapCache)
            environment.config.logger.error(output, {
              timestamp: true,
            })
          } else {
            const output =
              c.dim(`[console.${payload.data.level}] `) + payload.data.message
            if (payload.data.level === 'error') {
              environment.config.logger.error(output, {
                timestamp: true,
              })
            } else if (payload.data.level === 'warn') {
              environment.config.logger.warn(output, {
                timestamp: true,
              })
            } else {
              environment.config.logger.info(output, {
                timestamp: true,
              })
            }
          }
        })
      }
    },
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function forwardConsolePlugin(pluginOpts: {
  environments: string[]
}): Plugin {
  const sourceMapCache = new Map<string, any>()

  return {
    name: 'vite:forward-console',
    apply: 'serve',
    configureServer(server) {
      for (const name of pluginOpts.environments) {
        const environment = server.environments[name]
        const bundledDevOutDir = getBundledDevOutDir(environment)
        environment.hot.on('vite:forward-console', (payload) => {
          if (
            payload.type === 'error' ||
            payload.type === 'unhandled-rejection'
          ) {
            const output = formatError(
              payload,
              environment,
              sourceMapCache,
              bundledDevOutDir,
            )
            environment.config.logger.error(output, {
              timestamp: true,
            })
          } else {
            const output =
              c.dim(`[console.${payload.data.level}] `) + payload.data.message
            if (payload.data.level === 'error') {
              environment.config.logger.error(output, {
                timestamp: true,
              })
            } else if (payload.data.level === 'warn') {
              environment.config.logger.warn(output, {
                timestamp: true,
              })
            } else {
              environment.config.logger.info(output, {
                timestamp: true,
              })
            }
          }
        })
      }
    },
  }
}
```

### 🔹 函式: `configureServer()`
- **變更前簽章 (Before)**: `configureServer(server)` (L19~L50)
- **變更後簽章 (After)**: `configureServer(server)` (L22~L59)

#### ◀️ 變更前實作碼 (Before Implementation):
```
configureServer(server) {
      for (const name of pluginOpts.environments) {
        const environment = server.environments[name]
        environment.hot.on('vite:forward-console', (payload) => {
          if (
            payload.type === 'error' ||
            payload.type === 'unhandled-rejection'
          ) {
            const output = formatError(payload, environment, sourceMapCache)
            environment.config.logger.error(output, {
              timestamp: true,
            })
          } else {
            const output =
              c.dim(`[console.${payload.data.level}] `) + payload.data.message
            if (payload.data.level === 'error') {
              environment.config.logger.error(output, {
                timestamp: true,
              })
            } else if (payload.data.level === 'warn') {
              environment.config.logger.warn(output, {
                timestamp: true,
              })
            } else {
              environment.config.logger.info(output, {
                timestamp: true,
              })
            }
          }
        })
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
configureServer(server) {
      for (const name of pluginOpts.environments) {
        const environment = server.environments[name]
        const bundledDevOutDir = getBundledDevOutDir(environment)
        environment.hot.on('vite:forward-console', (payload) => {
          if (
            payload.type === 'error' ||
            payload.type === 'unhandled-rejection'
          ) {
            const output = formatError(
              payload,
              environment,
              sourceMapCache,
              bundledDevOutDir,
            )
            environment.config.logger.error(output, {
              timestamp: true,
            })
          } else {
            const output =
              c.dim(`[console.${payload.data.level}] `) + payload.data.message
            if (payload.data.level === 'error') {
              environment.config.logger.error(output, {
                timestamp: true,
              })
            } else if (payload.data.level === 'warn') {
              environment.config.logger.warn(output, {
                timestamp: true,
              })
            } else {
              environment.config.logger.info(output, {
                timestamp: true,
              })
            }
          }
        })
      }
    }
```

### 🔹 函式: `formatError()`
- **變更前簽章 (Before)**: `function formatError(
  payload: Extract<
    ForwardConsolePayload,` (L54~L144)
- **變更後簽章 (After)**: `function formatError(
  payload: Extract<
    ForwardConsolePayload,` (L63~L176)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function formatError(
  payload: Extract<
    ForwardConsolePayload,
    { type: 'error' | 'unhandled-rejection' }
  >,
  environment: DevEnvironment,
  sourceMapCache: Map<string, any>,
) {
  const error = payload.data
  const stacks = parseErrorStacktrace(error, {
    getUrlId(id) {
      const moduleGraph = environment.moduleGraph
      const mod = moduleGraph.getModuleById(id)
      if (mod) {
        return id
      }
      const resolvedPath = normalizePath(
        path.resolve(environment.config.root, id.slice(1)),
      )
      const modUrl = moduleGraph.getModuleById(resolvedPath)
      if (modUrl) {
        return resolvedPath
      }
      // some browsers (looking at you, safari) don't report queries in stack traces
      // the next best thing is to try the first id that this file resolves to
      const files = moduleGraph.getModulesByFile(resolvedPath)
      if (files && files.size) {
        return files.values().next().value!.id!
      }
      return id
    },
    getSourceMap(id) {
      if (sourceMapCache.has(id)) {
        return sourceMapCache.get(id)
      }

      const result = environment.moduleGraph.getModuleById(id)?.transformResult
      // handle non-inline source map such as pre-bundled deps in node_modules/.vite
      if (result && !result.map) {
        try {
          const filePath = id.split('?')[0]
          const extracted = extractSourcemapFromFile(
            result.code,
            filePath,
            environment.config.logger,
          )
          sourceMapCache.set(id, extracted?.map)
          return extracted?.map
        } catch {
          sourceMapCache.set(id, null)
          return null
        }
      }

      sourceMapCache.set(id, result?.map)
      return result?.map
    },
    // override it to empty since vitest uses this option to skip internal files by default.
    // https://github.com/vitest-dev/vitest/blob/4783137cd8d766cf998bdf2d638890eaa51e08d9/packages/utils/src/source-map.ts#L17
    ignoreStackEntries: [],
  })

  const nearest = stacks.find((stack) => {
    const modules = environment.moduleGraph.getModulesByFile(stack.file)
    return (
      [...(modules || [])].some((m) => m.transformResult) &&
      fs.existsSync(stack.file)
    )
  })

  let output = ''
  const title =
    payload.type === 'unhandled-rejection'
      ? '[Unhandled rejection]'
      : '[Unhandled error]'
  output += c.red(`${title} ${c.bold(error.name)}: ${error.message}\n`)
  for (const stack of stacks) {
    const file = normalizePath(
      path.relative(environment.config.root, stack.file),
    )
    output += ` > ${[stack.method, `${file}:${stack.line}:${stack.column}`]
      .filter(Boolean)
      .join(' ')}\n`
    if (stack === nearest) {
      const code = fs.readFileSync(stack.file, 'utf-8')
      output += generateCodeFrame(code, stack).replace(/^/gm, '    ')
      output += '\n'
    }
  }
  return output
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function formatError(
  payload: Extract<
    ForwardConsolePayload,
    { type: 'error' | 'unhandled-rejection' }
  >,
  environment: DevEnvironment,
  sourceMapCache: Map<string, any>,
  bundledDevOutDir: string,
) {
  const error = payload.data
  const memoryFiles = environment.bundledDev?.memoryFiles
  const stacks = parseErrorStacktrace(error, {
    getUrlId(id) {
      if (memoryFiles) {
        return (
          getBundledDevChunkPath(
            environment,
            memoryFiles,
            bundledDevOutDir,
            id,
          ) ?? id
        )
      }
      const moduleGraph = environment.moduleGraph
      const mod = moduleGraph.getModuleById(id)
      if (mod) {
        return id
      }
      const resolvedPath = normalizePath(
        path.resolve(environment.config.root, id.slice(1)),
      )
      const modUrl = moduleGraph.getModuleById(resolvedPath)
      if (modUrl) {
        return resolvedPath
      }
      // some browsers (looking at you, safari) don't report queries in stack traces
      // the next best thing is to try the first id that this file resolves to
      const files = moduleGraph.getModulesByFile(resolvedPath)
      if (files && files.size) {
        return files.values().next().value!.id!
      }
      return id
    },
    getSourceMap(id) {
      if (memoryFiles) {
        return getBundledDevSourceMap(memoryFiles, bundledDevOutDir, id)
      }
      if (sourceMapCache.has(id)) {
        return sourceMapCache.get(id)
      }

      const result = environment.moduleGraph.getModuleById(id)?.transformResult
      // handle non-inline source map such as pre-bundled deps in node_modules/.vite
      if (result && !result.map) {
        try {
          const filePath = id.split('?')[0]
          const extracted = extractSourcemapFromFile(
            result.code,
            filePath,
            environment.config.logger,
          )
          sourceMapCache.set(id, extracted?.map)
          return extracted?.map
        } catch {
          sourceMapCache.set(id, null)
          return null
        }
      }

      sourceMapCache.set(id, result?.map)
      return result?.map
    },
    // override it to empty since vitest uses this option to skip internal files by default.
    // https://github.com/vitest-dev/vitest/blob/4783137cd8d766cf998bdf2d638890eaa51e08d9/packages/utils/src/source-map.ts#L17
    ignoreStackEntries: [],
  })

  const nearest = stacks.find((stack) => {
    if (memoryFiles) {
      return (
        !environment.config.dev.sourcemapIgnoreList(
          stack.file,
          `${stack.file}.map`,
        ) && fs.existsSync(stack.file)
      )
    }
    const modules = environment.moduleGraph.getModulesByFile(stack.file)
    return (
      [...(modules || [])].some((m) => m.transformResult) &&
      fs.existsSync(stack.file)
    )
  })

  let output = ''
  const title =
    payload.type === 'unhandled-rejection'
      ? '[Unhandled rejection]'
      : '[Unhandled error]'
  output += c.red(`${title} ${c.bold(error.name)}: ${error.message}\n`)
  for (const stack of stacks) {
    const file = normalizePath(
      path.relative(environment.config.root, stack.file),
    )
    output += ` > ${[stack.method, `${file}:${stack.line}:${stack.column}`]
      .filter(Boolean)
      .join(' ')}\n`
    if (stack === nearest) {
      const code = fs.readFileSync(stack.file, 'utf-8')
      output += generateCodeFrame(code, stack).replace(/^/gm, '    ')
      output += '\n'
    }
  }
  return output
}
```

### 🔹 函式: `getSourceMap()`
- **變更前簽章 (Before)**: `getSourceMap(id)` (L85~L110)
- **變更後簽章 (After)**: `getSourceMap(id)` (L106~L134)

#### ◀️ 變更前實作碼 (Before Implementation):
```
getSourceMap(id) {
      if (sourceMapCache.has(id)) {
        return sourceMapCache.get(id)
      }

      const result = environment.moduleGraph.getModuleById(id)?.transformResult
      // handle non-inline source map such as pre-bundled deps in node_modules/.vite
      if (result && !result.map) {
        try {
          const filePath = id.split('?')[0]
          const extracted = extractSourcemapFromFile(
            result.code,
            filePath,
            environment.config.logger,
          )
          sourceMapCache.set(id, extracted?.map)
          return extracted?.map
        } catch {
          sourceMapCache.set(id, null)
          return null
        }
      }

      sourceMapCache.set(id, result?.map)
      return result?.map
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
getSourceMap(id) {
      if (memoryFiles) {
        return getBundledDevSourceMap(memoryFiles, bundledDevOutDir, id)
      }
      if (sourceMapCache.has(id)) {
        return sourceMapCache.get(id)
      }

      const result = environment.moduleGraph.getModuleById(id)?.transformResult
      // handle non-inline source map such as pre-bundled deps in node_modules/.vite
      if (result && !result.map) {
        try {
          const filePath = id.split('?')[0]
          const extracted = extractSourcemapFromFile(
            result.code,
            filePath,
            environment.config.logger,
          )
          sourceMapCache.set(id, extracted?.map)
          return extracted?.map
        } catch {
          sourceMapCache.set(id, null)
          return null
        }
      }

      sourceMapCache.set(id, result?.map)
      return result?.map
    }
```

### 🔹 函式: `nearest()`
- **變更前簽章 (Before)**: `nearest(stack)` (L116~L122)
- **變更後簽章 (After)**: `nearest(stack)` (L140~L154)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(stack) => {
    const modules = environment.moduleGraph.getModulesByFile(stack.file)
    return (
      [...(modules || [])].some((m) => m.transformResult) &&
      fs.existsSync(stack.file)
    )
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(stack) => {
    if (memoryFiles) {
      return (
        !environment.config.dev.sourcemapIgnoreList(
          stack.file,
          `${stack.file}.map`,
        ) && fs.existsSync(stack.file)
      )
    }
    const modules = environment.moduleGraph.getModulesByFile(stack.file)
    return (
      [...(modules || [])].some((m) => m.transformResult) &&
      fs.existsSync(stack.file)
    )
  }
```

### 🔹 函式: `getUrlId()`
- **變更前簽章 (Before)**: `getUrlId(id)` (L64~L84)
- **變更後簽章 (After)**: `getUrlId(id)` (L75~L105)

#### ◀️ 變更前實作碼 (Before Implementation):
```
getUrlId(id) {
      const moduleGraph = environment.moduleGraph
      const mod = moduleGraph.getModuleById(id)
      if (mod) {
        return id
      }
      const resolvedPath = normalizePath(
        path.resolve(environment.config.root, id.slice(1)),
      )
      const modUrl = moduleGraph.getModuleById(resolvedPath)
      if (modUrl) {
        return resolvedPath
      }
      // some browsers (looking at you, safari) don't report queries in stack traces
      // the next best thing is to try the first id that this file resolves to
      const files = moduleGraph.getModulesByFile(resolvedPath)
      if (files && files.size) {
        return files.values().next().value!.id!
      }
      return id
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
getUrlId(id) {
      if (memoryFiles) {
        return (
          getBundledDevChunkPath(
            environment,
            memoryFiles,
            bundledDevOutDir,
            id,
          ) ?? id
        )
      }
      const moduleGraph = environment.moduleGraph
      const mod = moduleGraph.getModuleById(id)
      if (mod) {
        return id
      }
      const resolvedPath = normalizePath(
        path.resolve(environment.config.root, id.slice(1)),
      )
      const modUrl = moduleGraph.getModuleById(resolvedPath)
      if (modUrl) {
        return resolvedPath
      }
      // some browsers (looking at you, safari) don't report queries in stack traces
      // the next best thing is to try the first id that this file resolves to
      const files = moduleGraph.getModulesByFile(resolvedPath)
      if (files && files.size) {
        return files.values().next().value!.id!
      }
      return id
    }
```


---

### 🔹 Commit #08: `c2c9ef4d`
- **完整 Hash**: `c2c9ef4dcd05b3e4d88844ea3a13dc23819ca2a5`
- **說明 (Ground Truth)**: fix(server): handle socket errors on upgrade requests not taken by the HMR server (#23728)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/server/ws.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:33, E:14, A:0) ➔ After(N:33, E:14, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'handleUpgrade' 被深鎖在內部閉包 (scope:createWebSocketServer@after/packages/vite/src/node/server/ws.ts:L118C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createWebSocketServer()`
- **變更前簽章 (Before)**: `function createWebSocketServer(
  server: HttpServer | null,
  config: ResolvedConfig,
  httpsOptions?: HttpsServerOptions,
): WebSocketServer` (L118~L467)
- **變更後簽章 (After)**: `function createWebSocketServer(
  server: HttpServer | null,
  config: ResolvedConfig,
  httpsOptions?: HttpsServerOptions,
): WebSocketServer` (L118~L473)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function createWebSocketServer(
  server: HttpServer | null,
  config: ResolvedConfig,
  httpsOptions?: HttpsServerOptions,
): WebSocketServer {
  if (config.server.ws === false) {
    return {
      [isWebSocketServer]: true,
      get clients() {
        return new Set<WebSocketClient>()
      },
      async close() {
        // noop
      },
      on: noop as any as WebSocketServer['on'],
      off: noop as any as WebSocketServer['off'],
      setInvokeHandler: noop,
      handleInvoke: async () => ({
        error: {
          name: 'TransportError',
          message: 'handleInvoke not implemented',
          stack: new Error().stack,
        },
      }),
      listen: noop,
      send: noop,
    }
  }

  let wsHttpServer: Server | undefined = undefined

  const wsOptions = isObject(config.server.ws) ? config.server.ws : undefined
  const wsCustomServer = wsOptions?.server
  const wsPort = wsOptions?.port
  // TODO: the main server port may not have been chosen yet as it may use the next available
  const portsAreCompatible = !wsPort || wsPort === config.server.port
  const wsServer = wsCustomServer || (portsAreCompatible && server)
  let hmrServerWsListener: (
    req: InstanceType<typeof IncomingMessage>,
    socket: Duplex,
    head: Buffer,
  ) => void
  const customListeners = new Map<string, Set<WebSocketCustomListener<any>>>()
  const clientsMap = new WeakMap<WebSocketRaw, WebSocketClient>()
  const port = wsPort || 24678
  const host = wsOptions?.host || undefined
  const allowedHosts =
    config.server.allowedHosts === true
      ? config.server.allowedHosts
      : Object.freeze([...config.server.allowedHosts]) // Freeze the array to allow caching

  const shouldHandle = (req: IncomingMessage) => {
    const protocol = req.headers['sec-websocket-protocol']!
    // vite-ping is allowed to connect from anywhere
    // because it needs to be connected before the client fetches the new `/@vite/client`
    // this is fine because vite-ping does not receive / send any meaningful data
    if (protocol === 'vite-ping') return true

    if (
      allowedHosts !== true &&
      !isHostAllowed(req.headers.host, allowedHosts)
    ) {
      return false
    }

    if (config.legacy?.skipWebSocketTokenCheck) {
      return true
    }

    // If the Origin header is set, this request might be coming from a browser.
    // Browsers always sets the Origin header for WebSocket connections.
    if (req.headers.origin) {
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      return hasValidToken(config, parsedUrl)
    }

    // We allow non-browser requests to connect without a token
    // for backward compat and convenience
    // This is fine because if you can sent a request without the SOP limitation,
    // you can also send a normal HTTP request to the server.
    return true
  }
  const handleUpgrade = (
    req: IncomingMessage,
    socket: Duplex,
    head: Buffer,
    isPing: boolean,
  ) => {
    wss.handleUpgrade(req, socket as Socket, head, (ws) => {
      // vite-ping is allowed to connect from anywhere
      // we close the connection immediately without connection event
      // so that the client does not get included in `wss.clients`
      if (isPing) {
        ws.close(/* Normal Closure */ 1000)
        return
      }
      wss.emit('connection', ws, req)
    })
  }
  const wss: WebSocketServerRaw_ = new WebSocketServerRaw({ noServer: true })
  wss.shouldHandle = shouldHandle

  if (wsServer) {
    let hmrBase = config.base
    const wsPath = wsOptions?.path
    if (wsPath) {
      hmrBase = path.posix.join(hmrBase, wsPath)
    }
    hmrServerWsListener = (req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      if (
        [HMR_HEADER, 'vite-ping'].includes(protocol) &&
        parsedUrl.pathname === hmrBase
      ) {
        handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
      }
    }
    wsServer.on('upgrade', hmrServerWsListener)
  } else {
    // http server request handler keeps the same with
    // https://github.com/websockets/ws/blob/45e17acea791d865df6b255a55182e9c42e5877a/lib/websocket-server.js#L88-L96
    const route = ((_, res) => {
      const statusCode = 426
      const body = STATUS_CODES[statusCode]
      if (!body)
        throw new Error(`No body text found for the ${statusCode} status code`)

      res.writeHead(statusCode, {
        'Content-Length': body.length,
        'Content-Type': 'text/plain',
      })
      res.end(body)
    }) as Parameters<typeof createHttpServer>[1]
    // vite dev server in middleware mode
    // need to call ws listen manually
    if (httpsOptions) {
      wsHttpServer = createHttpsServer(httpsOptions, route)
    } else {
      wsHttpServer = createHttpServer(route)
    }
    wsHttpServer.on('upgrade', (req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      if (protocol === 'vite-ping' && server && !server.listening) {
        // reject connection to tell the vite/client that the server is not ready
        // if the http server is not listening
        // because the ws server listens before the http server listens
        req.destroy()
        return
      }
      handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
    })
    wsHttpServer.on('error', (e: Error & { code: string; port: number }) => {
      if (e.code === 'EADDRINUSE') {
        config.logger.error(
          colors.red(
            `WebSocket server error: Port ${e.port} is already in use`,
          ),
          { error: e },
        )
      } else {
        config.logger.error(
          colors.red(`WebSocket server error:\n${e.stack || e.message}`),
          { error: e },
        )
      }
    })
  }

  const emitCustomEvent = <T extends string>(
    event: T,
    data: InferCustomEventPayload<T>,
    socket: WebSocketRaw,
  ) => {
    const listeners = customListeners.get(event)
    if (!listeners?.size) return

    const client = getSocketClient(socket)
    for (const listener of listeners) {
      listener(data, client)
    }
  }

  wss.on('connection', (socket) => {
    socket.on('message', (raw) => {
      if (!customListeners.size) return
      let parsed: any
      try {
        parsed = JSON.parse(String(raw))
      } catch {}
      if (!parsed || parsed.type !== 'custom' || !parsed.event) return
      emitCustomEvent(parsed.event, parsed.data, socket)
    })
    socket.on('error', (err) => {
      config.logger.error(`${colors.red(`ws error:`)}\n${err.stack}`, {
        timestamp: true,
        error: err,
      })
    })
    socket.on('close', () => {
      emitCustomEvent('vite:client:disconnect', undefined, socket)
    })

    emitCustomEvent('vite:client:connect', undefined, socket)

    socket.send(JSON.stringify({ type: 'connected' }))
    if (bufferedMessage) {
      socket.send(JSON.stringify(bufferedMessage))
      bufferedMessage = null
    }
  })

  wss.on('error', (e: Error & { code: string; port: number }) => {
    if (e.code === 'EADDRINUSE') {
      config.logger.error(
        colors.red(`WebSocket server error: Port ${e.port} is already in use`),
        { error: e },
      )
    } else {
      config.logger.error(
        colors.red(`WebSocket server error:\n${e.stack || e.message}`),
        { error: e },
      )
    }
  })

  // Provide a wrapper to the ws client so we can send messages in JSON format
  // To be consistent with server.ws.send
  function getSocketClient(socket: WebSocketRaw) {
    if (!clientsMap.has(socket)) {
      clientsMap.set(socket, {
        send: (...args: any[]) => {
          let payload: HotPayload
          if (typeof args[0] === 'string') {
            payload = {
              type: 'custom',
              event: args[0],
              data: args[1],
            }
          } else {
            payload = args[0]
          }
          socket.send(JSON.stringify(payload))
        },
        socket,
      })
    }
    return clientsMap.get(socket)!
  }

  // On page reloads, if a file fails to compile and returns 500, the server
  // sends the error payload before the client connection is established.
  // If we have no open clients, buffer the error and send it to the next
  // connected client.
  // The same thing may happen when the optimizer runs fast enough to
  // finish the bundling before the client connects.
  let bufferedMessage: ErrorPayload | FullReloadPayload | null = null

  const normalizedHotChannel = normalizeHotChannel(
    {
      send(payload) {
        if (
          (payload.type === 'error' || payload.type === 'full-reload') &&
          !wss.clients.size
        ) {
          bufferedMessage = payload
          return
        }

        const stringified = JSON.stringify(payload)
        wss.clients.forEach((client) => {
          // readyState 1 means the connection is open
          if (client.readyState === 1) {
            client.send(stringified)
          }
        })
      },
      on(event: string, fn: any) {
        if (!customListeners.has(event)) {
          customListeners.set(event, new Set())
        }
        customListeners.get(event)!.add(fn)
      },
      off(event: string, fn: any) {
        customListeners.get(event)?.delete(fn)
      },
      listen() {
        wsHttpServer?.listen(port, host)
      },
      close() {
        // should remove listener if hmr.server is set
        // otherwise the old listener swallows all WebSocket connections
        if (hmrServerWsListener && wsServer) {
          wsServer.off('upgrade', hmrServerWsListener)
        }
        return new Promise<void>((resolve, reject) => {
          wss.clients.forEach((client) => {
            client.terminate()
          })
          wss.close((err) => {
            if (err) {
              reject(err)
            } else {
              if (wsHttpServer) {
                wsHttpServer.close((err) => {
                  if (err) {
                    reject(err)
                  } else {
                    resolve()
                  }
                })
              } else {
                resolve()
              }
            }
          })
        })
      },
    },
    config.server.hmr !== false,
    // Don't normalize client as we already handles the send, and to keep `.socket`
    false,
  )
  return {
    ...normalizedHotChannel,

    on: ((event: string, fn: any) => {
      if (wsServerEvents.includes(event)) {
        wss.on(event, fn)
        return
      }
      normalizedHotChannel.on(event, fn)
    }) as WebSocketServer['on'],
    off: ((event: string, fn: any) => {
      if (wsServerEvents.includes(event)) {
        wss.off(event, fn)
        return
      }
      normalizedHotChannel.off(event, fn)
    }) as WebSocketServer['off'],
    async close() {
      await normalizedHotChannel.close()
    },

    [isWebSocketServer]: true,
    get clients() {
      return new Set([...wss.clients].map(getSocketClient))
    },
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function createWebSocketServer(
  server: HttpServer | null,
  config: ResolvedConfig,
  httpsOptions?: HttpsServerOptions,
): WebSocketServer {
  if (config.server.ws === false) {
    return {
      [isWebSocketServer]: true,
      get clients() {
        return new Set<WebSocketClient>()
      },
      async close() {
        // noop
      },
      on: noop as any as WebSocketServer['on'],
      off: noop as any as WebSocketServer['off'],
      setInvokeHandler: noop,
      handleInvoke: async () => ({
        error: {
          name: 'TransportError',
          message: 'handleInvoke not implemented',
          stack: new Error().stack,
        },
      }),
      listen: noop,
      send: noop,
    }
  }

  let wsHttpServer: Server | undefined = undefined

  const wsOptions = isObject(config.server.ws) ? config.server.ws : undefined
  const wsCustomServer = wsOptions?.server
  const wsPort = wsOptions?.port
  // TODO: the main server port may not have been chosen yet as it may use the next available
  const portsAreCompatible = !wsPort || wsPort === config.server.port
  const wsServer = wsCustomServer || (portsAreCompatible && server)
  let hmrServerWsListener: (
    req: InstanceType<typeof IncomingMessage>,
    socket: Duplex,
    head: Buffer,
  ) => void
  const customListeners = new Map<string, Set<WebSocketCustomListener<any>>>()
  const clientsMap = new WeakMap<WebSocketRaw, WebSocketClient>()
  const port = wsPort || 24678
  const host = wsOptions?.host || undefined
  const allowedHosts =
    config.server.allowedHosts === true
      ? config.server.allowedHosts
      : Object.freeze([...config.server.allowedHosts]) // Freeze the array to allow caching

  const shouldHandle = (req: IncomingMessage) => {
    const protocol = req.headers['sec-websocket-protocol']!
    // vite-ping is allowed to connect from anywhere
    // because it needs to be connected before the client fetches the new `/@vite/client`
    // this is fine because vite-ping does not receive / send any meaningful data
    if (protocol === 'vite-ping') return true

    if (
      allowedHosts !== true &&
      !isHostAllowed(req.headers.host, allowedHosts)
    ) {
      return false
    }

    if (config.legacy?.skipWebSocketTokenCheck) {
      return true
    }

    // If the Origin header is set, this request might be coming from a browser.
    // Browsers always sets the Origin header for WebSocket connections.
    if (req.headers.origin) {
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      return hasValidToken(config, parsedUrl)
    }

    // We allow non-browser requests to connect without a token
    // for backward compat and convenience
    // This is fine because if you can sent a request without the SOP limitation,
    // you can also send a normal HTTP request to the server.
    return true
  }
  const handleUpgrade = (
    req: IncomingMessage,
    socket: Duplex,
    head: Buffer,
    isPing: boolean,
  ) => {
    wss.handleUpgrade(req, socket as Socket, head, (ws) => {
      // vite-ping is allowed to connect from anywhere
      // we close the connection immediately without connection event
      // so that the client does not get included in `wss.clients`
      if (isPing) {
        ws.close(/* Normal Closure */ 1000)
        return
      }
      wss.emit('connection', ws, req)
    })
  }
  const wss: WebSocketServerRaw_ = new WebSocketServerRaw({ noServer: true })
  wss.shouldHandle = shouldHandle

  if (wsServer) {
    let hmrBase = config.base
    const wsPath = wsOptions?.path
    if (wsPath) {
      hmrBase = path.posix.join(hmrBase, wsPath)
    }
    hmrServerWsListener = (req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      if (
        [HMR_HEADER, 'vite-ping'].includes(protocol) &&
        parsedUrl.pathname === hmrBase
      ) {
        handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
      } else {
        // Node.js detaches its own socket error handler before emitting
        // `upgrade`, so a socket that no listener takes over would crash the
        // process when the client resets the connection (e.g. ECONNRESET).
        // Other listeners (proxy, plugins) still receive the error as usual.
        socket.on('error', noop)
      }
    }
    wsServer.on('upgrade', hmrServerWsListener)
  } else {
    // http server request handler keeps the same with
    // https://github.com/websockets/ws/blob/45e17acea791d865df6b255a55182e9c42e5877a/lib/websocket-server.js#L88-L96
    const route = ((_, res) => {
      const statusCode = 426
      const body = STATUS_CODES[statusCode]
      if (!body)
        throw new Error(`No body text found for the ${statusCode} status code`)

      res.writeHead(statusCode, {
        'Content-Length': body.length,
        'Content-Type': 'text/plain',
      })
      res.end(body)
    }) as Parameters<typeof createHttpServer>[1]
    // vite dev server in middleware mode
    // need to call ws listen manually
    if (httpsOptions) {
      wsHttpServer = createHttpsServer(httpsOptions, route)
    } else {
      wsHttpServer = createHttpServer(route)
    }
    wsHttpServer.on('upgrade', (req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      if (protocol === 'vite-ping' && server && !server.listening) {
        // reject connection to tell the vite/client that the server is not ready
        // if the http server is not listening
        // because the ws server listens before the http server listens
        req.destroy()
        return
      }
      handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
    })
    wsHttpServer.on('error', (e: Error & { code: string; port: number }) => {
      if (e.code === 'EADDRINUSE') {
        config.logger.error(
          colors.red(
            `WebSocket server error: Port ${e.port} is already in use`,
          ),
          { error: e },
        )
      } else {
        config.logger.error(
          colors.red(`WebSocket server error:\n${e.stack || e.message}`),
          { error: e },
        )
      }
    })
  }

  const emitCustomEvent = <T extends string>(
    event: T,
    data: InferCustomEventPayload<T>,
    socket: WebSocketRaw,
  ) => {
    const listeners = customListeners.get(event)
    if (!listeners?.size) return

    const client = getSocketClient(socket)
    for (const listener of listeners) {
      listener(data, client)
    }
  }

  wss.on('connection', (socket) => {
    socket.on('message', (raw) => {
      if (!customListeners.size) return
      let parsed: any
      try {
        parsed = JSON.parse(String(raw))
      } catch {}
      if (!parsed || parsed.type !== 'custom' || !parsed.event) return
      emitCustomEvent(parsed.event, parsed.data, socket)
    })
    socket.on('error', (err) => {
      config.logger.error(`${colors.red(`ws error:`)}\n${err.stack}`, {
        timestamp: true,
        error: err,
      })
    })
    socket.on('close', () => {
      emitCustomEvent('vite:client:disconnect', undefined, socket)
    })

    emitCustomEvent('vite:client:connect', undefined, socket)

    socket.send(JSON.stringify({ type: 'connected' }))
    if (bufferedMessage) {
      socket.send(JSON.stringify(bufferedMessage))
      bufferedMessage = null
    }
  })

  wss.on('error', (e: Error & { code: string; port: number }) => {
    if (e.code === 'EADDRINUSE') {
      config.logger.error(
        colors.red(`WebSocket server error: Port ${e.port} is already in use`),
        { error: e },
      )
    } else {
      config.logger.error(
        colors.red(`WebSocket server error:\n${e.stack || e.message}`),
        { error: e },
      )
    }
  })

  // Provide a wrapper to the ws client so we can send messages in JSON format
  // To be consistent with server.ws.send
  function getSocketClient(socket: WebSocketRaw) {
    if (!clientsMap.has(socket)) {
      clientsMap.set(socket, {
        send: (...args: any[]) => {
          let payload: HotPayload
          if (typeof args[0] === 'string') {
            payload = {
              type: 'custom',
              event: args[0],
              data: args[1],
            }
          } else {
            payload = args[0]
          }
          socket.send(JSON.stringify(payload))
        },
        socket,
      })
    }
    return clientsMap.get(socket)!
  }

  // On page reloads, if a file fails to compile and returns 500, the server
  // sends the error payload before the client connection is established.
  // If we have no open clients, buffer the error and send it to the next
  // connected client.
  // The same thing may happen when the optimizer runs fast enough to
  // finish the bundling before the client connects.
  let bufferedMessage: ErrorPayload | FullReloadPayload | null = null

  const normalizedHotChannel = normalizeHotChannel(
    {
      send(payload) {
        if (
          (payload.type === 'error' || payload.type === 'full-reload') &&
          !wss.clients.size
        ) {
          bufferedMessage = payload
          return
        }

        const stringified = JSON.stringify(payload)
        wss.clients.forEach((client) => {
          // readyState 1 means the connection is open
          if (client.readyState === 1) {
            client.send(stringified)
          }
        })
      },
      on(event: string, fn: any) {
        if (!customListeners.has(event)) {
          customListeners.set(event, new Set())
        }
        customListeners.get(event)!.add(fn)
      },
      off(event: string, fn: any) {
        customListeners.get(event)?.delete(fn)
      },
      listen() {
        wsHttpServer?.listen(port, host)
      },
      close() {
        // should remove listener if hmr.server is set
        // otherwise the old listener swallows all WebSocket connections
        if (hmrServerWsListener && wsServer) {
          wsServer.off('upgrade', hmrServerWsListener)
        }
        return new Promise<void>((resolve, reject) => {
          wss.clients.forEach((client) => {
            client.terminate()
          })
          wss.close((err) => {
            if (err) {
              reject(err)
            } else {
              if (wsHttpServer) {
                wsHttpServer.close((err) => {
                  if (err) {
                    reject(err)
                  } else {
                    resolve()
                  }
                })
              } else {
                resolve()
              }
            }
          })
        })
      },
    },
    config.server.hmr !== false,
    // Don't normalize client as we already handles the send, and to keep `.socket`
    false,
  )
  return {
    ...normalizedHotChannel,

    on: ((event: string, fn: any) => {
      if (wsServerEvents.includes(event)) {
        wss.on(event, fn)
        return
      }
      normalizedHotChannel.on(event, fn)
    }) as WebSocketServer['on'],
    off: ((event: string, fn: any) => {
      if (wsServerEvents.includes(event)) {
        wss.off(event, fn)
        return
      }
      normalizedHotChannel.off(event, fn)
    }) as WebSocketServer['off'],
    async close() {
      await normalizedHotChannel.close()
    },

    [isWebSocketServer]: true,
    get clients() {
      return new Set([...wss.clients].map(getSocketClient))
    },
  }
}
```

### 🔹 函式: `hmrServerWsListener()`
- **變更前簽章 (Before)**: `hmrServerWsListener(req, socket, head)` (L226~L235)
- **變更後簽章 (After)**: `hmrServerWsListener(req, socket, head)` (L226~L241)

#### ◀️ 變更前實作碼 (Before Implementation):
```
(req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      if (
        [HMR_HEADER, 'vite-ping'].includes(protocol) &&
        parsedUrl.pathname === hmrBase
      ) {
        handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
      }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
(req, socket, head) => {
      const protocol = req.headers['sec-websocket-protocol']!
      const parsedUrl = new URL(`http://example.com${req.url!}`)
      if (
        [HMR_HEADER, 'vite-ping'].includes(protocol) &&
        parsedUrl.pathname === hmrBase
      ) {
        handleUpgrade(req, socket as Socket, head, protocol === 'vite-ping')
      } else {
        // Node.js detaches its own socket error handler before emitting
        // `upgrade`, so a socket that no listener takes over would crash the
        // process when the client resets the connection (e.g. ECONNRESET).
        // Other listeners (proxy, plugins) still receive the error as usual.
        socket.on('error', noop)
      }
    }
```


---

### 🔹 Commit #09: `38f3cb45`
- **完整 Hash**: `38f3cb45b1490ed24775547ceafa677b91a57714`
- **說明 (Ground Truth)**: fix(optimizer): scan `oxc.jsxInject` imports (#23758)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/optimizer/scan.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:62, E:35, A:0) ➔ After(N:62, E:35, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'scan' 被深鎖在內部閉包 (scope:scanImports@after/packages/vite/src/node/optimizer/scan.ts:L116C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `rolldownScanPlugin()`
- **變更前簽章 (Before)**: `function rolldownScanPlugin(
  environment: ScanEnvironment,
  depImports: Record<string, string>,
  missing: Record<string, string>,
  entries: string[],
  jsxOptions: OxcTransformOptions['jsx'],
): Plugin[]` (L366~L757)
- **變更後簽章 (After)**: `function rolldownScanPlugin(
  environment: ScanEnvironment,
  depImports: Record<string, string>,
  missing: Record<string, string>,
  entries: string[],
  jsxOptions: OxcTransformOptions['jsx'],
): Plugin[]` (L366~L757)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function rolldownScanPlugin(
  environment: ScanEnvironment,
  depImports: Record<string, string>,
  missing: Record<string, string>,
  entries: string[],
  jsxOptions: OxcTransformOptions['jsx'],
): Plugin[] {
  const seen = new Map<string, string | undefined>()
  async function resolveId(
    id: string,
    importer?: string,
    options?: Parameters<EnvironmentPluginContainer['resolveId']>[2],
  ): Promise<PartialResolvedId | null> {
    return environment.pluginContainer.resolveId(
      id,
      importer && normalizePath(importer),
      { scan: true, ...options },
    )
  }
  const resolve = async (
    id: string,
    importer?: string,
    options?: Parameters<typeof resolveId>[2],
  ) => {
    const key = JSON.stringify([
      id,
      importer && path.dirname(importer),
      options,
    ])
    if (seen.has(key)) {
      return seen.get(key)
    }
    const resolved = await resolveId(id, importer, options)
    const res = resolved?.id
    seen.set(key, res)
    return res
  }

  const optimizeDepsOptions = environment.config.optimizeDeps
  const include = optimizeDepsOptions.include
  const exclude = [
    ...(optimizeDepsOptions.exclude ?? []),
    '@vite/client',
    '@vite/env',
  ]

  const externalUnlessEntry = ({ path }: { path: string }) => ({
    id: path,
    external: !entries.includes(path),
  })

  const doTransformGlobImport = async (
    contents: string,
    id: string,
    loader: Loader,
  ) => {
    let transpiledContents: string
    // transpile because `transformGlobImport` only expects js
    if (loader !== 'js') {
      const result = transformSync(id, contents, {
        ...(jsxOptions !== undefined ? { jsx: jsxOptions } : {}),
        lang: loader,
        tsconfig: false,
      })
      if (result.errors.length > 0) {
        throw new AggregateError(result.errors, 'oxc transform error')
      }
      transpiledContents = result.code
    } else {
      transpiledContents = contents
    }

    const result = await transformGlobImport(
      transpiledContents,
      id,
      environment.config.root,
      resolve,
    )

    return result?.s.toString() || transpiledContents
  }

  const scripts: Record<
    string,
    {
      contents: string
      loader: Loader
    }
  > = {}

  const htmlTypeOnLoadCallback = async (id: string): Promise<string> => {
    let raw = await fsp.readFile(id, 'utf-8')
    // Avoid matching the content of the comment
    raw = raw.replace(commentRE, '<!---->')
    const isHtml = id.endsWith('.html')
    let js = ''
    let scriptId = 0
    const matches = raw.matchAll(scriptRE)
    for (const [, openTag, content] of matches) {
      const typeMatch = typeRE.exec(openTag)
      const type = typeMatch && (typeMatch[1] || typeMatch[2] || typeMatch[3])
      const langMatch = langRE.exec(openTag)
      const lang = langMatch && (langMatch[1] || langMatch[2] || langMatch[3])
      // skip non type module script
      if (isHtml && type !== 'module') {
        continue
      }
      // skip type="application/ld+json" and other non-JS types
      if (
        type &&
        !(
          type.includes('javascript') ||
          type.includes('ecmascript') ||
          type === 'module'
        )
      ) {
        continue
      }
      let loader: Loader = 'js'
      if (lang === 'ts' || lang === 'tsx' || lang === 'jsx') {
        loader = lang
      } else if (id.endsWith('.astro')) {
        loader = 'ts'
      }
      const srcMatch = srcRE.exec(openTag)
      if (srcMatch) {
        const src = srcMatch[1] || srcMatch[2] || srcMatch[3]
        js += `import ${JSON.stringify(src)}\n`
      } else if (content.trim()) {
        // The reason why virtual modules are needed:
        // 1. There can be module scripts (`<script context="module">` in Svelte and `<script>` in Vue)
        // or local scripts (`<script>` in Svelte and `<script setup>` in Vue)
        // 2. There can be multiple module scripts in html
        // We need to handle these separately in case variable names are reused between them

        // append imports in TS to prevent esbuild from removing them
        // since they may be used in the template
        const contents =
          content + (loader.startsWith('ts') ? extractImportPaths(content) : '')

        const key = `${id}?id=${scriptId++}`
        if (contents.includes('import.meta.glob')) {
          scripts[key] = {
            loader: 'js', // since it is transpiled
            contents: await doTransformGlobImport(contents, id, loader),
          }
        } else {
          scripts[key] = {
            loader,
            contents,
          }
        }

        const virtualModulePath = JSON.stringify(virtualModulePrefix + key)

        let addedImport = false

        // For Svelte files, exports in <script context="module"> or <script module> means module exports,
        // exports in <script> means component props. To avoid having two same export name from the
        // star exports, we need to ignore exports in <script>
        if (id.endsWith('.svelte')) {
          let isModule = svelteModuleRE.test(openTag) // test for svelte5 <script module> syntax
          if (!isModule) {
            // fallback, test for svelte4 <script context="module"> syntax
            const contextMatch = svelteScriptModuleRE.exec(openTag)
            const context =
              contextMatch &&
              (contextMatch[1] || contextMatch[2] || contextMatch[3])
            isModule = context === 'module'
          }
          if (!isModule) {
            addedImport = true
            js += `import ${virtualModulePath}\n`
          }
        }

        if (!addedImport) {
          js += `export * from ${virtualModulePath}\n`
        }
      }
    }

    // This will trigger incorrectly if `export default` is contained
    // anywhere in a string. Svelte and Astro files can't have
    // `export default` as code so we know if it's encountered it's a
    // false positive (e.g. contained in a string)
    if (!id.endsWith('.vue') || !js.includes('export default')) {
      js += '\nexport default {}'
    }

    return js
  }

  const ASSET_TYPE_RE = new RegExp(`\\.(${KNOWN_ASSET_TYPES.join('|')})$`)

  return [
    {
      name: 'vite:dep-scan:resolve-external-url',
      resolveId: {
        // external urls
        filter: { id: externalRE },
        handler: (id) => ({ id, external: true }),
      },
    },
    {
      name: 'vite:dep-scan:resolve-data-url',
      resolveId: {
        // data urls
        filter: { id: dataUrlRE },
        handler: (id) => ({ id, external: true }),
      },
    },
    {
      // local scripts (`<script>` in Svelte and `<script setup>` in Vue)
      name: 'vite:dep-scan:local-scripts',
      resolveId: {
        filter: { id: virtualModuleRE },
        handler: (id) => ({ id }),
      },
      load: {
        filter: { id: virtualModuleRE },
        handler(id) {
          const script = scripts[id.replace(virtualModulePrefix, '')]
          return {
            code: script.contents,
            moduleType: script.loader,
          }
        },
      },
    },

    {
      name: 'vite:dep-scan:resolve',
      async resolveId(id, importer) {
        // Make sure virtual module importer can be resolve
        importer =
          importer && virtualModuleRE.test(importer)
            ? importer.replace(virtualModulePrefix, '')
            : importer

        // html types: extract script contents -----------------------------------
        if (htmlTypesRE.test(id)) {
          const resolved = await resolve(id, importer)
          if (!resolved) return
          // It is possible for the scanner to scan html types in node_modules.
          // If we can optimize this html type, skip it so it's handled by the
          // bare import resolve, and recorded as optimization dep.
          if (
            !isInNodeModules(resolved) ||
            !isOptimizable(resolved, optimizeDepsOptions)
          ) {
            if (shouldExternalizeDep(resolved, id)) {
              return externalUnlessEntry({ path: id })
            }
            return resolved
          }
        }

        // bare imports: record and externalize ----------------------------------
        // avoid matching windows volume
        if (/^[\w@][^:]/.test(id)) {
          if (moduleListContains(exclude, id)) {
            return externalUnlessEntry({ path: id })
          }
          if (depImports[id]) {
            return externalUnlessEntry({ path: id })
          }
          const resolved = await resolve(id, importer)
          if (resolved) {
            if (shouldExternalizeDep(resolved, id)) {
              return externalUnlessEntry({ path: id })
            }
            if (isInNodeModules(resolved) || include?.includes(id)) {
              // dependency or forced included, externalize and stop crawling
              if (isOptimizable(resolved, optimizeDepsOptions)) {
                depImports[id] = resolved
              }
              return externalUnlessEntry({ path: id })
            } else if (isScannable(resolved, optimizeDepsOptions.extensions)) {
              // linked package, keep crawling
              return path.resolve(resolved)
            } else {
              return externalUnlessEntry({ path: id })
            }
          } else {
            missing[id] = normalizePath(importer!)
          }
        }

        // Externalized file types -----------------------------------------------
        // these are done on raw ids using esbuild's native regex filter so it
        // should be faster than doing it in the catch-all via js
        // they are done after the bare import resolve because a package name
        // may end with these extensions

        // css
        if (CSS_LANGS_RE.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // json & wasm
        if (/\.(?:json|json5|wasm)$/.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // known asset types
        if (ASSET_TYPE_RE.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // known vite query types: ?worker, ?raw
        if (SPECIAL_QUERY_RE.test(id)) {
          return {
            id,
            external: true,
          }
        }

        // catch all -------------------------------------------------------------

        // use vite resolver to support urls and omitted extensions
        const resolved = await resolve(id, importer)
        if (resolved) {
          if (
            shouldExternalizeDep(resolved, id) ||
            !isScannable(resolved, optimizeDepsOptions.extensions)
          ) {
            return externalUnlessEntry({ path: id })
          }
          return path.resolve(cleanUrl(resolved))
        }

        // resolve failed... probably unsupported type
        return externalUnlessEntry({ path: id })
      },
    },
    {
      name: 'vite:dep-scan:load:html',
      load: {
        // extract scripts inside HTML-like files and treat it as a js module
        filter: { id: htmlTypesRE },
        async handler(id) {
          return {
            code: await htmlTypeOnLoadCallback(id),
            moduleType: 'js',
          }
        },
      },
    },
    // for jsx/tsx, we need to access the content and check for
    // presence of import.meta.glob, since it results in import relationships
    // but isn't crawled by esbuild.
    ...(environment.config.esbuild && environment.config.esbuild.jsxInject
      ? [
          {
            name: 'vite:dep-scan:transform:jsx-inject',
            transform: {
              filter: {
                id: /\.[jt]sx$/,
              },
              handler(code) {
                const esbuildConfig = environment.config.esbuild
                if (esbuildConfig && esbuildConfig.jsxInject) {
                  code = esbuildConfig.jsxInject + `\n` + code
                }
                return code
              },
            },
          } satisfies Plugin,
        ]
      : []),
    {
      name: 'vite:dep-scan:transform:js-glob',
      transform: {
        filter: {
          code: 'import.meta.glob',
        },
        async handler(code, id) {
          if (JS_TYPES_RE.test(id)) {
            let ext = path.extname(id).slice(1)
            if (ext === 'mjs') ext = 'js'
            const loader = ext as 'js' | 'ts' | 'jsx' | 'tsx'
            return {
              moduleType: 'js',
              code: await doTransformGlobImport(code, id, loader),
            }
          }
        },
      },
    },
  ]
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function rolldownScanPlugin(
  environment: ScanEnvironment,
  depImports: Record<string, string>,
  missing: Record<string, string>,
  entries: string[],
  jsxOptions: OxcTransformOptions['jsx'],
): Plugin[] {
  const seen = new Map<string, string | undefined>()
  async function resolveId(
    id: string,
    importer?: string,
    options?: Parameters<EnvironmentPluginContainer['resolveId']>[2],
  ): Promise<PartialResolvedId | null> {
    return environment.pluginContainer.resolveId(
      id,
      importer && normalizePath(importer),
      { scan: true, ...options },
    )
  }
  const resolve = async (
    id: string,
    importer?: string,
    options?: Parameters<typeof resolveId>[2],
  ) => {
    const key = JSON.stringify([
      id,
      importer && path.dirname(importer),
      options,
    ])
    if (seen.has(key)) {
      return seen.get(key)
    }
    const resolved = await resolveId(id, importer, options)
    const res = resolved?.id
    seen.set(key, res)
    return res
  }

  const optimizeDepsOptions = environment.config.optimizeDeps
  const include = optimizeDepsOptions.include
  const exclude = [
    ...(optimizeDepsOptions.exclude ?? []),
    '@vite/client',
    '@vite/env',
  ]

  const externalUnlessEntry = ({ path }: { path: string }) => ({
    id: path,
    external: !entries.includes(path),
  })

  const doTransformGlobImport = async (
    contents: string,
    id: string,
    loader: Loader,
  ) => {
    let transpiledContents: string
    // transpile because `transformGlobImport` only expects js
    if (loader !== 'js') {
      const result = transformSync(id, contents, {
        ...(jsxOptions !== undefined ? { jsx: jsxOptions } : {}),
        lang: loader,
        tsconfig: false,
      })
      if (result.errors.length > 0) {
        throw new AggregateError(result.errors, 'oxc transform error')
      }
      transpiledContents = result.code
    } else {
      transpiledContents = contents
    }

    const result = await transformGlobImport(
      transpiledContents,
      id,
      environment.config.root,
      resolve,
    )

    return result?.s.toString() || transpiledContents
  }

  const scripts: Record<
    string,
    {
      contents: string
      loader: Loader
    }
  > = {}

  const htmlTypeOnLoadCallback = async (id: string): Promise<string> => {
    let raw = await fsp.readFile(id, 'utf-8')
    // Avoid matching the content of the comment
    raw = raw.replace(commentRE, '<!---->')
    const isHtml = id.endsWith('.html')
    let js = ''
    let scriptId = 0
    const matches = raw.matchAll(scriptRE)
    for (const [, openTag, content] of matches) {
      const typeMatch = typeRE.exec(openTag)
      const type = typeMatch && (typeMatch[1] || typeMatch[2] || typeMatch[3])
      const langMatch = langRE.exec(openTag)
      const lang = langMatch && (langMatch[1] || langMatch[2] || langMatch[3])
      // skip non type module script
      if (isHtml && type !== 'module') {
        continue
      }
      // skip type="application/ld+json" and other non-JS types
      if (
        type &&
        !(
          type.includes('javascript') ||
          type.includes('ecmascript') ||
          type === 'module'
        )
      ) {
        continue
      }
      let loader: Loader = 'js'
      if (lang === 'ts' || lang === 'tsx' || lang === 'jsx') {
        loader = lang
      } else if (id.endsWith('.astro')) {
        loader = 'ts'
      }
      const srcMatch = srcRE.exec(openTag)
      if (srcMatch) {
        const src = srcMatch[1] || srcMatch[2] || srcMatch[3]
        js += `import ${JSON.stringify(src)}\n`
      } else if (content.trim()) {
        // The reason why virtual modules are needed:
        // 1. There can be module scripts (`<script context="module">` in Svelte and `<script>` in Vue)
        // or local scripts (`<script>` in Svelte and `<script setup>` in Vue)
        // 2. There can be multiple module scripts in html
        // We need to handle these separately in case variable names are reused between them

        // append imports in TS to prevent esbuild from removing them
        // since they may be used in the template
        const contents =
          content + (loader.startsWith('ts') ? extractImportPaths(content) : '')

        const key = `${id}?id=${scriptId++}`
        if (contents.includes('import.meta.glob')) {
          scripts[key] = {
            loader: 'js', // since it is transpiled
            contents: await doTransformGlobImport(contents, id, loader),
          }
        } else {
          scripts[key] = {
            loader,
            contents,
          }
        }

        const virtualModulePath = JSON.stringify(virtualModulePrefix + key)

        let addedImport = false

        // For Svelte files, exports in <script context="module"> or <script module> means module exports,
        // exports in <script> means component props. To avoid having two same export name from the
        // star exports, we need to ignore exports in <script>
        if (id.endsWith('.svelte')) {
          let isModule = svelteModuleRE.test(openTag) // test for svelte5 <script module> syntax
          if (!isModule) {
            // fallback, test for svelte4 <script context="module"> syntax
            const contextMatch = svelteScriptModuleRE.exec(openTag)
            const context =
              contextMatch &&
              (contextMatch[1] || contextMatch[2] || contextMatch[3])
            isModule = context === 'module'
          }
          if (!isModule) {
            addedImport = true
            js += `import ${virtualModulePath}\n`
          }
        }

        if (!addedImport) {
          js += `export * from ${virtualModulePath}\n`
        }
      }
    }

    // This will trigger incorrectly if `export default` is contained
    // anywhere in a string. Svelte and Astro files can't have
    // `export default` as code so we know if it's encountered it's a
    // false positive (e.g. contained in a string)
    if (!id.endsWith('.vue') || !js.includes('export default')) {
      js += '\nexport default {}'
    }

    return js
  }

  const ASSET_TYPE_RE = new RegExp(`\\.(${KNOWN_ASSET_TYPES.join('|')})$`)

  return [
    {
      name: 'vite:dep-scan:resolve-external-url',
      resolveId: {
        // external urls
        filter: { id: externalRE },
        handler: (id) => ({ id, external: true }),
      },
    },
    {
      name: 'vite:dep-scan:resolve-data-url',
      resolveId: {
        // data urls
        filter: { id: dataUrlRE },
        handler: (id) => ({ id, external: true }),
      },
    },
    {
      // local scripts (`<script>` in Svelte and `<script setup>` in Vue)
      name: 'vite:dep-scan:local-scripts',
      resolveId: {
        filter: { id: virtualModuleRE },
        handler: (id) => ({ id }),
      },
      load: {
        filter: { id: virtualModuleRE },
        handler(id) {
          const script = scripts[id.replace(virtualModulePrefix, '')]
          return {
            code: script.contents,
            moduleType: script.loader,
          }
        },
      },
    },

    {
      name: 'vite:dep-scan:resolve',
      async resolveId(id, importer) {
        // Make sure virtual module importer can be resolve
        importer =
          importer && virtualModuleRE.test(importer)
            ? importer.replace(virtualModulePrefix, '')
            : importer

        // html types: extract script contents -----------------------------------
        if (htmlTypesRE.test(id)) {
          const resolved = await resolve(id, importer)
          if (!resolved) return
          // It is possible for the scanner to scan html types in node_modules.
          // If we can optimize this html type, skip it so it's handled by the
          // bare import resolve, and recorded as optimization dep.
          if (
            !isInNodeModules(resolved) ||
            !isOptimizable(resolved, optimizeDepsOptions)
          ) {
            if (shouldExternalizeDep(resolved, id)) {
              return externalUnlessEntry({ path: id })
            }
            return resolved
          }
        }

        // bare imports: record and externalize ----------------------------------
        // avoid matching windows volume
        if (/^[\w@][^:]/.test(id)) {
          if (moduleListContains(exclude, id)) {
            return externalUnlessEntry({ path: id })
          }
          if (depImports[id]) {
            return externalUnlessEntry({ path: id })
          }
          const resolved = await resolve(id, importer)
          if (resolved) {
            if (shouldExternalizeDep(resolved, id)) {
              return externalUnlessEntry({ path: id })
            }
            if (isInNodeModules(resolved) || include?.includes(id)) {
              // dependency or forced included, externalize and stop crawling
              if (isOptimizable(resolved, optimizeDepsOptions)) {
                depImports[id] = resolved
              }
              return externalUnlessEntry({ path: id })
            } else if (isScannable(resolved, optimizeDepsOptions.extensions)) {
              // linked package, keep crawling
              return path.resolve(resolved)
            } else {
              return externalUnlessEntry({ path: id })
            }
          } else {
            missing[id] = normalizePath(importer!)
          }
        }

        // Externalized file types -----------------------------------------------
        // these are done on raw ids using esbuild's native regex filter so it
        // should be faster than doing it in the catch-all via js
        // they are done after the bare import resolve because a package name
        // may end with these extensions

        // css
        if (CSS_LANGS_RE.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // json & wasm
        if (/\.(?:json|json5|wasm)$/.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // known asset types
        if (ASSET_TYPE_RE.test(id)) {
          return externalUnlessEntry({ path: id })
        }

        // known vite query types: ?worker, ?raw
        if (SPECIAL_QUERY_RE.test(id)) {
          return {
            id,
            external: true,
          }
        }

        // catch all -------------------------------------------------------------

        // use vite resolver to support urls and omitted extensions
        const resolved = await resolve(id, importer)
        if (resolved) {
          if (
            shouldExternalizeDep(resolved, id) ||
            !isScannable(resolved, optimizeDepsOptions.extensions)
          ) {
            return externalUnlessEntry({ path: id })
          }
          return path.resolve(cleanUrl(resolved))
        }

        // resolve failed... probably unsupported type
        return externalUnlessEntry({ path: id })
      },
    },
    {
      name: 'vite:dep-scan:load:html',
      load: {
        // extract scripts inside HTML-like files and treat it as a js module
        filter: { id: htmlTypesRE },
        async handler(id) {
          return {
            code: await htmlTypeOnLoadCallback(id),
            moduleType: 'js',
          }
        },
      },
    },
    // for jsx/tsx, we need to access the content and check for
    // presence of import.meta.glob, since it results in import relationships
    // but isn't crawled by esbuild.
    ...(environment.config.oxc && environment.config.oxc.jsxInject
      ? [
          {
            name: 'vite:dep-scan:transform:jsx-inject',
            transform: {
              filter: {
                id: /\.[jt]sx$/,
              },
              handler(code) {
                const oxcConfig = environment.config.oxc
                if (oxcConfig && oxcConfig.jsxInject) {
                  code = oxcConfig.jsxInject + `\n` + code
                }
                return code
              },
            },
          } satisfies Plugin,
        ]
      : []),
    {
      name: 'vite:dep-scan:transform:js-glob',
      transform: {
        filter: {
          code: 'import.meta.glob',
        },
        async handler(code, id) {
          if (JS_TYPES_RE.test(id)) {
            let ext = path.extname(id).slice(1)
            if (ext === 'mjs') ext = 'js'
            const loader = ext as 'js' | 'ts' | 'jsx' | 'tsx'
            return {
              moduleType: 'js',
              code: await doTransformGlobImport(code, id, loader),
            }
          }
        },
      },
    },
  ]
}
```

### 🔹 函式: `handler()`
- **變更前簽章 (Before)**: `handler(code)` (L726~L732)
- **變更後簽章 (After)**: `handler(code)` (L726~L732)

#### ◀️ 變更前實作碼 (Before Implementation):
```
handler(code) {
                const esbuildConfig = environment.config.esbuild
                if (esbuildConfig && esbuildConfig.jsxInject) {
                  code = esbuildConfig.jsxInject + `\n` + code
                }
                return code
              }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
handler(code) {
                const oxcConfig = environment.config.oxc
                if (oxcConfig && oxcConfig.jsxInject) {
                  code = oxcConfig.jsxInject + `\n` + code
                }
                return code
              }
```


---

### 🔹 Commit #10: `6019aa79`
- **完整 Hash**: `6019aa79975465516da7c6f532d568422b019a25`
- **說明 (Ground Truth)**: fix(bundled-dev): include user `import.meta.env.*` defines in the `import.meta.env` object (#23713)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/plugins/define.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:16, E:12, A:0) ➔ After(N:16, E:12, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `generatePattern()`
- **變更前簽章 (Before)**: `function generatePattern(environment: Environment)` (L30~L101)
- **變更後簽章 (After)**: `function generatePattern(environment: Environment)` (L30~L101)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function generatePattern(environment: Environment) {
    const isBundled = environment.config.isBundled
    const keepProcessEnv = environment.config.keepProcessEnv

    // during dev, import.meta properties are handled by importAnalysis plugin.
    const importMetaKeys: Record<string, string> = {}
    const importMetaEnvKeys: Record<string, string> = {}
    const importMetaFallbackKeys: Record<string, string> = {}
    if (isBuild) {
      importMetaKeys['import.meta.hot'] = `undefined`
    }
    if (isBundled) {
      for (const key in config.env) {
        const val = JSON.stringify(config.env[key])
        importMetaKeys[`import.meta.env.${key}`] = val
        importMetaEnvKeys[key] = val
      }
      // these will be set to a proper value below
      importMetaKeys['import.meta.env.SSR'] = `undefined`
      importMetaFallbackKeys['import.meta.env'] = `undefined`
    }

    const userDefine: Record<string, string> = {}
    const userDefineEnv: Record<string, any> = {}
    for (const key in environment.config.define) {
      userDefine[key] = handleDefineValue(environment.config.define[key])

      // make sure `import.meta.env` object has user define properties
      if (isBuild && key.startsWith('import.meta.env.')) {
        userDefineEnv[key.slice(16)] = environment.config.define[key]
      }
    }

    const define: Record<string, string> = {
      ...(keepProcessEnv ? {} : processEnv),
      ...importMetaKeys,
      ...userDefine,
      ...importMetaFallbackKeys,
    }

    // Additional define fixes based on `ssr` value
    const ssr = environment.config.consumer === 'server'

    if ('import.meta.env.SSR' in define) {
      define['import.meta.env.SSR'] = ssr + ''
    }

    const importMetaEnvVal = serializeDefine({
      ...importMetaEnvKeys,
      SSR: ssr + '',
      ...userDefineEnv,
    })

    // Create regex pattern as a fast check before running esbuild
    const patternKeys = Object.keys(userDefine)
    if (!keepProcessEnv && Object.keys(processEnv).length) {
      patternKeys.push('process.env')
    }
    if (Object.keys(importMetaKeys).length) {
      patternKeys.push('import.meta.env', 'import.meta.hot')
    }
    const pattern = patternKeys.length
      ? new RegExp(
          patternKeys
            // replace `\.` (ignore `\\.`) with `\??\.` to match with `?.` as well
            .map((key) => escapeRegex(key).replaceAll(escapedDotRE, '\\??\\.'))
            .join('|'),
        )
      : null

    return [define, pattern, importMetaEnvVal] as const
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function generatePattern(environment: Environment) {
    const isBundled = environment.config.isBundled
    const keepProcessEnv = environment.config.keepProcessEnv

    // during dev, import.meta properties are handled by importAnalysis plugin.
    const importMetaKeys: Record<string, string> = {}
    const importMetaEnvKeys: Record<string, string> = {}
    const importMetaFallbackKeys: Record<string, string> = {}
    if (isBuild) {
      importMetaKeys['import.meta.hot'] = `undefined`
    }
    if (isBundled) {
      for (const key in config.env) {
        const val = JSON.stringify(config.env[key])
        importMetaKeys[`import.meta.env.${key}`] = val
        importMetaEnvKeys[key] = val
      }
      // these will be set to a proper value below
      importMetaKeys['import.meta.env.SSR'] = `undefined`
      importMetaFallbackKeys['import.meta.env'] = `undefined`
    }

    const userDefine: Record<string, string> = {}
    const userDefineEnv: Record<string, any> = {}
    for (const key in environment.config.define) {
      userDefine[key] = handleDefineValue(environment.config.define[key])

      // make sure `import.meta.env` object has user define properties
      if (isBundled && key.startsWith('import.meta.env.')) {
        userDefineEnv[key.slice(16)] = environment.config.define[key]
      }
    }

    const define: Record<string, string> = {
      ...(keepProcessEnv ? {} : processEnv),
      ...importMetaKeys,
      ...userDefine,
      ...importMetaFallbackKeys,
    }

    // Additional define fixes based on `ssr` value
    const ssr = environment.config.consumer === 'server'

    if ('import.meta.env.SSR' in define) {
      define['import.meta.env.SSR'] = ssr + ''
    }

    const importMetaEnvVal = serializeDefine({
      ...importMetaEnvKeys,
      SSR: ssr + '',
      ...userDefineEnv,
    })

    // Create regex pattern as a fast check before running esbuild
    const patternKeys = Object.keys(userDefine)
    if (!keepProcessEnv && Object.keys(processEnv).length) {
      patternKeys.push('process.env')
    }
    if (Object.keys(importMetaKeys).length) {
      patternKeys.push('import.meta.env', 'import.meta.hot')
    }
    const pattern = patternKeys.length
      ? new RegExp(
          patternKeys
            // replace `\.` (ignore `\\.`) with `\??\.` to match with `?.` as well
            .map((key) => escapeRegex(key).replaceAll(escapedDotRE, '\\??\\.'))
            .join('|'),
        )
      : null

    return [define, pattern, importMetaEnvVal] as const
  }
```

### 🔹 函式: `definePlugin()`
- **變更前簽章 (Before)**: `function definePlugin(config: ResolvedConfig): Plugin` (L12~L168)
- **變更後簽章 (After)**: `function definePlugin(config: ResolvedConfig): Plugin` (L12~L168)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function definePlugin(config: ResolvedConfig): Plugin {
  const isBuild = config.command === 'build'
  const isBuildLib = isBuild && config.build.lib

  // ignore replace process.env in lib build
  const processEnv: Record<string, string> = {}
  if (!isBuildLib) {
    const nodeEnv = process.env.NODE_ENV || config.mode
    Object.assign(processEnv, {
      'process.env': `{}`,
      'global.process.env': `{}`,
      'globalThis.process.env': `{}`,
      'process.env.NODE_ENV': JSON.stringify(nodeEnv),
      'global.process.env.NODE_ENV': JSON.stringify(nodeEnv),
      'globalThis.process.env.NODE_ENV': JSON.stringify(nodeEnv),
    })
  }

  function generatePattern(environment: Environment) {
    const isBundled = environment.config.isBundled
    const keepProcessEnv = environment.config.keepProcessEnv

    // during dev, import.meta properties are handled by importAnalysis plugin.
    const importMetaKeys: Record<string, string> = {}
    const importMetaEnvKeys: Record<string, string> = {}
    const importMetaFallbackKeys: Record<string, string> = {}
    if (isBuild) {
      importMetaKeys['import.meta.hot'] = `undefined`
    }
    if (isBundled) {
      for (const key in config.env) {
        const val = JSON.stringify(config.env[key])
        importMetaKeys[`import.meta.env.${key}`] = val
        importMetaEnvKeys[key] = val
      }
      // these will be set to a proper value below
      importMetaKeys['import.meta.env.SSR'] = `undefined`
      importMetaFallbackKeys['import.meta.env'] = `undefined`
    }

    const userDefine: Record<string, string> = {}
    const userDefineEnv: Record<string, any> = {}
    for (const key in environment.config.define) {
      userDefine[key] = handleDefineValue(environment.config.define[key])

      // make sure `import.meta.env` object has user define properties
      if (isBuild && key.startsWith('import.meta.env.')) {
        userDefineEnv[key.slice(16)] = environment.config.define[key]
      }
    }

    const define: Record<string, string> = {
      ...(keepProcessEnv ? {} : processEnv),
      ...importMetaKeys,
      ...userDefine,
      ...importMetaFallbackKeys,
    }

    // Additional define fixes based on `ssr` value
    const ssr = environment.config.consumer === 'server'

    if ('import.meta.env.SSR' in define) {
      define['import.meta.env.SSR'] = ssr + ''
    }

    const importMetaEnvVal = serializeDefine({
      ...importMetaEnvKeys,
      SSR: ssr + '',
      ...userDefineEnv,
    })

    // Create regex pattern as a fast check before running esbuild
    const patternKeys = Object.keys(userDefine)
    if (!keepProcessEnv && Object.keys(processEnv).length) {
      patternKeys.push('process.env')
    }
    if (Object.keys(importMetaKeys).length) {
      patternKeys.push('import.meta.env', 'import.meta.hot')
    }
    const pattern = patternKeys.length
      ? new RegExp(
          patternKeys
            // replace `\.` (ignore `\\.`) with `\??\.` to match with `?.` as well
            .map((key) => escapeRegex(key).replaceAll(escapedDotRE, '\\??\\.'))
            .join('|'),
        )
      : null

    return [define, pattern, importMetaEnvVal] as const
  }

  const patternsCache = new WeakMap<
    Environment,
    readonly [Record<string, string>, RegExp | null, string]
  >()
  function getPattern(environment: Environment) {
    let pattern = patternsCache.get(environment)
    if (!pattern) {
      pattern = generatePattern(environment)
      patternsCache.set(environment, pattern)
    }
    return pattern
  }

  return {
    name: 'vite:define',

    applyToEnvironment(environment) {
      if (environment.config.isBundled) {
        return {
          name: 'vite:define',
          options(option) {
            const [define, _pattern, importMetaEnvVal] = getPattern(
              this.environment,
            )
            define['import.meta.env'] = importMetaEnvVal
            define['import.meta.env.*'] = 'undefined'
            option.transform ??= {}
            option.transform.define = { ...option.transform.define, ...define }
          },
        }
      }
      return true
    },

    transform: {
      handler(code, id) {
        if (this.environment.config.consumer === 'client') {
          // for dev we inject actual global defines in the vite client to
          // avoid the transform cost. see the `clientInjection` and
          // `importAnalysis` plugin.
          return
        }

        if (
          // exclude html, css and static assets for performance
          isHTMLRequest(id) ||
          isCSSRequest(id) ||
          isNonJsRequest(id) ||
          config.assetsInclude(id)
        ) {
          return
        }

        const [define, pattern] = getPattern(this.environment)
        if (!pattern) return

        // Check if our code needs any replacements before running esbuild
        pattern.lastIndex = 0
        if (!pattern.test(code)) return

        const result = replaceDefine(this.environment, code, id, define)
        return result
      },
    },
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function definePlugin(config: ResolvedConfig): Plugin {
  const isBuild = config.command === 'build'
  const isBuildLib = isBuild && config.build.lib

  // ignore replace process.env in lib build
  const processEnv: Record<string, string> = {}
  if (!isBuildLib) {
    const nodeEnv = process.env.NODE_ENV || config.mode
    Object.assign(processEnv, {
      'process.env': `{}`,
      'global.process.env': `{}`,
      'globalThis.process.env': `{}`,
      'process.env.NODE_ENV': JSON.stringify(nodeEnv),
      'global.process.env.NODE_ENV': JSON.stringify(nodeEnv),
      'globalThis.process.env.NODE_ENV': JSON.stringify(nodeEnv),
    })
  }

  function generatePattern(environment: Environment) {
    const isBundled = environment.config.isBundled
    const keepProcessEnv = environment.config.keepProcessEnv

    // during dev, import.meta properties are handled by importAnalysis plugin.
    const importMetaKeys: Record<string, string> = {}
    const importMetaEnvKeys: Record<string, string> = {}
    const importMetaFallbackKeys: Record<string, string> = {}
    if (isBuild) {
      importMetaKeys['import.meta.hot'] = `undefined`
    }
    if (isBundled) {
      for (const key in config.env) {
        const val = JSON.stringify(config.env[key])
        importMetaKeys[`import.meta.env.${key}`] = val
        importMetaEnvKeys[key] = val
      }
      // these will be set to a proper value below
      importMetaKeys['import.meta.env.SSR'] = `undefined`
      importMetaFallbackKeys['import.meta.env'] = `undefined`
    }

    const userDefine: Record<string, string> = {}
    const userDefineEnv: Record<string, any> = {}
    for (const key in environment.config.define) {
      userDefine[key] = handleDefineValue(environment.config.define[key])

      // make sure `import.meta.env` object has user define properties
      if (isBundled && key.startsWith('import.meta.env.')) {
        userDefineEnv[key.slice(16)] = environment.config.define[key]
      }
    }

    const define: Record<string, string> = {
      ...(keepProcessEnv ? {} : processEnv),
      ...importMetaKeys,
      ...userDefine,
      ...importMetaFallbackKeys,
    }

    // Additional define fixes based on `ssr` value
    const ssr = environment.config.consumer === 'server'

    if ('import.meta.env.SSR' in define) {
      define['import.meta.env.SSR'] = ssr + ''
    }

    const importMetaEnvVal = serializeDefine({
      ...importMetaEnvKeys,
      SSR: ssr + '',
      ...userDefineEnv,
    })

    // Create regex pattern as a fast check before running esbuild
    const patternKeys = Object.keys(userDefine)
    if (!keepProcessEnv && Object.keys(processEnv).length) {
      patternKeys.push('process.env')
    }
    if (Object.keys(importMetaKeys).length) {
      patternKeys.push('import.meta.env', 'import.meta.hot')
    }
    const pattern = patternKeys.length
      ? new RegExp(
          patternKeys
            // replace `\.` (ignore `\\.`) with `\??\.` to match with `?.` as well
            .map((key) => escapeRegex(key).replaceAll(escapedDotRE, '\\??\\.'))
            .join('|'),
        )
      : null

    return [define, pattern, importMetaEnvVal] as const
  }

  const patternsCache = new WeakMap<
    Environment,
    readonly [Record<string, string>, RegExp | null, string]
  >()
  function getPattern(environment: Environment) {
    let pattern = patternsCache.get(environment)
    if (!pattern) {
      pattern = generatePattern(environment)
      patternsCache.set(environment, pattern)
    }
    return pattern
  }

  return {
    name: 'vite:define',

    applyToEnvironment(environment) {
      if (environment.config.isBundled) {
        return {
          name: 'vite:define',
          options(option) {
            const [define, _pattern, importMetaEnvVal] = getPattern(
              this.environment,
            )
            define['import.meta.env'] = importMetaEnvVal
            define['import.meta.env.*'] = 'undefined'
            option.transform ??= {}
            option.transform.define = { ...option.transform.define, ...define }
          },
        }
      }
      return true
    },

    transform: {
      handler(code, id) {
        if (this.environment.config.consumer === 'client') {
          // for dev we inject actual global defines in the vite client to
          // avoid the transform cost. see the `clientInjection` and
          // `importAnalysis` plugin.
          return
        }

        if (
          // exclude html, css and static assets for performance
          isHTMLRequest(id) ||
          isCSSRequest(id) ||
          isNonJsRequest(id) ||
          config.assetsInclude(id)
        ) {
          return
        }

        const [define, pattern] = getPattern(this.environment)
        if (!pattern) return

        // Check if our code needs any replacements before running esbuild
        pattern.lastIndex = 0
        if (!pattern.test(code)) return

        const result = replaceDefine(this.environment, code, id, define)
        return result
      },
    },
  }
}
```


---

### 🔹 Commit #11: `f2060963`
- **完整 Hash**: `f20609630faa93026924275115d1426fdc08629e`
- **說明 (Ground Truth)**: fix(optimizer): fall back to yarn.lock for lockfile hash (#23667)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/optimizer/index.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:90, E:106, A:0) ➔ After(N:93, E:106, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `fallbackLockfilePaths` (FUNCTION_DEF)
  • + [新增節點] `fallbackLockfileFormats` (MODULE_STATE)
  • + [新增節點] `fallbackLockfilePaths` (MODULE_STATE)

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'cleanUp' 被深鎖在內部閉包 (scope:runOptimizeDeps@after/packages/vite/src/node/optimizer/index.ts:L523C8)，外部無法調用！ (共 2 處)

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getLockfileHash()`
- **變更前簽章 (Before)**: `function getLockfileHash(environment: Environment): string` (L1347~L1369)
- **變更後簽章 (After)**: `function getLockfileHash(root: string): string` (L1361~L1385)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getLockfileHash(environment: Environment): string {
  const lockfilePath = lookupFile(environment.config.root, lockfilePaths)
  let content = lockfilePath ? fs.readFileSync(lockfilePath, 'utf-8') : ''
  if (lockfilePath) {
    const normalizedLockfilePath = lockfilePath.replaceAll('\\', '/')
    const lockfileFormat = lockfileFormats.find((f) =>
      normalizedLockfilePath.endsWith(f.path),
    )!
    if (lockfileFormat.checkPatchesDir) {
      // Default of https://github.com/ds300/patch-package
      const baseDir = lockfilePath.slice(0, -lockfileFormat.path.length)
      const fullPath = path.join(
        baseDir,
        lockfileFormat.checkPatchesDir as string,
      )
      const stat = tryStatSync(fullPath)
      if (stat?.isDirectory()) {
        content += stat.mtimeMs.toString()
      }
    }
  }
  return getHash(content)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getLockfileHash(root: string): string {
  const lockfilePath =
    lookupFile(root, lockfilePaths) ?? lookupFile(root, fallbackLockfilePaths)
  let content = lockfilePath ? fs.readFileSync(lockfilePath, 'utf-8') : ''
  if (lockfilePath) {
    const normalizedLockfilePath = lockfilePath.replaceAll('\\', '/')
    const lockfileFormat = [
      ...lockfileFormats,
      ...fallbackLockfileFormats,
    ].find((f) => normalizedLockfilePath.endsWith(f.path))!
    if (lockfileFormat.checkPatchesDir) {
      // Default of https://github.com/ds300/patch-package
      const baseDir = lockfilePath.slice(0, -lockfileFormat.path.length)
      const fullPath = path.join(
        baseDir,
        lockfileFormat.checkPatchesDir as string,
      )
      const stat = tryStatSync(fullPath)
      if (stat?.isDirectory()) {
        content += stat.mtimeMs.toString()
      }
    }
  }
  return getHash(content)
}
```

### 🔹 函式: `loadCachedDepOptimizationMetadata()`
- **變更前簽章 (Before)**: `async function loadCachedDepOptimizationMetadata(
  environment: Environment,
  force: boolean = environment.config.optimizeDeps.force ?? false,
  asCommand = false,
): Promise<DepOptimizationMetadata | undefined>` (L384~L455)
- **變更後簽章 (After)**: `async function loadCachedDepOptimizationMetadata(
  environment: Environment,
  force: boolean = environment.config.optimizeDeps.force ?? false,
  asCommand = false,
): Promise<DepOptimizationMetadata | undefined>` (L384~L457)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function loadCachedDepOptimizationMetadata(
  environment: Environment,
  force: boolean = environment.config.optimizeDeps.force ?? false,
  asCommand = false,
): Promise<DepOptimizationMetadata | undefined> {
  const log = asCommand ? environment.logger.info : debug

  if (firstLoadCachedDepOptimizationMetadata) {
    firstLoadCachedDepOptimizationMetadata = false
    // Fire up a clean up of stale processing deps dirs if older process exited early
    setTimeout(
      () => cleanupDepsCacheStaleDirs(environment.getTopLevelConfig()),
      0,
    ).unref()
  }

  const depsCacheDir = getDepsCacheDir(environment)

  // When run inside Vite Task, the dep optimizer cache is both read and
  // written under this directory (metadata + pre-bundled deps). Tell Vite
  // Task to treat it as neither a build input nor a build output: the
  // lockfile hash stored in the metadata already drives re-optimization,
  // and the cache is process-local scratch space, not a build artifact.
  ignoreInput(depsCacheDir)
  ignoreOutput(depsCacheDir)

  if (!force) {
    let cachedMetadata: DepOptimizationMetadata | undefined
    try {
      const cachedMetadataPath = path.join(depsCacheDir, METADATA_FILENAME)
      cachedMetadata = parseDepsOptimizerMetadata(
        await fsp.readFile(cachedMetadataPath, 'utf-8'),
        depsCacheDir,
      )
    } catch {}
    // hash is consistent, no need to re-bundle
    if (cachedMetadata) {
      if (cachedMetadata.lockfileHash !== getLockfileHash(environment)) {
        environment.logger.info(
          'Re-optimizing dependencies because lockfile has changed',
          {
            timestamp: true,
          },
        )
      } else if (cachedMetadata.configHash !== getConfigHash(environment)) {
        environment.logger.info(
          'Re-optimizing dependencies because vite config has changed',
          {
            timestamp: true,
          },
        )
      } else {
        log?.(
          `(${environment.name}) Hash is consistent. Skipping. Use --force to override.`,
        )
        // Nothing to commit or cancel as we are using the cache, we only
        // need to resolve the processing promise so requests can move on
        return cachedMetadata
      }
    }
  } else {
    environment.logger.info('Forced re-optimization of dependencies', {
      timestamp: true,
    })
  }

  // Start with a fresh cache
  debug?.(
    `(${environment.name}) ${colors.green(`removing old cache dir ${depsCacheDir}`)}`,
  )
  await fsp.rm(depsCacheDir, { recursive: true, force: true })
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function loadCachedDepOptimizationMetadata(
  environment: Environment,
  force: boolean = environment.config.optimizeDeps.force ?? false,
  asCommand = false,
): Promise<DepOptimizationMetadata | undefined> {
  const log = asCommand ? environment.logger.info : debug

  if (firstLoadCachedDepOptimizationMetadata) {
    firstLoadCachedDepOptimizationMetadata = false
    // Fire up a clean up of stale processing deps dirs if older process exited early
    setTimeout(
      () => cleanupDepsCacheStaleDirs(environment.getTopLevelConfig()),
      0,
    ).unref()
  }

  const depsCacheDir = getDepsCacheDir(environment)

  // When run inside Vite Task, the dep optimizer cache is both read and
  // written under this directory (metadata + pre-bundled deps). Tell Vite
  // Task to treat it as neither a build input nor a build output: the
  // lockfile hash stored in the metadata already drives re-optimization,
  // and the cache is process-local scratch space, not a build artifact.
  ignoreInput(depsCacheDir)
  ignoreOutput(depsCacheDir)

  if (!force) {
    let cachedMetadata: DepOptimizationMetadata | undefined
    try {
      const cachedMetadataPath = path.join(depsCacheDir, METADATA_FILENAME)
      cachedMetadata = parseDepsOptimizerMetadata(
        await fsp.readFile(cachedMetadataPath, 'utf-8'),
        depsCacheDir,
      )
    } catch {}
    // hash is consistent, no need to re-bundle
    if (cachedMetadata) {
      if (
        cachedMetadata.lockfileHash !== getLockfileHash(environment.config.root)
      ) {
        environment.logger.info(
          'Re-optimizing dependencies because lockfile has changed',
          {
            timestamp: true,
          },
        )
      } else if (cachedMetadata.configHash !== getConfigHash(environment)) {
        environment.logger.info(
          'Re-optimizing dependencies because vite config has changed',
          {
            timestamp: true,
          },
        )
      } else {
        log?.(
          `(${environment.name}) Hash is consistent. Skipping. Use --force to override.`,
        )
        // Nothing to commit or cancel as we are using the cache, we only
        // need to resolve the processing promise so requests can move on
        return cachedMetadata
      }
    }
  } else {
    environment.logger.info('Forced re-optimization of dependencies', {
      timestamp: true,
    })
  }

  // Start with a fresh cache
  debug?.(
    `(${environment.name}) ${colors.green(`removing old cache dir ${depsCacheDir}`)}`,
  )
  await fsp.rm(depsCacheDir, { recursive: true, force: true })
}
```

### 🔹 函式: `getDepHash()`
- **變更前簽章 (Before)**: `function getDepHash(environment: Environment):` (L1371~L1384)
- **變更後簽章 (After)**: `function getDepHash(environment: Environment):` (L1387~L1400)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getDepHash(environment: Environment): {
  lockfileHash: string
  configHash: string
  hash: string
} {
  const lockfileHash = getLockfileHash(environment)
  const configHash = getConfigHash(environment)
  const hash = getHash(lockfileHash + configHash)
  return {
    hash,
    lockfileHash,
    configHash,
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getDepHash(environment: Environment): {
  lockfileHash: string
  configHash: string
  hash: string
} {
  const lockfileHash = getLockfileHash(environment.config.root)
  const configHash = getConfigHash(environment)
  const hash = getHash(lockfileHash + configHash)
  return {
    hash,
    lockfileHash,
    configHash,
  }
}
```


---

### 🔹 Commit #12: `cfe917d6`
- **完整 Hash**: `cfe917d67d279a13f20ae9449e3befa736b64b07`
- **說明 (Ground Truth)**: fix(bundled-dev): ignore build.chunkImportMap (#23685)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/build.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:133, E:110, A:0) ➔ After(N:133, E:110, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resolveBuildEnvironmentOptions()`
- **變更前簽章 (Before)**: `function resolveBuildEnvironmentOptions(
  raw: BuildEnvironmentOptions,
  logger: Logger,
  consumer: 'client' | 'server' | undefined,
  isBundledDev: boolean,
  input?: InputOption,
  isSsrTargetWebworkerEnvironment?: boolean,
): ResolvedBuildEnvironmentOptions` (L432~L524)
- **變更後簽章 (After)**: `function resolveBuildEnvironmentOptions(
  raw: BuildEnvironmentOptions,
  logger: Logger,
  consumer: 'client' | 'server' | undefined,
  isBundledDev: boolean,
  input?: InputOption,
  isSsrTargetWebworkerEnvironment?: boolean,
): ResolvedBuildEnvironmentOptions` (L432~L527)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function resolveBuildEnvironmentOptions(
  raw: BuildEnvironmentOptions,
  logger: Logger,
  consumer: 'client' | 'server' | undefined,
  isBundledDev: boolean,
  input?: InputOption,
  isSsrTargetWebworkerEnvironment?: boolean,
): ResolvedBuildEnvironmentOptions {
  const deprecatedPolyfillModulePreload = raw.polyfillModulePreload
  const { polyfillModulePreload, ...rest } = raw
  raw = rest
  if (deprecatedPolyfillModulePreload !== undefined) {
    logger.warn(
      'polyfillModulePreload is deprecated. Use modulePreload.polyfill instead.',
    )
  }
  if (
    deprecatedPolyfillModulePreload === false &&
    raw.modulePreload === undefined
  ) {
    raw.modulePreload = { polyfill: false }
  }

  const merged = mergeWithDefaults(
    {
      ..._buildEnvironmentOptionsDefaults,
      cssCodeSplit: !raw.lib,
      minify: consumer === 'server' || isBundledDev ? false : 'oxc',
      rollupOptions: {},
      rolldownOptions: undefined,
      ssr: consumer === 'server',
      emitAssets: consumer === 'client',
      createEnvironment: (name, config) => new BuildEnvironment(name, config),
    } satisfies BuildEnvironmentOptions,
    raw,
  )
  setupRollupOptionCompat(merged, 'build')
  merged.rolldownOptions = {
    platform:
      consumer === 'client' || isSsrTargetWebworkerEnvironment
        ? 'browser'
        : 'node',
    ...merged.rolldownOptions,
  }
  if (merged.lib && merged.lib.entry == null && input != null) {
    // avoid mutating the user-provided lib options object
    merged.lib = { ...merged.lib, entry: input }
  }

  // handle special build targets
  if (merged.target === 'baseline-widely-available') {
    merged.target = ESBUILD_BASELINE_WIDELY_AVAILABLE_TARGET
  }
  // dedupe target
  if (Array.isArray(merged.target)) {
    // esbuild allowed duplicate targets but oxc does not
    merged.target = unique(merged.target)
  }

  // normalize false string into actual false
  if ((merged.minify as string) === 'false') {
    merged.minify = false
  } else if (merged.minify === true) {
    merged.minify = 'oxc'
  }

  const defaultModulePreload = {
    polyfill: true,
  }

  const resolved: ResolvedBuildEnvironmentOptions = {
    ...merged,
    cssTarget: merged.cssTarget ?? merged.target,
    cssMinify:
      merged.cssMinify ??
      (consumer === 'server' ? 'lightningcss' : !!merged.minify),
    // Resolve to false | object
    modulePreload:
      merged.modulePreload === false
        ? false
        : merged.modulePreload === true
          ? defaultModulePreload
          : {
              ...defaultModulePreload,
              ...merged.modulePreload,
            },
  }
  // The object spread above evaluates the `rollupOptions` getter set up on
  // `merged` and copies it as a plain data property.
  setupRollupOptionCompat(resolved, 'build')

  return resolved
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function resolveBuildEnvironmentOptions(
  raw: BuildEnvironmentOptions,
  logger: Logger,
  consumer: 'client' | 'server' | undefined,
  isBundledDev: boolean,
  input?: InputOption,
  isSsrTargetWebworkerEnvironment?: boolean,
): ResolvedBuildEnvironmentOptions {
  const deprecatedPolyfillModulePreload = raw.polyfillModulePreload
  const { polyfillModulePreload, ...rest } = raw
  raw = rest
  if (deprecatedPolyfillModulePreload !== undefined) {
    logger.warn(
      'polyfillModulePreload is deprecated. Use modulePreload.polyfill instead.',
    )
  }
  if (
    deprecatedPolyfillModulePreload === false &&
    raw.modulePreload === undefined
  ) {
    raw.modulePreload = { polyfill: false }
  }

  const merged = mergeWithDefaults(
    {
      ..._buildEnvironmentOptionsDefaults,
      cssCodeSplit: !raw.lib,
      minify: consumer === 'server' || isBundledDev ? false : 'oxc',
      rollupOptions: {},
      rolldownOptions: undefined,
      ssr: consumer === 'server',
      emitAssets: consumer === 'client',
      createEnvironment: (name, config) => new BuildEnvironment(name, config),
    } satisfies BuildEnvironmentOptions,
    raw,
  )
  setupRollupOptionCompat(merged, 'build')
  if (isBundledDev) {
    merged.chunkImportMap = false
  }
  merged.rolldownOptions = {
    platform:
      consumer === 'client' || isSsrTargetWebworkerEnvironment
        ? 'browser'
        : 'node',
    ...merged.rolldownOptions,
  }
  if (merged.lib && merged.lib.entry == null && input != null) {
    // avoid mutating the user-provided lib options object
    merged.lib = { ...merged.lib, entry: input }
  }

  // handle special build targets
  if (merged.target === 'baseline-widely-available') {
    merged.target = ESBUILD_BASELINE_WIDELY_AVAILABLE_TARGET
  }
  // dedupe target
  if (Array.isArray(merged.target)) {
    // esbuild allowed duplicate targets but oxc does not
    merged.target = unique(merged.target)
  }

  // normalize false string into actual false
  if ((merged.minify as string) === 'false') {
    merged.minify = false
  } else if (merged.minify === true) {
    merged.minify = 'oxc'
  }

  const defaultModulePreload = {
    polyfill: true,
  }

  const resolved: ResolvedBuildEnvironmentOptions = {
    ...merged,
    cssTarget: merged.cssTarget ?? merged.target,
    cssMinify:
      merged.cssMinify ??
      (consumer === 'server' ? 'lightningcss' : !!merged.minify),
    // Resolve to false | object
    modulePreload:
      merged.modulePreload === false
        ? false
        : merged.modulePreload === true
          ? defaultModulePreload
          : {
              ...defaultModulePreload,
              ...merged.modulePreload,
            },
  }
  // The object spread above evaluates the `rollupOptions` getter set up on
  // `merged` and copies it as a plain data property.
  setupRollupOptionCompat(resolved, 'build')

  return resolved
}
```


---

### 🔹 Commit #13: `df4e02cc`
- **完整 Hash**: `df4e02cc8317a62f21edefc79a9690571ffed1f3`
- **說明 (Ground Truth)**: fix(bundled-dev): normalize served output files (#23684)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/server/bundledDev.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:44, E:22, A:0) ➔ After(N:45, E:23, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `normalizePath (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `storeOutputFiles` ──[CALLS [guarded]]──> `normalizePath (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `storeOutputFiles()`
- **變更前簽章 (Before)**: `storeOutputFiles(output: RolldownOutput['output'][number][])` (L407~L419)
- **變更後簽章 (After)**: `storeOutputFiles(output: RolldownOutput['output'][number][])` (L411~L423)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private storeOutputFiles(output: RolldownOutput['output'][number][]): void {
    // NOTE: don't clear memoryFiles here as incremental build reuses the files
    for (const outputFile of output) {
      this.memoryFiles.set(outputFile.fileName, () => {
        const source =
          outputFile.type === 'chunk' ? outputFile.code : outputFile.source
        return {
          source,
          etag: getEtag(Buffer.from(source), { weak: true }),
        }
      })
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private storeOutputFiles(output: RolldownOutput['output'][number][]): void {
    // NOTE: don't clear memoryFiles here as incremental build reuses the files
    for (const outputFile of output) {
      this.memoryFiles.set(normalizePath(outputFile.fileName), () => {
        const source =
          outputFile.type === 'chunk' ? outputFile.code : outputFile.source
        return {
          source,
          etag: getEtag(Buffer.from(source), { weak: true }),
        }
      })
    }
  }
```


---

### 🔹 Commit #14: `52ba8776`
- **完整 Hash**: `52ba877693c8633458d163117504a8259beb3cf5`
- **說明 (Ground Truth)**: fix(bundled-dev): apply `server.origin` to asset URLs (#23683)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/plugins/asset.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:61, E:62, A:0) ➔ After(N:61, E:63, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `toOutputFilePathInJSForBundledDev` ──[CALLS [guard: (typeof outputUrl === 'object')]]──> `joinUrlSegments (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `publicFileToBuiltUrl()`
- **變更前簽章 (Before)**: `function publicFileToBuiltUrl(
  url: string,
  config: ResolvedConfig,
): string` (L519~L537)
- **變更後簽章 (After)**: `function publicFileToBuiltUrl(
  url: string,
  config: ResolvedConfig,
): string` (L519~L538)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function publicFileToBuiltUrl(
  url: string,
  config: ResolvedConfig,
): string {
  if (config.command !== 'build') {
    // We don't need relative base or renderBuiltUrl support during dev
    return joinUrlSegments(config.decodedBase, url)
  }
  const hash = getHash(url)
  let cache = publicAssetUrlCache.get(config)
  if (!cache) {
    cache = new Map<string, string>()
    publicAssetUrlCache.set(config, cache)
  }
  if (!cache.get(hash)) {
    cache.set(hash, url)
  }
  return `__VITE_PUBLIC_ASSET__${hash}__`
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function publicFileToBuiltUrl(
  url: string,
  config: ResolvedConfig,
): string {
  if (config.command !== 'build') {
    // We don't need relative base or renderBuiltUrl support during dev
    const base = joinUrlSegments(config.server.origin ?? '', config.decodedBase)
    return joinUrlSegments(base, url)
  }
  const hash = getHash(url)
  let cache = publicAssetUrlCache.get(config)
  if (!cache) {
    cache = new Map<string, string>()
    publicAssetUrlCache.set(config, cache)
  }
  if (!cache.get(hash)) {
    cache.set(hash, url)
  }
  return `__VITE_PUBLIC_ASSET__${hash}__`
}
```

### 🔹 函式: `toOutputFilePathInJSForBundledDev()`
- **變更前簽章 (Before)**: `function toOutputFilePathInJSForBundledDev(
  environment: PartialEnvironment,
  filename: string,
): string` (L714~L733)
- **變更後簽章 (After)**: `function toOutputFilePathInJSForBundledDev(
  environment: PartialEnvironment,
  filename: string,
): string` (L715~L737)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function toOutputFilePathInJSForBundledDev(
  environment: PartialEnvironment,
  filename: string,
): string {
  const outputUrl = toOutputFilePathInJS(
    environment,
    filename,
    'asset',
    // in bundled dev, the chunks are always emitted to `assets` directory
    'assets/dummy.js',
    'js',
    // relative base is not supported in bundled dev
    () => {
      throw new Error('unreachable')
    },
  )
  // renderBuiltUrl is not supported in bundled dev
  if (typeof outputUrl === 'object') throw new Error('unreachable')
  return outputUrl
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function toOutputFilePathInJSForBundledDev(
  environment: PartialEnvironment,
  filename: string,
): string {
  const outputUrl = toOutputFilePathInJS(
    environment,
    filename,
    'asset',
    // in bundled dev, the chunks are always emitted to `assets` directory
    'assets/dummy.js',
    'js',
    // relative base is not supported in bundled dev
    () => {
      throw new Error('unreachable')
    },
  )
  // renderBuiltUrl is not supported in bundled dev
  if (typeof outputUrl === 'object') throw new Error('unreachable')
  return joinUrlSegments(
    environment.getTopLevelConfig().server.origin ?? '',
    outputUrl,
  )
}
```


---

### 🔹 Commit #15: `3dfde87b`
- **完整 Hash**: `3dfde87b90a9f80b125d710e3e5d4fc795662db6`
- **說明 (Ground Truth)**: fix(server): only strip base when path matches a full segment (#23641)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/server/middlewares/base.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:6, E:5, A:0) ➔ After(N:6, E:5, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `baseMiddleware()`
- **變更前簽章 (Before)**: `function baseMiddleware(
  rawBase: string,
  middlewareMode: boolean,
): Connect.NextHandleFunction` (L7~L62)
- **變更後簽章 (After)**: `function baseMiddleware(
  rawBase: string,
  middlewareMode: boolean,
): Connect.NextHandleFunction` (L7~L62)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function baseMiddleware(
  rawBase: string,
  middlewareMode: boolean,
): Connect.NextHandleFunction {
  // Keep the named function. The name is visible in debug logs via `DEBUG=connect:dispatcher ...`
  return function viteBaseMiddleware(req, res, next) {
    const url = req.url!
    const pathname = cleanUrl(url)
    const base = rawBase

    if (pathname.startsWith(base)) {
      // rewrite url to remove base. this ensures that other middleware does
      // not need to consider base being prepended or not
      req.url = stripBase(url, base)
      return next()
    }

    // skip redirect and error fallback on middleware mode, #4057
    if (middlewareMode) {
      return next()
    }

    if (pathname === '/' || pathname === '/index.html') {
      // redirect root visit to based url with search and hash
      res.writeHead(302, {
        Location: base + url.slice(pathname.length),
      })
      res.end()
      return
    }

    // non-based page visit
    const redirectPath =
      withTrailingSlash(url) !== base ? joinUrlSegments(base, url) : base
    if (req.headers.accept?.includes('text/html')) {
      res.writeHead(404, {
        'Content-Type': 'text/html',
      })
      res.end(
        `The server is configured with a public base URL of ${base} - ` +
          `did you mean to visit <a href="${redirectPath}">${redirectPath}</a> instead?`,
      )
      return
    } else {
      // not found for resources
      res.writeHead(404, {
        'Content-Type': 'text/plain',
      })
      res.end(
        `The server is configured with a public base URL of ${base} - ` +
          `did you mean to visit ${redirectPath} instead?`,
      )
      return
    }
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function baseMiddleware(
  rawBase: string,
  middlewareMode: boolean,
): Connect.NextHandleFunction {
  // Keep the named function. The name is visible in debug logs via `DEBUG=connect:dispatcher ...`
  return function viteBaseMiddleware(req, res, next) {
    const url = req.url!
    const pathname = cleanUrl(url)
    const base = rawBase

    if (pathname === base || pathname.startsWith(withTrailingSlash(base))) {
      // rewrite url to remove base. this ensures that other middleware does
      // not need to consider base being prepended or not
      req.url = stripBase(url, base)
      return next()
    }

    // skip redirect and error fallback on middleware mode, #4057
    if (middlewareMode) {
      return next()
    }

    if (pathname === '/' || pathname === '/index.html') {
      // redirect root visit to based url with search and hash
      res.writeHead(302, {
        Location: base + url.slice(pathname.length),
      })
      res.end()
      return
    }

    // non-based page visit
    const redirectPath =
      withTrailingSlash(url) !== base ? joinUrlSegments(base, url) : base
    if (req.headers.accept?.includes('text/html')) {
      res.writeHead(404, {
        'Content-Type': 'text/html',
      })
      res.end(
        `The server is configured with a public base URL of ${base} - ` +
          `did you mean to visit <a href="${redirectPath}">${redirectPath}</a> instead?`,
      )
      return
    } else {
      // not found for resources
      res.writeHead(404, {
        'Content-Type': 'text/plain',
      })
      res.end(
        `The server is configured with a public base URL of ${base} - ` +
          `did you mean to visit ${redirectPath} instead?`,
      )
      return
    }
  }
}
```


---

### 🔹 Commit #16: `b28db28e`
- **完整 Hash**: `b28db28e9e62d9866a9a0f1b22e74589cc180577`
- **說明 (Ground Truth)**: fix(server): match static aliases on path boundaries (#23643)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/server/middlewares/static.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:40, E:42, A:0) ➔ After(N:41, E:43, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🔴 BLOCKED_BY_INVARIANTS` (通過: `False`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `applyStaticAlias` (FUNCTION_DEF)
  • + [新增呼叫邊] `serveStaticMiddleware` ──[CALLS [guard: (
      cleanedUrl.endsWith('/') ||
      path.extname(cleanedUrl) === '.html' ||
      isInternalRequest(req.url!) ||
      // skip url starting with // as these will be interpreted as
      // scheme relative URLs by new URL() and will not be a valid file path
      req.url?.startsWith('//')
    )]]──> `applyStaticAlias`

❌ **本次 Commit 新引入之作用域死穴 (New Scope Traps):**
  - 💥 作用域阻隔: 函式 'getHeaders' 被深鎖在內部閉包 (scope:servePublicMiddleware@after/packages/vite/src/node/server/middlewares/static.ts:L81C8)，外部無法調用！

**最終驗收裁決: 🔴 BLOCKED_BY_INVARIANTS**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `serveStaticMiddleware()`
- **變更前簽章 (Before)**: `function serveStaticMiddleware(
  server: ViteDevServer,
): Connect.NextHandleFunction` (L124~L199)
- **變更後簽章 (After)**: `function serveStaticMiddleware(
  server: ViteDevServer,
): Connect.NextHandleFunction` (L125~L193)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function serveStaticMiddleware(
  server: ViteDevServer,
): Connect.NextHandleFunction {
  const dir = server.config.root
  const serve = sirv(
    dir,
    sirvOptions({
      config: server.config,
      getHeaders: () => server.config.server.headers,
    }),
  )

  // Keep the named function. The name is visible in debug logs via `DEBUG=connect:dispatcher ...`
  return function viteServeStaticMiddleware(req, res, next) {
    // only serve the file if it's not an html request or ends with `/`
    // so that html requests can fallthrough to our html middleware for
    // special processing
    // also skip internal requests `/@fs/ /@vite-client` etc...
    const cleanedUrl = cleanUrl(req.url!)
    if (
      cleanedUrl.endsWith('/') ||
      path.extname(cleanedUrl) === '.html' ||
      isInternalRequest(req.url!) ||
      // skip url starting with // as these will be interpreted as
      // scheme relative URLs by new URL() and will not be a valid file path
      req.url?.startsWith('//')
    ) {
      return next()
    }

    const url = new URL(req.url!, 'http://example.com')
    const pathname = decodeURIIfPossible(url.pathname)
    if (pathname === undefined) {
      return next()
    }

    // apply aliases to static requests as well
    let redirectedPathname: string | undefined
    for (const { find, replacement } of server.config.resolve.alias) {
      const matches =
        typeof find === 'string'
          ? pathname.startsWith(find)
          : find.test(pathname)
      if (matches) {
        redirectedPathname = pathname.replace(find, replacement)
        break
      }
    }
    if (redirectedPathname) {
      // dir is pre-normalized to posix style
      if (redirectedPathname.startsWith(withTrailingSlash(dir))) {
        redirectedPathname = redirectedPathname.slice(dir.length)
      }
    }

    const resolvedPathname = redirectedPathname || pathname
    let fileUrl = path.resolve(dir, removeLeadingSlash(resolvedPathname))
    if (resolvedPathname.endsWith('/') && fileUrl.at(-1) !== '/') {
      fileUrl = withTrailingSlash(fileUrl)
    }
    if (redirectedPathname) {
      url.pathname = encodeURI(redirectedPathname)
      req.url = url.href.slice(url.origin.length)
    }

    try {
      serve(req, res, next)
    } catch (e) {
      if (e && 'code' in e && e.code === ERR_DENIED_FILE) {
        respondWithAccessDenied(e.path, server, res)
        return
      }
      throw e
    }
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function serveStaticMiddleware(
  server: ViteDevServer,
): Connect.NextHandleFunction {
  const dir = server.config.root
  const serve = sirv(
    dir,
    sirvOptions({
      config: server.config,
      getHeaders: () => server.config.server.headers,
    }),
  )

  // Keep the named function. The name is visible in debug logs via `DEBUG=connect:dispatcher ...`
  return function viteServeStaticMiddleware(req, res, next) {
    // only serve the file if it's not an html request or ends with `/`
    // so that html requests can fallthrough to our html middleware for
    // special processing
    // also skip internal requests `/@fs/ /@vite-client` etc...
    const cleanedUrl = cleanUrl(req.url!)
    if (
      cleanedUrl.endsWith('/') ||
      path.extname(cleanedUrl) === '.html' ||
      isInternalRequest(req.url!) ||
      // skip url starting with // as these will be interpreted as
      // scheme relative URLs by new URL() and will not be a valid file path
      req.url?.startsWith('//')
    ) {
      return next()
    }

    const url = new URL(req.url!, 'http://example.com')
    const pathname = decodeURIIfPossible(url.pathname)
    if (pathname === undefined) {
      return next()
    }

    // apply aliases to static requests as well
    let redirectedPathname = applyStaticAlias(
      pathname,
      server.config.resolve.alias,
    )
    if (redirectedPathname) {
      // dir is pre-normalized to posix style
      if (redirectedPathname.startsWith(withTrailingSlash(dir))) {
        redirectedPathname = redirectedPathname.slice(dir.length)
      }
    }

    const resolvedPathname = redirectedPathname || pathname
    let fileUrl = path.resolve(dir, removeLeadingSlash(resolvedPathname))
    if (resolvedPathname.endsWith('/') && fileUrl.at(-1) !== '/') {
      fileUrl = withTrailingSlash(fileUrl)
    }
    if (redirectedPathname) {
      url.pathname = encodeURI(redirectedPathname)
      req.url = url.href.slice(url.origin.length)
    }

    try {
      serve(req, res, next)
    } catch (e) {
      if (e && 'code' in e && e.code === ERR_DENIED_FILE) {
        respondWithAccessDenied(e.path, server, res)
        return
      }
      throw e
    }
  }
}
```


---

### 🔹 Commit #17: `bc0f21c5`
- **完整 Hash**: `bc0f21c56a2e003a4d2dd23ccb9da3ec8c706c4e`
- **說明 (Ground Truth)**: feat(bundled-dev): support `import.meta.hot.acceptExports` (#23463)
- **變更檔案數**: 4

#### 📄 檔案: `packages/vite/src/client/bundledDevClient.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:11, E:0, A:0) ➔ After(N:11, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `bundledDevHmrClient()`
- **變更前簽章 (Before)**: `[Module State] bundledDevHmrClient` (L49~L60)
- **變更後簽章 (After)**: `[Module State] bundledDevHmrClient` (L51~L63)

#### ◀️ 變更前實作碼 (Before Implementation):
```
bundledDevHmrClient = new BundledDevHMRClient(
    {
      error: (err) => console.error('[vite]', err),
      debug: (...msg) => console.debug('[vite]', ...msg),
    },
    transport,
    runtime,
    {
      base,
      beforeApply: clearOverlayOrReloadOnFirstUpdate,
    },
  )
```

#### ▶️ 變更後實作碼 (After Implementation):
```
bundledDevHmrClient = new BundledDevHMRClient(
    {
      error: (err) => console.error('[vite]', err),
      debug: (...msg) => console.debug('[vite]', ...msg),
    },
    transport,
    runtime,
    {
      base,
      partialAccept: __HMR_PARTIAL_ACCEPT__,
      beforeApply: clearOverlayOrReloadOnFirstUpdate,
    },
  )
```


#### 📄 檔案: `packages/vite/src/client/bundledDevHmrClient.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:22, E:2, A:0) ➔ After(N:25, E:2, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `acceptsAllExports` (FUNCTION_DEF)
  • + [新增節點] `getAcceptedExports` (FUNCTION_DEF)
  • + [新增節點] `importsOnlyAccepted` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `acceptsDep()`
- **變更前簽章 (Before)**: `acceptsDep(parent: string, id: string)` (L65~L71)
- **變更後簽章 (After)**: `acceptsDep(parent: string, id: string)` (L64~L70)

#### ◀️ 變更前實作碼 (Before Implementation):
```
acceptsDep(parent: string, id: string): boolean {
    return (
      this.hotModulesMap
        .get(parent)
        ?.callbacks.some((c) => c.deps.includes(id)) ?? false
    )
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
acceptsDep(parent: string, id: string): boolean {
    return (
      this.hotModulesMap
        .get(parent)
        ?.callbacks.some((c) => !c.exports && c.deps.includes(id)) ?? false
    )
  }
```

### 🔹 函式: `bubble()`
- **變更前簽章 (Before)**: `bubble(
    id: string,
    stack: string[],
    updateSet: Set<string>,
    boundaries: PropagationBoundary[],
    firstInvalidatedBy: string | undefined,
    traversedModules: Set<string>,
  )` (L99~L158)
- **變更後簽章 (After)**: `bubble(
    id: string,
    stack: string[],
    updateSet: Set<string>,
    boundaries: PropagationBoundary[],
    firstInvalidatedBy: string | undefined,
    traversedModules: Set<string>,
  )` (L127~L197)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private bubble(
    id: string,
    stack: string[],
    updateSet: Set<string>,
    boundaries: PropagationBoundary[],
    firstInvalidatedBy: string | undefined,
    traversedModules: Set<string>,
  ): HmrUpdate | undefined {
    if (traversedModules.has(id)) return
    traversedModules.add(id)
    updateSet.add(id)
    if (firstInvalidatedBy !== undefined && id === firstInvalidatedBy) {
      return {
        type: 'full-reload',
        reason: `update propagated back to ${firstInvalidatedBy}, which already called \`import.meta.hot.invalidate()\``,
      }
    }
    if (this.isSelfAccepted(id)) {
      boundaries.push({
        boundary: id,
        acceptedVia: id,
        isWithinCircularImport: this.isNodeWithinCircularImports(id, stack),
      })
      return
    }
    const parents = this.runtime
      .getImporters(id)
      .filter((p) => this.runtime.isExecuted(p))
    if (!parents.length) {
      return {
        type: 'full-reload',
        reason: `no hmr boundary found for module \`${id}\``,
      }
    }
    for (const parent of parents) {
      const subChain = [...stack, parent]
      if (this.acceptsDep(parent, id)) {
        boundaries.push({
          boundary: parent,
          acceptedVia: id,
          isWithinCircularImport: this.isNodeWithinCircularImports(
            parent,
            subChain,
          ),
        })
        continue
      }
      if (!stack.includes(parent)) {
        const fullReload = this.bubble(
          parent,
          subChain,
          updateSet,
          boundaries,
          firstInvalidatedBy,
          traversedModules,
        )
        if (fullReload) return fullReload
      }
    }
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private bubble(
    id: string,
    stack: string[],
    updateSet: Set<string>,
    boundaries: PropagationBoundary[],
    firstInvalidatedBy: string | undefined,
    traversedModules: Set<string>,
  ): HmrUpdate | undefined {
    if (traversedModules.has(id)) return
    traversedModules.add(id)
    updateSet.add(id)
    if (firstInvalidatedBy !== undefined && id === firstInvalidatedBy) {
      return {
        type: 'full-reload',
        reason: `update propagated back to ${firstInvalidatedBy}, which already called \`import.meta.hot.invalidate()\``,
      }
    }
    const acceptedExports = this.getAcceptedExports(id)
    const selfAccepted =
      this.isSelfAccepted(id) ||
      (acceptedExports !== undefined &&
        this.acceptsAllExports(id, acceptedExports))
    if (selfAccepted || acceptedExports) {
      boundaries.push({
        boundary: id,
        acceptedVia: id,
        isWithinCircularImport: this.isNodeWithinCircularImports(id, stack),
      })
      if (selfAccepted) return
    }
    const parents = this.runtime
      .getImporters(id)
      .filter((p) => this.runtime.isExecuted(p))
    if (!acceptedExports && !parents.length) {
      return {
        type: 'full-reload',
        reason: `no hmr boundary found for module \`${id}\``,
      }
    }
    for (const parent of parents) {
      const subChain = [...stack, parent]
      if (this.acceptsDep(parent, id)) {
        boundaries.push({
          boundary: parent,
          acceptedVia: id,
          isWithinCircularImport: this.isNodeWithinCircularImports(
            parent,
            subChain,
          ),
        })
        continue
      }
      if (
        acceptedExports &&
        this.importsOnlyAccepted(parent, id, acceptedExports)
      ) {
        continue
      }
      if (!stack.includes(parent)) {
        const fullReload = this.bubble(
          parent,
          subChain,
          updateSet,
          boundaries,
          firstInvalidatedBy,
          traversedModules,
        )
        if (fullReload) return fullReload
      }
    }
  }
```

### 🔹 函式: `isSelfAccepted()`
- **變更前簽章 (Before)**: `isSelfAccepted(id: string)` (L58~L63)
- **變更後簽章 (After)**: `isSelfAccepted(id: string)` (L60~L62)

#### ◀️ 變更前實作碼 (Before Implementation):
```
isSelfAccepted(id: string): boolean {
    return (
      this.hotModulesMap.get(id)?.callbacks.some((c) => c.deps.includes(id)) ??
      false
    )
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
isSelfAccepted(id: string): boolean {
    return this.acceptsDep(id, id)
  }
```


#### 📄 檔案: `packages/vite/src/node/plugins/clientInjections.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:33, E:19, A:0) ➔ After(N:33, E:19, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createClientConfigValueReplacer()`
- **變更前簽章 (Before)**: `async function createClientConfigValueReplacer(
  config: ResolvedConfig,
): Promise<(code: string) => string>` (L82~L149)
- **變更後簽章 (After)**: `async function createClientConfigValueReplacer(
  config: ResolvedConfig,
): Promise<(code: string) => string>` (L82~L153)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async function createClientConfigValueReplacer(
  config: ResolvedConfig,
): Promise<(code: string) => string> {
  const resolvedServerHostname = (await resolveHostname(config.server.host))
    .name
  const resolvedServerPort = config.server.port!
  const devBase = config.base

  const serverHost = `${resolvedServerHostname}:${resolvedServerPort}${devBase}`

  const wsConfig = isObject(config.server.ws) ? config.server.ws : undefined
  const host = wsConfig?.host || null
  const protocol = wsConfig?.protocol || null
  const timeout = wsConfig?.timeout || 30000
  const isWsServerSpecified = !!wsConfig?.server
  const hmrConfigName = path.basename(config.configFile || 'vite.config.js')

  const hmrConfig = isObject(config.server.hmr) ? config.server.hmr : undefined
  const overlay = hmrConfig?.overlay !== false

  // ws.clientPort -> ws.port
  // -> (24678 if middleware mode and WS server is not specified) -> new URL(import.meta.url).port
  let port = wsConfig?.clientPort || wsConfig?.port || null
  if (config.server.middlewareMode && !isWsServerSpecified) {
    port ||= 24678
  }

  let directTarget = wsConfig?.host || resolvedServerHostname
  directTarget += `:${wsConfig?.port || resolvedServerPort}`
  directTarget += devBase

  let hmrBase = devBase
  if (wsConfig?.path) {
    hmrBase = path.posix.join(hmrBase, wsConfig.path)
  }

  const modeReplacement = escapeReplacement(config.mode)
  const baseReplacement = escapeReplacement(devBase)
  const serverHostReplacement = escapeReplacement(serverHost)
  const hmrProtocolReplacement = escapeReplacement(protocol)
  const hmrHostnameReplacement = escapeReplacement(host)
  const hmrPortReplacement = escapeReplacement(port)
  const hmrDirectTargetReplacement = escapeReplacement(directTarget)
  const hmrBaseReplacement = escapeReplacement(hmrBase)
  const hmrTimeoutReplacement = escapeReplacement(timeout)
  const hmrEnableOverlayReplacement = escapeReplacement(overlay)
  const hmrConfigNameReplacement = escapeReplacement(hmrConfigName)
  const wsTokenReplacement = escapeReplacement(config.webSocketToken)
  const serverForwardConsoleReplacement = escapeReplacement(
    config.server.forwardConsole as any,
  )

  return (code) =>
    code
      .replace(`__MODE__`, modeReplacement)
      .replace(/__BASE__/g, baseReplacement)
      .replace(`__SERVER_HOST__`, serverHostReplacement)
      .replace(`__HMR_PROTOCOL__`, hmrProtocolReplacement)
      .replace(`__HMR_HOSTNAME__`, hmrHostnameReplacement)
      .replace(`__HMR_PORT__`, hmrPortReplacement)
      .replace(`__HMR_DIRECT_TARGET__`, hmrDirectTargetReplacement)
      .replace(`__HMR_BASE__`, hmrBaseReplacement)
      .replace(`__HMR_TIMEOUT__`, hmrTimeoutReplacement)
      .replace(`__HMR_ENABLE_OVERLAY__`, hmrEnableOverlayReplacement)
      .replace(`__HMR_CONFIG_NAME__`, hmrConfigNameReplacement)
      .replace(`__WS_TOKEN__`, wsTokenReplacement)
      .replace(`__SERVER_FORWARD_CONSOLE__`, serverForwardConsoleReplacement)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async function createClientConfigValueReplacer(
  config: ResolvedConfig,
): Promise<(code: string) => string> {
  const resolvedServerHostname = (await resolveHostname(config.server.host))
    .name
  const resolvedServerPort = config.server.port!
  const devBase = config.base

  const serverHost = `${resolvedServerHostname}:${resolvedServerPort}${devBase}`

  const wsConfig = isObject(config.server.ws) ? config.server.ws : undefined
  const host = wsConfig?.host || null
  const protocol = wsConfig?.protocol || null
  const timeout = wsConfig?.timeout || 30000
  const isWsServerSpecified = !!wsConfig?.server
  const hmrConfigName = path.basename(config.configFile || 'vite.config.js')

  const hmrConfig = isObject(config.server.hmr) ? config.server.hmr : undefined
  const overlay = hmrConfig?.overlay !== false

  // ws.clientPort -> ws.port
  // -> (24678 if middleware mode and WS server is not specified) -> new URL(import.meta.url).port
  let port = wsConfig?.clientPort || wsConfig?.port || null
  if (config.server.middlewareMode && !isWsServerSpecified) {
    port ||= 24678
  }

  let directTarget = wsConfig?.host || resolvedServerHostname
  directTarget += `:${wsConfig?.port || resolvedServerPort}`
  directTarget += devBase

  let hmrBase = devBase
  if (wsConfig?.path) {
    hmrBase = path.posix.join(hmrBase, wsConfig.path)
  }

  const modeReplacement = escapeReplacement(config.mode)
  const baseReplacement = escapeReplacement(devBase)
  const serverHostReplacement = escapeReplacement(serverHost)
  const hmrProtocolReplacement = escapeReplacement(protocol)
  const hmrHostnameReplacement = escapeReplacement(host)
  const hmrPortReplacement = escapeReplacement(port)
  const hmrDirectTargetReplacement = escapeReplacement(directTarget)
  const hmrBaseReplacement = escapeReplacement(hmrBase)
  const hmrTimeoutReplacement = escapeReplacement(timeout)
  const hmrEnableOverlayReplacement = escapeReplacement(overlay)
  const hmrConfigNameReplacement = escapeReplacement(hmrConfigName)
  const hmrPartialAcceptReplacement = escapeReplacement(
    config.experimental.hmrPartialAccept,
  )
  const wsTokenReplacement = escapeReplacement(config.webSocketToken)
  const serverForwardConsoleReplacement = escapeReplacement(
    config.server.forwardConsole as any,
  )

  return (code) =>
    code
      .replace(`__MODE__`, modeReplacement)
      .replace(/__BASE__/g, baseReplacement)
      .replace(`__SERVER_HOST__`, serverHostReplacement)
      .replace(`__HMR_PROTOCOL__`, hmrProtocolReplacement)
      .replace(`__HMR_HOSTNAME__`, hmrHostnameReplacement)
      .replace(`__HMR_PORT__`, hmrPortReplacement)
      .replace(`__HMR_DIRECT_TARGET__`, hmrDirectTargetReplacement)
      .replace(`__HMR_BASE__`, hmrBaseReplacement)
      .replace(`__HMR_TIMEOUT__`, hmrTimeoutReplacement)
      .replace(`__HMR_ENABLE_OVERLAY__`, hmrEnableOverlayReplacement)
      .replace(`__HMR_CONFIG_NAME__`, hmrConfigNameReplacement)
      .replace(`__HMR_PARTIAL_ACCEPT__`, hmrPartialAcceptReplacement)
      .replace(`__WS_TOKEN__`, wsTokenReplacement)
      .replace(`__SERVER_FORWARD_CONSOLE__`, serverForwardConsoleReplacement)
}
```


#### 📄 檔案: `packages/vite/src/shared/hmr.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:29, E:11, A:0) ➔ After(N:29, E:11, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `acceptDeps()`
- **變更前簽章 (Before)**: `acceptDeps(
    deps: string[],
    callback: HotCallback['fn'] = () => {},
  )` (L154~L167)
- **變更後簽章 (After)**: `acceptDeps(
    deps: string[],
    callback: HotCallback['fn'] = () => {},
    exports?: readonly string[],
  )` (L157~L172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
private acceptDeps(
    deps: string[],
    callback: HotCallback['fn'] = () => {},
  ): void {
    const mod: HotModule = this.hmrClient.hotModulesMap.get(this.ownerPath) || {
      id: this.ownerPath,
      callbacks: [],
    }
    mod.callbacks.push({
      deps,
      fn: callback,
    })
    this.hmrClient.hotModulesMap.set(this.ownerPath, mod)
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
private acceptDeps(
    deps: string[],
    callback: HotCallback['fn'] = () => {},
    exports?: readonly string[],
  ): void {
    const mod: HotModule = this.hmrClient.hotModulesMap.get(this.ownerPath) || {
      id: this.ownerPath,
      callbacks: [],
    }
    mod.callbacks.push({
      deps,
      fn: callback,
      exports,
    })
    this.hmrClient.hotModulesMap.set(this.ownerPath, mod)
  }
```

### 🔹 函式: `acceptExports()`
- **變更前簽章 (Before)**: `acceptExports(
    _: string | readonly string[],
    callback?: (data: any) => void,
  )` (L80~L85)
- **變更後簽章 (After)**: `acceptExports(
    exportNames: string | readonly string[],
    callback?: (data: any) => void,
  )` (L79~L88)

#### ◀️ 變更前實作碼 (Before Implementation):
```
acceptExports(
    _: string | readonly string[],
    callback?: (data: any) => void,
  ): void {
    this.acceptDeps([this.ownerPath], ([mod]) => callback?.(mod))
  }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
acceptExports(
    exportNames: string | readonly string[],
    callback?: (data: any) => void,
  ): void {
    this.acceptDeps(
      [this.ownerPath],
      ([mod]) => callback?.(mod),
      typeof exportNames === 'string' ? [exportNames] : exportNames,
    )
  }
```


---

### 🔹 Commit #18: `fa714693`
- **完整 Hash**: `fa7146938b0ca703653c90c20907191a01c032ba`
- **說明 (Ground Truth)**: fix(client): skip rewriting unchanged adopted styles (#23697)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/client/client.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:86, E:53, A:7) ➔ After(N:86, E:53, A:7)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  🌲 **#document** `(Control)`
    └── ⚡ **on('visibilitychange')**
        └── 🎯 [TRIGGERS] `onVisibilityChange()`
    └── ⚡ **on('visibilitychange')**
        └── 🎯 [TRIGGERS] `onVisibilityChange()`
            └── 🎯 [CALLS] `listener (External/Unresolved)()`
  🌲 **#el** `(Control)`
  🌲 **#newLinkTag** `(Control)`
    └── ⚡ **on('error')**
        └── 🎯 [TRIGGERS] `removeOldEl()`
            └── 🎯 [CALLS] `resolve (External/Unresolved)()`
    └── ⚡ **on('load')**
        └── *ref:`removeOldEl` [已折疊指針]
  🌲 **#self** `(Control)`
    └── ⚡ **on('connect')**
        └── 🎯 [CALLS] `waitForSuccessfulPingInternal()`
            └── 🎯 ⏳ [await] [CALLS] `ping()`
            └── 🎯 ⏳ [await] [CALLS] `wait()`
            └── 🎯 ⏳ [await] [CALLS] `waitForWindowShow()`
  🌲 **#sharedWorker.port** `(Control)`
    └── ⚡ **on('message')**
        └── 🎯 [CALLS] `reject (External/Unresolved)()`
        └── 🎯 [CALLS] `resolve (External/Unresolved)()`
        └── 🎯 [CALLS] `removeEventListener()()`
    └── ⚡ **on('message')**
        └── 🎯 [CALLS] `listener (External/Unresolved)()`
  🌲 **#socket** `(Control)`
    └── ⚡ **on('error')**
        └── 🎯 [TRIGGERS] `onError()`
            └── 🎯 [CALLS] `close()`
                └── 🎯 [CALLS] `removeEventListener()()`
                └── 🎯 [CALLS] `removeEventListener()()`
            └── 🎯 [CALLS] `resolve (External/Unresolved)()`
    └── ⚡ **on('open')**
        └── 🎯 [TRIGGERS] `onOpen()`
            └── *ref:`close` [已折疊指針]
            └── *ref:`resolve (External/Unresolved)` [已折疊指針]
  🌲 **#window** `(Control)`
    └── ⚡ **on('beforeunload')**
    └── 🎯 [CALLS] `debounceReload()`
        └── 🎯 [CALLS] `clearTimeout (External/Unresolved)()`
    └── 🎯 [CALLS] `createHMRHandler (External/Unresolved)()`
    └── 🎯 [CALLS] `pageReload (External/Unresolved)()`
    └── 🎯 [CALLS] `setupForwardConsoleHandler (External/Unresolved)()`
    └── 🎯 [CALLS] `wrapIdIfNeeded()`
        └── 🎯 [CALLS] `wrapId (External/Unresolved)()`

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `updateStyle()`
- **變更前簽章 (Before)**: `function updateStyle(id: string, content: string): void` (L558~L587)
- **變更後簽章 (After)**: `function updateStyle(id: string, content: string): void` (L558~L589)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function updateStyle(id: string, content: string): void {
  if (linkSheetsMap.has(id)) return

  let style = sheetsMap.get(id)
  if (!style) {
    style = document.createElement('style')
    style.setAttribute('type', 'text/css')
    style.setAttribute('data-vite-dev-id', id)
    style.textContent = content
    if (cspNonce) {
      style.setAttribute('nonce', cspNonce)
    }

    if (!lastInsertedStyle) {
      document.head.appendChild(style)

      // reset lastInsertedStyle after async
      // because dynamically imported css will be split into a different file
      setTimeout(() => {
        lastInsertedStyle = undefined
      }, 0)
    } else {
      lastInsertedStyle.insertAdjacentElement('afterend', style)
    }
    lastInsertedStyle = style
  } else {
    style.textContent = content
  }
  sheetsMap.set(id, style)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function updateStyle(id: string, content: string): void {
  if (linkSheetsMap.has(id)) return

  let style = sheetsMap.get(id)
  if (!style) {
    style = document.createElement('style')
    style.setAttribute('type', 'text/css')
    style.setAttribute('data-vite-dev-id', id)
    style.textContent = content
    if (cspNonce) {
      style.setAttribute('nonce', cspNonce)
    }

    if (!lastInsertedStyle) {
      document.head.appendChild(style)

      // reset lastInsertedStyle after async
      // because dynamically imported css will be split into a different file
      setTimeout(() => {
        lastInsertedStyle = undefined
      }, 0)
    } else {
      lastInsertedStyle.insertAdjacentElement('afterend', style)
    }
    lastInsertedStyle = style
  } else if (style.textContent !== content) {
    // skip identical css, e.g. in a server rendered style: rewriting it still
    // replaces the stylesheet, which can re-create the font faces it declares
    style.textContent = content
  }
  sheetsMap.set(id, style)
}
```


---

### 🔹 Commit #19: `2a8c0f05`
- **完整 Hash**: `2a8c0f05c76e35c43ab3560984a5103c8db8dbcd`
- **說明 (Ground Truth)**: fix(build): correct preloads when chunkImportMap is enabled with non-root base (#23698)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/plugins/html.ts`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:123, E:112, A:0) ➔ After(N:123, E:112, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `getImportMapBaseUrl()`
- **變更前簽章 (Before)**: `function getImportMapBaseUrl(options: ResolvedEnvironmentOptions): string` (L1724~L1731)
- **變更後簽章 (After)**: `function getImportMapBaseUrl(
  options: ResolvedEnvironmentOptions & ResolvedConfig,
): string` (L1724~L1729)

#### ◀️ 變更前實作碼 (Before Implementation):
```
function getImportMapBaseUrl(options: ResolvedEnvironmentOptions): string {
  const chunkImportMap =
    options.build.rolldownOptions.experimental?.chunkImportMap
  if (typeof chunkImportMap === 'object' && chunkImportMap.baseUrl) {
    return chunkImportMap.baseUrl
  }
  return '/'
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
function getImportMapBaseUrl(
  options: ResolvedEnvironmentOptions & ResolvedConfig,
): string {
  // Vite overrides Rolldown's chunkImportMap.baseUrl with the resolved base.
  return options.base
}
```


---

### 🔹 Commit #20: `3a7f2aea`
- **完整 Hash**: `3a7f2aea757d59bae66ad6edf6b321d26a7e6778`
- **說明 (Ground Truth)**: fix(html): avoid adding filesystem root to watcher (#23689)
- **變更檔案數**: 1

#### 📄 檔案: `packages/vite/src/node/server/middlewares/indexHtml.ts`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:55, E:59, A:0) ➔ After(N:56, E:60, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `tryStatSync (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `devHtmlHook` ──[CALLS [guard: (!trailingSlash && tryStatSync(filename)?.isFile())]]──> `tryStatSync (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `devHtmlHook()`
- **變更前簽章 (Before)**: `devHtmlHook(
  html,
  { path: htmlPath, filename, server, originalUrl },
)` (L207~L459)
- **變更後簽章 (After)**: `devHtmlHook(
  html,
  { path: htmlPath, filename, server, originalUrl },
)` (L208~L459)

#### ◀️ 變更前實作碼 (Before Implementation):
```
async (
  html,
  { path: htmlPath, filename, server, originalUrl },
) => {
  // There's no way to express a relative URL that starts with `//`. URLs starting with `//` is relative to the scheme.
  // The relative URL is needed to generate the URL in script tags and link tags.
  // We replace `//` with `/` here for workaround, which is the best we can do.
  if (htmlPath.startsWith('//')) {
    htmlPath = htmlPath.replace(multipleLeadingSlashesRE, '/')
  }

  const { config, watcher } = server!
  const base = config.base || '/'
  const decodedBase = config.decodedBase || '/'

  let proxyModulePath: string
  let proxyModuleUrl: string

  const trailingSlash = htmlPath.endsWith('/')
  if (!trailingSlash && fs.existsSync(filename)) {
    // If htmlPath is a /@fs/ URL (e.g. vitest-browser always uses this form
    // for testerHtmlPath), normalise to an absolute FS path so proxyCacheUrl
    // is always root-relative.
    proxyModulePath = htmlPath.startsWith(FS_PREFIX) ? filename : htmlPath
    proxyModuleUrl = htmlPath
  } else {
    // There are users of vite.transformIndexHtml calling it with url '/'
    // for SSR integrations #7993, filename is root for this case
    // A user may also use a valid name for a virtual html file
    // Mark the path as virtual in both cases so sourcemaps aren't processed
    // and ids are properly handled
    const validPath = `${htmlPath}${trailingSlash ? 'index.html' : ''}`
    proxyModulePath = `\0${validPath}`
    proxyModuleUrl = wrapId(proxyModulePath)
  }
  proxyModuleUrl = joinUrlSegments(decodedBase, proxyModuleUrl)

  const s = new MagicString(html)
  let inlineModuleIndex = -1
  // The key to the proxyHtml cache is decoded, as it will be compared
  // against decoded URLs by the HTML plugins.
  const proxyCacheUrl = decodeURI(
    cleanUrl(proxyModulePath).replace(normalizePath(config.root), ''),
  )
  const styleUrl: AssetNode[] = []
  const inlineStyles: InlineStyleAttribute[] = []
  const inlineModulePaths: string[] = []

  const addInlineModule = (
    node: DefaultTreeAdapterMap['element'],
    ext: 'js',
  ) => {
    inlineModuleIndex++

    const contentNode = node.childNodes[0] as DefaultTreeAdapterMap['textNode']

    const code = contentNode.value

    let map: SourceMapInput | undefined
    if (proxyModulePath[0] !== '\0') {
      map = new MagicString(html)
        .snip(
          contentNode.sourceCodeLocation!.startOffset,
          contentNode.sourceCodeLocation!.endOffset,
        )
        .generateMap({ hires: 'boundary' })
      map.sources = [filename]
      map.file = filename
    }

    // add HTML Proxy to Map
    addToHTMLProxyCache(config, proxyCacheUrl, inlineModuleIndex, { code, map })

    // inline js module. convert to src="proxy" (dev only, base is never relative)
    const modulePath = `${proxyModuleUrl}?html-proxy&index=${inlineModuleIndex}.${ext}`
    inlineModulePaths.push(modulePath)

    s.update(
      node.sourceCodeLocation!.startOffset,
      node.sourceCodeLocation!.endOffset,
      `<script type="module" src="${modulePath}"></script>`,
    )
    preTransformRequest(server!, modulePath, decodedBase)
  }

  await traverseHtml(html, filename, config.logger.warn, (node) => {
    if (!nodeIsElement(node)) {
      return
    }

    // script tags
    if (node.nodeName === 'script') {
      const { src, srcSourceCodeLocation, isModule, isIgnored } =
        getScriptInfo(node)

      if (isIgnored) {
        removeViteIgnoreAttr(s, node.sourceCodeLocation!)
      } else if (src) {
        const processedUrl = processNodeUrl(
          src.value,
          /* useSrcSetReplacer */ false,
          config,
          htmlPath,
          originalUrl,
          server,
          !isModule,
        )
        if (processedUrl !== src.value) {
          overwriteAttrValue(s, srcSourceCodeLocation!, processedUrl)
        }
      } else if (isModule && node.childNodes.length) {
        addInlineModule(node, 'js')
      } else if (node.childNodes.length) {
        const scriptNode = node.childNodes.at(
          -1,
        ) as DefaultTreeAdapterMap['textNode']
        for (const {
          url,
          start,
          end,
        } of extractImportExpressionFromClassicScript(scriptNode)) {
          const processedUrl = processNodeUrl(
            url,
            false,
            config,
            htmlPath,
            originalUrl,
          )
          if (processedUrl !== url) {
            s.update(start, end, processedUrl)
          }
        }
      }
    }

    const inlineStyle = findNeedTransformStyleAttribute(node)
    if (inlineStyle) {
      inlineModuleIndex++
      inlineStyles.push({
        index: inlineModuleIndex,
        location: inlineStyle.location!,
        code: inlineStyle.attr.value,
      })
    }

    if (node.nodeName === 'style' && node.childNodes.length) {
      const children = node.childNodes[0] as DefaultTreeAdapterMap['textNode']
      styleUrl.push({
        start: children.sourceCodeLocation!.startOffset,
        end: children.sourceCodeLocation!.endOffset,
        code: children.value,
      })
    }

    // elements with [href/src] attrs
    const assetAttributes = getNodeAssetAttributes(
      node,
      config.html?.additionalAssetSources,
    )
    for (const attr of assetAttributes) {
      if (attr.type === 'remove') {
        s.remove(attr.location.startOffset, attr.location.endOffset)
      } else {
        const processedUrl = processNodeUrl(
          attr.value,
          attr.type === 'srcset',
          config,
          htmlPath,
          originalUrl,
        )
        if (processedUrl !== attr.value) {
          overwriteAttrValue(s, attr.location, processedUrl)
        }
      }
    }
  })

  // invalidate the module so the newly cached contents will be served
  const clientModuleGraph = server?.environments.client.moduleGraph
  if (clientModuleGraph) {
    await Promise.all(
      inlineModulePaths.map(async (url) => {
        const module = await clientModuleGraph.getModuleByUrl(url)
        if (module) {
          clientModuleGraph.invalidateModule(module)
        }
      }),
    )
  }

  await Promise.all([
    ...styleUrl.map(async ({ start, end, code }, index) => {
      const url = `${proxyModulePath}?html-proxy&direct&index=${index}.css`

      // ensure module in graph after successful load
      const mod =
        await server!.environments.client.moduleGraph.ensureEntryFromUrl(
          url,
          false,
        )
      ensureWatchedFile(watcher, mod.file, config.root)

      const result =
        await server!.environments.client.pluginContainer.transform(
          code,
          mod.id!,
        )
      let content = ''
      if (result.map && 'version' in result.map) {
        if (result.map.mappings) {
          await injectSourcesContent(result.map, proxyModulePath, config.logger)
        }
        content = getCodeWithSourcemap('css', result.code, result.map)
      } else {
        content = result.code
      }
      s.overwrite(start, end, content)
    }),
    ...inlineStyles.map(async ({ index, location, code }) => {
      // will transform with css plugin and cache result with css-post plugin
      const url = `${proxyModulePath}?html-proxy&inline-css&style-attr&index=${index}.css`

      const mod =
        await server!.environments.client.moduleGraph.ensureEntryFromUrl(
          url,
          false,
        )
      ensureWatchedFile(watcher, mod.file, config.root)

      await server?.environments.client.pluginContainer.transform(code, mod.id!)

      const hash = getHash(cleanUrl(mod.id!))
      const result = htmlProxyResult.get(`${hash}_${index}`)
      overwriteAttrValue(s, location, result ?? '')
    }),
  ])

  html = s.toString()

  return {
    html,
    tags: [
      {
        tag: 'script',
        attrs: {
          type: 'module',
          src: path.posix.join(base, CLIENT_PUBLIC_PATH),
        },
        injectTo: 'head-prepend',
      },
    ],
  }
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
async (
  html,
  { path: htmlPath, filename, server, originalUrl },
) => {
  // There's no way to express a relative URL that starts with `//`. URLs starting with `//` is relative to the scheme.
  // The relative URL is needed to generate the URL in script tags and link tags.
  // We replace `//` with `/` here for workaround, which is the best we can do.
  if (htmlPath.startsWith('//')) {
    htmlPath = htmlPath.replace(multipleLeadingSlashesRE, '/')
  }

  const { config, watcher } = server!
  const base = config.base || '/'
  const decodedBase = config.decodedBase || '/'

  let proxyModulePath: string
  let proxyModuleUrl: string

  const trailingSlash = htmlPath.endsWith('/')
  if (!trailingSlash && tryStatSync(filename)?.isFile()) {
    ensureWatchedFile(watcher, filename, config.root)
    // If htmlPath is a /@fs/ URL (e.g. vitest-browser always uses this form
    // for testerHtmlPath), normalise to an absolute FS path so proxyCacheUrl
    // is always root-relative.
    proxyModulePath = htmlPath.startsWith(FS_PREFIX) ? filename : htmlPath
    proxyModuleUrl = htmlPath
  } else {
    // There are users of vite.transformIndexHtml calling it with url '/'
    // for SSR integrations #7993, filename is root for this case
    // A user may also use a valid name for a virtual html file
    // Mark the path as virtual in both cases so sourcemaps aren't processed
    // and ids are properly handled
    const validPath = `${htmlPath}${trailingSlash ? 'index.html' : ''}`
    proxyModulePath = `\0${validPath}`
    proxyModuleUrl = wrapId(proxyModulePath)
  }
  proxyModuleUrl = joinUrlSegments(decodedBase, proxyModuleUrl)

  const s = new MagicString(html)
  let inlineModuleIndex = -1
  // The key to the proxyHtml cache is decoded, as it will be compared
  // against decoded URLs by the HTML plugins.
  const proxyCacheUrl = decodeURI(
    cleanUrl(proxyModulePath).replace(normalizePath(config.root), ''),
  )
  const styleUrl: AssetNode[] = []
  const inlineStyles: InlineStyleAttribute[] = []
  const inlineModulePaths: string[] = []

  const addInlineModule = (
    node: DefaultTreeAdapterMap['element'],
    ext: 'js',
  ) => {
    inlineModuleIndex++

    const contentNode = node.childNodes[0] as DefaultTreeAdapterMap['textNode']

    const code = contentNode.value

    let map: SourceMapInput | undefined
    if (proxyModulePath[0] !== '\0') {
      map = new MagicString(html)
        .snip(
          contentNode.sourceCodeLocation!.startOffset,
          contentNode.sourceCodeLocation!.endOffset,
        )
        .generateMap({ hires: 'boundary' })
      map.sources = [filename]
      map.file = filename
    }

    // add HTML Proxy to Map
    addToHTMLProxyCache(config, proxyCacheUrl, inlineModuleIndex, { code, map })

    // inline js module. convert to src="proxy" (dev only, base is never relative)
    const modulePath = `${proxyModuleUrl}?html-proxy&index=${inlineModuleIndex}.${ext}`
    inlineModulePaths.push(modulePath)

    s.update(
      node.sourceCodeLocation!.startOffset,
      node.sourceCodeLocation!.endOffset,
      `<script type="module" src="${modulePath}"></script>`,
    )
    preTransformRequest(server!, modulePath, decodedBase)
  }

  await traverseHtml(html, filename, config.logger.warn, (node) => {
    if (!nodeIsElement(node)) {
      return
    }

    // script tags
    if (node.nodeName === 'script') {
      const { src, srcSourceCodeLocation, isModule, isIgnored } =
        getScriptInfo(node)

      if (isIgnored) {
        removeViteIgnoreAttr(s, node.sourceCodeLocation!)
      } else if (src) {
        const processedUrl = processNodeUrl(
          src.value,
          /* useSrcSetReplacer */ false,
          config,
          htmlPath,
          originalUrl,
          server,
          !isModule,
        )
        if (processedUrl !== src.value) {
          overwriteAttrValue(s, srcSourceCodeLocation!, processedUrl)
        }
      } else if (isModule && node.childNodes.length) {
        addInlineModule(node, 'js')
      } else if (node.childNodes.length) {
        const scriptNode = node.childNodes.at(
          -1,
        ) as DefaultTreeAdapterMap['textNode']
        for (const {
          url,
          start,
          end,
        } of extractImportExpressionFromClassicScript(scriptNode)) {
          const processedUrl = processNodeUrl(
            url,
            false,
            config,
            htmlPath,
            originalUrl,
          )
          if (processedUrl !== url) {
            s.update(start, end, processedUrl)
          }
        }
      }
    }

    const inlineStyle = findNeedTransformStyleAttribute(node)
    if (inlineStyle) {
      inlineModuleIndex++
      inlineStyles.push({
        index: inlineModuleIndex,
        location: inlineStyle.location!,
        code: inlineStyle.attr.value,
      })
    }

    if (node.nodeName === 'style' && node.childNodes.length) {
      const children = node.childNodes[0] as DefaultTreeAdapterMap['textNode']
      styleUrl.push({
        start: children.sourceCodeLocation!.startOffset,
        end: children.sourceCodeLocation!.endOffset,
        code: children.value,
      })
    }

    // elements with [href/src] attrs
    const assetAttributes = getNodeAssetAttributes(
      node,
      config.html?.additionalAssetSources,
    )
    for (const attr of assetAttributes) {
      if (attr.type === 'remove') {
        s.remove(attr.location.startOffset, attr.location.endOffset)
      } else {
        const processedUrl = processNodeUrl(
          attr.value,
          attr.type === 'srcset',
          config,
          htmlPath,
          originalUrl,
        )
        if (processedUrl !== attr.value) {
          overwriteAttrValue(s, attr.location, processedUrl)
        }
      }
    }
  })

  // invalidate the module so the newly cached contents will be served
  const clientModuleGraph = server?.environments.client.moduleGraph
  if (clientModuleGraph) {
    await Promise.all(
      inlineModulePaths.map(async (url) => {
        const module = await clientModuleGraph.getModuleByUrl(url)
        if (module) {
          clientModuleGraph.invalidateModule(module)
        }
      }),
    )
  }

  await Promise.all([
    ...styleUrl.map(async ({ start, end, code }, index) => {
      const url = `${proxyModulePath}?html-proxy&direct&index=${index}.css`

      // ensure module in graph after successful load
      const mod =
        await server!.environments.client.moduleGraph.ensureEntryFromUrl(
          url,
          false,
        )

      const result =
        await server!.environments.client.pluginContainer.transform(
          code,
          mod.id!,
        )
      let content = ''
      if (result.map && 'version' in result.map) {
        if (result.map.mappings) {
          await injectSourcesContent(result.map, proxyModulePath, config.logger)
        }
        content = getCodeWithSourcemap('css', result.code, result.map)
      } else {
        content = result.code
      }
      s.overwrite(start, end, content)
    }),
    ...inlineStyles.map(async ({ index, location, code }) => {
      // will transform with css plugin and cache result with css-post plugin
      const url = `${proxyModulePath}?html-proxy&inline-css&style-attr&index=${index}.css`

      const mod =
        await server!.environments.client.moduleGraph.ensureEntryFromUrl(
          url,
          false,
        )

      await server?.environments.client.pluginContainer.transform(code, mod.id!)

      const hash = getHash(cleanUrl(mod.id!))
      const result = htmlProxyResult.get(`${hash}_${index}`)
      overwriteAttrValue(s, location, result ?? '')
    }),
  ])

  html = s.toString()

  return {
    html,
    tags: [
      {
        tag: 'script',
        attrs: {
          type: 'module',
          src: path.posix.join(base, CLIENT_PUBLIC_PATH),
        },
        injectTo: 'head-prepend',
      },
    ],
  }
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/vite show 15c85ddae2bbbc3808d96a223a5a18a800883252
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 15c85ddae2bbbc3808d96a223a5a18a800883252~1 --file test_repos/vite/packages/create-vite/src/index.ts
   ```
