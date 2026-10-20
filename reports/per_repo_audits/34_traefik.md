# 🔬 CODE-Map 基準審查獨立驗證報告: `traefik`
> **技術生態**: `Go (邊緣路由器 / 動態中介軟體管線)`  
> **本地倉庫路徑**: `test_repos/traefik`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 30 Files  
> **報告生成時間**: 2026-10-20 21:44:45  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `19` / `30` | `63.3%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `7` / `30` | `23.3%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `30` | `13.3%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`26` / `30`** | **`86.7%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `30` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `2157e701`
- **完整 Hash**: `2157e70100babb64cd4e001fc8ca7e6a187cfa82`
- **說明 (Ground Truth)**: Fix cross-namespace check on shared auth-tls-secret TLS options
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:126, E:187, A:0) ➔ After(N:123, E:186, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 4, +Edges: 5, -Edges: 6, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `pascalCaseWordBoundaryRegexp.ReplaceAllString (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `strings.SplitN (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `tlsOptionName` (MODULE_STATE)
  • - [移除節點] `tlsOption` (MODULE_STATE)
  • - [移除節點] `pascalCaseWordBoundary.ReplaceAllString (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.buildClientAuthTLSOption` ──[CALLS]──> `strings.Cut (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildClientAuthTLSOption` ──[CALLS]──> `regexp.MustCompile (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildClientAuthTLSOption` ──[CALLS]──> `strings.ToLower (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildClientAuthTLSOption` ──[CALLS]──> `pascalCaseWordBoundaryRegexp.ReplaceAllString (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildClientAuthTLSOption` ──[CALLS]──> `strconv.Itoa (External/Pkg)`
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `regexp.MustCompile (External/Pkg)`
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `pascalCaseWordBoundary.ReplaceAllString (External/Pkg)`
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `clientAuthTypeFromString`
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `strings.Cut (External/Pkg)`
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `strconv.Itoa (External/Pkg)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.buildClientAuthTLSOption()`
- **變更前簽章 (Before)**: `func Provider.buildClientAuthTLSOption(ingressNamespace string, cfg IngressConfig)` (L931~L962)
- **變更後簽章 (After)**: `func Provider.buildClientAuthTLSOption(ingressNamespace string, cfg IngressConfig, tlsOptionsCache map[string]*tls.Options)` (L920~L962)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildClientAuthTLSOption(ingressNamespace string, cfg IngressConfig) (*tls.Options, error) {
	if cfg.AuthTLSSecret == nil {
		return nil, errors.New("auth-tls-secret is nil")
	}

	parts := strings.SplitN(*cfg.AuthTLSSecret, "/", 2)
	if len(parts) != 2 || parts[0] == "" || parts[1] == "" {
		return nil, errors.New("auth-tls-secret must be in namespace/name format")
	}

	secretNamespace, secretName := parts[0], parts[1]
	if !p.AllowCrossNamespaceResources && secretNamespace != ingressNamespace {
		return nil, fmt.Errorf("cross-namespace auth-tls-secret not allowed: %s/%s", secretNamespace, secretName)
	}

	blocks, err := p.certificateBlocks(secretNamespace, secretName)
	if err != nil {
		return nil, fmt.Errorf("reading client certificate: %w", err)
	}

	if blocks.ca == nil {
		return nil, errors.New("secret does not contain a CA certificate")
	}

	opt := &tls.Options{}
	opt.SetDefaults()
	opt.ClientAuth = tls.ClientAuth{
		CAFiles:        []types.FileOrContent{types.FileOrContent(blocks.ca)},
		ClientAuthType: clientAuthTypeFromString(cfg.AuthTLSVerifyClient),
	}
	return opt, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildClientAuthTLSOption(ingressNamespace string, cfg IngressConfig, tlsOptionsCache map[string]*tls.Options) (string, *tls.Options, error) {
	if cfg.AuthTLSSecret == nil {
		return "", nil, errors.New("auth-tls-secret is nil")
	}

	secretNamespace, secretName, found := strings.Cut(*cfg.AuthTLSSecret, "/")
	if !found || secretNamespace == "" || secretName == "" {
		return "", nil, errors.New("auth-tls-secret must be in namespace/name format")
	}

	if !p.AllowCrossNamespaceResources && secretNamespace != ingressNamespace {
		return "", nil, fmt.Errorf("cross-namespace auth-tls-secret not allowed: %s/%s", secretNamespace, secretName)
	}

	// The namespace and the secret name are suffixed by their own length so that the name unambiguously encodes the pair.
	pascalCaseWordBoundaryRegexp := regexp.MustCompile(`([a-z0-9])([A-Z])`)
	clientAuthType := clientAuthTypeFromString(cfg.AuthTLSVerifyClient)
	clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundaryRegexp.ReplaceAllString(clientAuthType, "$1-$2"))
	optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

	if opt, exists := tlsOptionsCache[optName]; exists {
		return optName, opt, nil
	}

	blocks, err := p.certificateBlocks(secretNamespace, secretName)
	if err != nil {
		return "", nil, fmt.Errorf("reading client certificate: %w", err)
	}

	if blocks.ca == nil {
		return "", nil, errors.New("secret does not contain a CA certificate")
	}

	opt := &tls.Options{}
	opt.SetDefaults()
	opt.ClientAuth = tls.ClientAuth{
		CAFiles:        []types.FileOrContent{types.FileOrContent(blocks.ca)},
		ClientAuthType: clientAuthType,
	}
	tlsOptionsCache[optName] = opt

	return optName, opt, nil
}
```

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L654)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L639)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	hostsWithRootPath := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen
	serverAppRoots := make(map[string]string)

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			// The ingress default backend becomes a host-only catch-all location, which matches "/" as well.
			if ingress.Spec.DefaultBackend != nil && ingress.Spec.DefaultBackend.Service != nil {
				hostsWithRootPath[rule.Host] = true
			}

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if appRoot := ptr.Deref(cfg.AppRoot, ""); strings.HasPrefix(appRoot, "/") && serverAppRoots[rule.Host] == "" {
				serverAppRoots[rule.Host] = appRoot
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}

					// An empty path produces a host-only rule, which matches "/" as well.
					if pa.Path == "/" || pa.Path == "" {
						hostsWithRootPath[rule.Host] = true
					}

					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	// The app-root "/" router is synthesized at most once per host, on the first
	// location that needs it, to avoid emitting several routers with the same rule.
	hostsWithAppRootRouter := make(map[string]bool)

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				if loc.Path == "/" || loc.Path == "" {
					inheritServerAppRoot(loc, serverAppRoots[rule.Host])
				}

				// ingress-nginx evaluates app-root at the server scope, so "/" is redirected
				// even when the Ingress declares no "/" path. In Traefik a request has to match
				// a router before any middleware runs, hence the extra router.
				if loc.AppRoot != nil && !hostsWithRootPath[rule.Host] && !hostsWithAppRootRouter[rule.Host] {
					loc.AppRootExtraRouterRule = buildAppRootRouterRule(rule.Host, loc.Aliases)
					hostsWithAppRootRouter[rule.Host] = true
				}

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				inheritServerAppRoot(loc, serverAppRoots[rule.Host])

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	applyServerClientAuth(ctx, mc.Servers)

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	hostsWithRootPath := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen
	serverAppRoots := make(map[string]string)

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			// The ingress default backend becomes a host-only catch-all location, which matches "/" as well.
			if ingress.Spec.DefaultBackend != nil && ingress.Spec.DefaultBackend.Service != nil {
				hostsWithRootPath[rule.Host] = true
			}

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if appRoot := ptr.Deref(cfg.AppRoot, ""); strings.HasPrefix(appRoot, "/") && serverAppRoots[rule.Host] == "" {
				serverAppRoots[rule.Host] = appRoot
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}

					// An empty path produces a host-only rule, which matches "/" as well.
					if pa.Path == "/" || pa.Path == "" {
						hostsWithRootPath[rule.Host] = true
					}

					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	// The app-root "/" router is synthesized at most once per host, on the first
	// location that needs it, to avoid emitting several routers with the same rule.
	hostsWithAppRootRouter := make(map[string]bool)

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var (
			tlsOptionName string
			tlsOption     *tls.Options
		)
		if ing.config.AuthTLSSecret != nil {
			tlsOptionName, tlsOption, err = p.buildClientAuthTLSOption(ing.Namespace, ing.config, tlsOptionCache)
			if err != nil {
				logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
				// Skipping the ingress entirely matches ingress-nginx behavior:
				// when the configured client-auth secret cannot be resolved, no
				// router/middleware/service should be exposed for the ingress.
				continue
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				if loc.Path == "/" || loc.Path == "" {
					inheritServerAppRoot(loc, serverAppRoots[rule.Host])
				}

				// ingress-nginx evaluates app-root at the server scope, so "/" is redirected
				// even when the Ingress declares no "/" path. In Traefik a request has to match
				// a router before any middleware runs, hence the extra router.
				if loc.AppRoot != nil && !hostsWithRootPath[rule.Host] && !hostsWithAppRootRouter[rule.Host] {
					loc.AppRootExtraRouterRule = buildAppRootRouterRule(rule.Host, loc.Aliases)
					hostsWithAppRootRouter[rule.Host] = true
				}

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				inheritServerAppRoot(loc, serverAppRoots[rule.Host])

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	applyServerClientAuth(ctx, mc.Servers)

	return mc
}
```


---

### 🔹 Commit #02: `a09200be`
- **完整 Hash**: `a09200bec563a9b970f56e99590a7aba6fec2749`
- **說明 (Ground Truth)**: Fix concurrent buffer reads on upgraded connections
- **變更檔案數**: 1

#### 📄 檔案: `pkg/proxy/fast/connpool.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:93, E:109, A:0) ➔ After(N:93, E:110, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `conn.readLoop` ──[CALLS]──> `conn.isUpgraded`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `conn.readLoop()`
- **變更前簽章 (Before)**: `func conn.readLoop()` (L93~L125)
- **變更後簽章 (After)**: `func conn.readLoop()` (L93~L131)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *conn) readLoop() {
	defer c.Close()

	for {
		_, err := c.br.Peek(1)
		if err != nil {
			select {
			// An error occurred while a response was expected to be handled.
			case <-c.RWCh:
				c.ErrCh <- err
			// An error occurred on an idle connection.
			default:
				c.broken.Store(true)
			}
			return
		}

		// Unsolicited response received on an idle connection.
		if !c.expectedResponse.Load() {
			c.broken.Store(true)
			return
		}

		r := <-c.RWCh
		if err = c.handleResponse(r); err != nil {
			c.ErrCh <- err
			return
		}

		c.expectedResponse.Store(false)
		c.ErrCh <- nil
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *conn) readLoop() {
	defer c.Close()

	for {
		_, err := c.br.Peek(1)
		if err != nil {
			select {
			// An error occurred while a response was expected to be handled.
			case <-c.RWCh:
				c.ErrCh <- err
			// An error occurred on an idle connection.
			default:
				c.broken.Store(true)
			}
			return
		}

		// Unsolicited response received on an idle connection.
		if !c.expectedResponse.Load() {
			c.broken.Store(true)
			return
		}

		r := <-c.RWCh
		if err = c.handleResponse(r); err != nil {
			c.ErrCh <- err
			return
		}

		c.expectedResponse.Store(false)
		c.ErrCh <- nil

		// An upgraded connection is handed over to the tunnel copiers, which read from the same bufio.Reader:
		// the read loop must not touch it anymore, and the connection can never be pooled again.
		if c.isUpgraded() {
			return
		}
	}
}
```


---

### 🔹 Commit #03: `b706c59e`
- **完整 Hash**: `b706c59e143424df99e4b5c0e901385a36683105`
- **說明 (Ground Truth)**: Apply auth-tls client authentication to the whole host
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:121, E:179, A:0) ➔ After(N:126, E:187, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 8, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `log.Ctx(ctx).Warn().
					Str("ingress", loc.IngressName).
					Str("namespace", loc.Namespace).
					Msgf (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `slices.IndexFunc (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `log.Ctx(ctx).Warn().
					Str("ingress", loc.IngressName).
					Str (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `log.Ctx(ctx).Warn().
					Str (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `applyServerClientAuth` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.build` ──[CALLS]──> `applyServerClientAuth`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `slices.IndexFunc (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `log.Ctx(ctx).Warn().
					Str("ingress", loc.IngressName).
					Str("namespace", loc.Namespace).
					Msgf (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `log.Ctx(ctx).Warn().
					Str("ingress", loc.IngressName).
					Str (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `log.Ctx(ctx).Warn().
					Str (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `log.Ctx(ctx).Warn (External/Pkg)`
  • + [新增呼叫邊] `applyServerClientAuth` ──[CALLS]──> `log.Ctx (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L652)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L654)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	hostsWithRootPath := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen
	serverAppRoots := make(map[string]string)

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			// The ingress default backend becomes a host-only catch-all location, which matches "/" as well.
			if ingress.Spec.DefaultBackend != nil && ingress.Spec.DefaultBackend.Service != nil {
				hostsWithRootPath[rule.Host] = true
			}

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if appRoot := ptr.Deref(cfg.AppRoot, ""); strings.HasPrefix(appRoot, "/") && serverAppRoots[rule.Host] == "" {
				serverAppRoots[rule.Host] = appRoot
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}

					// An empty path produces a host-only rule, which matches "/" as well.
					if pa.Path == "/" || pa.Path == "" {
						hostsWithRootPath[rule.Host] = true
					}

					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	// The app-root "/" router is synthesized at most once per host, on the first
	// location that needs it, to avoid emitting several routers with the same rule.
	hostsWithAppRootRouter := make(map[string]bool)

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				if loc.Path == "/" || loc.Path == "" {
					inheritServerAppRoot(loc, serverAppRoots[rule.Host])
				}

				// ingress-nginx evaluates app-root at the server scope, so "/" is redirected
				// even when the Ingress declares no "/" path. In Traefik a request has to match
				// a router before any middleware runs, hence the extra router.
				if loc.AppRoot != nil && !hostsWithRootPath[rule.Host] && !hostsWithAppRootRouter[rule.Host] {
					loc.AppRootExtraRouterRule = buildAppRootRouterRule(rule.Host, loc.Aliases)
					hostsWithAppRootRouter[rule.Host] = true
				}

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				inheritServerAppRoot(loc, serverAppRoots[rule.Host])

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	hostsWithRootPath := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen
	serverAppRoots := make(map[string]string)

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			// The ingress default backend becomes a host-only catch-all location, which matches "/" as well.
			if ingress.Spec.DefaultBackend != nil && ingress.Spec.DefaultBackend.Service != nil {
				hostsWithRootPath[rule.Host] = true
			}

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if appRoot := ptr.Deref(cfg.AppRoot, ""); strings.HasPrefix(appRoot, "/") && serverAppRoots[rule.Host] == "" {
				serverAppRoots[rule.Host] = appRoot
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}

					// An empty path produces a host-only rule, which matches "/" as well.
					if pa.Path == "/" || pa.Path == "" {
						hostsWithRootPath[rule.Host] = true
					}

					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	// The app-root "/" router is synthesized at most once per host, on the first
	// location that needs it, to avoid emitting several routers with the same rule.
	hostsWithAppRootRouter := make(map[string]bool)

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				if loc.Path == "/" || loc.Path == "" {
					inheritServerAppRoot(loc, serverAppRoots[rule.Host])
				}

				// ingress-nginx evaluates app-root at the server scope, so "/" is redirected
				// even when the Ingress declares no "/" path. In Traefik a request has to match
				// a router before any middleware runs, hence the extra router.
				if loc.AppRoot != nil && !hostsWithRootPath[rule.Host] && !hostsWithAppRootRouter[rule.Host] {
					loc.AppRootExtraRouterRule = buildAppRootRouterRule(rule.Host, loc.Aliases)
					hostsWithAppRootRouter[rule.Host] = true
				}

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				inheritServerAppRoot(loc, serverAppRoots[rule.Host])

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	applyServerClientAuth(ctx, mc.Servers)

	return mc
}
```


---

### 🔹 Commit #04: `83c9b495`
- **完整 Hash**: `83c9b4952de8289281945e3efdd3c919c828211b`
- **說明 (Ground Truth)**: Fix Ingress NGINX apply app-root when the Ingress declares no "/" path
- **變更檔案數**: 3

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:119, E:176, A:0) ➔ After(N:121, E:179, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `buildAppRootRouterRule (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `inheritServerAppRoot` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.build` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • + [新增呼叫邊] `Provider.build` ──[CALLS]──> `inheritServerAppRoot`
  • + [新增呼叫邊] `Provider.build` ──[CALLS]──> `buildAppRootRouterRule (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L619)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L652)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	hostsWithRootPath := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen
	serverAppRoots := make(map[string]string)

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			// The ingress default backend becomes a host-only catch-all location, which matches "/" as well.
			if ingress.Spec.DefaultBackend != nil && ingress.Spec.DefaultBackend.Service != nil {
				hostsWithRootPath[rule.Host] = true
			}

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if appRoot := ptr.Deref(cfg.AppRoot, ""); strings.HasPrefix(appRoot, "/") && serverAppRoots[rule.Host] == "" {
				serverAppRoots[rule.Host] = appRoot
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}

					// An empty path produces a host-only rule, which matches "/" as well.
					if pa.Path == "/" || pa.Path == "" {
						hostsWithRootPath[rule.Host] = true
					}

					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	// The app-root "/" router is synthesized at most once per host, on the first
	// location that needs it, to avoid emitting several routers with the same rule.
	hostsWithAppRootRouter := make(map[string]bool)

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				if loc.Path == "/" || loc.Path == "" {
					inheritServerAppRoot(loc, serverAppRoots[rule.Host])
				}

				// ingress-nginx evaluates app-root at the server scope, so "/" is redirected
				// even when the Ingress declares no "/" path. In Traefik a request has to match
				// a router before any middleware runs, hence the extra router.
				if loc.AppRoot != nil && !hostsWithRootPath[rule.Host] && !hostsWithAppRootRouter[rule.Host] {
					loc.AppRootExtraRouterRule = buildAppRootRouterRule(rule.Host, loc.Aliases)
					hostsWithAppRootRouter[rule.Host] = true
				}

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)
				inheritServerAppRoot(loc, serverAppRoots[rule.Host])

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```


#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/model.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:2, E:0, A:0) ➔ After(N:2, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
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

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/translator.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:51, E:76, A:0) ➔ After(N:54, E:84, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 9, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `buildAppRootRouterRule` (FUNCTION_DEF)
  • + [新增節點] `applyAppRootRedirect` (FUNCTION_DEF)
  • + [新增節點] `buildHostRule` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.translate` ──[CALLS]──> `applyAppRootRedirect`
  • + [新增呼叫邊] `buildAppRootRouterRule` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`
  • + [新增呼叫邊] `buildAppRootRouterRule` ──[CALLS]──> `buildHostRule`
  • + [新增呼叫邊] `buildHostRule` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `buildHostRule` ──[CALLS]──> `len (External/Pkg)`
  • + [新增呼叫邊] `buildHostRule` ──[CALLS]──> `append (External/Pkg)`
  • + [新增呼叫邊] `buildHostRule` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`
  • + [新增呼叫邊] `buildHostRule` ──[CALLS]──> `strings.Join (External/Pkg)`
  • + [新增呼叫邊] `buildRule` ──[CALLS]──> `buildHostRule`
  • - [移除呼叫邊] `buildRule` ──[CALLS]──> `make (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.translate()`
- **變更前簽章 (Before)**: `func Provider.translate(ctx context.Context, mc *model)` (L23~L314)
- **變更後簽章 (After)**: `func Provider.translate(ctx context.Context, mc *model)` (L23~L316)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesMetadata{
					Kind:      "Ingress",
					Namespace: mc.DefaultBackend.Namespace,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.Name = loc.IngressName
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		defaultBackendSvc := buildService(mc.DefaultBackend, serversTransportName)
		defaultBackendSvc.Observability = buildServiceObservability(mc.DefaultBackend)
		conf.HTTP.Services[defaultBackendName] = defaultBackendSvc

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			primarySvc := buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)
			primarySvc.Observability = buildServiceObservability(backend)
			conf.HTTP.Services[primarySvcName] = primarySvc

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesMetadata{
						Kind:      "Ingress",
						Namespace: loc.Namespace,
						Name:      loc.IngressName,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					canarySvc.Observability = buildServiceObservability(canaryBackend)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName)
			} else {
				routerKey = fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex)
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
			}

			// An ssl-passthrough host is served over TCP on the TLS entryPoints, so it gets no TLS router at all.
			var rtTLS *dynamic.Router
			if !loc.SSLPassthrough {
				rtTLS = &dynamic.Router{
					EntryPoints: p.TLSEntryPoints,
					Rule:        rule,
					RuleSyntax:  "default",
					Service:     routerSvcName,
					TLS: &dynamic.RouterTLSConfig{
						Options: loc.TLSOptionName,
					},
					Observability: obs,
				}

				if loc.Error {
					rtTLS.Service = unavailableServiceName
				}

				conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

				if !loc.Error {
					p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
					applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
				}
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				if rtTLS != nil {
					canaryKeyTLS := canaryKey + "-tls"
					canaryRouterTLS := &dynamic.Router{
						EntryPoints:   rtTLS.EntryPoints,
						Rule:          appendCanaryRule(rule, loc.Canary),
						RuleSyntax:    rtTLS.RuleSyntax,
						Service:       canarySvcName,
						TLS:           rtTLS.TLS,
						Observability: obs,
					}
					conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
					p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
				}
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				if rtTLS != nil {
					nonCanaryKeyTLS := nonCanaryKey + "-tls"
					nonCanaryRouterTLS := &dynamic.Router{
						EntryPoints:   rtTLS.EntryPoints,
						Rule:          appendNonCanaryRule(rule, loc.Canary),
						RuleSyntax:    rtTLS.RuleSyntax,
						Service:       primarySvcName,
						TLS:           rtTLS.TLS,
						Observability: obs,
					}
					conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
					p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
				}
			}
		}
	}

	return conf
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesMetadata{
					Kind:      "Ingress",
					Namespace: mc.DefaultBackend.Namespace,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.Name = loc.IngressName
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		defaultBackendSvc := buildService(mc.DefaultBackend, serversTransportName)
		defaultBackendSvc.Observability = buildServiceObservability(mc.DefaultBackend)
		conf.HTTP.Services[defaultBackendName] = defaultBackendSvc

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			primarySvc := buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)
			primarySvc.Observability = buildServiceObservability(backend)
			conf.HTTP.Services[primarySvcName] = primarySvc

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesMetadata{
						Kind:      "Ingress",
						Namespace: loc.Namespace,
						Name:      loc.IngressName,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					canarySvc.Observability = buildServiceObservability(canaryBackend)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName)
			} else {
				routerKey = fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex)
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
				applyAppRootRedirect(loc, routerKey, rt, obs, conf)
			}

			// An ssl-passthrough host is served over TCP on the TLS entryPoints, so it gets no TLS router at all.
			var rtTLS *dynamic.Router
			if !loc.SSLPassthrough {
				rtTLS = &dynamic.Router{
					EntryPoints: p.TLSEntryPoints,
					Rule:        rule,
					RuleSyntax:  "default",
					Service:     routerSvcName,
					TLS: &dynamic.RouterTLSConfig{
						Options: loc.TLSOptionName,
					},
					Observability: obs,
				}

				if loc.Error {
					rtTLS.Service = unavailableServiceName
				}

				conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

				if !loc.Error {
					p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
					applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
					applyAppRootRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
				}
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				if rtTLS != nil {
					canaryKeyTLS := canaryKey + "-tls"
					canaryRouterTLS := &dynamic.Router{
						EntryPoints:   rtTLS.EntryPoints,
						Rule:          appendCanaryRule(rule, loc.Canary),
						RuleSyntax:    rtTLS.RuleSyntax,
						Service:       canarySvcName,
						TLS:           rtTLS.TLS,
						Observability: obs,
					}
					conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
					p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
				}
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				if rtTLS != nil {
					nonCanaryKeyTLS := nonCanaryKey + "-tls"
					nonCanaryRouterTLS := &dynamic.Router{
						EntryPoints:   rtTLS.EntryPoints,
						Rule:          appendNonCanaryRule(rule, loc.Canary),
						RuleSyntax:    rtTLS.RuleSyntax,
						Service:       primarySvcName,
						TLS:           rtTLS.TLS,
						Observability: obs,
					}
					conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
					p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
				}
			}
		}
	}

	return conf
}
```

### 🔹 函式: `buildRule()`
- **變更前簽章 (Before)**: `func buildRule(host string, loc *location)` (L644~L684)
- **變更後簽章 (After)**: `func buildRule(host string, loc *location)` (L691~L722)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func buildRule(host string, loc *location) string {
	var rules []string

	if host != "" {
		hosts := append([]string{host}, loc.Aliases...)
		hostRules := make([]string, 0, len(hosts))
		for _, h := range hosts {
			hostRules = append(hostRules, fmt.Sprintf("Host(%q)", h))
		}
		if len(hostRules) > 1 {
			rules = append(rules, "("+strings.Join(hostRules, " || ")+")")
		} else {
			rules = append(rules, hostRules[0])
		}
	}

	if len(loc.Path) > 0 {
		pathType := ptr.Deref(loc.PathType, netv1.PathTypePrefix)

		regexPath := loc.Path
		if pathType == netv1.PathTypeImplementationSpecific {
			pathType = netv1.PathTypePrefix
			if hasAbsoluteRewriteTarget(loc) {
				regexPath = makeTrailingGroupOptional(loc.Path)
			}
		}

		switch pathType {
		case netv1.PathTypeExact:
			rules = append(rules, fmt.Sprintf("Path(%q)", loc.Path))
		case netv1.PathTypePrefix:
			if loc.UseRegex {
				rules = append(rules, fmt.Sprintf("PathRegexp(%q)", "(?i)^"+regexPath))
			} else {
				rules = append(rules, buildPrefixRule(loc.Path))
			}
		}
	}

	return strings.Join(rules, " && ")
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func buildRule(host string, loc *location) string {
	var rules []string

	if host != "" {
		rules = append(rules, buildHostRule(host, loc.Aliases))
	}

	if len(loc.Path) > 0 {
		pathType := ptr.Deref(loc.PathType, netv1.PathTypePrefix)

		regexPath := loc.Path
		if pathType == netv1.PathTypeImplementationSpecific {
			pathType = netv1.PathTypePrefix
			if hasAbsoluteRewriteTarget(loc) {
				regexPath = makeTrailingGroupOptional(loc.Path)
			}
		}

		switch pathType {
		case netv1.PathTypeExact:
			rules = append(rules, fmt.Sprintf("Path(%q)", loc.Path))
		case netv1.PathTypePrefix:
			if loc.UseRegex {
				rules = append(rules, fmt.Sprintf("PathRegexp(%q)", "(?i)^"+regexPath))
			} else {
				rules = append(rules, buildPrefixRule(loc.Path))
			}
		}
	}

	return strings.Join(rules, " && ")
}
```


---

### 🔹 Commit #05: `26c9ff9b`
- **完整 Hash**: `26c9ff9b8d3bb77a07b1e202ed76e4e4e7f9c91a`
- **說明 (Ground Truth)**: Avoid creating a TLS router for the ssl-passthrough default backend
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:119, E:176, A:0) ➔ After(N:119, E:176, A:0)
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

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L618)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L619)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough only adds the TCP router forwarding the connection to the backend without decrypting it.
		// The HTTP side of the ingress is built below like any other, ingress-nginx serving that host on the HTTP port from the regular location.
		sslPassthrough := ptr.Deref(ing.config.SSLPassthrough, false)
		if sslPassthrough {
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host),
				})
				markProcessedIngress(ing.Ingress)
			}
		}

		// Load TLS certificates into the shared mc.Certs map first.
		// They are kept even when the rest of the ingress is later skipped (e.g. when the serversTransport cannot be built, or when an auth-tls-secret fails to resolve), so the default certificate pool stays consistent.
		// When loading fails, hasTLS still signals that the ingress has a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Normal ingress: build serversTransport, TLS options, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
					SSLPassthrough:       sslPassthrough,
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
					SSLPassthrough:          sslPassthrough,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```


---

### 🔹 Commit #06: `4fb60c4e`
- **完整 Hash**: `4fb60c4e67c37a3a88808cedb4146f2a5741b2df`
- **說明 (Ground Truth)**: Fix the default address of partially configured internal entry points
- **變更檔案數**: 1

#### 📄 檔案: `pkg/config/static/static_config.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:40, E:36, A:0) ➔ After(N:40, E:36, A:0)
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

### 🔹 函式: `Configuration.SetEffectiveConfiguration()`
- **變更前簽章 (Before)**: `func Configuration.SetEffectiveConfiguration()` (L294~L440)
- **變更後簽章 (After)**: `func Configuration.SetEffectiveConfiguration()` (L294~L446)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Configuration) SetEffectiveConfiguration() {
	// Creates the default entry point if needed
	if !c.hasUserDefinedEntrypoint() {
		ep := &EntryPoint{Address: ":80"}
		ep.SetDefaults()
		// TODO: double check this tomorrow
		if c.EntryPoints == nil {
			c.EntryPoints = make(EntryPoints)
		}
		c.EntryPoints["http"] = ep
	}

	// Creates the internal traefik entry point if needed
	if (c.API != nil && c.API.Insecure) ||
		(c.Ping != nil && !c.Ping.ManualRouting && c.Ping.EntryPoint == DefaultInternalEntryPointName) ||
		(c.Metrics != nil && c.Metrics.Prometheus != nil && !c.Metrics.Prometheus.ManualRouting && c.Metrics.Prometheus.EntryPoint == DefaultInternalEntryPointName) ||
		(c.Providers != nil && c.Providers.Rest != nil && c.Providers.Rest.Insecure) {
		if _, ok := c.EntryPoints[DefaultInternalEntryPointName]; !ok {
			ep := &EntryPoint{Address: ":8080"}
			ep.SetDefaults()
			c.EntryPoints[DefaultInternalEntryPointName] = ep
		}
	}

	if c.Tracing != nil && c.Tracing.GlobalAttributes != nil && c.Tracing.ResourceAttributes == nil {
		c.Tracing.ResourceAttributes = c.Tracing.GlobalAttributes
	}

	for i, providerName := range c.Providers.Precedence {
		c.Providers.Precedence[i] = strings.ToLower(providerName)
	}

	if c.Providers.Docker != nil {
		if c.Providers.Docker.HTTPClientTimeout < 0 {
			c.Providers.Docker.HTTPClientTimeout = 0
		}
	}

	if c.Providers.Swarm != nil {
		if c.Providers.Swarm.RefreshSeconds <= 0 {
			c.Providers.Swarm.RefreshSeconds = ptypes.Duration(15 * time.Second)
		}

		if c.Providers.Swarm.HTTPClientTimeout < 0 {
			c.Providers.Swarm.HTTPClientTimeout = 0
		}
	}

	// Configure Gateway API provider
	if c.Providers.KubernetesGateway != nil {
		entryPoints := make(map[string]gateway.Entrypoint)
		for epName, entryPoint := range c.EntryPoints {
			entryPoints[epName] = gateway.Entrypoint{Address: entryPoint.GetAddress(), HasHTTPTLSConf: entryPoint.HTTP.TLS != nil}
		}

		if c.Providers.KubernetesCRD != nil {
			c.Providers.KubernetesCRD.FillExtensionBuilderRegistry(c.Providers.KubernetesGateway)
		}

		c.Providers.KubernetesGateway.EntryPoints = entryPoints
	}

	// Configure Ingress NGINX provider.
	if c.Providers.KubernetesIngressNGINX != nil {
		var hasDefinedDefaults bool
		for _, entryPoint := range c.EntryPoints {
			if entryPoint.AsDefault {
				hasDefinedDefaults = true
				break
			}
		}

		var nonTLSEntryPoints []string
		for epName, entryPoint := range c.EntryPoints {
			if hasDefinedDefaults && !entryPoint.AsDefault {
				continue
			}
			// Skip internal entrypoint.
			if epName == DefaultInternalEntryPointName {
				continue
			}
			if entryPoint.HTTP.TLS == nil {
				nonTLSEntryPoints = append(nonTLSEntryPoints, epName)
			}
		}

		c.Providers.KubernetesIngressNGINX.NonTLSEntryPoints = nonTLSEntryPoints
	}

	// Defines the default rule syntax for the Kubernetes Ingress Provider.
	// This allows the provider to adapt the matcher syntax to the desired rule syntax version.
	if c.Core != nil && c.Providers.KubernetesIngress != nil {
		c.Providers.KubernetesIngress.DefaultRuleSyntax = c.Core.DefaultRuleSyntax
	}

	for _, resolver := range c.CertificatesResolvers {
		if resolver.ACME == nil {
			continue
		}

		if resolver.ACME.DNSChallenge == nil {
			continue
		}

		switch resolver.ACME.DNSChallenge.Provider {
		case "googledomains", "cloudxns", "brandit":
			log.Warn().Msgf("%s DNS provider is deprecated.", resolver.ACME.DNSChallenge.Provider)
		case "dnspod":
			log.Warn().Msgf("%s provider is deprecated, please use 'tencentcloud' provider instead.", resolver.ACME.DNSChallenge.Provider)
		case "azure":
			log.Warn().Msgf("%s provider is deprecated, please use 'azuredns' provider instead.", resolver.ACME.DNSChallenge.Provider)
		}

		if resolver.ACME.DNSChallenge.DisablePropagationCheck {
			log.Warn().Msgf("disablePropagationCheck is now deprecated, please use propagation.disableChecks instead.")

			resolver.ACME.DNSChallenge.Propagation.DisableChecks = true
		}

		if resolver.ACME.DNSChallenge.DelayBeforeCheck > 0 {
			log.Warn().Msgf("delayBeforeCheck is now deprecated, please use propagation.delayBeforeChecks instead.")

			resolver.ACME.DNSChallenge.Propagation.DelayBeforeChecks = resolver.ACME.DNSChallenge.DelayBeforeCheck
		}
	}

	for _, resolver := range c.CertificatesResolvers {
		if resolver.ACME == nil {
			continue
		}

		if resolver.ACME.DNSChallenge == nil {
			continue
		}

		switch resolver.ACME.DNSChallenge.Provider {
		case "googledomains", "cloudxns", "brandit":
			log.Warn().Msgf("%s DNS provider is deprecated.", resolver.ACME.DNSChallenge.Provider)
		case "dnspod":
			log.Warn().Msgf("%s provider is deprecated, please use 'tencentcloud' provider instead.", resolver.ACME.DNSChallenge.Provider)
		case "azure":
			log.Warn().Msgf("%s provider is deprecated, please use 'azuredns' provider instead.", resolver.ACME.DNSChallenge.Provider)
		}
	}

	c.initACMEProvider()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Configuration) SetEffectiveConfiguration() {
	// Creates the default entry point if needed
	if !c.hasUserDefinedEntrypoint() {
		ep := &EntryPoint{Address: ":80"}
		ep.SetDefaults()
		// TODO: double check this tomorrow
		if c.EntryPoints == nil {
			c.EntryPoints = make(EntryPoints)
		}
		c.EntryPoints["http"] = ep
	}

	// Creates the internal traefik entry point if needed
	if (c.API != nil && c.API.Insecure) ||
		(c.Ping != nil && !c.Ping.ManualRouting && c.Ping.EntryPoint == DefaultInternalEntryPointName) ||
		(c.Metrics != nil && c.Metrics.Prometheus != nil && !c.Metrics.Prometheus.ManualRouting && c.Metrics.Prometheus.EntryPoint == DefaultInternalEntryPointName) ||
		(c.Providers != nil && c.Providers.Rest != nil && c.Providers.Rest.Insecure) {
		if _, ok := c.EntryPoints[DefaultInternalEntryPointName]; !ok {
			ep := &EntryPoint{Address: ":8080"}
			ep.SetDefaults()
			c.EntryPoints[DefaultInternalEntryPointName] = ep
		}
	}

	// If the entry point exists without an address, which happens when only its options are configured,
	// this ensures the address defaults to :8080.
	if ep, ok := c.EntryPoints[DefaultInternalEntryPointName]; ok && ep.Address == "" {
		ep.Address = ":8080"
	}

	if c.Tracing != nil && c.Tracing.GlobalAttributes != nil && c.Tracing.ResourceAttributes == nil {
		c.Tracing.ResourceAttributes = c.Tracing.GlobalAttributes
	}

	for i, providerName := range c.Providers.Precedence {
		c.Providers.Precedence[i] = strings.ToLower(providerName)
	}

	if c.Providers.Docker != nil {
		if c.Providers.Docker.HTTPClientTimeout < 0 {
			c.Providers.Docker.HTTPClientTimeout = 0
		}
	}

	if c.Providers.Swarm != nil {
		if c.Providers.Swarm.RefreshSeconds <= 0 {
			c.Providers.Swarm.RefreshSeconds = ptypes.Duration(15 * time.Second)
		}

		if c.Providers.Swarm.HTTPClientTimeout < 0 {
			c.Providers.Swarm.HTTPClientTimeout = 0
		}
	}

	// Configure Gateway API provider
	if c.Providers.KubernetesGateway != nil {
		entryPoints := make(map[string]gateway.Entrypoint)
		for epName, entryPoint := range c.EntryPoints {
			entryPoints[epName] = gateway.Entrypoint{Address: entryPoint.GetAddress(), HasHTTPTLSConf: entryPoint.HTTP.TLS != nil}
		}

		if c.Providers.KubernetesCRD != nil {
			c.Providers.KubernetesCRD.FillExtensionBuilderRegistry(c.Providers.KubernetesGateway)
		}

		c.Providers.KubernetesGateway.EntryPoints = entryPoints
	}

	// Configure Ingress NGINX provider.
	if c.Providers.KubernetesIngressNGINX != nil {
		var hasDefinedDefaults bool
		for _, entryPoint := range c.EntryPoints {
			if entryPoint.AsDefault {
				hasDefinedDefaults = true
				break
			}
		}

		var nonTLSEntryPoints []string
		for epName, entryPoint := range c.EntryPoints {
			if hasDefinedDefaults && !entryPoint.AsDefault {
				continue
			}
			// Skip internal entrypoint.
			if epName == DefaultInternalEntryPointName {
				continue
			}
			if entryPoint.HTTP.TLS == nil {
				nonTLSEntryPoints = append(nonTLSEntryPoints, epName)
			}
		}

		c.Providers.KubernetesIngressNGINX.NonTLSEntryPoints = nonTLSEntryPoints
	}

	// Defines the default rule syntax for the Kubernetes Ingress Provider.
	// This allows the provider to adapt the matcher syntax to the desired rule syntax version.
	if c.Core != nil && c.Providers.KubernetesIngress != nil {
		c.Providers.KubernetesIngress.DefaultRuleSyntax = c.Core.DefaultRuleSyntax
	}

	for _, resolver := range c.CertificatesResolvers {
		if resolver.ACME == nil {
			continue
		}

		if resolver.ACME.DNSChallenge == nil {
			continue
		}

		switch resolver.ACME.DNSChallenge.Provider {
		case "googledomains", "cloudxns", "brandit":
			log.Warn().Msgf("%s DNS provider is deprecated.", resolver.ACME.DNSChallenge.Provider)
		case "dnspod":
			log.Warn().Msgf("%s provider is deprecated, please use 'tencentcloud' provider instead.", resolver.ACME.DNSChallenge.Provider)
		case "azure":
			log.Warn().Msgf("%s provider is deprecated, please use 'azuredns' provider instead.", resolver.ACME.DNSChallenge.Provider)
		}

		if resolver.ACME.DNSChallenge.DisablePropagationCheck {
			log.Warn().Msgf("disablePropagationCheck is now deprecated, please use propagation.disableChecks instead.")

			resolver.ACME.DNSChallenge.Propagation.DisableChecks = true
		}

		if resolver.ACME.DNSChallenge.DelayBeforeCheck > 0 {
			log.Warn().Msgf("delayBeforeCheck is now deprecated, please use propagation.delayBeforeChecks instead.")

			resolver.ACME.DNSChallenge.Propagation.DelayBeforeChecks = resolver.ACME.DNSChallenge.DelayBeforeCheck
		}
	}

	for _, resolver := range c.CertificatesResolvers {
		if resolver.ACME == nil {
			continue
		}

		if resolver.ACME.DNSChallenge == nil {
			continue
		}

		switch resolver.ACME.DNSChallenge.Provider {
		case "googledomains", "cloudxns", "brandit":
			log.Warn().Msgf("%s DNS provider is deprecated.", resolver.ACME.DNSChallenge.Provider)
		case "dnspod":
			log.Warn().Msgf("%s provider is deprecated, please use 'tencentcloud' provider instead.", resolver.ACME.DNSChallenge.Provider)
		case "azure":
			log.Warn().Msgf("%s provider is deprecated, please use 'azuredns' provider instead.", resolver.ACME.DNSChallenge.Provider)
		}
	}

	c.initACMEProvider()
}
```


---

### 🔹 Commit #07: `a7089396`
- **完整 Hash**: `a7089396fe1c846a36d2a4d995d1731d9d6d1562`
- **說明 (Ground Truth)**: Ensure that the request TLS state is always set
- **變更檔案數**: 1

#### 📄 檔案: `pkg/server/server_entrypoint_tcp.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:165, E:233, A:0) ➔ After(N:168, E:239, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `tlsConn.ConnectionState (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `populateRequestTLS` (FUNCTION_DEF)
  • + [新增節點] `req.Context().Value (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `createHTTPServer` ──[CALLS]──> `populateRequestTLS`
  • + [新增呼叫邊] `populateRequestTLS` ──[CALLS]──> `http.HandlerFunc (External/Pkg)`
  • + [新增呼叫邊] `populateRequestTLS` ──[CALLS]──> `req.Context().Value (External/Pkg)`
  • + [新增呼叫邊] `populateRequestTLS` ──[CALLS]──> `req.Context (External/Pkg)`
  • + [新增呼叫邊] `populateRequestTLS` ──[CALLS]──> `tlsConn.ConnectionState (External/Pkg)`
  • + [新增呼叫邊] `populateRequestTLS` ──[CALLS]──> `h.ServeHTTP (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `createHTTPServer()`
- **變更前簽章 (Before)**: `func createHTTPServer(ctx context.Context, ln net.Listener, configuration *static.EntryPoint, withH2c bool, reqDecorator *requestdecorator.RequestDecorator)` (L576~L721)
- **變更後簽章 (After)**: `func createHTTPServer(ctx context.Context, ln net.Listener, configuration *static.EntryPoint, withH2c bool, reqDecorator *requestdecorator.RequestDecorator)` (L576~L725)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func createHTTPServer(ctx context.Context, ln net.Listener, configuration *static.EntryPoint, withH2c bool, reqDecorator *requestdecorator.RequestDecorator) (*httpServer, error) {
	if configuration.HTTP2.MaxConcurrentStreams < 0 {
		return nil, errors.New("max concurrent streams value must be greater than or equal to zero")
	}

	httpSwitcher := middlewares.NewHandlerSwitcher(router.BuildDefaultHTTPRouter())

	next, err := alice.New(requestdecorator.WrapHandler(reqDecorator)).Then(httpSwitcher)
	if err != nil {
		return nil, err
	}

	var handler http.Handler
	handler, err = forwardedheaders.NewXForwarded(
		configuration.ForwardedHeaders.Insecure,
		configuration.ForwardedHeaders.TrustedIPs,
		configuration.ForwardedHeaders.Connection,
		next)
	if err != nil {
		return nil, err
	}

	debugConnection := os.Getenv(debugConnectionEnv) != ""
	if debugConnection || (configuration.Transport != nil && (configuration.Transport.KeepAliveMaxTime > 0 || configuration.Transport.KeepAliveMaxRequests > 0)) {
		handler = newKeepAliveMiddleware(handler, configuration.Transport.KeepAliveMaxRequests, configuration.Transport.KeepAliveMaxTime)
	}

	var protocols http.Protocols
	protocols.SetHTTP1(true)
	protocols.SetHTTP2(true)

	// With the addition of UnencryptedHTTP2 in http.Server#Protocols in go1.24 setting the h2c handler is not necessary anymore.
	protocols.SetUnencryptedHTTP2(withH2c)

	if configuration.HTTP.EncodeQuerySemicolons {
		handler = encodeQuerySemicolons(handler)
	} else {
		handler = http.AllowQuerySemicolons(handler)
	}

	handler = routingPath(handler)

	// Note that the Path sanitization has to be done after the path normalization,
	// hence the wrapping has to be done before the normalize path wrapping.
	if configuration.HTTP.SanitizePath != nil && *configuration.HTTP.SanitizePath {
		handler = sanitizePath(handler)
	}

	handler = normalizePath(handler)

	handler = denyFragment(handler)

	switch configuration.HTTP.AliasHeadersStrategy {
	case "":
		// The aliasHeadersStrategy option is not configured, fall back on the deprecated underscoreHeadersStrategy option.
		//nolint:staticcheck // Support of the deprecated underscoreHeadersStrategy option.
		switch configuration.HTTP.UnderscoreHeadersStrategy {
		case "", static.UnderscoreHeadersStrategyKeep:
			// Headers with underscores are forwarded as is.
		case static.UnderscoreHeadersStrategyDelete:
			handler = removeHeadersWithUnderscores(handler)
		case static.UnderscoreHeadersStrategyReject:
			handler = rejectHeadersWithUnderscores(handler)
		default:
			return nil, fmt.Errorf("invalid underscoreHeadersStrategy value %q", configuration.HTTP.UnderscoreHeadersStrategy)
		}
	case static.AliasHeadersStrategyKeep:
		// Headers whose name aliases another header name are forwarded as is.
	case static.AliasHeadersStrategyDelete:
		handler = removeAliasingHeaders(handler)
	case static.AliasHeadersStrategyReject:
		handler = rejectAliasingHeaders(handler)
	default:
		return nil, fmt.Errorf("invalid aliasHeadersStrategy value %q", configuration.HTTP.AliasHeadersStrategy)
	}

	// An opaque URL has to be rejected before any handler deriving the path or the request URI from it,
	// hence the wrapping has to be done last so that it is the first handler executed.
	handler = denyOpaque(handler)

	var connContext multipleConnContext
	connContext.AddConnContextFunc(func(ctx context.Context, c net.Conn) context.Context {
		// This adds an empty struct in order to store a RoundTripper in the ConnContext in case of Kerberos or NTLM.
		ctx = service.AddTransportOnContext(ctx)

		if tlsConn, ok := c.(*tls.Conn); ok {
			if tlsConnWithOptionsName, ok := tlsConn.NetConn().(tcp.TLSConn); ok {
				return tcp.AddTLSOptionsNameInContext(ctx, tlsConnWithOptionsName.TLSOptionsName)
			}
		}

		return ctx
	})

	if debugConnection || (configuration.Transport != nil && (configuration.Transport.KeepAliveMaxTime > 0 || configuration.Transport.KeepAliveMaxRequests > 0)) {
		connContext.AddConnContextFunc(func(ctx context.Context, c net.Conn) context.Context {
			cState := &connState{Start: time.Now()}
			if debugConnection {
				clientConnectionStatesMu.Lock()
				clientConnectionStates[getConnKey(c)] = cState
				clientConnectionStatesMu.Unlock()
			}

			return context.WithValue(ctx, connStateKey, cState)
		})
	}

	var connState func(c net.Conn, state http.ConnState)
	if debugConnection {
		connState = func(c net.Conn, state http.ConnState) {
			clientConnectionStatesMu.Lock()
			if clientConnectionStates[getConnKey(c)] != nil {
				clientConnectionStates[getConnKey(c)].State = state.String()
			}
			clientConnectionStatesMu.Unlock()
		}
	}

	serverHTTP := &http.Server{
		Protocols:      &protocols,
		Handler:        handler,
		ErrorLog:       httpServerLogger,
		ReadTimeout:    time.Duration(configuration.Transport.RespondingTimeouts.ReadTimeout),
		WriteTimeout:   time.Duration(configuration.Transport.RespondingTimeouts.WriteTimeout),
		IdleTimeout:    time.Duration(configuration.Transport.RespondingTimeouts.IdleTimeout),
		MaxHeaderBytes: configuration.HTTP.MaxHeaderBytes,
		HTTP2: &http.HTTP2Config{
			MaxConcurrentStreams: int(configuration.HTTP2.MaxConcurrentStreams),
		},
		ConnContext: connContext.Build(),
		ConnState:   connState,
	}

	listener := newHTTPForwarder(ln)
	go func() {
		err := serverHTTP.Serve(listener)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.FromContext(ctx).Errorf("Error while starting server: %v", err)
		}
	}()
	return &httpServer{
		Server:    serverHTTP,
		Forwarder: listener,
		Switcher:  httpSwitcher,
	}, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func createHTTPServer(ctx context.Context, ln net.Listener, configuration *static.EntryPoint, withH2c bool, reqDecorator *requestdecorator.RequestDecorator) (*httpServer, error) {
	if configuration.HTTP2.MaxConcurrentStreams < 0 {
		return nil, errors.New("max concurrent streams value must be greater than or equal to zero")
	}

	httpSwitcher := middlewares.NewHandlerSwitcher(router.BuildDefaultHTTPRouter())

	next, err := alice.New(requestdecorator.WrapHandler(reqDecorator)).Then(httpSwitcher)
	if err != nil {
		return nil, err
	}

	var handler http.Handler
	handler, err = forwardedheaders.NewXForwarded(
		configuration.ForwardedHeaders.Insecure,
		configuration.ForwardedHeaders.TrustedIPs,
		configuration.ForwardedHeaders.Connection,
		next)
	if err != nil {
		return nil, err
	}

	debugConnection := os.Getenv(debugConnectionEnv) != ""
	if debugConnection || (configuration.Transport != nil && (configuration.Transport.KeepAliveMaxTime > 0 || configuration.Transport.KeepAliveMaxRequests > 0)) {
		handler = newKeepAliveMiddleware(handler, configuration.Transport.KeepAliveMaxRequests, configuration.Transport.KeepAliveMaxTime)
	}

	var protocols http.Protocols
	protocols.SetHTTP1(true)
	protocols.SetHTTP2(true)

	// With the addition of UnencryptedHTTP2 in http.Server#Protocols in go1.24 setting the h2c handler is not necessary anymore.
	protocols.SetUnencryptedHTTP2(withH2c)

	if configuration.HTTP.EncodeQuerySemicolons {
		handler = encodeQuerySemicolons(handler)
	} else {
		handler = http.AllowQuerySemicolons(handler)
	}

	handler = routingPath(handler)

	// Note that the Path sanitization has to be done after the path normalization,
	// hence the wrapping has to be done before the normalize path wrapping.
	if configuration.HTTP.SanitizePath != nil && *configuration.HTTP.SanitizePath {
		handler = sanitizePath(handler)
	}

	handler = normalizePath(handler)

	handler = denyFragment(handler)

	switch configuration.HTTP.AliasHeadersStrategy {
	case "":
		// The aliasHeadersStrategy option is not configured, fall back on the deprecated underscoreHeadersStrategy option.
		//nolint:staticcheck // Support of the deprecated underscoreHeadersStrategy option.
		switch configuration.HTTP.UnderscoreHeadersStrategy {
		case "", static.UnderscoreHeadersStrategyKeep:
			// Headers with underscores are forwarded as is.
		case static.UnderscoreHeadersStrategyDelete:
			handler = removeHeadersWithUnderscores(handler)
		case static.UnderscoreHeadersStrategyReject:
			handler = rejectHeadersWithUnderscores(handler)
		default:
			return nil, fmt.Errorf("invalid underscoreHeadersStrategy value %q", configuration.HTTP.UnderscoreHeadersStrategy)
		}
	case static.AliasHeadersStrategyKeep:
		// Headers whose name aliases another header name are forwarded as is.
	case static.AliasHeadersStrategyDelete:
		handler = removeAliasingHeaders(handler)
	case static.AliasHeadersStrategyReject:
		handler = rejectAliasingHeaders(handler)
	default:
		return nil, fmt.Errorf("invalid aliasHeadersStrategy value %q", configuration.HTTP.AliasHeadersStrategy)
	}

	// An opaque URL has to be rejected before any handler deriving the path or the request URI from it,
	// hence the wrapping has to be done last so that it is the first handler executed.
	handler = denyOpaque(handler)

	handler = populateRequestTLS(handler)

	var connContext multipleConnContext
	connContext.AddConnContextFunc(func(ctx context.Context, c net.Conn) context.Context {
		// This adds an empty struct in order to store a RoundTripper in the ConnContext in case of Kerberos or NTLM.
		ctx = service.AddTransportOnContext(ctx)

		if tlsConn, ok := c.(*tls.Conn); ok {
			ctx = context.WithValue(ctx, tlsConnKey{}, tlsConn)

			if tlsConnWithOptionsName, ok := tlsConn.NetConn().(tcp.TLSConn); ok {
				return tcp.AddTLSOptionsNameInContext(ctx, tlsConnWithOptionsName.TLSOptionsName)
			}
		}

		return ctx
	})

	if debugConnection || (configuration.Transport != nil && (configuration.Transport.KeepAliveMaxTime > 0 || configuration.Transport.KeepAliveMaxRequests > 0)) {
		connContext.AddConnContextFunc(func(ctx context.Context, c net.Conn) context.Context {
			cState := &connState{Start: time.Now()}
			if debugConnection {
				clientConnectionStatesMu.Lock()
				clientConnectionStates[getConnKey(c)] = cState
				clientConnectionStatesMu.Unlock()
			}

			return context.WithValue(ctx, connStateKey, cState)
		})
	}

	var connState func(c net.Conn, state http.ConnState)
	if debugConnection {
		connState = func(c net.Conn, state http.ConnState) {
			clientConnectionStatesMu.Lock()
			if clientConnectionStates[getConnKey(c)] != nil {
				clientConnectionStates[getConnKey(c)].State = state.String()
			}
			clientConnectionStatesMu.Unlock()
		}
	}

	serverHTTP := &http.Server{
		Protocols:      &protocols,
		Handler:        handler,
		ErrorLog:       httpServerLogger,
		ReadTimeout:    time.Duration(configuration.Transport.RespondingTimeouts.ReadTimeout),
		WriteTimeout:   time.Duration(configuration.Transport.RespondingTimeouts.WriteTimeout),
		IdleTimeout:    time.Duration(configuration.Transport.RespondingTimeouts.IdleTimeout),
		MaxHeaderBytes: configuration.HTTP.MaxHeaderBytes,
		HTTP2: &http.HTTP2Config{
			MaxConcurrentStreams: int(configuration.HTTP2.MaxConcurrentStreams),
		},
		ConnContext: connContext.Build(),
		ConnState:   connState,
	}

	listener := newHTTPForwarder(ln)
	go func() {
		err := serverHTTP.Serve(listener)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.FromContext(ctx).Errorf("Error while starting server: %v", err)
		}
	}()
	return &httpServer{
		Server:    serverHTTP,
		Forwarder: listener,
		Switcher:  httpSwitcher,
	}, nil
}
```


---

### 🔹 Commit #08: `e0c2da51`
- **完整 Hash**: `e0c2da5104e4218f47177acb971380fa747add0a`
- **說明 (Ground Truth)**: Fix TLSRoute router name collision across listeners sharing an entry point
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/gateway/tlsroute.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:62, E:74, A:0) ➔ After(N:62, E:74, A:0)
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

### 🔹 函式: `Provider.loadTLSRoute()`
- **變更前簽章 (Before)**: `func Provider.loadTLSRoute(gatewayName, gatewayNamespace string, listener gatewayListener, route *gatev1.TLSRoute, hostnames []gatev1.Hostname)` (L150~L222)
- **變更後簽章 (After)**: `func Provider.loadTLSRoute(gatewayName, gatewayNamespace string, listener gatewayListener, route *gatev1.TLSRoute, hostnames []gatev1.Hostname)` (L150~L223)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) loadTLSRoute(gatewayName, gatewayNamespace string, listener gatewayListener, route *gatev1.TLSRoute, hostnames []gatev1.Hostname) ([]tlsRouteRouter, metav1.Condition) {
	var routers []tlsRouteRouter

	condition := metav1.Condition{
		Type:               string(gatev1.RouteConditionResolvedRefs),
		Status:             metav1.ConditionTrue,
		ObservedGeneration: route.Generation,
		LastTransitionTime: metav1.Now(),
		Reason:             string(gatev1.RouteConditionResolvedRefs),
	}

	for ri, routeRule := range route.Spec.Rules {
		if len(routeRule.BackendRefs) == 0 {
			// Should not happen due to validation.
			// https://github.com/kubernetes-sigs/gateway-api/blob/v0.4.0/apis/v1alpha2/tlsroute_types.go#L120
			continue
		}

		rule, priority := hostSNIRule(hostnames)
		router := dynamic.TCPRouter{
			RuleSyntax:  "default",
			Rule:        rule,
			Priority:    priority,
			EntryPoints: []string{listener.EPName},
			TLS: &dynamic.RouterTCPTLSConfig{
				Passthrough: listener.TLS != nil && listener.TLS.Mode != nil && *listener.TLS.Mode == gatev1.TLSModePassthrough,
			},
		}

		// Routing criteria should be introduced at some point.
		routerName := makeRouterName(strings.ToLower(kindTLSRoute), "", route.Namespace, route.Name, gatewayNamespace, gatewayName, listener.EPName, ri)

		routerConf := &dynamic.Configuration{
			TCP: &dynamic.TCPConfiguration{
				Routers:           make(map[string]*dynamic.TCPRouter),
				Middlewares:       make(map[string]*dynamic.TCPMiddleware),
				Services:          make(map[string]*dynamic.TCPService),
				ServersTransports: make(map[string]*dynamic.TCPServersTransport),
			},
		}

		if len(routeRule.BackendRefs) == 1 && isInternalService(routeRule.BackendRefs[0]) {
			if !isCrossProviderNamespaceAllowed(p.CrossProviderNamespaces, route.Namespace) {
				condition = metav1.Condition{
					Type:               string(gatev1.RouteConditionResolvedRefs),
					Status:             metav1.ConditionFalse,
					ObservedGeneration: route.Generation,
					LastTransitionTime: metav1.Now(),
					Reason:             string(gatev1.RouteReasonRefNotPermitted),
					Message:            fmt.Sprintf("Cannot load TLSRoute BackendRef %s: internal service reference is not allowed: TLSRoute namespace %q is not in crossProviderNamespaces", routeRule.BackendRefs[0].Name, route.Namespace),
				}

				continue
			}

			router.Service = string(routeRule.BackendRefs[0].Name)
			routerConf.TCP.Routers[routerName] = &router
			routers = append(routers, tlsRouteRouter{Name: routerName, Conf: routerConf})
			continue
		}

		var serviceCondition *metav1.Condition
		router.Service, serviceCondition = p.loadTLSWRRService(routerConf, routerName, routeRule.BackendRefs, route)
		if serviceCondition != nil {
			condition = *serviceCondition
		}

		routerConf.TCP.Routers[routerName] = &router
		routers = append(routers, tlsRouteRouter{Name: routerName, Conf: routerConf})
	}

	return routers, condition
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) loadTLSRoute(gatewayName, gatewayNamespace string, listener gatewayListener, route *gatev1.TLSRoute, hostnames []gatev1.Hostname) ([]tlsRouteRouter, metav1.Condition) {
	var routers []tlsRouteRouter

	condition := metav1.Condition{
		Type:               string(gatev1.RouteConditionResolvedRefs),
		Status:             metav1.ConditionTrue,
		ObservedGeneration: route.Generation,
		LastTransitionTime: metav1.Now(),
		Reason:             string(gatev1.RouteConditionResolvedRefs),
	}

	for ri, routeRule := range route.Spec.Rules {
		if len(routeRule.BackendRefs) == 0 {
			// Should not happen due to validation.
			// https://github.com/kubernetes-sigs/gateway-api/blob/v0.4.0/apis/v1alpha2/tlsroute_types.go#L120
			continue
		}

		rule, priority := hostSNIRule(hostnames)
		router := dynamic.TCPRouter{
			RuleSyntax:  "default",
			Rule:        rule,
			Priority:    priority,
			EntryPoints: []string{listener.EPName},
			TLS: &dynamic.RouterTCPTLSConfig{
				Passthrough: listener.TLS != nil && listener.TLS.Mode != nil && *listener.TLS.Mode == gatev1.TLSModePassthrough,
			},
		}

		// The rule tells apart the routers of the listeners sharing the entry point,
		// as they differ by the hostnames they match.
		routerName := makeRouterName(strings.ToLower(kindTLSRoute), rule, route.Namespace, route.Name, gatewayNamespace, gatewayName, listener.EPName, ri)

		routerConf := &dynamic.Configuration{
			TCP: &dynamic.TCPConfiguration{
				Routers:           make(map[string]*dynamic.TCPRouter),
				Middlewares:       make(map[string]*dynamic.TCPMiddleware),
				Services:          make(map[string]*dynamic.TCPService),
				ServersTransports: make(map[string]*dynamic.TCPServersTransport),
			},
		}

		if len(routeRule.BackendRefs) == 1 && isInternalService(routeRule.BackendRefs[0]) {
			if !isCrossProviderNamespaceAllowed(p.CrossProviderNamespaces, route.Namespace) {
				condition = metav1.Condition{
					Type:               string(gatev1.RouteConditionResolvedRefs),
					Status:             metav1.ConditionFalse,
					ObservedGeneration: route.Generation,
					LastTransitionTime: metav1.Now(),
					Reason:             string(gatev1.RouteReasonRefNotPermitted),
					Message:            fmt.Sprintf("Cannot load TLSRoute BackendRef %s: internal service reference is not allowed: TLSRoute namespace %q is not in crossProviderNamespaces", routeRule.BackendRefs[0].Name, route.Namespace),
				}

				continue
			}

			router.Service = string(routeRule.BackendRefs[0].Name)
			routerConf.TCP.Routers[routerName] = &router
			routers = append(routers, tlsRouteRouter{Name: routerName, Conf: routerConf})
			continue
		}

		var serviceCondition *metav1.Condition
		router.Service, serviceCondition = p.loadTLSWRRService(routerConf, routerName, routeRule.BackendRefs, route)
		if serviceCondition != nil {
			condition = *serviceCondition
		}

		routerConf.TCP.Routers[routerName] = &router
		routers = append(routers, tlsRouteRouter{Name: routerName, Conf: routerConf})
	}

	return routers, condition
}
```


---

### 🔹 Commit #09: `bab93de2`
- **完整 Hash**: `bab93de245fd21d1d81deba81212a8cd4b243f4e`
- **說明 (Ground Truth)**: Fix the second server selection bias in the P2C load balancer
- **變更檔案數**: 1

#### 📄 檔案: `pkg/server/service/loadbalancer/p2c/p2c.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:43, E:46, A:0) ➔ After(N:43, E:46, A:0)
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

### 🔹 函式: `Balancer.nextServer()`
- **變更前簽章 (Before)**: `func Balancer.nextServer()` (L195~L237)
- **變更後簽章 (After)**: `func Balancer.nextServer()` (L195~L237)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (b *Balancer) nextServer() (*namedHandler, error) {
	// We kept the same representation (map) as in the WRR strategy to improve maintainability.
	// However, with the P2C strategy, we only need a slice of healthy servers.
	b.handlersMu.RLock()
	var healthy []*namedHandler
	for _, h := range b.handlers {
		if _, ok := b.status[h.name]; ok {
			if _, fenced := b.fenced[h.name]; !fenced {
				healthy = append(healthy, h)
			}
		}
	}
	b.handlersMu.RUnlock()

	if len(healthy) == 0 {
		return nil, errNoAvailableServer
	}

	// If there is only one healthy server, return it.
	if len(healthy) == 1 {
		return healthy[0], nil
	}
	// In order to not get the same backend twice, we make the second call to s.rand.Intn one fewer
	// than the length of the slice. We then have to shift over the second index if it is equal or
	// greater than the first index, wrapping round if needed.
	b.randMu.Lock()
	n1, n2 := b.rand.Intn(len(healthy)), b.rand.Intn(len(healthy))
	b.randMu.Unlock()

	if n2 == n1 {
		n2 = (n2 + 1) % len(healthy)
	}

	h1, h2 := healthy[n1], healthy[n2]
	// Ensure h1 has fewer inflight requests than h2.
	if h2.inflight.Load() < h1.inflight.Load() {
		log.Debug().Msgf("Service selected by P2C: %s", h2.name)
		return h2, nil
	}

	log.Debug().Msgf("Service selected by P2C: %s", h1.name)
	return h1, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (b *Balancer) nextServer() (*namedHandler, error) {
	// We kept the same representation (map) as in the WRR strategy to improve maintainability.
	// However, with the P2C strategy, we only need a slice of healthy servers.
	b.handlersMu.RLock()
	var healthy []*namedHandler
	for _, h := range b.handlers {
		if _, ok := b.status[h.name]; ok {
			if _, fenced := b.fenced[h.name]; !fenced {
				healthy = append(healthy, h)
			}
		}
	}
	b.handlersMu.RUnlock()

	if len(healthy) == 0 {
		return nil, errNoAvailableServer
	}

	// If there is only one healthy server, return it.
	if len(healthy) == 1 {
		return healthy[0], nil
	}
	// In order to not get the same backend twice, we make the second call to b.rand.Intn one fewer
	// than the length of the slice. We then have to shift over the second index if it is equal or
	// greater than the first index.
	b.randMu.Lock()
	n1, n2 := b.rand.Intn(len(healthy)), b.rand.Intn(len(healthy)-1)
	b.randMu.Unlock()

	if n2 >= n1 {
		n2++
	}

	h1, h2 := healthy[n1], healthy[n2]
	// Ensure h1 has fewer inflight requests than h2.
	if h2.inflight.Load() < h1.inflight.Load() {
		log.Debug().Msgf("Service selected by P2C: %s", h2.name)
		return h2, nil
	}

	log.Debug().Msgf("Service selected by P2C: %s", h1.name)
	return h1, nil
}
```


---

### 🔹 Commit #10: `8b809992`
- **完整 Hash**: `8b8099929fe85ebb45a28f16c2a3b35af992eefd`
- **說明 (Ground Truth)**: Fix misleading trailer comments in header strategy handlers
- **變更檔案數**: 1

#### 📄 檔案: `pkg/server/server_entrypoint_tcp.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:194, E:270, A:0) ➔ After(N:194, E:270, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 2 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #11: `9eb2b0e8`
- **完整 Hash**: `9eb2b0e8e29dc011c9587311b1bf098ad77c8d3c`
- **說明 (Ground Truth)**: Stable sort Gateways to keep the TLS certificate order stable
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/gateway/kubernetes.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:187, E:240, A:0) ➔ After(N:187, E:250, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 1, +Edges: 11, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cmp.Or (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `cmp.Compare (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `slices.SortStableFunc (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `cmp.Or (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `a.GetCreationTimestamp().Time.Compare (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `a.GetCreationTimestamp (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `b.GetCreationTimestamp (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `a.GetNamespace (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `b.GetNamespace (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `a.GetName (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadConfigurationFromGateways` ──[CALLS]──> `b.GetName (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadHTTPAndGRPCRoutes` ──[CALLS]──> `cmp.Or (External/Pkg)`
  • + [新增呼叫邊] `Provider.loadHTTPAndGRPCRoutes` ──[CALLS]──> `strings.Compare (External/Pkg)`
  • - [移除呼叫邊] `Provider.loadHTTPAndGRPCRoutes` ──[CALLS]──> `cmp.Compare (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.loadHTTPAndGRPCRoutes()`
- **變更前簽章 (Before)**: `func Provider.loadHTTPAndGRPCRoutes(ctx context.Context, gateways []gatewayWithListeners, conf *dynamic.Configuration)` (L485~L520)
- **變更後簽章 (After)**: `func Provider.loadHTTPAndGRPCRoutes(ctx context.Context, gateways []gatewayWithListeners, conf *dynamic.Configuration)` (L491~L525)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) loadHTTPAndGRPCRoutes(ctx context.Context, gateways []gatewayWithListeners, conf *dynamic.Configuration) {
	routes := make([]metav1.Object, 0)

	httpRoutes, err := p.client.ListHTTPRoutes()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list HTTPRoutes")
	}
	for _, route := range httpRoutes {
		routes = append(routes, route)
	}

	grpcRoutes, err := p.client.ListGRPCRoutes()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list GRPCRoutes")
	}
	for _, route := range grpcRoutes {
		routes = append(routes, route)
	}

	slices.SortStableFunc(routes, func(a, b metav1.Object) int {
		if c := a.GetCreationTimestamp().Time.Compare(b.GetCreationTimestamp().Time); c != 0 {
			return c
		}
		return cmp.Compare(a.GetNamespace()+"/"+a.GetName(), b.GetNamespace()+"/"+b.GetName())
	})

	attached := make(attachedRoutes)
	for _, route := range routes {
		switch route := route.(type) {
		case *gatev1.HTTPRoute:
			p.loadHTTPRoute(ctx, gateways, route, conf, attached)
		case *gatev1.GRPCRoute:
			p.loadGRPCRoute(ctx, gateways, route, conf, attached)
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) loadHTTPAndGRPCRoutes(ctx context.Context, gateways []gatewayWithListeners, conf *dynamic.Configuration) {
	routes := make([]metav1.Object, 0)

	httpRoutes, err := p.client.ListHTTPRoutes()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list HTTPRoutes")
	}
	for _, route := range httpRoutes {
		routes = append(routes, route)
	}

	grpcRoutes, err := p.client.ListGRPCRoutes()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list GRPCRoutes")
	}
	for _, route := range grpcRoutes {
		routes = append(routes, route)
	}

	slices.SortStableFunc(routes, func(a, b metav1.Object) int {
		return cmp.Or(a.GetCreationTimestamp().Time.Compare(b.GetCreationTimestamp().Time),
			strings.Compare(a.GetNamespace(), b.GetNamespace()),
			strings.Compare(a.GetName(), b.GetName()))
	})

	attached := make(attachedRoutes)
	for _, route := range routes {
		switch route := route.(type) {
		case *gatev1.HTTPRoute:
			p.loadHTTPRoute(ctx, gateways, route, conf, attached)
		case *gatev1.GRPCRoute:
			p.loadGRPCRoute(ctx, gateways, route, conf, attached)
		}
	}
}
```

### 🔹 函式: `Provider.loadConfigurationFromGateways()`
- **變更前簽章 (Before)**: `func Provider.loadConfigurationFromGateways(ctx context.Context)` (L340~L479)
- **變更後簽章 (After)**: `func Provider.loadConfigurationFromGateways(ctx context.Context)` (L340~L485)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) loadConfigurationFromGateways(ctx context.Context) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           map[string]*dynamic.Router{},
			Middlewares:       map[string]*dynamic.Middleware{},
			Services:          map[string]*dynamic.Service{},
			ServersTransports: map[string]*dynamic.ServersTransport{},
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:           map[string]*dynamic.TCPRouter{},
			Middlewares:       map[string]*dynamic.TCPMiddleware{},
			Services:          map[string]*dynamic.TCPService{},
			ServersTransports: map[string]*dynamic.TCPServersTransport{},
		},
		UDP: &dynamic.UDPConfiguration{
			Routers:  map[string]*dynamic.UDPRouter{},
			Services: map[string]*dynamic.UDPService{},
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	addresses, err := p.gatewayAddresses()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to get Gateway status addresses")
		return nil
	}

	gatewayClasses, err := p.client.ListGatewayClasses()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list GatewayClasses")
		return nil
	}

	var supportedFeatures []gatev1.SupportedFeature
	for _, feature := range SupportedFeatures() {
		supportedFeatures = append(supportedFeatures, gatev1.SupportedFeature{Name: gatev1.FeatureName(feature)})
	}
	slices.SortFunc(supportedFeatures, func(a, b gatev1.SupportedFeature) int {
		return strings.Compare(string(a.Name), string(b.Name))
	})

	gatewayClassNames := map[string]struct{}{}
	for _, gatewayClass := range gatewayClasses {
		if gatewayClass.Spec.ControllerName != controllerName {
			continue
		}

		gatewayClassNames[gatewayClass.Name] = struct{}{}

		status := gatev1.GatewayClassStatus{
			Conditions: upsertGatewayClassConditionAccepted(gatewayClass.Status.Conditions, metav1.Condition{
				Type:               string(gatev1.GatewayClassConditionStatusAccepted),
				Status:             metav1.ConditionTrue,
				ObservedGeneration: gatewayClass.Generation,
				Reason:             "Handled",
				Message:            "Handled by Traefik controller",
				LastTransitionTime: metav1.Now(),
			}),
			SupportedFeatures: supportedFeatures,
		}

		if err := p.client.UpdateGatewayClassStatus(ctx, gatewayClass.Name, status); err != nil {
			log.Ctx(ctx).
				Warn().
				Err(err).
				Str("gateway_class", gatewayClass.Name).
				Msg("Unable to update GatewayClass status")
		}
	}

	var gateways []*gatev1.Gateway
	for _, gateway := range p.client.ListGateways() {
		if _, ok := gatewayClassNames[string(gateway.Spec.GatewayClassName)]; !ok {
			continue
		}
		if !p.managesGateway(gateway) {
			continue
		}
		gateways = append(gateways, gateway)
	}

	var selectedGateways []gatewayWithListeners
	for _, gateway := range gateways {
		logger := log.Ctx(ctx).With().
			Str("gateway", gateway.Name).
			Str("namespace", gateway.Namespace).
			Logger()

		selectedGateways = append(selectedGateways, gatewayWithListeners{
			Name:      gateway.Name,
			Namespace: gateway.Namespace,
			listeners: p.loadGatewayListeners(logger.WithContext(ctx), gateway, conf),
		})
	}

	p.loadHTTPAndGRPCRoutes(ctx, selectedGateways, conf)

	p.loadTLSRoutes(ctx, selectedGateways, conf)

	if p.ExperimentalChannel {
		p.loadTCPRoutes(ctx, selectedGateways, conf)
	}

	for _, gateway := range gateways {
		logger := log.Ctx(ctx).With().
			Str("gateway", gateway.Name).
			Str("namespace", gateway.Namespace).
			Logger()

		var listeners []gatewayListener
		for _, selectedGateway := range selectedGateways {
			if selectedGateway.Name == gateway.Name && selectedGateway.Namespace == gateway.Namespace {
				listeners = append(listeners, selectedGateway.listeners...)
			}
		}

		gatewayStatus, errConditions := p.makeGatewayStatus(gateway, listeners, addresses)
		if len(errConditions) > 0 {
			messages := map[string]struct{}{}
			for _, condition := range errConditions {
				messages[condition.Message] = struct{}{}
			}
			var conditionsErr error
			for message := range messages {
				conditionsErr = errors.Join(conditionsErr, errors.New(message))
			}
			logger.Debug().
				Err(conditionsErr).
				Msg("Gateway Not Accepted")
		}

		if err = p.client.UpdateGatewayStatus(ctx, ktypes.NamespacedName{Name: gateway.Name, Namespace: gateway.Namespace}, gatewayStatus); err != nil {
			logger.Warn().
				Err(err).
				Msg("Unable to update Gateway status")
		}
	}

	return conf
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) loadConfigurationFromGateways(ctx context.Context) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           map[string]*dynamic.Router{},
			Middlewares:       map[string]*dynamic.Middleware{},
			Services:          map[string]*dynamic.Service{},
			ServersTransports: map[string]*dynamic.ServersTransport{},
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:           map[string]*dynamic.TCPRouter{},
			Middlewares:       map[string]*dynamic.TCPMiddleware{},
			Services:          map[string]*dynamic.TCPService{},
			ServersTransports: map[string]*dynamic.TCPServersTransport{},
		},
		UDP: &dynamic.UDPConfiguration{
			Routers:  map[string]*dynamic.UDPRouter{},
			Services: map[string]*dynamic.UDPService{},
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	addresses, err := p.gatewayAddresses()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to get Gateway status addresses")
		return nil
	}

	gatewayClasses, err := p.client.ListGatewayClasses()
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msg("Unable to list GatewayClasses")
		return nil
	}

	var supportedFeatures []gatev1.SupportedFeature
	for _, feature := range SupportedFeatures() {
		supportedFeatures = append(supportedFeatures, gatev1.SupportedFeature{Name: gatev1.FeatureName(feature)})
	}
	slices.SortFunc(supportedFeatures, func(a, b gatev1.SupportedFeature) int {
		return strings.Compare(string(a.Name), string(b.Name))
	})

	gatewayClassNames := map[string]struct{}{}
	for _, gatewayClass := range gatewayClasses {
		if gatewayClass.Spec.ControllerName != controllerName {
			continue
		}

		gatewayClassNames[gatewayClass.Name] = struct{}{}

		status := gatev1.GatewayClassStatus{
			Conditions: upsertGatewayClassConditionAccepted(gatewayClass.Status.Conditions, metav1.Condition{
				Type:               string(gatev1.GatewayClassConditionStatusAccepted),
				Status:             metav1.ConditionTrue,
				ObservedGeneration: gatewayClass.Generation,
				Reason:             "Handled",
				Message:            "Handled by Traefik controller",
				LastTransitionTime: metav1.Now(),
			}),
			SupportedFeatures: supportedFeatures,
		}

		if err := p.client.UpdateGatewayClassStatus(ctx, gatewayClass.Name, status); err != nil {
			log.Ctx(ctx).
				Warn().
				Err(err).
				Str("gateway_class", gatewayClass.Name).
				Msg("Unable to update GatewayClass status")
		}
	}

	var gateways []*gatev1.Gateway
	for _, gateway := range p.client.ListGateways() {
		if _, ok := gatewayClassNames[string(gateway.Spec.GatewayClassName)]; !ok {
			continue
		}
		if !p.managesGateway(gateway) {
			continue
		}
		gateways = append(gateways, gateway)
	}

	slices.SortStableFunc(gateways, func(a, b *gatev1.Gateway) int {
		return cmp.Or(a.GetCreationTimestamp().Time.Compare(b.GetCreationTimestamp().Time),
			strings.Compare(a.GetNamespace(), b.GetNamespace()),
			strings.Compare(a.GetName(), b.GetName()))
	})

	var selectedGateways []gatewayWithListeners
	for _, gateway := range gateways {
		logger := log.Ctx(ctx).With().
			Str("gateway", gateway.Name).
			Str("namespace", gateway.Namespace).
			Logger()

		selectedGateways = append(selectedGateways, gatewayWithListeners{
			Name:      gateway.Name,
			Namespace: gateway.Namespace,
			listeners: p.loadGatewayListeners(logger.WithContext(ctx), gateway, conf),
		})
	}

	p.loadHTTPAndGRPCRoutes(ctx, selectedGateways, conf)

	p.loadTLSRoutes(ctx, selectedGateways, conf)

	if p.ExperimentalChannel {
		p.loadTCPRoutes(ctx, selectedGateways, conf)
	}

	for _, gateway := range gateways {
		logger := log.Ctx(ctx).With().
			Str("gateway", gateway.Name).
			Str("namespace", gateway.Namespace).
			Logger()

		var listeners []gatewayListener
		for _, selectedGateway := range selectedGateways {
			if selectedGateway.Name == gateway.Name && selectedGateway.Namespace == gateway.Namespace {
				listeners = append(listeners, selectedGateway.listeners...)
			}
		}

		gatewayStatus, errConditions := p.makeGatewayStatus(gateway, listeners, addresses)
		if len(errConditions) > 0 {
			messages := map[string]struct{}{}
			for _, condition := range errConditions {
				messages[condition.Message] = struct{}{}
			}
			var conditionsErr error
			for message := range messages {
				conditionsErr = errors.Join(conditionsErr, errors.New(message))
			}
			logger.Debug().
				Err(conditionsErr).
				Msg("Gateway Not Accepted")
		}

		if err = p.client.UpdateGatewayStatus(ctx, ktypes.NamespacedName{Name: gateway.Name, Namespace: gateway.Namespace}, gatewayStatus); err != nil {
			logger.Warn().
				Err(err).
				Msg("Unable to update Gateway status")
		}
	}

	return conf
}
```


---

### 🔹 Commit #12: `b497a87f`
- **完整 Hash**: `b497a87f87f7a97b5242024e011fdbc09fee07f1`
- **說明 (Ground Truth)**: Copy UDP datagrams into right-sized buffers before queuing
- **變更檔案數**: 1

#### 📄 檔案: `pkg/udp/conn.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:48, E:57, A:0) ➔ After(N:48, E:58, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 1, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `Listener.readLoop` ──[CALLS]──> `copy (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Listener.readLoop()`
- **變更前簽章 (Before)**: `func Listener.readLoop()` (L127~L149)
- **變更後簽章 (After)**: `func Listener.readLoop()` (L127~L154)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (l *Listener) readLoop() {
	for {
		// Allocating a new buffer for every read avoids
		// overwriting data in c.msgs in case the next packet is received
		// before c.msgs is emptied via Read()
		buf := make([]byte, maxDatagramSize)

		n, raddr, err := l.pConn.ReadFrom(buf)
		if err != nil {
			return
		}
		conn, err := l.getConn(raddr)
		if err != nil {
			continue
		}

		select {
		case conn.receiveCh <- buf[:n]:
		case <-conn.doneCh:
			continue
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (l *Listener) readLoop() {
	// The read buffer must be able to hold the largest possible datagram,
	// as ReadFrom silently discards the bytes that do not fit.
	buf := make([]byte, maxDatagramSize)

	for {
		n, raddr, err := l.pConn.ReadFrom(buf)
		if err != nil {
			return
		}
		conn, err := l.getConn(raddr)
		if err != nil {
			continue
		}

		// The datagram is copied into a buffer of its own size before being queued in c.msgs.
		// Queuing buf[:n] directly would retain the whole maxDatagramSize backing array for each queued datagram,
		// and would require allocating a new read buffer for every datagram to avoid overwriting queued data.
		msg := make([]byte, n)
		copy(msg, buf[:n])

		select {
		case conn.receiveCh <- msg:
		case <-conn.doneCh:
			continue
		}
	}
}
```


---

### 🔹 Commit #13: `013f84fb`
- **完整 Hash**: `013f84fbe1b83dcc304521bd203b1e1985853481`
- **說明 (Ground Truth)**: Do not normalize resource names in the ingress-nginx provider
- **變更檔案數**: 2

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:121, E:180, A:0) ➔ After(N:120, E:177, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 3, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `strings.TrimPrefix (External/Pkg)` (FUNCTION_DEF)
  • - [移除呼叫邊] `Provider.build` ──[CALLS]──> `strings.TrimPrefix (External/Pkg)`
  • - [移除呼叫邊] `Provider.buildServersTransport` ──[CALLS]──> `provider.Normalize (External/Pkg)`
  • - [移除呼叫邊] `Provider.resolveBackend` ──[CALLS]──> `provider.Normalize (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L640)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L640)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := provider.Normalize(canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough: handled per-rule.
		if ptr.Deref(ing.config.SSLPassthrough, false) {
			// Even with ssl-passthrough, the Spec.TLS section's certificates are still loaded so they remain available as the default certificate.
			hasTLS := len(ing.Spec.TLS) > 0
			if hasTLS {
				if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
					logger.Warn().Err(err).Msg("Error loading TLS certificates for ssl-passthrough ingress")
				}
			}
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := provider.Normalize(ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				routerKey := strings.TrimPrefix(provider.Normalize(ing.Namespace+"-"+ing.Name+"-"+rule.Host), "-")
				ptBackend := &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   routerKey,
					SSLRedirect: sslRedirectEnabled(ing.config, hasTLS),
					Config:      ing.config,
				}

				// The serversTransport only shapes the HTTP router: when it cannot be built,
				// the TCP passthrough router must still be created.
				nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot build serversTransport for ssl-passthrough on host %q, skipping its HTTP router", rule.Host)
				} else {
					ptBackend.HTTPServiceName = provider.Normalize(ing.Namespace + "-" + ing.Name + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
					ptBackend.ServersTransportName = nst.name
					ptBackend.ServersTransport = nst.ServersTransport
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, ptBackend)
				markProcessedIngress(ing.Ingress)
			}
			continue
		}

		// Normal ingress: build serversTransport, TLS options, TLS certs, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}
		// Load TLS certificates into the shared mc.Certs map first. They are kept
		// even when the rest of the ingress is later skipped (e.g. when an
		// auth-tls-secret fails to resolve), so the default certificate pool stays
		// consistent. When loading fails, hasTLS still signals that the ingress has
		// a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := provider.Normalize(secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey)

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-default-backend")
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:        canaryBackendName,
						Namespace:   canaryIngress.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough: handled per-rule.
		if ptr.Deref(ing.config.SSLPassthrough, false) {
			// Even with ssl-passthrough, the Spec.TLS section's certificates are still loaded so they remain available as the default certificate.
			hasTLS := len(ing.Spec.TLS) > 0
			if hasTLS {
				if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
					logger.Warn().Err(err).Msg("Error loading TLS certificates for ssl-passthrough ingress")
				}
			}
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:        ptBackendName,
						Namespace:   ing.Namespace,
						ServiceName: ingBackend.Service.Name,
						ServicePort: portString(ingBackend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				routerKey := ing.Namespace + "-" + ing.Name + "-" + provider.Normalize(rule.Host)
				ptBackend := &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   routerKey,
					SSLRedirect: sslRedirectEnabled(ing.config, hasTLS),
					Config:      ing.config,
				}

				// The serversTransport only shapes the HTTP router: when it cannot be built,
				// the TCP passthrough router must still be created.
				nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot build serversTransport for ssl-passthrough on host %q, skipping its HTTP router", rule.Host)
				} else {
					ptBackend.HTTPServiceName = ing.Namespace + "-" + ing.Name + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
					ptBackend.ServersTransportName = nst.name
					ptBackend.ServersTransport = nst.ServersTransport
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, ptBackend)
				markProcessedIngress(ing.Ingress)
			}
			continue
		}

		// Normal ingress: build serversTransport, TLS options, TLS certs, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}
		// Load TLS certificates into the shared mc.Certs map first. They are kept
		// even when the rest of the ingress is later skipped (e.g. when an
		// auth-tls-secret fails to resolve), so the default certificate pool stays
		// consistent. When loading fails, hasTLS still signals that the ingress has
		// a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port)
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:        backendName,
						Namespace:   ing.Namespace,
						ServiceName: pa.Backend.Service.Name,
						ServicePort: portString(pa.Backend.Service.Port),
						Endpoints:   endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:        errBackendName,
										Namespace:   ing.Namespace,
										ServiceName: defaultSvcName,
										ServicePort: "0",
										Endpoints:   endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						ServicePort: portString(db.Service.Port),
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := ing.Namespace + "-" + ing.Name + "-default-backend"
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:        ingDefaultBackendName,
					Namespace:   ing.Namespace,
					ServiceName: db.Service.Name,
					ServicePort: portString(db.Service.Port),
					Endpoints:   endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

### 🔹 函式: `Provider.resolveBackend()`
- **變更前簽章 (Before)**: `func Provider.resolveBackend(namespace string, ingBackend netv1.IngressBackend, cfg IngressConfig)` (L796~L810)
- **變更後簽章 (After)**: `func Provider.resolveBackend(namespace string, ingBackend netv1.IngressBackend, cfg IngressConfig)` (L796~L810)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) resolveBackend(namespace string, ingBackend netv1.IngressBackend, cfg IngressConfig) (*backend, error) {
	endpoints, err := p.getBackendEndpoints(namespace, ingBackend, cfg)
	if err != nil {
		return nil, err
	}

	name := provider.Normalize(namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
	return &backend{
		Name:        name,
		Namespace:   namespace,
		ServiceName: ingBackend.Service.Name,
		ServicePort: portString(ingBackend.Service.Port),
		Endpoints:   endpoints,
	}, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) resolveBackend(namespace string, ingBackend netv1.IngressBackend, cfg IngressConfig) (*backend, error) {
	endpoints, err := p.getBackendEndpoints(namespace, ingBackend, cfg)
	if err != nil {
		return nil, err
	}

	name := namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port)
	return &backend{
		Name:        name,
		Namespace:   namespace,
		ServiceName: ingBackend.Service.Name,
		ServicePort: portString(ingBackend.Service.Port),
		Endpoints:   endpoints,
	}, nil
}
```

### 🔹 函式: `Provider.buildServersTransport()`
- **變更前簽章 (Before)**: `func Provider.buildServersTransport(ctx context.Context, namespace, name string, cfg IngressConfig)` (L642~L701)
- **變更後簽章 (After)**: `func Provider.buildServersTransport(ctx context.Context, namespace, name string, cfg IngressConfig)` (L642~L701)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildServersTransport(ctx context.Context, namespace, name string, cfg IngressConfig) (namedServersTransport, error) {
	nst := namedServersTransport{
		name: provider.Normalize(namespace + "-" + name),
		ServersTransport: &dynamic.ServersTransport{
			ForwardingTimeouts: &dynamic.ForwardingTimeouts{
				DialTimeout:     ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxyConnectTimeout, p.ProxyConnectTimeout)) * time.Second),
				ReadTimeout:     ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxyReadTimeout, p.ProxyReadTimeout)) * time.Second),
				WriteTimeout:    ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxySendTimeout, p.ProxySendTimeout)) * time.Second),
				IdleConnTimeout: ptypes.Duration(time.Duration(p.UpstreamKeepaliveTimeout) * time.Second),
			},
		},
	}

	if proxyHTTPVersion := ptr.Deref(cfg.ProxyHTTPVersion, ""); proxyHTTPVersion != "" {
		switch proxyHTTPVersion {
		case "1.1":
			nst.DisableHTTP2 = true
		case "1.0":
			log.Ctx(ctx).Warn().Msg("Value '1.0' is not supported with proxy-http-version, ignoring")
		default:
			log.Ctx(ctx).Warn().Msgf("Invalid proxy-http-version value: %q, ignoring", proxyHTTPVersion)
		}
	}

	if scheme := parseBackendProtocol(ptr.Deref(cfg.BackendProtocol, "HTTP")); scheme != "https" {
		return nst, nil
	}

	nst.ServerName = ptr.Deref(cfg.ProxySSLName, ptr.Deref(cfg.ProxySSLServerName, ""))
	nst.InsecureSkipVerify = strings.ToLower(ptr.Deref(cfg.ProxySSLVerify, "off")) != "on"

	if sslSecret := ptr.Deref(cfg.ProxySSLSecret, ""); sslSecret != "" {
		parts := strings.Split(sslSecret, "/")
		if len(parts) != 2 {
			return namedServersTransport{}, fmt.Errorf("malformed proxy SSL secret: %s", sslSecret)
		}

		secretNamespace, secretName := parts[0], parts[1]
		if !p.AllowCrossNamespaceResources && secretNamespace != namespace {
			return namedServersTransport{}, fmt.Errorf("cross-namespace proxy SSL secret not allowed: %s/%s", secretNamespace, secretName)
		}

		blocks, err := p.certificateBlocks(secretNamespace, secretName)
		if err != nil {
			return namedServersTransport{}, fmt.Errorf("getting certificate blocks: %w", err)
		}

		if len(blocks.ca) > 0 {
			nst.RootCAs = []types.FileOrContent{types.FileOrContent(blocks.ca)}
		}
		if len(blocks.cert) > 0 && len(blocks.key) > 0 {
			nst.Certificates = []tls.Certificate{{
				CertFile: types.FileOrContent(blocks.cert),
				KeyFile:  types.FileOrContent(blocks.key),
			}}
		}
	}

	return nst, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildServersTransport(ctx context.Context, namespace, name string, cfg IngressConfig) (namedServersTransport, error) {
	nst := namedServersTransport{
		name: namespace + "-" + name,
		ServersTransport: &dynamic.ServersTransport{
			ForwardingTimeouts: &dynamic.ForwardingTimeouts{
				DialTimeout:     ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxyConnectTimeout, p.ProxyConnectTimeout)) * time.Second),
				ReadTimeout:     ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxyReadTimeout, p.ProxyReadTimeout)) * time.Second),
				WriteTimeout:    ptypes.Duration(time.Duration(ptr.Deref(cfg.ProxySendTimeout, p.ProxySendTimeout)) * time.Second),
				IdleConnTimeout: ptypes.Duration(time.Duration(p.UpstreamKeepaliveTimeout) * time.Second),
			},
		},
	}

	if proxyHTTPVersion := ptr.Deref(cfg.ProxyHTTPVersion, ""); proxyHTTPVersion != "" {
		switch proxyHTTPVersion {
		case "1.1":
			nst.DisableHTTP2 = true
		case "1.0":
			log.Ctx(ctx).Warn().Msg("Value '1.0' is not supported with proxy-http-version, ignoring")
		default:
			log.Ctx(ctx).Warn().Msgf("Invalid proxy-http-version value: %q, ignoring", proxyHTTPVersion)
		}
	}

	if scheme := parseBackendProtocol(ptr.Deref(cfg.BackendProtocol, "HTTP")); scheme != "https" {
		return nst, nil
	}

	nst.ServerName = ptr.Deref(cfg.ProxySSLName, ptr.Deref(cfg.ProxySSLServerName, ""))
	nst.InsecureSkipVerify = strings.ToLower(ptr.Deref(cfg.ProxySSLVerify, "off")) != "on"

	if sslSecret := ptr.Deref(cfg.ProxySSLSecret, ""); sslSecret != "" {
		parts := strings.Split(sslSecret, "/")
		if len(parts) != 2 {
			return namedServersTransport{}, fmt.Errorf("malformed proxy SSL secret: %s", sslSecret)
		}

		secretNamespace, secretName := parts[0], parts[1]
		if !p.AllowCrossNamespaceResources && secretNamespace != namespace {
			return namedServersTransport{}, fmt.Errorf("cross-namespace proxy SSL secret not allowed: %s/%s", secretNamespace, secretName)
		}

		blocks, err := p.certificateBlocks(secretNamespace, secretName)
		if err != nil {
			return namedServersTransport{}, fmt.Errorf("getting certificate blocks: %w", err)
		}

		if len(blocks.ca) > 0 {
			nst.RootCAs = []types.FileOrContent{types.FileOrContent(blocks.ca)}
		}
		if len(blocks.cert) > 0 && len(blocks.key) > 0 {
			nst.Certificates = []tls.Certificate{{
				CertFile: types.FileOrContent(blocks.cert),
				KeyFile:  types.FileOrContent(blocks.key),
			}}
		}
	}

	return nst, nil
}
```


#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/translator.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:50, E:76, A:0) ➔ After(N:49, E:75, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `provider.Normalize (External/Pkg)` (FUNCTION_DEF)
  • - [移除呼叫邊] `Provider.translate` ──[CALLS]──> `provider.Normalize (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.translate()`
- **變更前簽章 (Before)**: `func Provider.translate(ctx context.Context, mc *model)` (L24~L334)
- **變更後簽章 (After)**: `func Provider.translate(ctx context.Context, mc *model)` (L23~L333)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesMetadata{
					Kind:      "Ingress",
					Namespace: mc.DefaultBackend.Namespace,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.Name = loc.IngressName
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		defaultBackendSvc := buildService(mc.DefaultBackend, serversTransportName)
		defaultBackendSvc.Observability = buildServiceObservability(mc.DefaultBackend)
		conf.HTTP.Services[defaultBackendName] = defaultBackendSvc

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}

		// The HTTP part is skipped when the serversTransport could not be built,
		// the TCP passthrough router above being unaffected by it.
		if pt.HTTPServiceName == "" {
			continue
		}

		// Like ingress-nginx, the host also gets an HTTP router proxying to the backend
		// (honoring backend-protocol), so plain HTTP requests and requests bypassing the
		// SSL redirect (e.g. X-Forwarded-Proto: https) behave like nginx instead of
		// hitting an internal service.
		if pt.ServersTransport != nil && pt.ServersTransportName != "" {
			if _, exists := conf.HTTP.ServersTransports[pt.ServersTransportName]; !exists {
				conf.HTTP.ServersTransports[pt.ServersTransportName] = pt.ServersTransport
			}
		}
		conf.HTTP.Services[pt.HTTPServiceName] = buildServiceWithLocConfig(backend, pt.ServersTransportName, pt.Config)

		rt := &dynamic.Router{
			EntryPoints: p.NonTLSEntryPoints,
			Rule:        fmt.Sprintf("Host(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.HTTPServiceName,
		}

		if pt.SSLRedirect {
			redirectMWName := pt.RouterKey + "-redirect-scheme"
			conf.HTTP.Middlewares[redirectMWName] = &dynamic.Middleware{
				RedirectScheme: &dynamic.RedirectScheme{Scheme: "https", ForcePermanentRedirect: true},
			}
			rt.Middlewares = []string{redirectMWName}
		}

		conf.HTTP.Routers[pt.RouterKey+"-http"] = rt
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			primarySvc := buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)
			primarySvc.Observability = buildServiceObservability(backend)
			conf.HTTP.Services[primarySvcName] = primarySvc

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesMetadata{
						Kind:      "Ingress",
						Namespace: loc.Namespace,
						Name:      loc.IngressName,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					canarySvc.Observability = buildServiceObservability(canaryBackend)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName))
			} else {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex))
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			rtTLS := &dynamic.Router{
				EntryPoints: p.TLSEntryPoints,
				Rule:        rule,
				RuleSyntax:  "default",
				Service:     routerSvcName,
				TLS: &dynamic.RouterTLSConfig{
					Options: loc.TLSOptionName,
				},
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
				rtTLS.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt
			conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
				applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				canaryKeyTLS := canaryKey + "-tls"
				canaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       canarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
				p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				nonCanaryKeyTLS := nonCanaryKey + "-tls"
				nonCanaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       primarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
				p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
			}
		}
	}

	return conf
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesMetadata{
					Kind:      "Ingress",
					Namespace: mc.DefaultBackend.Namespace,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.Name = loc.IngressName
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		defaultBackendSvc := buildService(mc.DefaultBackend, serversTransportName)
		defaultBackendSvc.Observability = buildServiceObservability(mc.DefaultBackend)
		conf.HTTP.Services[defaultBackendName] = defaultBackendSvc

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}

		// The HTTP part is skipped when the serversTransport could not be built,
		// the TCP passthrough router above being unaffected by it.
		if pt.HTTPServiceName == "" {
			continue
		}

		// Like ingress-nginx, the host also gets an HTTP router proxying to the backend
		// (honoring backend-protocol), so plain HTTP requests and requests bypassing the
		// SSL redirect (e.g. X-Forwarded-Proto: https) behave like nginx instead of
		// hitting an internal service.
		if pt.ServersTransport != nil && pt.ServersTransportName != "" {
			if _, exists := conf.HTTP.ServersTransports[pt.ServersTransportName]; !exists {
				conf.HTTP.ServersTransports[pt.ServersTransportName] = pt.ServersTransport
			}
		}
		conf.HTTP.Services[pt.HTTPServiceName] = buildServiceWithLocConfig(backend, pt.ServersTransportName, pt.Config)

		rt := &dynamic.Router{
			EntryPoints: p.NonTLSEntryPoints,
			Rule:        fmt.Sprintf("Host(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.HTTPServiceName,
		}

		if pt.SSLRedirect {
			redirectMWName := pt.RouterKey + "-redirect-scheme"
			conf.HTTP.Middlewares[redirectMWName] = &dynamic.Middleware{
				RedirectScheme: &dynamic.RedirectScheme{Scheme: "https", ForcePermanentRedirect: true},
			}
			rt.Middlewares = []string{redirectMWName}
		}

		conf.HTTP.Routers[pt.RouterKey+"-http"] = rt
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			primarySvc := buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)
			primarySvc.Observability = buildServiceObservability(backend)
			conf.HTTP.Services[primarySvcName] = primarySvc

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesMetadata{
						Kind:      "Ingress",
						Namespace: loc.Namespace,
						Name:      loc.IngressName,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					canarySvc.Observability = buildServiceObservability(canaryBackend)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName)
			} else {
				routerKey = fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex)
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			rtTLS := &dynamic.Router{
				EntryPoints: p.TLSEntryPoints,
				Rule:        rule,
				RuleSyntax:  "default",
				Service:     routerSvcName,
				TLS: &dynamic.RouterTLSConfig{
					Options: loc.TLSOptionName,
				},
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
				rtTLS.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt
			conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
				applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				canaryKeyTLS := canaryKey + "-tls"
				canaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       canarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
				p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				nonCanaryKeyTLS := nonCanaryKey + "-tls"
				nonCanaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       primarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
				p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
			}
		}
	}

	return conf
}
```


---

### 🔹 Commit #14: `45c42a63`
- **完整 Hash**: `45c42a6355c9ff2e297eb5cb0ea336393d76e357`
- **說明 (Ground Truth)**: Set the Ssl-Client-* request headers on the Ingress-NGINX HTTP router
- **變更檔案數**: 2

#### 📄 檔案: `pkg/middlewares/ingressnginx/authtlspasscertificatetoupstream/auth_tls_pass_certificate_to_upstream.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:30, E:28, A:0) ➔ After(N:33, E:31, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 1, +Edges: 4, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `normalizeHeaderName` (FUNCTION_DEF)
  • + [新增節點] `deleteManagedHeaders` (FUNCTION_DEF)
  • + [新增節點] `delete (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `managedHeaders` (MODULE_STATE)
  • - [移除節點] `req.Header.Del (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `deleteManagedHeaders` ──[CALLS]──> `normalizeHeaderName`
  • + [新增呼叫邊] `deleteManagedHeaders` ──[CALLS]──> `delete (External/Pkg)`
  • + [新增呼叫邊] `normalizeHeaderName` ──[CALLS]──> `string (External/Pkg)`
  • + [新增呼叫邊] `authTLSPassCertificateToUpstream.ServeHTTP` ──[CALLS]──> `deleteManagedHeaders`
  • - [移除呼叫邊] `authTLSPassCertificateToUpstream.ServeHTTP` ──[CALLS]──> `req.Header.Del (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `authTLSPassCertificateToUpstream.ServeHTTP()`
- **變更前簽章 (Before)**: `func authTLSPassCertificateToUpstream.ServeHTTP(rw http.ResponseWriter, req *http.Request)` (L61~L95)
- **變更後簽章 (After)**: `func authTLSPassCertificateToUpstream.ServeHTTP(rw http.ResponseWriter, req *http.Request)` (L111~L155)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *authTLSPassCertificateToUpstream) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	logger := middlewares.GetLogger(req.Context(), p.name, typeName)
	ctx := logger.WithContext(req.Context())

	if req.TLS == nil || len(req.TLS.PeerCertificates) == 0 {
		logger.Debug().Msg("Tried to extract a certificate on a request without mutual TLS")
		req.Header.Set(sslClientVerify, "NONE")
		// Prevent client-supplied values from reaching the upstream on the no-mTLS path.
		req.Header.Del(sslClientCert)
		req.Header.Del(sslClientSubjectDN)
		req.Header.Del(sslClientIssuerDN)
		p.next.ServeHTTP(rw, req)
		return
	}

	// Nginx only returns the leaf certificate.
	cert := req.TLS.PeerCertificates[0]

	clientVerify := "SUCCESS"
	// Go's RequestClientCert doesn't verify at TLS level, so we have to verify in the middleware to return the correct Ssl-Client-Verify header.
	// For other cases, validation happens during the handshake, so if it reaches this middleware, it means that the certificate is valid.
	if p.clientAuthType == tls.RequestClientCert {
		_, err := cert.Verify(x509.VerifyOptions{Roots: p.caCertPool})
		if err != nil {
			clientVerify = "FAILED:" + err.Error()
		}
	}

	req.Header.Set(sslClientVerify, clientVerify)
	req.Header.Set(sslClientSubjectDN, cert.Subject.String())
	req.Header.Set(sslClientIssuerDN, cert.Issuer.String())
	req.Header.Set(sslClientCert, extractCertificatePEM(ctx, cert))

	p.next.ServeHTTP(rw, req)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *authTLSPassCertificateToUpstream) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	logger := middlewares.GetLogger(req.Context(), p.name, typeName)
	ctx := logger.WithContext(req.Context())

	// This middleware owns the Ssl-Client-* headers, so no value a client sent for them may reach the
	// upstream, whether the request carries a client certificate or not.
	deleteManagedHeaders(req.Header)

	// Nginx builds these headers from the $ssl_client_* variables, which are empty outside of a TLS
	// connection, and proxy_set_header omits a header whose value is empty.
	// A plaintext request therefore carries none of them, rather than carrying NONE, which would tell
	// the backend that the client presented no certificate over a connection that was never TLS.
	if req.TLS == nil {
		logger.Debug().Msg("Tried to extract a certificate on a request without TLS")
		p.next.ServeHTTP(rw, req)
		return
	}

	if len(req.TLS.PeerCertificates) == 0 {
		logger.Debug().Msg("Tried to extract a certificate on a request without mutual TLS")
		req.Header.Set(sslClientVerify, "NONE")
		p.next.ServeHTTP(rw, req)
		return
	}

	// Nginx only returns the leaf certificate.
	cert := req.TLS.PeerCertificates[0]

	clientVerify := "SUCCESS"
	// Go's RequestClientCert doesn't verify at TLS level, so we have to verify in the middleware to return the correct Ssl-Client-Verify header.
	// For other cases, validation happens during the handshake, so if it reaches this middleware, it means that the certificate is valid.
	if p.clientAuthType == tls.RequestClientCert {
		_, err := cert.Verify(x509.VerifyOptions{Roots: p.caCertPool})
		if err != nil {
			clientVerify = "FAILED:" + err.Error()
		}
	}

	req.Header.Set(sslClientVerify, clientVerify)
	req.Header.Set(sslClientSubjectDN, cert.Subject.String())
	req.Header.Set(sslClientIssuerDN, cert.Issuer.String())
	req.Header.Set(sslClientCert, extractCertificatePEM(ctx, cert))

	p.next.ServeHTTP(rw, req)
}
```


#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/translator.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:50, E:76, A:0) ➔ After(N:50, E:76, A:0)
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

### 🔹 函式: `Provider.applyMiddlewares()`
- **變更前簽章 (Before)**: `func Provider.applyMiddlewares(mc *model, loc *location, routerKey string, rt *dynamic.Router, conf *dynamic.Configuration)` (L461~L612)
- **變更後簽章 (After)**: `func Provider.applyMiddlewares(mc *model, loc *location, routerKey string, rt *dynamic.Router, conf *dynamic.Configuration)` (L461~L614)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) applyMiddlewares(mc *model, loc *location, routerKey string, rt *dynamic.Router, conf *dynamic.Configuration) {
	if loc.SSLRedirectOnly && rt.TLS == nil {
		name := routerKey + "-redirect-scheme"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			RedirectScheme: &dynamic.RedirectScheme{Scheme: "https", ForcePermanentRedirect: true},
		}
		rt.Middlewares = []string{name}
	}

	if loc.AccessLog != nil {
		if rt.Observability == nil {
			rt.Observability = &dynamic.RouterObservabilityConfig{}
		}
		rt.Observability.AccessLogs = new(*loc.AccessLog)
	}

	if loc.CustomHTTPErrors != nil {
		e := loc.CustomHTTPErrors
		errorSvcName := e.ErrorServiceName
		if e.ErrorBackendName != "" {
			errorSvcName = "default-backend-" + routerKey
			if errBackend, ok := mc.Backends[e.ErrorBackendName]; ok {
				errSvc := buildServiceWithLocConfig(errBackend, "", loc.Config)
				errSvc.Observability = buildServiceObservability(errBackend)
				conf.HTTP.Services[errorSvcName] = errSvc
			}
		}
		headers := http.Header{
			"X-Namespaces":   {e.Namespace},
			"X-Ingress-Name": {e.IngressName},
			"X-Service-Name": {e.ServiceName},
			"X-Service-Port": {e.ServicePort},
		}
		name := routerKey + "-custom-http-errors"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			Errors: &dynamic.ErrorPage{
				Status:       e.Status,
				Service:      errorSvcName,
				NginxHeaders: &headers,
			},
		}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.AppRoot != nil {
		name := routerKey + "-app-root"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{AppRoot: loc.AppRoot}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Redirect != nil {
		name := routerKey + "-redirect"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RedirectRegex: loc.Redirect}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.BasicAuth != nil {
		name := routerKey + "-basic-auth"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{BasicAuth: loc.BasicAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.DigestAuth != nil {
		name := routerKey + "-digest-auth"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{DigestAuth: loc.DigestAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Buffering != nil {
		name := routerKey + "-buffering"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Buffering: loc.Buffering}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.IPAllowList != nil {
		name := routerKey + "-allowed-source-range"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{IPAllowList: loc.IPAllowList}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.CORS != nil {
		name := routerKey + "-cors"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Headers: loc.CORS}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.RewriteTarget != nil {
		name := routerKey + "-rewrite-target"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RewriteTarget: loc.RewriteTarget}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.UpstreamVhost != nil {
		name := routerKey + "-vhost"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{UpstreamVHost: loc.UpstreamVhost}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.RateLimitRPM != nil {
		name := routerKey + "-limit-rpm"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RateLimit: loc.RateLimitRPM}
		rt.Middlewares = append(rt.Middlewares, name)
	}
	if loc.RateLimitRPS != nil {
		name := routerKey + "-limit-rps"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RateLimit: loc.RateLimitRPS}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.LimitConnections != nil {
		name := routerKey + "-limit-connections"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{InFlightReq: loc.LimitConnections}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.AuthTLSPassCert != nil && rt.TLS != nil {
		name := routerKey + "-pass-certificate-to-upstream"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{AuthTLSPassCertificateToUpstream: loc.AuthTLSPassCert}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if len(loc.ResolvedCustomHeaders) > 0 {
		name := routerKey + "-custom-headers"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			Headers: &dynamic.Headers{CustomResponseHeaders: loc.ResolvedCustomHeaders},
		}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.SnippetAuth != nil {
		name := routerKey + "-snippet"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Snippet: loc.SnippetAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Retry != nil {
		name := routerKey + "-retry"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Retry: loc.Retry}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if p.applyMiddlewareFunc != nil {
		if err := p.applyMiddlewareFunc(routerKey, rt, conf, loc.Config); err != nil {
			log.Error().Err(err).Str("router", routerKey).Msg("Error in ApplyMiddlewareFunc")
		}
	} else if ptr.Deref(loc.Config.EnableModSecurity, false) ||
		ptr.Deref(loc.Config.EnableOWASPCoreRules, false) ||
		ptr.Deref(loc.Config.ModSecuritySnippet, "") != "" ||
		ptr.Deref(loc.Config.ModSecurityTransactionID, "") != "" {
		log.Error().Str("router", routerKey).Msg("mod-security annotations require ApplyMiddlewareFunc to be set")
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) applyMiddlewares(mc *model, loc *location, routerKey string, rt *dynamic.Router, conf *dynamic.Configuration) {
	if loc.SSLRedirectOnly && rt.TLS == nil {
		name := routerKey + "-redirect-scheme"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			RedirectScheme: &dynamic.RedirectScheme{Scheme: "https", ForcePermanentRedirect: true},
		}
		rt.Middlewares = []string{name}
	}

	if loc.AccessLog != nil {
		if rt.Observability == nil {
			rt.Observability = &dynamic.RouterObservabilityConfig{}
		}
		rt.Observability.AccessLogs = new(*loc.AccessLog)
	}

	if loc.CustomHTTPErrors != nil {
		e := loc.CustomHTTPErrors
		errorSvcName := e.ErrorServiceName
		if e.ErrorBackendName != "" {
			errorSvcName = "default-backend-" + routerKey
			if errBackend, ok := mc.Backends[e.ErrorBackendName]; ok {
				errSvc := buildServiceWithLocConfig(errBackend, "", loc.Config)
				errSvc.Observability = buildServiceObservability(errBackend)
				conf.HTTP.Services[errorSvcName] = errSvc
			}
		}
		headers := http.Header{
			"X-Namespaces":   {e.Namespace},
			"X-Ingress-Name": {e.IngressName},
			"X-Service-Name": {e.ServiceName},
			"X-Service-Port": {e.ServicePort},
		}
		name := routerKey + "-custom-http-errors"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			Errors: &dynamic.ErrorPage{
				Status:       e.Status,
				Service:      errorSvcName,
				NginxHeaders: &headers,
			},
		}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.AppRoot != nil {
		name := routerKey + "-app-root"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{AppRoot: loc.AppRoot}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Redirect != nil {
		name := routerKey + "-redirect"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RedirectRegex: loc.Redirect}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.BasicAuth != nil {
		name := routerKey + "-basic-auth"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{BasicAuth: loc.BasicAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.DigestAuth != nil {
		name := routerKey + "-digest-auth"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{DigestAuth: loc.DigestAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Buffering != nil {
		name := routerKey + "-buffering"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Buffering: loc.Buffering}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.IPAllowList != nil {
		name := routerKey + "-allowed-source-range"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{IPAllowList: loc.IPAllowList}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.CORS != nil {
		name := routerKey + "-cors"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Headers: loc.CORS}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.RewriteTarget != nil {
		name := routerKey + "-rewrite-target"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RewriteTarget: loc.RewriteTarget}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.UpstreamVhost != nil {
		name := routerKey + "-vhost"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{UpstreamVHost: loc.UpstreamVhost}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.RateLimitRPM != nil {
		name := routerKey + "-limit-rpm"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RateLimit: loc.RateLimitRPM}
		rt.Middlewares = append(rt.Middlewares, name)
	}
	if loc.RateLimitRPS != nil {
		name := routerKey + "-limit-rps"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{RateLimit: loc.RateLimitRPS}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.LimitConnections != nil {
		name := routerKey + "-limit-connections"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{InFlightReq: loc.LimitConnections}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	// The middleware is attached to the plaintext router as well, and not only to the TLS one:
	// it owns the Ssl-Client-* headers, and is what removes the values a client supplied for them.
	if loc.AuthTLSPassCert != nil {
		name := routerKey + "-pass-certificate-to-upstream"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{AuthTLSPassCertificateToUpstream: loc.AuthTLSPassCert}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if len(loc.ResolvedCustomHeaders) > 0 {
		name := routerKey + "-custom-headers"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{
			Headers: &dynamic.Headers{CustomResponseHeaders: loc.ResolvedCustomHeaders},
		}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.SnippetAuth != nil {
		name := routerKey + "-snippet"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Snippet: loc.SnippetAuth}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if loc.Retry != nil {
		name := routerKey + "-retry"
		conf.HTTP.Middlewares[name] = &dynamic.Middleware{Retry: loc.Retry}
		rt.Middlewares = append(rt.Middlewares, name)
	}

	if p.applyMiddlewareFunc != nil {
		if err := p.applyMiddlewareFunc(routerKey, rt, conf, loc.Config); err != nil {
			log.Error().Err(err).Str("router", routerKey).Msg("Error in ApplyMiddlewareFunc")
		}
	} else if ptr.Deref(loc.Config.EnableModSecurity, false) ||
		ptr.Deref(loc.Config.EnableOWASPCoreRules, false) ||
		ptr.Deref(loc.Config.ModSecuritySnippet, "") != "" ||
		ptr.Deref(loc.Config.ModSecurityTransactionID, "") != "" {
		log.Error().Str("router", routerKey).Msg("mod-security annotations require ApplyMiddlewareFunc to be set")
	}
}
```


---

### 🔹 Commit #15: `f63a006b`
- **完整 Hash**: `f63a006b091904cf43ef812c05471ecf955384bf`
- **說明 (Ground Truth)**: Support wildcard origins in cors-allow-origin for the ingress-nginx provider
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/middleware.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:56, E:85, A:0) ➔ After(N:63, E:91, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 6, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `corsWildcardOriginRegexp` (MODULE_STATE)
  • + [新增節點] `wildcardOriginRegex` (FUNCTION_DEF)
  • + [新增節點] `strings.Replace (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `corsWildcardOriginRegexp.MatchString (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strings.Contains (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `regexp.QuoteMeta (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `originList,` (MODULE_STATE)
  • + [新增呼叫邊] `wildcardOriginRegex` ──[CALLS]──> `regexp.QuoteMeta (External/Pkg)`
  • + [新增呼叫邊] `wildcardOriginRegex` ──[CALLS]──> `strings.Replace (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildCORS` ──[CALLS]──> `strings.Contains (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildCORS` ──[CALLS]──> `corsWildcardOriginRegexp.MatchString (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildCORS` ──[CALLS]──> `append (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildCORS` ──[CALLS]──> `wildcardOriginRegex`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.buildCORS()`
- **變更前簽章 (Before)**: `func Provider.buildCORS(loc *location)` (L260~L273)
- **變更後簽章 (After)**: `func Provider.buildCORS(loc *location)` (L274~L302)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildCORS(loc *location) {
	if !ptr.Deref(loc.Config.EnableCORS, false) {
		return
	}

	loc.CORS = &dynamic.Headers{
		AccessControlAllowCredentials: ptr.Deref(loc.Config.EnableCORSAllowCredentials, true),
		AccessControlExposeHeaders:    ptr.Deref(loc.Config.CORSExposeHeaders, []string{}),
		AccessControlAllowHeaders:     ptr.Deref(loc.Config.CORSAllowHeaders, []string{"DNT", "Keep-Alive", "User-Agent", "X-Requested-With", "If-Modified-Since", "Cache-Control", "Content-Type", "Range", "Authorization"}),
		AccessControlAllowMethods:     ptr.Deref(loc.Config.CORSAllowMethods, []string{"GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS"}),
		AccessControlAllowOriginList:  ptr.Deref(loc.Config.CORSAllowOrigin, []string{"*"}),
		AccessControlMaxAge:           new(int64(ptr.Deref(loc.Config.CORSMaxAge, 1728000))),
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildCORS(loc *location) {
	if !ptr.Deref(loc.Config.EnableCORS, false) {
		return
	}

	// ingress-nginx supports single-level wildcard origins, which the exact-match origin
	// list cannot express; route them to the regex matcher to preserve behavior on migration.
	// Values with a wildcard anywhere else are skipped, as ingress-nginx does.
	var originList, originRegexList []string
	for _, origin := range ptr.Deref(loc.Config.CORSAllowOrigin, []string{"*"}) {
		if origin != "*" && strings.Contains(origin, "*") {
			if corsWildcardOriginRegexp.MatchString(origin) {
				originRegexList = append(originRegexList, wildcardOriginRegex(origin))
			}
			continue
		}
		originList = append(originList, origin)
	}

	loc.CORS = &dynamic.Headers{
		AccessControlAllowCredentials:     ptr.Deref(loc.Config.EnableCORSAllowCredentials, true),
		AccessControlExposeHeaders:        ptr.Deref(loc.Config.CORSExposeHeaders, []string{}),
		AccessControlAllowHeaders:         ptr.Deref(loc.Config.CORSAllowHeaders, []string{"DNT", "Keep-Alive", "User-Agent", "X-Requested-With", "If-Modified-Since", "Cache-Control", "Content-Type", "Range", "Authorization"}),
		AccessControlAllowMethods:         ptr.Deref(loc.Config.CORSAllowMethods, []string{"GET", "PUT", "POST", "DELETE", "PATCH", "OPTIONS"}),
		AccessControlAllowOriginList:      originList,
		AccessControlAllowOriginListRegex: originRegexList,
		AccessControlMaxAge:               new(int64(ptr.Deref(loc.Config.CORSMaxAge, 1728000))),
	}
}
```


---

### 🔹 Commit #16: `591a5e9a`
- **完整 Hash**: `591a5e9a36f93c2ecf885272cf7421c8b25b55a5`
- **說明 (Ground Truth)**: Downgrade default TLS resources namespace mismatch log to warning
- **變更檔案數**: 1

#### 📄 檔案: `pkg/provider/kubernetes/crd/kubernetes.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:249, E:333, A:0) ➔ After(N:249, E:334, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 2, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `Provider.buildTLSStores` ──[CALLS]──> `logger.Warn().Msgf (External/Pkg)`
  • + [新增呼叫邊] `Provider.buildTLSStores` ──[CALLS]──> `logger.Warn (External/Pkg)`
  • - [移除呼叫邊] `Provider.buildTLSOptions` ──[CALLS]──> `logger.Error().Msgf (External/Pkg)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.buildTLSStores()`
- **變更前簽章 (Before)**: `func Provider.buildTLSStores(ctx context.Context, client Client)` (L1425~L1500)
- **變更後簽章 (After)**: `func Provider.buildTLSStores(ctx context.Context, client Client)` (L1425~L1500)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildTLSStores(ctx context.Context, client Client) (map[string]tls.Store, map[string]*tls.CertAndStores) {
	tlsStoreCRD := client.GetTLSStores()
	if len(tlsStoreCRD) == 0 {
		return nil, nil
	}

	var nsDefault []string
	tlsStores := make(map[string]tls.Store)
	tlsConfigs := make(map[string]*tls.CertAndStores)

	for _, t := range tlsStoreCRD {
		logger := log.Ctx(ctx).With().Str("TLSStore", t.Name).Str("namespace", t.Namespace).Logger()

		// When a namespace is explicitly configured, the default TLS store can only be defined in this namespace.
		if t.Name == tls.DefaultTLSStoreName &&
			p.DefaultTLSResourcesNamespace != "" && t.Namespace != p.DefaultTLSResourcesNamespace {
			logger.Error().Msgf("Ignoring default TLS store: it can only be defined in the %q namespace", p.DefaultTLSResourcesNamespace)
			continue
		}

		id := p.nameBuilder.makeRawID(t.Namespace, t.Name)

		// If the name is default, we override the default config.
		if t.Name == tls.DefaultTLSStoreName {
			id = t.Name
			nsDefault = append(nsDefault, t.Namespace)
		}

		var tlsStore tls.Store

		if t.Spec.DefaultCertificate != nil {
			secretName := t.Spec.DefaultCertificate.SecretName

			secret, exists, err := client.GetSecret(t.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to fetch secret %s/%s", t.Namespace, secretName)
				continue
			}
			if !exists {
				logger.Error().Msgf("Secret %s/%s does not exist", t.Namespace, secretName)
				continue
			}

			cert, key, err := getCertificateBlocks(secret, t.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msg("Could not get certificate blocks")
				continue
			}

			tlsStore.DefaultCertificate = &tls.Certificate{
				CertFile: types.FileOrContent(cert),
				KeyFile:  types.FileOrContent(key),
			}
		}

		if t.Spec.DefaultGeneratedCert != nil {
			tlsStore.DefaultGeneratedCert = &tls.GeneratedCert{
				Resolver: t.Spec.DefaultGeneratedCert.Resolver,
				Domain:   t.Spec.DefaultGeneratedCert.Domain,
			}
		}

		// buildCertificates now handles missing secrets gracefully and continues processing
		// other certificates, so we don't fail the entire TLS store if one certificate is missing
		buildCertificates(ctx, client, id, t.Namespace, t.Spec.Certificates, tlsConfigs)

		addToConfig(&logger, "TLS store", id, tlsStores, tlsStore)
	}

	if len(nsDefault) > 1 {
		delete(tlsStores, tls.DefaultTLSStoreName)
		log.Ctx(ctx).Error().Msgf("Default TLS Stores defined in multiple namespaces: %v", nsDefault)
	}

	return tlsStores, tlsConfigs
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildTLSStores(ctx context.Context, client Client) (map[string]tls.Store, map[string]*tls.CertAndStores) {
	tlsStoreCRD := client.GetTLSStores()
	if len(tlsStoreCRD) == 0 {
		return nil, nil
	}

	var nsDefault []string
	tlsStores := make(map[string]tls.Store)
	tlsConfigs := make(map[string]*tls.CertAndStores)

	for _, t := range tlsStoreCRD {
		logger := log.Ctx(ctx).With().Str("TLSStore", t.Name).Str("namespace", t.Namespace).Logger()

		// When a namespace is explicitly configured, the default TLS store can only be defined in this namespace.
		if t.Name == tls.DefaultTLSStoreName &&
			p.DefaultTLSResourcesNamespace != "" && t.Namespace != p.DefaultTLSResourcesNamespace {
			logger.Warn().Msgf("Ignoring default TLS store: it can only be defined in the %q namespace", p.DefaultTLSResourcesNamespace)
			continue
		}

		id := p.nameBuilder.makeRawID(t.Namespace, t.Name)

		// If the name is default, we override the default config.
		if t.Name == tls.DefaultTLSStoreName {
			id = t.Name
			nsDefault = append(nsDefault, t.Namespace)
		}

		var tlsStore tls.Store

		if t.Spec.DefaultCertificate != nil {
			secretName := t.Spec.DefaultCertificate.SecretName

			secret, exists, err := client.GetSecret(t.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to fetch secret %s/%s", t.Namespace, secretName)
				continue
			}
			if !exists {
				logger.Error().Msgf("Secret %s/%s does not exist", t.Namespace, secretName)
				continue
			}

			cert, key, err := getCertificateBlocks(secret, t.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msg("Could not get certificate blocks")
				continue
			}

			tlsStore.DefaultCertificate = &tls.Certificate{
				CertFile: types.FileOrContent(cert),
				KeyFile:  types.FileOrContent(key),
			}
		}

		if t.Spec.DefaultGeneratedCert != nil {
			tlsStore.DefaultGeneratedCert = &tls.GeneratedCert{
				Resolver: t.Spec.DefaultGeneratedCert.Resolver,
				Domain:   t.Spec.DefaultGeneratedCert.Domain,
			}
		}

		// buildCertificates now handles missing secrets gracefully and continues processing
		// other certificates, so we don't fail the entire TLS store if one certificate is missing
		buildCertificates(ctx, client, id, t.Namespace, t.Spec.Certificates, tlsConfigs)

		addToConfig(&logger, "TLS store", id, tlsStores, tlsStore)
	}

	if len(nsDefault) > 1 {
		delete(tlsStores, tls.DefaultTLSStoreName)
		log.Ctx(ctx).Error().Msgf("Default TLS Stores defined in multiple namespaces: %v", nsDefault)
	}

	return tlsStores, tlsConfigs
}
```

### 🔹 函式: `Provider.buildTLSOptions()`
- **變更前簽章 (Before)**: `func Provider.buildTLSOptions(ctx context.Context, client Client)` (L1341~L1423)
- **變更後簽章 (After)**: `func Provider.buildTLSOptions(ctx context.Context, client Client)` (L1341~L1423)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildTLSOptions(ctx context.Context, client Client) map[string]tls.Options {
	tlsOptionsCRDs := client.GetTLSOptions()
	var tlsOptions map[string]tls.Options

	if len(tlsOptionsCRDs) == 0 {
		return tlsOptions
	}
	tlsOptions = make(map[string]tls.Options)
	var nsDefault []string

	for _, tlsOptionsCRD := range tlsOptionsCRDs {
		logger := log.Ctx(ctx).With().Str("tlsOption", tlsOptionsCRD.Name).Str("namespace", tlsOptionsCRD.Namespace).Logger()

		// When a namespace is explicitly configured, the default TLS options can only be defined in this namespace.
		if tlsOptionsCRD.Name == tls.DefaultTLSConfigName &&
			p.DefaultTLSResourcesNamespace != "" && tlsOptionsCRD.Namespace != p.DefaultTLSResourcesNamespace {
			logger.Error().Msgf("Ignoring default TLS options: they can only be defined in the %q namespace", p.DefaultTLSResourcesNamespace)
			continue
		}

		var clientCAs []types.FileOrContent

		for _, secretName := range tlsOptionsCRD.Spec.ClientAuth.SecretNames {
			secret, exists, err := client.GetSecret(tlsOptionsCRD.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to fetch secret %s/%s", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			if !exists {
				logger.Warn().Msgf("Secret %s/%s does not exist", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			cert, err := getCABlocks(secret, tlsOptionsCRD.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to extract CA from secret %s/%s", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			clientCAs = append(clientCAs, types.FileOrContent(cert))
		}

		id := p.nameBuilder.makeRawID(tlsOptionsCRD.Namespace, tlsOptionsCRD.Name)
		// If the name is default, we override the default config.
		if tlsOptionsCRD.Name == tls.DefaultTLSConfigName {
			id = tlsOptionsCRD.Name
			nsDefault = append(nsDefault, tlsOptionsCRD.Namespace)
		}

		tlsOption := tls.Options{}
		tlsOption.SetDefaults()

		tlsOption.MinVersion = tlsOptionsCRD.Spec.MinVersion
		tlsOption.MaxVersion = tlsOptionsCRD.Spec.MaxVersion

		if tlsOptionsCRD.Spec.CipherSuites != nil {
			tlsOption.CipherSuites = tlsOptionsCRD.Spec.CipherSuites
		}

		tlsOption.CurvePreferences = tlsOptionsCRD.Spec.CurvePreferences
		tlsOption.ClientAuth = tls.ClientAuth{
			CAFiles:        clientCAs,
			ClientAuthType: tlsOptionsCRD.Spec.ClientAuth.ClientAuthType,
		}
		tlsOption.SniStrict = tlsOptionsCRD.Spec.SniStrict

		if tlsOptionsCRD.Spec.ALPNProtocols != nil {
			tlsOption.ALPNProtocols = tlsOptionsCRD.Spec.ALPNProtocols
		}

		tlsOption.DisableSessionTickets = tlsOptionsCRD.Spec.DisableSessionTickets

		addToConfig(&logger, "TLS option", id, tlsOptions, tlsOption)
	}

	if len(nsDefault) > 1 {
		delete(tlsOptions, tls.DefaultTLSConfigName)
		log.Ctx(ctx).Error().Msgf("Default TLS Options defined in multiple namespaces: %v", nsDefault)
	}

	return tlsOptions
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildTLSOptions(ctx context.Context, client Client) map[string]tls.Options {
	tlsOptionsCRDs := client.GetTLSOptions()
	var tlsOptions map[string]tls.Options

	if len(tlsOptionsCRDs) == 0 {
		return tlsOptions
	}
	tlsOptions = make(map[string]tls.Options)
	var nsDefault []string

	for _, tlsOptionsCRD := range tlsOptionsCRDs {
		logger := log.Ctx(ctx).With().Str("tlsOption", tlsOptionsCRD.Name).Str("namespace", tlsOptionsCRD.Namespace).Logger()

		// When a namespace is explicitly configured, the default TLS options can only be defined in this namespace.
		if tlsOptionsCRD.Name == tls.DefaultTLSConfigName &&
			p.DefaultTLSResourcesNamespace != "" && tlsOptionsCRD.Namespace != p.DefaultTLSResourcesNamespace {
			logger.Warn().Msgf("Ignoring default TLS options: they can only be defined in the %q namespace", p.DefaultTLSResourcesNamespace)
			continue
		}

		var clientCAs []types.FileOrContent

		for _, secretName := range tlsOptionsCRD.Spec.ClientAuth.SecretNames {
			secret, exists, err := client.GetSecret(tlsOptionsCRD.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to fetch secret %s/%s", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			if !exists {
				logger.Warn().Msgf("Secret %s/%s does not exist", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			cert, err := getCABlocks(secret, tlsOptionsCRD.Namespace, secretName)
			if err != nil {
				logger.Error().Err(err).Msgf("Failed to extract CA from secret %s/%s", tlsOptionsCRD.Namespace, secretName)
				continue
			}

			clientCAs = append(clientCAs, types.FileOrContent(cert))
		}

		id := p.nameBuilder.makeRawID(tlsOptionsCRD.Namespace, tlsOptionsCRD.Name)
		// If the name is default, we override the default config.
		if tlsOptionsCRD.Name == tls.DefaultTLSConfigName {
			id = tlsOptionsCRD.Name
			nsDefault = append(nsDefault, tlsOptionsCRD.Namespace)
		}

		tlsOption := tls.Options{}
		tlsOption.SetDefaults()

		tlsOption.MinVersion = tlsOptionsCRD.Spec.MinVersion
		tlsOption.MaxVersion = tlsOptionsCRD.Spec.MaxVersion

		if tlsOptionsCRD.Spec.CipherSuites != nil {
			tlsOption.CipherSuites = tlsOptionsCRD.Spec.CipherSuites
		}

		tlsOption.CurvePreferences = tlsOptionsCRD.Spec.CurvePreferences
		tlsOption.ClientAuth = tls.ClientAuth{
			CAFiles:        clientCAs,
			ClientAuthType: tlsOptionsCRD.Spec.ClientAuth.ClientAuthType,
		}
		tlsOption.SniStrict = tlsOptionsCRD.Spec.SniStrict

		if tlsOptionsCRD.Spec.ALPNProtocols != nil {
			tlsOption.ALPNProtocols = tlsOptionsCRD.Spec.ALPNProtocols
		}

		tlsOption.DisableSessionTickets = tlsOptionsCRD.Spec.DisableSessionTickets

		addToConfig(&logger, "TLS option", id, tlsOptions, tlsOption)
	}

	if len(nsDefault) > 1 {
		delete(tlsOptions, tls.DefaultTLSConfigName)
		log.Ctx(ctx).Error().Msgf("Default TLS Options defined in multiple namespaces: %v", nsDefault)
	}

	return tlsOptions
}
```


---

### 🔹 Commit #17: `24d4ab06`
- **完整 Hash**: `24d4ab06809667ccf1e10b42ad39f867799666f9`
- **說明 (Ground Truth)**: Redact duplicate TLS certificates in provider merge logs
- **變更檔案數**: 4

#### 📄 檔案: `pkg/observability/logs/fields.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:0, E:0, A:0) ➔ After(N:0, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
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

#### 📄 檔案: `pkg/provider/merge.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:86, E:99, A:0) ➔ After(N:86, E:98, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 2, +Edges: 3, -Edges: 4, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `reflect.TypeFor (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `certificate.Certificate.GetTruncatedCertificateName (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `log.Ctx(ctx).Warn().
						Str("origin", origin).
						Msgf (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `log.Ctx(ctx).Warn().
						Str (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `mergeCertificates` ──[CALLS]──> `logSkippedDuplicate`
  • + [新增呼叫邊] `mergeCertificates` ──[CALLS]──> `reflect.TypeFor (External/Pkg)`
  • + [新增呼叫邊] `mergeCertificates` ──[CALLS]──> `certificate.Certificate.GetTruncatedCertificateName (External/Pkg)`
  • - [移除呼叫邊] `mergeCertificates` ──[CALLS]──> `log.Ctx(ctx).Warn().
						Str("origin", origin).
						Msgf (External/Pkg)`
  • - [移除呼叫邊] `mergeCertificates` ──[CALLS]──> `log.Ctx(ctx).Warn().
						Str (External/Pkg)`
  • - [移除呼叫邊] `mergeCertificates` ──[CALLS]──> `log.Ctx(ctx).Warn (External/Pkg)`
  • - [移除呼叫邊] `mergeCertificates` ──[CALLS]──> `log.Ctx (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `resourceLogFields()`
- **變更前簽章 (Before)**: `[Module State] resourceLogFields` (L22~L33)
- **變更後簽章 (After)**: `[Module State] resourceLogFields` (L22~L34)

#### ◀️ 變更前實作碼 (Before Implementation):
```
var resourceLogFields = map[reflect.Type]resourceMeta{
	reflect.TypeFor[dynamic.Router]():              {logs.RouterName, "HTTP router"},
	reflect.TypeFor[dynamic.Service]():             {logs.ServiceName, "HTTP service"},
	reflect.TypeFor[dynamic.Middleware]():          {logs.MiddlewareName, "HTTP middleware"},
	reflect.TypeFor[dynamic.ServersTransport]():    {logs.ServersTransportName, "HTTP servers transport"},
	reflect.TypeFor[dynamic.TCPRouter]():           {logs.RouterName, "TCP router"},
	reflect.TypeFor[dynamic.TCPService]():          {logs.ServiceName, "TCP service"},
	reflect.TypeFor[dynamic.TCPMiddleware]():       {logs.MiddlewareName, "TCP middleware"},
	reflect.TypeFor[dynamic.TCPServersTransport](): {logs.ServersTransportName, "TCP servers transport"},
	reflect.TypeFor[dynamic.UDPRouter]():           {logs.RouterName, "UDP router"},
	reflect.TypeFor[dynamic.UDPService]():          {logs.ServiceName, "UDP service"},
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
var resourceLogFields = map[reflect.Type]resourceMeta{
	reflect.TypeFor[dynamic.Router]():              {logs.RouterName, "HTTP router"},
	reflect.TypeFor[dynamic.Service]():             {logs.ServiceName, "HTTP service"},
	reflect.TypeFor[dynamic.Middleware]():          {logs.MiddlewareName, "HTTP middleware"},
	reflect.TypeFor[dynamic.ServersTransport]():    {logs.ServersTransportName, "HTTP servers transport"},
	reflect.TypeFor[dynamic.TCPRouter]():           {logs.RouterName, "TCP router"},
	reflect.TypeFor[dynamic.TCPService]():          {logs.ServiceName, "TCP service"},
	reflect.TypeFor[dynamic.TCPMiddleware]():       {logs.MiddlewareName, "TCP middleware"},
	reflect.TypeFor[dynamic.TCPServersTransport](): {logs.ServersTransportName, "TCP servers transport"},
	reflect.TypeFor[dynamic.UDPRouter]():           {logs.RouterName, "UDP router"},
	reflect.TypeFor[dynamic.UDPService]():          {logs.ServiceName, "UDP service"},
	reflect.TypeFor[tls.Certificate]():             {logs.CertificateName, "TLS certificate"},
}
```

### 🔹 函式: `mergeCertificates()`
- **變更前簽章 (Before)**: `func mergeCertificates(ctx context.Context, certificates []*tls.CertAndStores, newCertificates []*tls.CertAndStores, origin string, strategy ResourceStrategy)` (L221~L247)
- **變更後簽章 (After)**: `func mergeCertificates(ctx context.Context, certificates []*tls.CertAndStores, newCertificates []*tls.CertAndStores, origin string, strategy ResourceStrategy)` (L222~L246)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func mergeCertificates(ctx context.Context, certificates []*tls.CertAndStores, newCertificates []*tls.CertAndStores, origin string, strategy ResourceStrategy) []*tls.CertAndStores {
	for _, certificate := range newCertificates {
		var found bool
		for _, existingCertificate := range certificates {
			if existingCertificate.Certificate == certificate.Certificate {
				found = true

				switch strategy {
				case ResourceStrategyMerge:
					existingCertificate.Stores = mergeStores(existingCertificate.Stores, certificate.Stores)
				case ResourceStrategySkipDuplicates:
					log.Ctx(ctx).Warn().
						Str("origin", origin).
						Msgf("TLS certificate %v already configured, skipping", certificate.Certificate)
				}

				break
			}
		}

		if !found {
			certificates = append(certificates, certificate)
		}
	}

	return certificates
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func mergeCertificates(ctx context.Context, certificates []*tls.CertAndStores, newCertificates []*tls.CertAndStores, origin string, strategy ResourceStrategy) []*tls.CertAndStores {
	for _, certificate := range newCertificates {
		var found bool
		for _, existingCertificate := range certificates {
			if existingCertificate.Certificate == certificate.Certificate {
				found = true

				switch strategy {
				case ResourceStrategyMerge:
					existingCertificate.Stores = mergeStores(existingCertificate.Stores, certificate.Stores)
				case ResourceStrategySkipDuplicates:
					logSkippedDuplicate(ctx, reflect.TypeFor[tls.Certificate](), certificate.Certificate.GetTruncatedCertificateName(), origin)
				}

				break
			}
		}

		if !found {
			certificates = append(certificates, certificate)
		}
	}

	return certificates
}
```


#### 📄 檔案: `pkg/tls/certificate.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:32, E:36, A:0) ➔ After(N:31, E:35, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 2, +Edges: 1, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `min (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `strings.HasPrefix (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `strings.TrimPrefix (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Certificate.GetTruncatedCertificateName` ──[CALLS]──> `min (External/Pkg)`
  • - [移除呼叫邊] `Certificate.GetTruncatedCertificateName` ──[CALLS]──> `strings.HasPrefix (External/Pkg)`
  • - [移除呼叫邊] `Certificate.GetTruncatedCertificateName` ──[CALLS]──> `strings.TrimPrefix (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Certificate.GetTruncatedCertificateName()`
- **變更前簽章 (Before)**: `func Certificate.GetTruncatedCertificateName()` (L114~L123)
- **變更後簽章 (After)**: `func Certificate.GetTruncatedCertificateName()` (L114~L127)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Certificate) GetTruncatedCertificateName() string {
	certName := c.CertFile.String()

	// Truncate certificate information only if it's a well formed certificate content with more than 50 characters
	if !c.CertFile.IsPath() && strings.HasPrefix(certName, certificateHeader) && len(certName) > len(certificateHeader)+50 {
		certName = strings.TrimPrefix(c.CertFile.String(), certificateHeader)[:50]
	}

	return certName
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Certificate) GetTruncatedCertificateName() string {
	certName := c.CertFile.String()
	if c.CertFile.IsPath() {
		return certName
	}

	// The content is of unknown nature: providers inline the CertFile before it reaches the TLS manager, a missing
	// path is indistinguishable from inlined content, and the content may be a bundle carrying the private key.
	// Both ends are excerpted, 16 characters being what it takes to read a PEM block type, and never more than half
	// of the content, to keep a short one from being printed in full.
	edge := min(len(certName)/4, 16)

	return certName[:edge] + "[...]" + certName[len(certName)-edge:]
}
```


#### 📄 檔案: `pkg/tls/tls.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:2, E:0, A:0) ➔ After(N:1, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `certificateHeader` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #18: `55bbda4f`
- **完整 Hash**: `55bbda4f65e0f9c533c870983a767a7081126db7`
- **說明 (Ground Truth)**: Do not forward request trailer values to the backend
- **變更檔案數**: 1

#### 📄 檔案: `pkg/proxy/httputil/proxy.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:49, E:48, A:0) ➔ After(N:49, E:48, A:0)
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

### 🔹 函式: `rewriteRequestBuilder()`
- **變更前簽章 (Before)**: `func rewriteRequestBuilder(target *url.URL, passHostHeader bool, preservePath bool)` (L67~L129)
- **變更後簽章 (After)**: `func rewriteRequestBuilder(target *url.URL, passHostHeader bool, preservePath bool)` (L67~L142)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func rewriteRequestBuilder(target *url.URL, passHostHeader bool, preservePath bool) func(*httputil.ProxyRequest) {
	return func(pr *httputil.ProxyRequest) {
		copyForwardedHeader(pr.Out.Header, pr.In.Header)
		if !ShouldNotAppendXFF(pr.In.Context()) {
			if clientIP, _, err := net.SplitHostPort(pr.In.RemoteAddr); err == nil {
				// If we aren't the first proxy retain prior
				// X-Forwarded-For information as a comma+space
				// separated list and fold multiple headers into one.
				prior, ok := pr.Out.Header["X-Forwarded-For"]
				omit := ok && prior == nil // Issue 38079: nil now means don't populate the header
				if len(prior) > 0 {
					clientIP = strings.Join(prior, ", ") + ", " + clientIP
				}
				if !omit {
					pr.Out.Header.Set("X-Forwarded-For", clientIP)
				}
			}
		}

		pr.Out.URL.Scheme = target.Scheme
		pr.Out.URL.Host = target.Host

		u := pr.Out.URL
		if pr.Out.RequestURI != "" {
			parsedURL, err := url.ParseRequestURI(pr.Out.RequestURI)
			if err == nil {
				u = parsedURL
			}
		}

		pr.Out.URL.Path = u.Path
		pr.Out.URL.RawPath = u.RawPath

		if preservePath {
			pr.Out.URL.Path, pr.Out.URL.RawPath = JoinURLPath(target, u)
		}

		// If a plugin/middleware adds semicolons in query params, they should be urlEncoded.
		pr.Out.URL.RawQuery = strings.ReplaceAll(u.RawQuery, ";", "&")
		pr.Out.RequestURI = "" // Outgoing request should not have RequestURI
		// URL.RequestURI gives Opaque precedence over the path, an opaque outgoing URL would discard the path set above.
		pr.Out.URL.Opaque = ""

		pr.Out.Proto = "HTTP/1.1"
		pr.Out.ProtoMajor = 1
		pr.Out.ProtoMinor = 1

		// Adding the "Connection: close" header to the request ensures that we are not reusing the connection for
		// subsequent requests in case the backend does not support CONNECT and returns a 2xx response.
		if pr.Out.Method == http.MethodConnect {
			pr.Out.Close = true
		}

		// Do not pass client Host header unless option PassHostHeader is set.
		if !passHostHeader {
			pr.Out.Host = pr.Out.URL.Host
		}

		if isWebSocketUpgrade(pr.Out) {
			cleanWebSocketHeaders(pr.Out)
		}
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func rewriteRequestBuilder(target *url.URL, passHostHeader bool, preservePath bool) func(*httputil.ProxyRequest) {
	return func(pr *httputil.ProxyRequest) {
		copyForwardedHeader(pr.Out.Header, pr.In.Header)
		if !ShouldNotAppendXFF(pr.In.Context()) {
			if clientIP, _, err := net.SplitHostPort(pr.In.RemoteAddr); err == nil {
				// If we aren't the first proxy retain prior
				// X-Forwarded-For information as a comma+space
				// separated list and fold multiple headers into one.
				prior, ok := pr.Out.Header["X-Forwarded-For"]
				omit := ok && prior == nil // Issue 38079: nil now means don't populate the header
				if len(prior) > 0 {
					clientIP = strings.Join(prior, ", ") + ", " + clientIP
				}
				if !omit {
					pr.Out.Header.Set("X-Forwarded-For", clientIP)
				}
			}
		}

		pr.Out.URL.Scheme = target.Scheme
		pr.Out.URL.Host = target.Host

		u := pr.Out.URL
		if pr.Out.RequestURI != "" {
			parsedURL, err := url.ParseRequestURI(pr.Out.RequestURI)
			if err == nil {
				u = parsedURL
			}
		}

		pr.Out.URL.Path = u.Path
		pr.Out.URL.RawPath = u.RawPath

		if preservePath {
			pr.Out.URL.Path, pr.Out.URL.RawPath = JoinURLPath(target, u)
		}

		// If a plugin/middleware adds semicolons in query params, they should be urlEncoded.
		pr.Out.URL.RawQuery = strings.ReplaceAll(u.RawQuery, ";", "&")
		pr.Out.RequestURI = "" // Outgoing request should not have RequestURI
		// URL.RequestURI gives Opaque precedence over the path, an opaque outgoing URL would discard the path set above.
		pr.Out.URL.Opaque = ""

		// Forward the declared request trailer names, but never their values: they arrive
		// after the header section, once routing and security decisions are made, and would
		// otherwise reach the backend under a name sanitized in the header section.
		// Discarding them is allowed by https://www.rfc-editor.org/rfc/rfc9112#section-7.1.2,
		// and the names are kept as the hint of what was dropped described in
		// https://www.rfc-editor.org/rfc/rfc9110#section-6.6.2
		// Emptying the outgoing map is what makes this hold whatever the middleware chain did
		// to the incoming request, as the transport only writes pr.Out.Trailer.
		// Response trailers are unaffected.
		for name := range pr.Out.Trailer {
			pr.Out.Trailer[name] = nil
		}

		pr.Out.Proto = "HTTP/1.1"
		pr.Out.ProtoMajor = 1
		pr.Out.ProtoMinor = 1

		// Adding the "Connection: close" header to the request ensures that we are not reusing the connection for
		// subsequent requests in case the backend does not support CONNECT and returns a 2xx response.
		if pr.Out.Method == http.MethodConnect {
			pr.Out.Close = true
		}

		// Do not pass client Host header unless option PassHostHeader is set.
		if !passHostHeader {
			pr.Out.Host = pr.Out.URL.Host
		}

		if isWebSocketUpgrade(pr.Out) {
			cleanWebSocketHeaders(pr.Out)
		}
	}
}
```


---

### 🔹 Commit #19: `ddc1bf46`
- **完整 Hash**: `ddc1bf4660b85fd61fafdd821eb8216fb1a0b130`
- **說明 (Ground Truth)**: Prevent user enumeration through the basic auth singleflight key
- **變更檔案數**: 1

#### 📄 檔案: `pkg/middlewares/auth/basic_auth.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:30, E:29, A:0) ➔ After(N:31, E:30, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 3, -Edges: 2, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `singleflightKey` (FUNCTION_DEF)
  • + [新增呼叫邊] `basicAuth.checkPassword` ──[CALLS]──> `singleflightKey`
  • + [新增呼叫邊] `singleflightKey` ──[CALLS]──> `strconv.Itoa (External/Pkg)`
  • + [新增呼叫邊] `singleflightKey` ──[CALLS]──> `len (External/Pkg)`
  • - [移除呼叫邊] `basicAuth.checkPassword` ──[CALLS]──> `strconv.Itoa (External/Pkg)`
  • - [移除呼叫邊] `basicAuth.checkPassword` ──[CALLS]──> `len (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `basicAuth.checkPassword()`
- **變更前簽章 (Before)**: `func basicAuth.checkPassword(user, password string)` (L121~L137)
- **變更後簽章 (After)**: `func basicAuth.checkPassword(user, password string)` (L121~L134)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (b *basicAuth) checkPassword(user, password string) bool {
	secret := b.auth.Secrets(user, b.auth.Realm)

	// Prefix the password length so the key unambiguously encodes the
	// (password, secret) pair and distinct pairs cannot collide.
	key := strconv.Itoa(len(password)) + ":" + password + secret
	match, _, _ := b.singleflightGroup.Do(key, func() (any, error) {
		if secret == "" {
			_ = b.checkSecret(password, b.notFoundSecret)
			return false, nil
		}

		return b.checkSecret(password, secret), nil
	})

	return match.(bool)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (b *basicAuth) checkPassword(user, password string) bool {
	secret := b.auth.Secrets(user, b.auth.Realm)

	match, _, _ := b.singleflightGroup.Do(singleflightKey(user, password), func() (any, error) {
		if secret == "" {
			_ = b.checkSecret(password, b.notFoundSecret)
			return false, nil
		}

		return b.checkSecret(password, secret), nil
	})

	return match.(bool)
}
```


---

### 🔹 Commit #20: `81f4e3cd`
- **完整 Hash**: `81f4e3cd718c350e8d58547323967a83d2f38360`
- **說明 (Ground Truth)**: Create HTTP redirect router for ssl-passthrough with force-ssl-redirect
- **變更檔案數**: 4

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/build.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:120, E:179, A:0) ➔ After(N:121, E:180, A:0)
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
  • + [新增節點] `sslRedirectEnabled (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.build` ──[CALLS]──> `sslRedirectEnabled (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.build()`
- **變更前簽章 (Before)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L613)
- **變更後簽章 (After)**: `func Provider.build(ctx context.Context, ingressClasses []*netv1.IngressClass)` (L55~L629)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := provider.Normalize(canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:      canaryBackendName,
						Namespace: canaryIngress.Namespace,
						Endpoints: endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough: handled per-rule. serversTransport is not needed for passthrough.
		if ptr.Deref(ing.config.SSLPassthrough, false) {
			// Even with ssl-passthrough, the Spec.TLS section's certificates are still loaded so they remain available as the default certificate.
			if len(ing.Spec.TLS) > 0 {
				if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
					logger.Warn().Err(err).Msg("Error loading TLS certificates for ssl-passthrough ingress")
				}
			}
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := provider.Normalize(ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:      ptBackendName,
						Namespace: ing.Namespace,
						Endpoints: endpoints,
					}
				}

				routerKey := strings.TrimPrefix(provider.Normalize(ing.Namespace+"-"+ing.Name+"-"+rule.Host), "-")
				mc.PassthroughBackends = append(mc.PassthroughBackends, &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   routerKey,
				})
				markProcessedIngress(ing.Ingress)
			}
			continue
		}

		// Normal ingress: build serversTransport, TLS options, TLS certs, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}
		// Load TLS certificates into the shared mc.Certs map first. They are kept
		// even when the rest of the ingress is later skipped (e.g. when an
		// auth-tls-secret fails to resolve), so the default certificate pool stays
		// consistent. When loading fails, hasTLS still signals that the ingress has
		// a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := provider.Normalize(secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey)

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:      backendName,
						Namespace: ing.Namespace,
						Endpoints: endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:      errBackendName,
										Namespace: ing.Namespace,
										Endpoints: endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-default-backend")
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:      ingDefaultBackendName,
					Namespace: ing.Namespace,
					Endpoints: endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) build(ctx context.Context, ingressClasses []*netv1.IngressClass) *model {
	mc := &model{
		Backends: make(map[string]*backend),
		Servers:  make(map[string]*server),
		Certs:    make(map[string]certPair),
	}
	processedIngresses := make(map[string]struct{})
	markProcessedIngress := func(ing *netv1.Ingress) {
		key := ing.Namespace + "/" + ing.Name
		if _, exists := processedIngresses[key]; exists {
			return
		}

		processedIngresses[key] = struct{}{}
		mc.ProcessedIngresses = append(mc.ProcessedIngresses, ing)
	}

	// Builder-local cache of TLS options resolved per ingress. Each Location
	// that needs an option carries a pointer to the cached entry; the translator
	// registers each unique option once in conf.TLS.Options.
	tlsOptionCache := make(map[string]*tls.Options)

	allHosts := make(map[string]bool)
	hostsWithUseRegex := make(map[string]bool)
	claimedAliases := make(map[string]string)

	// Provider-level default backend.
	if p.defaultBackendServiceNamespace != "" && p.defaultBackendServiceName != "" {
		backend, err := p.resolveBackend(
			p.defaultBackendServiceNamespace,
			netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: p.defaultBackendServiceName}},
			IngressConfig{},
		)
		if err != nil {
			log.Ctx(ctx).Error().Err(err).Msg("Cannot resolve default backend service")
		} else {
			mc.Backends[backend.Name] = backend
			mc.DefaultBackend = backend
		}
	}

	// First pass: collect all regular and canary ingresses.
	var (
		regularIngresses []ingressEntry
		canaryIngresses  []ingressEntry
	)

	// ingressPaths tracks existing paths for canary matching.
	// key: namespace/host+path+pathType → (backend service, IngressConfig)
	ingressPaths := make(map[string]pathEntry)

	serverSnippets := make(map[string]string) // host → first server-snippet seen

	// Sort ingresses by creation timestamp (ascending). Ties are broken by
	// descending namespace/name lexicographic order, matching ingress-nginx
	// behavior. This ordering is what makes server-alias conflict resolution
	// deterministic: the first ingress in this order to claim an alias owns it.
	ingresses := p.k8sClient.ListIngresses()
	sort.SliceStable(ingresses, func(a, b int) bool {
		ta, tb := ingresses[a].CreationTimestamp, ingresses[b].CreationTimestamp
		if ta.Equal(&tb) {
			ia := ingresses[a].Namespace + "/" + ingresses[a].Name
			ib := ingresses[b].Namespace + "/" + ingresses[b].Name
			return ia > ib
		}
		return ta.Before(&tb)
	})

	for _, ingress := range ingresses {
		if !p.shouldProcess(ingress, ingressClasses) {
			continue
		}

		logger := log.Ctx(ctx).With().
			Str("ingress", ingress.Name).
			Str("namespace", ingress.Namespace).
			Logger()

		cfg := parseIngressConfig(ingress)
		entry := ingressEntry{Ingress: ingress, config: cfg}

		if err := p.validateIngress(entry.Ingress, entry.config); err != nil {
			logger.Error().Err(err).Msg("Invalid Ingress, skipping")
			continue
		}

		if ptr.Deref(cfg.Canary, false) {
			canaryIngresses = append(canaryIngresses, entry)
			continue
		}

		for _, alias := range ptr.Deref(cfg.ServerAlias, nil) {
			a := strings.ToLower(alias)
			if _, exists := claimedAliases[a]; !exists {
				claimedAliases[a] = ingress.Namespace + "/" + ingress.Name
			}
		}

		for _, rule := range ingress.Spec.Rules {
			allHosts[rule.Host] = true

			if ptr.Deref(cfg.UseRegex, false) || ptr.Deref(cfg.RewriteTarget, "") != "" {
				hostsWithUseRegex[rule.Host] = true
			}

			if srvSnippet := ptr.Deref(cfg.ServerSnippet, ""); srvSnippet != "" {
				if serverSnippets[rule.Host] == "" {
					serverSnippets[rule.Host] = srvSnippet
				}
			}

			if rule.HTTP != nil {
				for _, pa := range rule.HTTP.Paths {
					if pa.Backend.Service == nil {
						continue
					}
					key := ingressPathKey(ingress.Namespace, rule.Host, pa)
					ingressPaths[key] = pathEntry{HTTPIngressPath: pa, config: cfg}
				}
			}
		}

		regularIngresses = append(regularIngresses, entry)
	}

	// Second pass: resolve canary backends.
	// canaryMap: key = namespace/svcName/port → CanaryConfig
	canaryConfigs := make(map[string]canaryConfig) // primary backend key → canary info
	alreadyMatchedPaths := make(map[string]struct{})

	for _, canaryIngress := range canaryIngresses {
		logger := log.With().
			Str("ingress", canaryIngress.Name).
			Str("namespace", canaryIngress.Namespace).
			Logger()

		for _, rule := range canaryIngress.Spec.Rules {
			if rule.HTTP == nil {
				continue
			}
			for _, pa := range rule.HTTP.Paths {
				pathKey := ingressPathKey(canaryIngress.Namespace, rule.Host, pa)
				prodIngressPath, ok := ingressPaths[pathKey]
				if !ok {
					logger.Error().Msgf("Canary ingress does not match any Ingress rule for host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if _, ok := alreadyMatchedPaths[pathKey]; ok {
					logger.Error().Msgf("A canary ingress is already matching Ingress rule host=%s path=%s", rule.Host, pa.Path)
					continue
				}

				if pa.Backend.Service == nil {
					continue
				}

				// Skip if the canary path uses the same service as the production path — this
				// is a "non-matching" canary ingress where the matching path doesn't actually
				// route to a different backend.
				prodSvc := prodIngressPath.Backend.Service
				if pa.Backend.Service.Name == prodSvc.Name &&
					portString(pa.Backend.Service.Port) == portString(prodSvc.Port) {
					continue
				}

				// The canary backend's addresses are checked using the original ingress config.
				endpoints, err := p.getBackendEndpoints(canaryIngress.Namespace, pa.Backend, prodIngressPath.config)
				if err != nil || len(endpoints) == 0 {
					continue
				}

				alreadyMatchedPaths[pathKey] = struct{}{}

				weightTotal := max(ptr.Deref(canaryIngress.config.CanaryWeightTotal, 0), 100)
				weight := min(max(ptr.Deref(canaryIngress.config.CanaryWeight, 0), 0), weightTotal)

				// Resolve canary backend.
				canaryBackendName := provider.Normalize(canaryIngress.Namespace + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[canaryBackendName]; !exists {
					mc.Backends[canaryBackendName] = &backend{
						Name:      canaryBackendName,
						Namespace: canaryIngress.Namespace,
						Endpoints: endpoints,
					}
				}

				// Primary backend key for the original ingress path.
				primaryKey := canaryPrimaryKey(canaryIngress.Namespace, *prodIngressPath.Backend.Service)
				canaryConfigs[primaryKey] = canaryConfig{
					BackendName:   canaryBackendName,
					Weight:        weight,
					WeightTotal:   weightTotal,
					Header:        ptr.Deref(canaryIngress.config.CanaryHeader, ""),
					HeaderValue:   ptr.Deref(canaryIngress.config.CanaryHeaderValue, ""),
					HeaderPattern: ptr.Deref(canaryIngress.config.CanaryHeaderPattern, ""),
					Cookie:        ptr.Deref(canaryIngress.config.CanaryCookie, ""),
				}
				markProcessedIngress(canaryIngress.Ingress)
			}
		}
	}

	// Third pass: build Servers and Locations from regular ingresses.
	loadedSecrets := make(map[string]bool) // cross-ingress secret-load dedup

	for _, ing := range regularIngresses {
		logger := log.Ctx(ctx).With().
			Str("ingress", ing.Name).
			Str("namespace", ing.Namespace).
			Logger()
		ctxIng := logger.WithContext(ctx)

		// ssl-passthrough: handled per-rule.
		if ptr.Deref(ing.config.SSLPassthrough, false) {
			// Even with ssl-passthrough, the Spec.TLS section's certificates are still loaded so they remain available as the default certificate.
			hasTLS := len(ing.Spec.TLS) > 0
			if hasTLS {
				if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
					logger.Warn().Err(err).Msg("Error loading TLS certificates for ssl-passthrough ingress")
				}
			}
			for _, rule := range ing.Spec.Rules {
				if rule.Host == "" {
					logger.Error().Msg("Cannot process ssl-passthrough: rule has no host")
					continue
				}

				var ingBackend *netv1.IngressBackend
				if rule.HTTP != nil {
					for _, pa := range rule.HTTP.Paths {
						if pa.Path == "/" {
							ingBackend = &pa.Backend
							break
						}
					}
				} else if ing.Spec.DefaultBackend != nil {
					ingBackend = ing.Spec.DefaultBackend
				}

				if ingBackend == nil || ingBackend.Service == nil {
					logger.Error().Msgf("No backend found for ssl-passthrough on host %q", rule.Host)
					continue
				}

				endpoints, err := p.getBackendEndpoints(ing.Namespace, *ingBackend, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot resolve passthrough backend for host %q", rule.Host)
					continue
				}

				ptBackendName := provider.Normalize(ing.Namespace + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
				if _, exists := mc.Backends[ptBackendName]; !exists {
					mc.Backends[ptBackendName] = &backend{
						Name:      ptBackendName,
						Namespace: ing.Namespace,
						Endpoints: endpoints,
					}
				}

				routerKey := strings.TrimPrefix(provider.Normalize(ing.Namespace+"-"+ing.Name+"-"+rule.Host), "-")
				ptBackend := &sslPassthroughBackend{
					BackendName: ptBackendName,
					Hostname:    rule.Host,
					RouterKey:   routerKey,
					SSLRedirect: sslRedirectEnabled(ing.config, hasTLS),
					Config:      ing.config,
				}

				// The serversTransport only shapes the HTTP router: when it cannot be built,
				// the TCP passthrough router must still be created.
				nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
				if err != nil {
					logger.Error().Err(err).Msgf("Cannot build serversTransport for ssl-passthrough on host %q, skipping its HTTP router", rule.Host)
				} else {
					ptBackend.HTTPServiceName = provider.Normalize(ing.Namespace + "-" + ing.Name + "-" + ingBackend.Service.Name + "-" + portString(ingBackend.Service.Port))
					ptBackend.ServersTransportName = nst.name
					ptBackend.ServersTransport = nst.ServersTransport
				}

				mc.PassthroughBackends = append(mc.PassthroughBackends, ptBackend)
				markProcessedIngress(ing.Ingress)
			}
			continue
		}

		// Normal ingress: build serversTransport, TLS options, TLS certs, and Locations.
		nst, err := p.buildServersTransport(ctxIng, ing.Namespace, ing.Name, ing.config)
		if err != nil {
			logger.Error().Err(err).Msg("Cannot build serversTransport, skipping ingress")
			continue
		}
		// Load TLS certificates into the shared mc.Certs map first. They are kept
		// even when the rest of the ingress is later skipped (e.g. when an
		// auth-tls-secret fails to resolve), so the default certificate pool stays
		// consistent. When loading fails, hasTLS still signals that the ingress has
		// a TLS section so the translator can fall back to the default cert.
		hasTLS := len(ing.Spec.TLS) > 0
		if hasTLS {
			if err := p.loadCertificates(ctxIng, ing.Ingress, mc.Certs, loadedSecrets); err != nil {
				logger.Warn().Err(err).Msg("Error loading TLS certificates, defaulting to default certificate")
			}
		}

		// Resolve TLS option (auth-tls-secret).
		var tlsOptionName string
		var tlsOption *tls.Options
		if ing.config.AuthTLSSecret != nil {
			// The option name must be a pure function of what determines the TLSOption's content, so that multiple Ingresses
			// sharing one mTLS policy on the same host resolve to the same TLS option.
			// The namespace and the secret name are suffixed by their own length so that the key unambiguously
			// encodes the pair.
			pascalCaseWordBoundary := regexp.MustCompile(`([a-z0-9])([A-Z])`)
			clientAuthTypeKey := strings.ToLower(pascalCaseWordBoundary.ReplaceAllString(clientAuthTypeFromString(ing.config.AuthTLSVerifyClient), "$1-$2"))
			secretNamespace, secretName, _ := strings.Cut(*ing.config.AuthTLSSecret, "/")
			optName := provider.Normalize(secretNamespace + "-" + strconv.Itoa(len(secretNamespace)) + "-" + secretName + "-" + strconv.Itoa(len(secretName)) + "-" + clientAuthTypeKey)

			if cached, exists := tlsOptionCache[optName]; exists {
				tlsOptionName = optName
				tlsOption = cached
			} else {
				tlsOpt, err := p.buildClientAuthTLSOption(ing.Namespace, ing.config)
				if err != nil {
					logger.Error().Err(err).Msg("Cannot build client auth TLS option, skipping ingress")
					// Skipping the ingress entirely matches ingress-nginx behavior:
					// when the configured client-auth secret cannot be resolved, no
					// router/middleware/service should be exposed for the ingress.
					continue
				}
				tlsOptionName = optName
				tlsOption = tlsOpt
				tlsOptionCache[optName] = tlsOption
			}
		}

		for ri, rule := range ing.Spec.Rules {
			srv := getOrCreateServer(mc.Servers, rule.Host)

			if rule.HTTP == nil {
				continue
			}
			for pi, pa := range rule.HTTP.Paths {
				if pa.Backend.Service == nil {
					continue
				}

				// Resolve primary backend. Missing/unavailable services are tolerated:
				// the location is still emitted with an empty backend so the router
				// (and its middlewares) exist, mirroring ingress-nginx's 503-on-no-servers
				// behavior.
				endpoints, err := p.getBackendEndpoints(ing.Namespace, pa.Backend, ing.config)
				if err != nil {
					logger.Warn().
						Str("service", pa.Backend.Service.Name).
						Err(err).
						Msg("Cannot resolve backend addresses, emitting empty backend")
					endpoints = nil
				}

				backendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-" + pa.Backend.Service.Name + "-" + portString(pa.Backend.Service.Port))
				if _, exists := mc.Backends[backendName]; !exists {
					mc.Backends[backendName] = &backend{
						Name:      backendName,
						Namespace: ing.Namespace,
						Endpoints: endpoints,
					}
				}

				loc := &location{
					Path:                 pa.Path,
					PathType:             pa.PathType,
					BackendName:          backendName,
					ServersTransportName: nst.name,
					ServersTransport:     nst.ServersTransport,
					LocationIndex:        pi,
					RuleIndex:            ri,
					Config:               ing.config,
					TLSOptionName:        tlsOptionName,
					TLSOption:            tlsOption,
					HasTLS:               hasTLS,
					ServerSnippet:        serverSnippets[rule.Host],
					Namespace:            ing.Namespace,
					IngressName:          ing.Name,
					ServiceName:          pa.Backend.Service.Name,
					ServicePort:          portString(pa.Backend.Service.Port),
				}

				// Attach canary config if one exists for this primary backend.
				primaryKey := canaryPrimaryKey(ing.Namespace, *pa.Backend.Service)
				if cc, ok := canaryConfigs[primaryKey]; ok {
					loc.Canary = &cc
				}

				// Pre-resolve basic auth.
				if ing.config.AuthType != nil {
					basic, digest, err := p.resolveBasicAuth(ing.Namespace, ing.config)
					if err != nil {
						logger.Error().
							Err(err).
							Str("ingress", fmt.Sprintf("%s/%s rule-%d path-%d", ing.Namespace, ing.Name, ri, pi)).
							Msg("Cannot resolve auth secret, skipping ingress")
						// Skipping the ingress entirely when auth secret resolution fails,
						// to match ingress-nginx behavior.
						continue
					}
					loc.BasicAuth = basic
					loc.DigestAuth = digest
				}

				// Pre-resolve custom headers ConfigMap.
				if ing.config.CustomHeaders != nil {
					headers, err := p.resolveCustomHeaders(ing.Namespace, *ing.config.CustomHeaders)
					if err != nil {
						logger.Error().Err(err).Msg("Cannot resolve custom-headers ConfigMap")
						loc.Error = true
					} else {
						loc.ResolvedCustomHeaders = headers
					}
				}

				// Pre-resolve custom-http-errors default backend.
				customErrors := ptr.Deref(ing.config.CustomHTTPErrors, nil)
				if len(customErrors) > 0 {
					if errBackendName := p.resolveHTTPErrorBackend(ing.Namespace, ing.config); errBackendName != "" {
						loc.ResolvedHTTPErrorBackendName = errBackendName
						if _, exists := mc.Backends[errBackendName]; !exists {
							// Build the error backend using defaultBackend annotation or provider default.
							defaultSvcName := ptr.Deref(ing.config.DefaultBackend, "")
							if defaultSvcName != "" {
								endpoints, err := p.getBackendEndpoints(ing.Namespace,
									netv1.IngressBackend{Service: &netv1.IngressServiceBackend{Name: defaultSvcName}},
									ing.config)
								if err == nil {
									mc.Backends[errBackendName] = &backend{
										Name:      errBackendName,
										Namespace: ing.Namespace,
										Endpoints: endpoints,
									}
								}
							}
						}
					}
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Build all middleware configurations so the translator only registers them.
				endpointCount := 0
				if backend, ok := mc.Backends[backendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}

		// Ingress-level spec.defaultBackend: emit one host-only catch-all location
		// per distinct host in the ingress rules. Mirrors ingress-nginx which uses
		// the ingress defaultBackend as the fallback location for each server block.
		// When the ingress has no rules, register the backend as the global catch-all
		// (default-backend / default-backend-tls routers) so it still serves traffic.
		if ing.Spec.DefaultBackend != nil && ing.Spec.DefaultBackend.Service != nil {
			db := ing.Spec.DefaultBackend
			endpoints, err := p.getBackendEndpoints(ing.Namespace, *db, ing.config)
			if err != nil {
				logger.Warn().
					Str("service", db.Service.Name).
					Err(err).
					Msg("Cannot resolve ingress default backend, emitting empty backend")
				endpoints = nil
			}

			if len(ing.Spec.Rules) == 0 {
				if mc.DefaultBackend == nil {
					loc := &location{
						BackendName:          defaultBackendName,
						ServersTransportName: nst.name,
						ServersTransport:     nst.ServersTransport,
						Config:               ing.config,
						TLSOptionName:        tlsOptionName,
						TLSOption:            tlsOption,
						HasTLS:               hasTLS,
						Namespace:            ing.Namespace,
						IngressName:          ing.Name,
						ServiceName:          db.Service.Name,
						ServicePort:          portString(db.Service.Port),
					}

					// Inherit basic/digest auth and custom headers like the rule
					// paths do, so the catch-all is not an unauthenticated bypass.
					if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
						logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping ingress")
						continue
					}
					p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

					bk := &backend{
						Name:        defaultBackendName,
						Namespace:   ing.Namespace,
						ServiceName: db.Service.Name,
						Endpoints:   endpoints,
					}
					mc.Backends[defaultBackendName] = bk
					mc.DefaultBackend = bk

					p.buildMiddlewares(ctx, loc, "", allHosts, len(endpoints))
					mc.DefaultBackendLocation = loc
					markProcessedIngress(ing.Ingress)
				}
				continue
			}

			ingDefaultBackendName := provider.Normalize(ing.Namespace + "-" + ing.Name + "-default-backend")
			if _, exists := mc.Backends[ingDefaultBackendName]; !exists {
				mc.Backends[ingDefaultBackendName] = &backend{
					Name:      ingDefaultBackendName,
					Namespace: ing.Namespace,
					Endpoints: endpoints,
				}
			}

			seenHosts := map[string]struct{}{}
			for _, rule := range ing.Spec.Rules {
				if _, ok := seenHosts[rule.Host]; ok {
					continue
				}
				seenHosts[rule.Host] = struct{}{}

				srv := getOrCreateServer(mc.Servers, rule.Host)

				loc := &location{
					Path:                    "",
					BackendName:             ingDefaultBackendName,
					ServersTransportName:    nst.name,
					ServersTransport:        nst.ServersTransport,
					Config:                  ing.config,
					TLSOptionName:           tlsOptionName,
					TLSOption:               tlsOption,
					HasTLS:                  hasTLS,
					ServerSnippet:           serverSnippets[rule.Host],
					Namespace:               ing.Namespace,
					IngressName:             ing.Name,
					ServiceName:             db.Service.Name,
					ServicePort:             portString(db.Service.Port),
					IsIngressDefaultBackend: true,
				}

				loc.Aliases = resolveAliases(ctx, loc, allHosts, claimedAliases)
				loc.UseRegex = hostsWithUseRegex[rule.Host]

				// Inherit basic/digest auth and custom headers like the rule paths
				// do, so the per-host fallback is not an unauthenticated bypass.
				if err := p.applyDefaultBackendAuth(ing.Namespace, ing.config, loc); err != nil {
					logger.Error().Err(err).Msg("Cannot resolve auth secret for default backend, skipping")
					continue
				}
				p.resolveDefaultBackendCustomErrors(mc, ing.Namespace, ing.config, loc)

				endpointCount := 0
				if backend, ok := mc.Backends[ingDefaultBackendName]; ok {
					endpointCount = len(backend.Endpoints)
				}
				p.buildMiddlewares(ctx, loc, rule.Host, allHosts, endpointCount)

				srv.Locations = append(srv.Locations, loc)
				markProcessedIngress(ing.Ingress)
			}
		}
	}

	return mc
}
```


#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/middleware.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:53, E:82, A:0) ➔ After(N:54, E:83, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 2, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `sslRedirectEnabled` (FUNCTION_DEF)
  • + [新增呼叫邊] `Provider.buildSSLRedirect` ──[CALLS]──> `sslRedirectEnabled`
  • + [新增呼叫邊] `sslRedirectEnabled` ──[CALLS]──> `ptr.Deref (External/Pkg)`
  • - [移除呼叫邊] `Provider.buildSSLRedirect` ──[CALLS]──> `ptr.Deref (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Provider.buildSSLRedirect()`
- **變更前簽章 (Before)**: `func Provider.buildSSLRedirect(loc *location)` (L46~L54)
- **變更後簽章 (After)**: `func Provider.buildSSLRedirect(loc *location)` (L46~L48)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) buildSSLRedirect(loc *location) {
	// force-ssl-redirect redirects to HTTPS regardless of whether the Ingress has a TLS block.
	forceSSLRedirect := ptr.Deref(loc.Config.ForceSSLRedirect, false)
	// When an Ingress has a TLS block, by default SSL redirect should be applied.
	// When an Ingress does not have a TLS block, SSL redirect should not be applied.
	sslRedirect := loc.HasTLS && ptr.Deref(loc.Config.SSLRedirect, true)

	loc.SSLRedirectOnly = forceSSLRedirect || sslRedirect
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) buildSSLRedirect(loc *location) {
	loc.SSLRedirectOnly = sslRedirectEnabled(loc.Config, loc.HasTLS)
}
```


#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/model.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:2, E:0, A:0) ➔ After(N:2, E:0, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
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

#### 📄 檔案: `pkg/provider/kubernetes/ingress-nginx/translator.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:44, E:67, A:0) ➔ After(N:44, E:67, A:0)
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

### 🔹 函式: `Provider.translate()`
- **變更前簽章 (Before)**: `func Provider.translate(ctx context.Context, mc *model)` (L23~L296)
- **變更後簽章 (After)**: `func Provider.translate(ctx context.Context, mc *model)` (L23~L330)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesIngressMetadata{
					Namespace:   mc.DefaultBackend.Namespace,
					ServiceName: mc.DefaultBackend.ServiceName,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.IngressName = loc.IngressName
			obs.Metadata.Ingress.ServicePort = loc.ServicePort
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		conf.HTTP.Services[defaultBackendName] = buildService(mc.DefaultBackend, serversTransportName)

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			conf.HTTP.Services[primarySvcName] = buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesIngressMetadata{
						Namespace:   loc.Namespace,
						IngressName: loc.IngressName,
						ServiceName: loc.ServiceName,
						ServicePort: loc.ServicePort,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName))
			} else {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex))
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			rtTLS := &dynamic.Router{
				EntryPoints: p.TLSEntryPoints,
				Rule:        rule,
				RuleSyntax:  "default",
				Service:     routerSvcName,
				TLS: &dynamic.RouterTLSConfig{
					Options: loc.TLSOptionName,
				},
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
				rtTLS.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt
			conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
				applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				canaryKeyTLS := canaryKey + "-tls"
				canaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       canarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
				p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				nonCanaryKeyTLS := nonCanaryKey + "-tls"
				nonCanaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       primarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
				p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
			}
		}
	}

	return conf
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (p *Provider) translate(ctx context.Context, mc *model) *dynamic.Configuration {
	conf := &dynamic.Configuration{
		HTTP: &dynamic.HTTPConfiguration{
			Routers:           make(map[string]*dynamic.Router),
			Middlewares:       make(map[string]*dynamic.Middleware),
			Services:          make(map[string]*dynamic.Service),
			ServersTransports: make(map[string]*dynamic.ServersTransport),
		},
		TCP: &dynamic.TCPConfiguration{
			Routers:  make(map[string]*dynamic.TCPRouter),
			Services: make(map[string]*dynamic.TCPService),
		},
		TLS: &dynamic.TLSConfiguration{},
	}

	lb := &dynamic.ServersLoadBalancer{}
	lb.SetDefaults()
	conf.HTTP.Services[unavailableServiceName] = &dynamic.Service{LoadBalancer: lb}

	for _, k := range slices.Sorted(maps.Keys(mc.Certs)) {
		cp := mc.Certs[k]
		conf.TLS.Certificates = append(conf.TLS.Certificates, &tls.CertAndStores{
			Certificate: tls.Certificate{
				CertFile: types.FileOrContent(cp.Cert),
				KeyFile:  types.FileOrContent(cp.Key),
			},
		})
	}

	if mc.DefaultBackend != nil {
		obs := &dynamic.RouterObservabilityConfig{
			Metadata: &dynamic.ObservabilityMetadata{
				Ingress: &dynamic.KubernetesIngressMetadata{
					Namespace:   mc.DefaultBackend.Namespace,
					ServiceName: mc.DefaultBackend.ServiceName,
				},
			},
		}

		var serversTransportName string
		if loc := mc.DefaultBackendLocation; loc != nil {
			obs.Metadata.Ingress.IngressName = loc.IngressName
			obs.Metadata.Ingress.ServicePort = loc.ServicePort
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				serversTransportName = loc.ServersTransportName
				conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
			}
		}

		conf.HTTP.Services[defaultBackendName] = buildService(mc.DefaultBackend, serversTransportName)

		rt := &dynamic.Router{
			EntryPoints:   p.NonTLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			Observability: obs,
		}
		rtTLS := &dynamic.Router{
			EntryPoints:   p.TLSEntryPoints,
			Rule:          `PathPrefix("/")`,
			RuleSyntax:    "default",
			Priority:      math.MinInt32,
			Service:       defaultBackendName,
			TLS:           &dynamic.RouterTLSConfig{},
			Observability: obs,
		}

		// Apply the full middleware stack from the ingress location annotations to
		// both catch-all routers, so options like enable-cors, custom-headers,
		// rate-limits, redirects, etc. configured on a "spec.defaultBackend only"
		// ingress reach its catch-all routers.
		if loc := mc.DefaultBackendLocation; loc != nil {
			// Client-auth TLS option (auth-tls-secret) must gate the catch-all TLS
			// router too, matching ingress-nginx which enforces it server-wide.
			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
				rtTLS.TLS.Options = loc.TLSOptionName
			}

			p.applyMiddlewares(mc, loc, defaultBackendName, rt, conf)
			p.applyMiddlewares(mc, loc, defaultBackendTLSName, rtTLS, conf)
		}

		conf.HTTP.Routers[defaultBackendName] = rt
		conf.HTTP.Routers[defaultBackendTLSName] = rtTLS
	}

	for _, pt := range mc.PassthroughBackends {
		backend, ok := mc.Backends[pt.BackendName]
		if !ok {
			log.Ctx(ctx).Error().Msgf("Passthrough backend %q not found in metamodel", pt.BackendName)
			continue
		}

		lb := &dynamic.TCPServersLoadBalancer{}
		for _, ep := range backend.Endpoints {
			lb.Servers = append(lb.Servers, dynamic.TCPServer{Address: ep.Address})
		}

		conf.TCP.Services[pt.BackendName] = &dynamic.TCPService{LoadBalancer: lb}
		conf.TCP.Routers[pt.RouterKey] = &dynamic.TCPRouter{
			EntryPoints: p.TLSEntryPoints,
			Rule:        fmt.Sprintf("HostSNI(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.BackendName,
			TLS:         &dynamic.RouterTCPTLSConfig{Passthrough: true},
		}

		// The HTTP part is skipped when the serversTransport could not be built,
		// the TCP passthrough router above being unaffected by it.
		if pt.HTTPServiceName == "" {
			continue
		}

		// Like ingress-nginx, the host also gets an HTTP router proxying to the backend
		// (honoring backend-protocol), so plain HTTP requests and requests bypassing the
		// SSL redirect (e.g. X-Forwarded-Proto: https) behave like nginx instead of
		// hitting an internal service.
		if pt.ServersTransport != nil && pt.ServersTransportName != "" {
			if _, exists := conf.HTTP.ServersTransports[pt.ServersTransportName]; !exists {
				conf.HTTP.ServersTransports[pt.ServersTransportName] = pt.ServersTransport
			}
		}
		conf.HTTP.Services[pt.HTTPServiceName] = buildServiceWithLocConfig(backend, pt.ServersTransportName, pt.Config)

		rt := &dynamic.Router{
			EntryPoints: p.NonTLSEntryPoints,
			Rule:        fmt.Sprintf("Host(%q)", pt.Hostname),
			RuleSyntax:  "default",
			Service:     pt.HTTPServiceName,
		}

		if pt.SSLRedirect {
			redirectMWName := pt.RouterKey + "-redirect-scheme"
			conf.HTTP.Middlewares[redirectMWName] = &dynamic.Middleware{
				RedirectScheme: &dynamic.RedirectScheme{Scheme: "https", ForcePermanentRedirect: true},
			}
			rt.Middlewares = []string{redirectMWName}
		}

		conf.HTTP.Routers[pt.RouterKey+"-http"] = rt
	}

	for _, srv := range mc.Servers {
		for _, loc := range srv.Locations {
			if loc.ServersTransport != nil && loc.ServersTransportName != "" {
				if _, exists := conf.HTTP.ServersTransports[loc.ServersTransportName]; !exists {
					conf.HTTP.ServersTransports[loc.ServersTransportName] = loc.ServersTransport
				}
			}

			if loc.TLSOption != nil && loc.TLSOptionName != "" {
				if conf.TLS.Options == nil {
					conf.TLS.Options = make(map[string]tls.Options)
				}
				if _, exists := conf.TLS.Options[loc.TLSOptionName]; !exists {
					conf.TLS.Options[loc.TLSOptionName] = *loc.TLSOption
				}
			}

			backend, ok := mc.Backends[loc.BackendName]
			if !ok {
				log.Ctx(ctx).Error().Msgf("Backend %q not found for location %s%s", loc.BackendName, srv.Hostname, loc.Path)
				continue
			}

			primarySvcName := loc.BackendName
			conf.HTTP.Services[primarySvcName] = buildServiceWithLocConfig(backend, loc.ServersTransportName, loc.Config)

			obs := &dynamic.RouterObservabilityConfig{
				Metadata: &dynamic.ObservabilityMetadata{
					Ingress: &dynamic.KubernetesIngressMetadata{
						Namespace:   loc.Namespace,
						IngressName: loc.IngressName,
						ServiceName: loc.ServiceName,
						ServicePort: loc.ServicePort,
					},
				},
			}

			routerSvcName := primarySvcName
			canarySvcName := primarySvcName + "-canary"
			if loc.Canary != nil {
				canaryBackend, ok := mc.Backends[loc.Canary.BackendName]
				if ok {
					canaryWRRName := primarySvcName + "-wrr"

					canarySvc := buildServiceWithLocConfig(canaryBackend, loc.ServersTransportName, loc.Config)
					conf.HTTP.Services[canarySvcName] = canarySvc

					conf.HTTP.Services[canaryWRRName] = &dynamic.Service{
						Weighted: &dynamic.WeightedRoundRobin{
							Sticky: buildSticky(loc.Config, "wrr"),
							Services: []dynamic.WRRService{
								{Name: primarySvcName, Weight: new(loc.Canary.WeightTotal - loc.Canary.Weight)},
								{Name: canarySvcName, Weight: new(loc.Canary.Weight)},
							},
						},
					}
					routerSvcName = canaryWRRName
				}
			}

			rule := buildRule(srv.Hostname, loc)

			var routerKey string
			if loc.IsIngressDefaultBackend {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-default-backend", loc.Namespace, loc.IngressName))
			} else {
				routerKey = provider.Normalize(fmt.Sprintf("%s-%s-rule-%d-path-%d", loc.Namespace, loc.IngressName, loc.RuleIndex, loc.LocationIndex))
			}

			rt := &dynamic.Router{
				EntryPoints:   p.NonTLSEntryPoints,
				Rule:          rule,
				RuleSyntax:    "default",
				Service:       routerSvcName,
				Observability: obs,
			}

			rtTLS := &dynamic.Router{
				EntryPoints: p.TLSEntryPoints,
				Rule:        rule,
				RuleSyntax:  "default",
				Service:     routerSvcName,
				TLS: &dynamic.RouterTLSConfig{
					Options: loc.TLSOptionName,
				},
				Observability: obs,
			}

			// TODO: in case we want to add the unavailable service only when it is used this should be done here.
			if loc.Error {
				rt.Service = unavailableServiceName
				rtTLS.Service = unavailableServiceName
			}

			conf.HTTP.Routers[routerKey] = rt
			conf.HTTP.Routers[routerKey+"-tls"] = rtTLS

			if !loc.Error {
				p.applyMiddlewares(mc, loc, routerKey, rt, conf)
				p.applyMiddlewares(mc, loc, routerKey+"-tls", rtTLS, conf)
				applyFromToWwwRedirect(loc, routerKey, rt, obs, conf)
				applyFromToWwwRedirect(loc, routerKey+"-tls", rtTLS, obs, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresCanaryRouter() {
				canaryKey := routerKey + "-canary"
				canaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       canarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKey] = canaryRouter
				p.applyMiddlewares(mc, loc, canaryKey, canaryRouter, conf)

				canaryKeyTLS := canaryKey + "-tls"
				canaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       canarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[canaryKeyTLS] = canaryRouterTLS
				p.applyMiddlewares(mc, loc, canaryKeyTLS, canaryRouterTLS, conf)
			}

			if loc.Canary != nil && loc.Canary.RequiresNonCanaryRouter() {
				nonCanaryKey := routerKey + "-non-canary"
				nonCanaryRouter := &dynamic.Router{
					EntryPoints:   rt.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rt.RuleSyntax,
					Service:       primarySvcName,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKey] = nonCanaryRouter
				p.applyMiddlewares(mc, loc, nonCanaryKey, nonCanaryRouter, conf)

				nonCanaryKeyTLS := nonCanaryKey + "-tls"
				nonCanaryRouterTLS := &dynamic.Router{
					EntryPoints:   rtTLS.EntryPoints,
					Rule:          appendNonCanaryRule(rule, loc.Canary),
					RuleSyntax:    rtTLS.RuleSyntax,
					Service:       primarySvcName,
					TLS:           rtTLS.TLS,
					Observability: obs,
				}
				conf.HTTP.Routers[nonCanaryKeyTLS] = nonCanaryRouterTLS
				p.applyMiddlewares(mc, loc, nonCanaryKeyTLS, nonCanaryRouterTLS, conf)
			}
		}
	}

	return conf
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/traefik show 2157e70100babb64cd4e001fc8ca7e6a187cfa82
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 2157e70100babb64cd4e001fc8ca7e6a187cfa82~1 --file test_repos/traefik/pkg/provider/kubernetes/ingress-nginx/build.go
   ```
