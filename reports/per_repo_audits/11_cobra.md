# 🔬 CODE-Map 基準審查獨立驗證報告: `cobra`
> **技術生態**: `Go (全域 CLI 命令樹 / 旗標分發基石)`  
> **本地倉庫路徑**: `test_repos/cobra`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 24 Files  
> **報告生成時間**: 2026-10-20 21:41:21  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `10` / `24` | `41.7%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `10` / `24` | `41.7%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `4` / `24` | `16.7%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`20` / `24`** | **`83.3%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `24` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `746ef071`
- **完整 Hash**: `746ef07158728502482cea9f880a6f4b21ef29a9`
- **說明 (Ground Truth)**: fix: prevent completions from mutating os.Args via append side effect (#2356)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:126, E:144, A:0) ➔ After(N:128, E:146, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 0, +Edges: 2, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `copy (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `make (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.getCompletions` ──[CALLS]──> `make (External/Pkg)`
  • + [新增呼叫邊] `Command.getCompletions` ──[CALLS]──> `copy (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.getCompletions()`
- **變更前簽章 (Before)**: `func Command.getCompletions(args []string)` (L316~L582)
- **變更後簽章 (After)**: `func Command.getCompletions(args []string)` (L316~L585)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []Completion, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !ok || flagCompletion {
			return finalCmd, []Completion{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []Completion{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []Completion{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []Completion
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				_, acceptsMultiple := flag.Value.(SliceValue)
				acceptsMultiple = acceptsMultiple ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo")

				if !flag.Changed || acceptsMultiple {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		// check current and parent commands for a custom DefaultShellCompDirective
		for cmd := finalCmd; cmd != nil; cmd = cmd.parent {
			if cmd.CompletionOptions.DefaultShellCompDirective != nil {
				directive = *cmd.CompletionOptions.DefaultShellCompDirective
				break
			}
		}

		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn CompletionFunc
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []Completion
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []Completion, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	// Copy trimmedArgs to a new slice to avoid mutating the caller's
	// backing array (which may be os.Args) when later appending "--".
	trimmedArgs := make([]string, len(args)-1)
	copy(trimmedArgs, args[:len(args)-1])

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !ok || flagCompletion {
			return finalCmd, []Completion{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []Completion{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []Completion{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []Completion
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				_, acceptsMultiple := flag.Value.(SliceValue)
				acceptsMultiple = acceptsMultiple ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo")

				if !flag.Changed || acceptsMultiple {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		// check current and parent commands for a custom DefaultShellCompDirective
		for cmd := finalCmd; cmd != nil; cmd = cmd.parent {
			if cmd.CompletionOptions.DefaultShellCompDirective != nil {
				directive = *cmd.CompletionOptions.DefaultShellCompDirective
				break
			}
		}

		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn CompletionFunc
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []Completion
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```


---

### 🔹 Commit #02: `61968e89`
- **完整 Hash**: `61968e893eee2f27696c2fbc8e34fa5c4afaf7c4`
- **說明 (Ground Truth)**: fix: quote args in fish shell completion (#2285)
- **變更檔案數**: 1

#### 📄 檔案: `fish_completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:12, E:11, A:0) ➔ After(N:12, E:11, A:0)
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

### 🔹 函式: `genFishComp()`
- **變更前簽章 (Before)**: `func genFishComp(buf io.StringWriter, name string, includeDesc bool)` (L25~L273)
- **變更後簽章 (After)**: `func genFishComp(buf io.StringWriter, name string, includeDesc bool)` (L25~L273)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func genFishComp(buf io.StringWriter, name string, includeDesc bool) {
	// Variables should not contain a '-' or ':' character
	nameForVar := name
	nameForVar = strings.ReplaceAll(nameForVar, "-", "_")
	nameForVar = strings.ReplaceAll(nameForVar, ":", "_")

	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}
	WriteStringAndCheck(buf, fmt.Sprintf("# fish completion for %-36s -*- shell-script -*-\n", name))
	WriteStringAndCheck(buf, fmt.Sprintf(`
function __%[1]s_debug
    set -l file "$BASH_COMP_DEBUG_FILE"
    if test -n "$file"
        echo "$argv" >> $file
    end
end

function __%[1]s_perform_completion
    __%[1]s_debug "Starting __%[1]s_perform_completion"

    # Extract all args except the last one
    set -l args (commandline -opc)
    # Extract the last arg and escape it in case it is a space
    set -l lastArg (string escape -- (commandline -ct))

    __%[1]s_debug "args: $args"
    __%[1]s_debug "last arg: $lastArg"

    # Disable ActiveHelp which is not supported for fish shell
    set -l requestComp "%[10]s=0 $args[1] %[3]s $args[2..-1] $lastArg"

    __%[1]s_debug "Calling $requestComp"
    set -l results (eval $requestComp 2> /dev/null)

    # Some programs may output extra empty lines after the directive.
    # Let's ignore them or else it will break completion.
    # Ref: https://github.com/spf13/cobra/issues/1279
    for line in $results[-1..1]
        if test (string trim -- $line) = ""
            # Found an empty line, remove it
            set results $results[1..-2]
        else
            # Found non-empty line, we have our proper output
            break
        end
    end

    set -l comps $results[1..-2]
    set -l directiveLine $results[-1]

    # For Fish, when completing a flag with an = (e.g., <program> -n=<TAB>)
    # completions must be prefixed with the flag
    set -l flagPrefix (string match -r -- '-.*=' "$lastArg")

    __%[1]s_debug "Comps: $comps"
    __%[1]s_debug "DirectiveLine: $directiveLine"
    __%[1]s_debug "flagPrefix: $flagPrefix"

    for comp in $comps
        printf "%%s%%s\n" "$flagPrefix" "$comp"
    end

    printf "%%s\n" "$directiveLine"
end

# this function limits calls to __%[1]s_perform_completion, by caching the result behind $__%[1]s_perform_completion_once_result
function __%[1]s_perform_completion_once
    __%[1]s_debug "Starting __%[1]s_perform_completion_once"

    if test -n "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "Seems like a valid result already exists, skipping __%[1]s_perform_completion"
        return 0
    end

    set --global __%[1]s_perform_completion_once_result (__%[1]s_perform_completion)
    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "No completions, probably due to a failure"
        return 1
    end

    __%[1]s_debug "Performed completions and set __%[1]s_perform_completion_once_result"
    return 0
end

# this function is used to clear the $__%[1]s_perform_completion_once_result variable after completions are run
function __%[1]s_clear_perform_completion_once_result
    __%[1]s_debug ""
    __%[1]s_debug "========= clearing previously set __%[1]s_perform_completion_once_result variable =========="
    set --erase __%[1]s_perform_completion_once_result
    __%[1]s_debug "Successfully erased the variable __%[1]s_perform_completion_once_result"
end

function __%[1]s_requires_order_preservation
    __%[1]s_debug ""
    __%[1]s_debug "========= checking if order preservation is required =========="

    __%[1]s_perform_completion_once
    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "Error determining if order preservation is required"
        return 1
    end

    set -l directive (string sub --start 2 $__%[1]s_perform_completion_once_result[-1])
    __%[1]s_debug "Directive is: $directive"

    set -l shellCompDirectiveKeepOrder %[9]d
    set -l keeporder (math (math --scale 0 $directive / $shellCompDirectiveKeepOrder) %% 2)
    __%[1]s_debug "Keeporder is: $keeporder"

    if test $keeporder -ne 0
        __%[1]s_debug "This does require order preservation"
        return 0
    end

    __%[1]s_debug "This doesn't require order preservation"
    return 1
end


# This function does two things:
# - Obtain the completions and store them in the global __%[1]s_comp_results
# - Return false if file completion should be performed
function __%[1]s_prepare_completions
    __%[1]s_debug ""
    __%[1]s_debug "========= starting completion logic =========="

    # Start fresh
    set --erase __%[1]s_comp_results

    __%[1]s_perform_completion_once
    __%[1]s_debug "Completion results: $__%[1]s_perform_completion_once_result"

    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "No completion, probably due to a failure"
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l directive (string sub --start 2 $__%[1]s_perform_completion_once_result[-1])
    set --global __%[1]s_comp_results $__%[1]s_perform_completion_once_result[1..-2]

    __%[1]s_debug "Completions are: $__%[1]s_comp_results"
    __%[1]s_debug "Directive is: $directive"

    set -l shellCompDirectiveError %[4]d
    set -l shellCompDirectiveNoSpace %[5]d
    set -l shellCompDirectiveNoFileComp %[6]d
    set -l shellCompDirectiveFilterFileExt %[7]d
    set -l shellCompDirectiveFilterDirs %[8]d

    if test -z "$directive"
        set directive 0
    end

    set -l compErr (math (math --scale 0 $directive / $shellCompDirectiveError) %% 2)
    if test $compErr -eq 1
        __%[1]s_debug "Received error directive: aborting."
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l filefilter (math (math --scale 0 $directive / $shellCompDirectiveFilterFileExt) %% 2)
    set -l dirfilter (math (math --scale 0 $directive / $shellCompDirectiveFilterDirs) %% 2)
    if test $filefilter -eq 1; or test $dirfilter -eq 1
        __%[1]s_debug "File extension filtering or directory filtering not supported"
        # Do full file completion instead
        return 1
    end

    set -l nospace (math (math --scale 0 $directive / $shellCompDirectiveNoSpace) %% 2)
    set -l nofiles (math (math --scale 0 $directive / $shellCompDirectiveNoFileComp) %% 2)

    __%[1]s_debug "nospace: $nospace, nofiles: $nofiles"

    # If we want to prevent a space, or if file completion is NOT disabled,
    # we need to count the number of valid completions.
    # To do so, we will filter on prefix as the completions we have received
    # may not already be filtered so as to allow fish to match on different
    # criteria than the prefix.
    if test $nospace -ne 0; or test $nofiles -eq 0
        set -l prefix (commandline -t | string escape --style=regex)
        __%[1]s_debug "prefix: $prefix"

        set -l completions (string match -r -- "^$prefix.*" $__%[1]s_comp_results)
        set --global __%[1]s_comp_results $completions
        __%[1]s_debug "Filtered completions are: $__%[1]s_comp_results"

        # Important not to quote the variable for count to work
        set -l numComps (count $__%[1]s_comp_results)
        __%[1]s_debug "numComps: $numComps"

        if test $numComps -eq 1; and test $nospace -ne 0
            # We must first split on \t to get rid of the descriptions to be
            # able to check what the actual completion will be.
            # We don't need descriptions anyway since there is only a single
            # real completion which the shell will expand immediately.
            set -l split (string split --max 1 \t $__%[1]s_comp_results[1])

            # Fish won't add a space if the completion ends with any
            # of the following characters: @=/:.,
            set -l lastChar (string sub -s -1 -- $split)
            if not string match -r -q "[@=/:.,]" -- "$lastChar"
                # In other cases, to support the "nospace" directive we trick the shell
                # by outputting an extra, longer completion.
                __%[1]s_debug "Adding second completion to perform nospace directive"
                set --global __%[1]s_comp_results $split[1] $split[1].
                __%[1]s_debug "Completions are now: $__%[1]s_comp_results"
            end
        end

        if test $numComps -eq 0; and test $nofiles -eq 0
            # To be consistent with bash and zsh, we only trigger file
            # completion when there are no other completions
            __%[1]s_debug "Requesting file completion"
            return 1
        end
    end

    return 0
end

# Since Fish completions are only loaded once the user triggers them, we trigger them ourselves
# so we can properly delete any completions provided by another script.
# Only do this if the program can be found, or else fish may print some errors; besides,
# the existing completions will only be loaded if the program can be found.
if type -q "%[2]s"
    # The space after the program name is essential to trigger completion for the program
    # and not completion of the program name itself.
    # Also, we use '> /dev/null 2>&1' since '&>' is not supported in older versions of fish.
    complete --do-complete "%[2]s " > /dev/null 2>&1
end

# Remove any pre-existing completions for the program since we will be handling all of them.
complete -c %[2]s -e

# this will get called after the two calls below and clear the $__%[1]s_perform_completion_once_result global
complete -c %[2]s -n '__%[1]s_clear_perform_completion_once_result'
# The call to __%[1]s_prepare_completions will setup __%[1]s_comp_results
# which provides the program's completion choices.
# If this doesn't require order preservation, we don't use the -k flag
complete -c %[2]s -n 'not __%[1]s_requires_order_preservation && __%[1]s_prepare_completions' -f -a '$__%[1]s_comp_results'
# otherwise we use the -k flag
complete -k -c %[2]s -n '__%[1]s_requires_order_preservation && __%[1]s_prepare_completions' -f -a '$__%[1]s_comp_results'
`, nameForVar, name, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder, activeHelpEnvVar(name)))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func genFishComp(buf io.StringWriter, name string, includeDesc bool) {
	// Variables should not contain a '-' or ':' character
	nameForVar := name
	nameForVar = strings.ReplaceAll(nameForVar, "-", "_")
	nameForVar = strings.ReplaceAll(nameForVar, ":", "_")

	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}
	WriteStringAndCheck(buf, fmt.Sprintf("# fish completion for %-36s -*- shell-script -*-\n", name))
	WriteStringAndCheck(buf, fmt.Sprintf(`
function __%[1]s_debug
    set -l file "$BASH_COMP_DEBUG_FILE"
    if test -n "$file"
        echo "$argv" >> $file
    end
end

function __%[1]s_perform_completion
    __%[1]s_debug "Starting __%[1]s_perform_completion"

    # Extract all args except the last one
    set -l args (commandline -opc)
    # Extract the last arg and escape it in case it is a space or wildcard
    set -l lastArg (string escape -- (commandline -ct))

    __%[1]s_debug "args: $args"
    __%[1]s_debug "last arg: $lastArg"

    # Disable ActiveHelp which is not supported for fish shell
    set -l requestComp "%[10]s=0 $args[1] %[3]s $(string join ' ' -- (string escape -- $args[2..-1])) $lastArg"

    __%[1]s_debug "Calling $requestComp"
    set -l results (eval $requestComp 2> /dev/null)

    # Some programs may output extra empty lines after the directive.
    # Let's ignore them or else it will break completion.
    # Ref: https://github.com/spf13/cobra/issues/1279
    for line in $results[-1..1]
        if test (string trim -- $line) = ""
            # Found an empty line, remove it
            set results $results[1..-2]
        else
            # Found non-empty line, we have our proper output
            break
        end
    end

    set -l comps $results[1..-2]
    set -l directiveLine $results[-1]

    # For Fish, when completing a flag with an = (e.g., <program> -n=<TAB>)
    # completions must be prefixed with the flag
    set -l flagPrefix (string match -r -- '-.*=' "$lastArg")

    __%[1]s_debug "Comps: $comps"
    __%[1]s_debug "DirectiveLine: $directiveLine"
    __%[1]s_debug "flagPrefix: $flagPrefix"

    for comp in $comps
        printf "%%s%%s\n" "$flagPrefix" "$comp"
    end

    printf "%%s\n" "$directiveLine"
end

# this function limits calls to __%[1]s_perform_completion, by caching the result behind $__%[1]s_perform_completion_once_result
function __%[1]s_perform_completion_once
    __%[1]s_debug "Starting __%[1]s_perform_completion_once"

    if test -n "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "Seems like a valid result already exists, skipping __%[1]s_perform_completion"
        return 0
    end

    set --global __%[1]s_perform_completion_once_result (__%[1]s_perform_completion)
    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "No completions, probably due to a failure"
        return 1
    end

    __%[1]s_debug "Performed completions and set __%[1]s_perform_completion_once_result"
    return 0
end

# this function is used to clear the $__%[1]s_perform_completion_once_result variable after completions are run
function __%[1]s_clear_perform_completion_once_result
    __%[1]s_debug ""
    __%[1]s_debug "========= clearing previously set __%[1]s_perform_completion_once_result variable =========="
    set --erase __%[1]s_perform_completion_once_result
    __%[1]s_debug "Successfully erased the variable __%[1]s_perform_completion_once_result"
end

function __%[1]s_requires_order_preservation
    __%[1]s_debug ""
    __%[1]s_debug "========= checking if order preservation is required =========="

    __%[1]s_perform_completion_once
    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "Error determining if order preservation is required"
        return 1
    end

    set -l directive (string sub --start 2 $__%[1]s_perform_completion_once_result[-1])
    __%[1]s_debug "Directive is: $directive"

    set -l shellCompDirectiveKeepOrder %[9]d
    set -l keeporder (math (math --scale 0 $directive / $shellCompDirectiveKeepOrder) %% 2)
    __%[1]s_debug "Keeporder is: $keeporder"

    if test $keeporder -ne 0
        __%[1]s_debug "This does require order preservation"
        return 0
    end

    __%[1]s_debug "This doesn't require order preservation"
    return 1
end


# This function does two things:
# - Obtain the completions and store them in the global __%[1]s_comp_results
# - Return false if file completion should be performed
function __%[1]s_prepare_completions
    __%[1]s_debug ""
    __%[1]s_debug "========= starting completion logic =========="

    # Start fresh
    set --erase __%[1]s_comp_results

    __%[1]s_perform_completion_once
    __%[1]s_debug "Completion results: $__%[1]s_perform_completion_once_result"

    if test -z "$__%[1]s_perform_completion_once_result"
        __%[1]s_debug "No completion, probably due to a failure"
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l directive (string sub --start 2 $__%[1]s_perform_completion_once_result[-1])
    set --global __%[1]s_comp_results $__%[1]s_perform_completion_once_result[1..-2]

    __%[1]s_debug "Completions are: $__%[1]s_comp_results"
    __%[1]s_debug "Directive is: $directive"

    set -l shellCompDirectiveError %[4]d
    set -l shellCompDirectiveNoSpace %[5]d
    set -l shellCompDirectiveNoFileComp %[6]d
    set -l shellCompDirectiveFilterFileExt %[7]d
    set -l shellCompDirectiveFilterDirs %[8]d

    if test -z "$directive"
        set directive 0
    end

    set -l compErr (math (math --scale 0 $directive / $shellCompDirectiveError) %% 2)
    if test $compErr -eq 1
        __%[1]s_debug "Received error directive: aborting."
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l filefilter (math (math --scale 0 $directive / $shellCompDirectiveFilterFileExt) %% 2)
    set -l dirfilter (math (math --scale 0 $directive / $shellCompDirectiveFilterDirs) %% 2)
    if test $filefilter -eq 1; or test $dirfilter -eq 1
        __%[1]s_debug "File extension filtering or directory filtering not supported"
        # Do full file completion instead
        return 1
    end

    set -l nospace (math (math --scale 0 $directive / $shellCompDirectiveNoSpace) %% 2)
    set -l nofiles (math (math --scale 0 $directive / $shellCompDirectiveNoFileComp) %% 2)

    __%[1]s_debug "nospace: $nospace, nofiles: $nofiles"

    # If we want to prevent a space, or if file completion is NOT disabled,
    # we need to count the number of valid completions.
    # To do so, we will filter on prefix as the completions we have received
    # may not already be filtered so as to allow fish to match on different
    # criteria than the prefix.
    if test $nospace -ne 0; or test $nofiles -eq 0
        set -l prefix (commandline -t | string escape --style=regex)
        __%[1]s_debug "prefix: $prefix"

        set -l completions (string match -r -- "^$prefix.*" $__%[1]s_comp_results)
        set --global __%[1]s_comp_results $completions
        __%[1]s_debug "Filtered completions are: $__%[1]s_comp_results"

        # Important not to quote the variable for count to work
        set -l numComps (count $__%[1]s_comp_results)
        __%[1]s_debug "numComps: $numComps"

        if test $numComps -eq 1; and test $nospace -ne 0
            # We must first split on \t to get rid of the descriptions to be
            # able to check what the actual completion will be.
            # We don't need descriptions anyway since there is only a single
            # real completion which the shell will expand immediately.
            set -l split (string split --max 1 \t $__%[1]s_comp_results[1])

            # Fish won't add a space if the completion ends with any
            # of the following characters: @=/:.,
            set -l lastChar (string sub -s -1 -- $split)
            if not string match -r -q "[@=/:.,]" -- "$lastChar"
                # In other cases, to support the "nospace" directive we trick the shell
                # by outputting an extra, longer completion.
                __%[1]s_debug "Adding second completion to perform nospace directive"
                set --global __%[1]s_comp_results $split[1] $split[1].
                __%[1]s_debug "Completions are now: $__%[1]s_comp_results"
            end
        end

        if test $numComps -eq 0; and test $nofiles -eq 0
            # To be consistent with bash and zsh, we only trigger file
            # completion when there are no other completions
            __%[1]s_debug "Requesting file completion"
            return 1
        end
    end

    return 0
end

# Since Fish completions are only loaded once the user triggers them, we trigger them ourselves
# so we can properly delete any completions provided by another script.
# Only do this if the program can be found, or else fish may print some errors; besides,
# the existing completions will only be loaded if the program can be found.
if type -q "%[2]s"
    # The space after the program name is essential to trigger completion for the program
    # and not completion of the program name itself.
    # Also, we use '> /dev/null 2>&1' since '&>' is not supported in older versions of fish.
    complete --do-complete "%[2]s " > /dev/null 2>&1
end

# Remove any pre-existing completions for the program since we will be handling all of them.
complete -c %[2]s -e

# this will get called after the two calls below and clear the $__%[1]s_perform_completion_once_result global
complete -c %[2]s -n '__%[1]s_clear_perform_completion_once_result'
# The call to __%[1]s_prepare_completions will setup __%[1]s_comp_results
# which provides the program's completion choices.
# If this doesn't require order preservation, we don't use the -k flag
complete -c %[2]s -n 'not __%[1]s_requires_order_preservation && __%[1]s_prepare_completions' -f -a '$__%[1]s_comp_results'
# otherwise we use the -k flag
complete -k -c %[2]s -n '__%[1]s_requires_order_preservation && __%[1]s_prepare_completions' -f -a '$__%[1]s_comp_results'
`, nameForVar, name, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder, activeHelpEnvVar(name)))
}
```


---

### 🔹 Commit #03: `6dec1ae2`
- **完整 Hash**: `6dec1ae26659a130bdb4c985768d1853b0e1bc06`
- **說明 (Ground Truth)**: The default ShellCompDirective can be customized for a command and its subcommands (#2238)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:125, E:144, A:0) ➔ After(N:126, E:144, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `CompletionOptions.SetDefaultShellCompDirective` (FUNCTION_DEF)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.getCompletions()`
- **變更前簽章 (Before)**: `func Command.getCompletions(args []string)` (L309~L567)
- **變更後簽章 (After)**: `func Command.getCompletions(args []string)` (L316~L582)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []Completion, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !ok || flagCompletion {
			return finalCmd, []Completion{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []Completion{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []Completion{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []Completion
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				_, acceptsMultiple := flag.Value.(SliceValue)
				acceptsMultiple = acceptsMultiple ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo")

				if !flag.Changed || acceptsMultiple {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn CompletionFunc
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []Completion
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []Completion, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []Completion{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !ok || flagCompletion {
			return finalCmd, []Completion{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []Completion{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []Completion{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []Completion
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				_, acceptsMultiple := flag.Value.(SliceValue)
				acceptsMultiple = acceptsMultiple ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo")

				if !flag.Changed || acceptsMultiple {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		// check current and parent commands for a custom DefaultShellCompDirective
		for cmd := finalCmd; cmd != nil; cmd = cmd.parent {
			if cmd.CompletionOptions.DefaultShellCompDirective != nil {
				directive = *cmd.CompletionOptions.DefaultShellCompDirective
				break
			}
		}

		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn CompletionFunc
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []Completion
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```


---

### 🔹 Commit #04: `4f9ef8cd`
- **完整 Hash**: `4f9ef8cdbbc88c5302be95e0e67fd78ebbfa9dd2`
- **說明 (Ground Truth)**: Update command.go (#2248)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:239, E:431, A:0) ➔ After(N:239, E:431, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `defaultUsageFunc()`
- **變更前簽章 (Before)**: `func defaultUsageFunc(w io.Writer, in interface{})` (L1974~L2040)
- **變更後簽章 (After)**: `func defaultUsageFunc(w io.Writer, in interface{})` (L1974~L2040)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func defaultUsageFunc(w io.Writer, in interface{}) error {
	c := in.(*Command)
	fmt.Fprint(w, "Usage:")
	if c.Runnable() {
		fmt.Fprintf(w, "\n  %s", c.UseLine())
	}
	if c.HasAvailableSubCommands() {
		fmt.Fprintf(w, "\n  %s [command]", c.CommandPath())
	}
	if len(c.Aliases) > 0 {
		fmt.Fprintf(w, "\n\nAliases:\n")
		fmt.Fprintf(w, "  %s", c.NameAndAliases())
	}
	if c.HasExample() {
		fmt.Fprintf(w, "\n\nExamples:\n")
		fmt.Fprintf(w, "%s", c.Example)
	}
	if c.HasAvailableSubCommands() {
		cmds := c.Commands()
		if len(c.Groups()) == 0 {
			fmt.Fprintf(w, "\n\nAvailable Commands:")
			for _, subcmd := range cmds {
				if subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName {
					fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
				}
			}
		} else {
			for _, group := range c.Groups() {
				fmt.Fprintf(w, "\n\n%s", group.Title)
				for _, subcmd := range cmds {
					if subcmd.GroupID == group.ID && (subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName) {
						fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
					}
				}
			}
			if !c.AllChildCommandsHaveGroup() {
				fmt.Fprintf(w, "\n\nAdditional Commands:")
				for _, subcmd := range cmds {
					if subcmd.GroupID == "" && (subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName) {
						fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
					}
				}
			}
		}
	}
	if c.HasAvailableLocalFlags() {
		fmt.Fprintf(w, "\n\nFlags:\n")
		fmt.Fprint(w, trimRightSpace(c.LocalFlags().FlagUsages()))
	}
	if c.HasAvailableInheritedFlags() {
		fmt.Fprintf(w, "\n\nGlobal Flags:\n")
		fmt.Fprint(w, trimRightSpace(c.InheritedFlags().FlagUsages()))
	}
	if c.HasHelpSubCommands() {
		fmt.Fprintf(w, "\n\nAdditional help topcis:")
		for _, subcmd := range c.Commands() {
			if subcmd.IsAdditionalHelpTopicCommand() {
				fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.CommandPath(), subcmd.CommandPathPadding()), subcmd.Short)
			}
		}
	}
	if c.HasAvailableSubCommands() {
		fmt.Fprintf(w, "\n\nUse \"%s [command] --help\" for more information about a command.", c.CommandPath())
	}
	fmt.Fprintln(w)
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func defaultUsageFunc(w io.Writer, in interface{}) error {
	c := in.(*Command)
	fmt.Fprint(w, "Usage:")
	if c.Runnable() {
		fmt.Fprintf(w, "\n  %s", c.UseLine())
	}
	if c.HasAvailableSubCommands() {
		fmt.Fprintf(w, "\n  %s [command]", c.CommandPath())
	}
	if len(c.Aliases) > 0 {
		fmt.Fprintf(w, "\n\nAliases:\n")
		fmt.Fprintf(w, "  %s", c.NameAndAliases())
	}
	if c.HasExample() {
		fmt.Fprintf(w, "\n\nExamples:\n")
		fmt.Fprintf(w, "%s", c.Example)
	}
	if c.HasAvailableSubCommands() {
		cmds := c.Commands()
		if len(c.Groups()) == 0 {
			fmt.Fprintf(w, "\n\nAvailable Commands:")
			for _, subcmd := range cmds {
				if subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName {
					fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
				}
			}
		} else {
			for _, group := range c.Groups() {
				fmt.Fprintf(w, "\n\n%s", group.Title)
				for _, subcmd := range cmds {
					if subcmd.GroupID == group.ID && (subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName) {
						fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
					}
				}
			}
			if !c.AllChildCommandsHaveGroup() {
				fmt.Fprintf(w, "\n\nAdditional Commands:")
				for _, subcmd := range cmds {
					if subcmd.GroupID == "" && (subcmd.IsAvailableCommand() || subcmd.Name() == helpCommandName) {
						fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.Name(), subcmd.NamePadding()), subcmd.Short)
					}
				}
			}
		}
	}
	if c.HasAvailableLocalFlags() {
		fmt.Fprintf(w, "\n\nFlags:\n")
		fmt.Fprint(w, trimRightSpace(c.LocalFlags().FlagUsages()))
	}
	if c.HasAvailableInheritedFlags() {
		fmt.Fprintf(w, "\n\nGlobal Flags:\n")
		fmt.Fprint(w, trimRightSpace(c.InheritedFlags().FlagUsages()))
	}
	if c.HasHelpSubCommands() {
		fmt.Fprintf(w, "\n\nAdditional help topics:")
		for _, subcmd := range c.Commands() {
			if subcmd.IsAdditionalHelpTopicCommand() {
				fmt.Fprintf(w, "\n  %s %s", rpad(subcmd.CommandPath(), subcmd.CommandPathPadding()), subcmd.Short)
			}
		}
	}
	if c.HasAvailableSubCommands() {
		fmt.Fprintf(w, "\n\nUse \"%s [command] --help\" for more information about a command.", c.CommandPath())
	}
	fmt.Fprintln(w)
	return nil
}
```


---

### 🔹 Commit #05: `1995054b`
- **完整 Hash**: `1995054b003053cc1e404bccfbf6d168e8731509`
- **說明 (Ground Truth)**: Flow context to command in SetHelpFunc (#2241)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:239, E:431, A:0) ➔ After(N:239, E:431, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.InitDefaultHelpCmd()`
- **變更前簽章 (Before)**: `func Command.InitDefaultHelpCmd()` (L1263~L1309)
- **變更後簽章 (After)**: `func Command.InitDefaultHelpCmd()` (L1263~L1314)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) InitDefaultHelpCmd() {
	if !c.HasSubCommands() {
		return
	}

	if c.helpCommand == nil {
		c.helpCommand = &Command{
			Use:   "help [command]",
			Short: "Help about any command",
			Long: `Help provides help for any command in the application.
Simply type ` + c.DisplayName() + ` help [path to command] for full details.`,
			ValidArgsFunction: func(c *Command, args []string, toComplete string) ([]Completion, ShellCompDirective) {
				var completions []Completion
				cmd, _, e := c.Root().Find(args)
				if e != nil {
					return nil, ShellCompDirectiveNoFileComp
				}
				if cmd == nil {
					// Root help command.
					cmd = c.Root()
				}
				for _, subCmd := range cmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == cmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
					}
				}
				return completions, ShellCompDirectiveNoFileComp
			},
			Run: func(c *Command, args []string) {
				cmd, _, e := c.Root().Find(args)
				if cmd == nil || e != nil {
					c.Printf("Unknown help topic %#q\n", args)
					CheckErr(c.Root().Usage())
				} else {
					cmd.InitDefaultHelpFlag()    // make possible 'help' flag to be shown
					cmd.InitDefaultVersionFlag() // make possible 'version' flag to be shown
					CheckErr(cmd.Help())
				}
			},
			GroupID: c.helpCommandGroupID,
		}
	}
	c.RemoveCommand(c.helpCommand)
	c.AddCommand(c.helpCommand)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) InitDefaultHelpCmd() {
	if !c.HasSubCommands() {
		return
	}

	if c.helpCommand == nil {
		c.helpCommand = &Command{
			Use:   "help [command]",
			Short: "Help about any command",
			Long: `Help provides help for any command in the application.
Simply type ` + c.DisplayName() + ` help [path to command] for full details.`,
			ValidArgsFunction: func(c *Command, args []string, toComplete string) ([]Completion, ShellCompDirective) {
				var completions []Completion
				cmd, _, e := c.Root().Find(args)
				if e != nil {
					return nil, ShellCompDirectiveNoFileComp
				}
				if cmd == nil {
					// Root help command.
					cmd = c.Root()
				}
				for _, subCmd := range cmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == cmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, CompletionWithDesc(subCmd.Name(), subCmd.Short))
						}
					}
				}
				return completions, ShellCompDirectiveNoFileComp
			},
			Run: func(c *Command, args []string) {
				cmd, _, e := c.Root().Find(args)
				if cmd == nil || e != nil {
					c.Printf("Unknown help topic %#q\n", args)
					CheckErr(c.Root().Usage())
				} else {
					// FLow the context down to be used in help text
					if cmd.ctx == nil {
						cmd.ctx = c.ctx
					}

					cmd.InitDefaultHelpFlag()    // make possible 'help' flag to be shown
					cmd.InitDefaultVersionFlag() // make possible 'version' flag to be shown
					CheckErr(cmd.Help())
				}
			},
			GroupID: c.helpCommandGroupID,
		}
	}
	c.RemoveCommand(c.helpCommand)
	c.AddCommand(c.helpCommand)
}
```


---

### 🔹 Commit #06: `a97f9fd4`
- **完整 Hash**: `a97f9fd47b290016526c8af2dac0531fea5cd773`
- **說明 (Ground Truth)**: fix CompletionFunc implementation (#2234)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:125, E:144, A:0) ➔ After(N:125, E:144, A:0)
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

---

### 🔹 Commit #07: `24ada7fe`
- **完整 Hash**: `24ada7fe71e3a3a8741dd52e0a7fc3b97450535a`
- **說明 (Ground Truth)**: Remove the default "completion" cmd if it is alone (#1559)
- **變更檔案數**: 2

#### 📄 檔案: `command.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:239, E:431, A:0) ➔ After(N:239, E:431, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.ExecuteC()`
- **變更前簽章 (Before)**: `func Command.ExecuteC()` (L1083~L1171)
- **變更後簽章 (After)**: `func Command.ExecuteC()` (L1083~L1172)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) ExecuteC() (cmd *Command, err error) {
	if c.ctx == nil {
		c.ctx = context.Background()
	}

	// Regardless of what command execute is called on, run on Root only
	if c.HasParent() {
		return c.Root().ExecuteC()
	}

	// windows hook
	if preExecHookFn != nil {
		preExecHookFn(c)
	}

	// initialize help at the last point to allow for user overriding
	c.InitDefaultHelpCmd()
	// initialize completion at the last point to allow for user overriding
	c.InitDefaultCompletionCmd()

	// Now that all commands have been created, let's make sure all groups
	// are properly created also
	c.checkCommandGroups()

	args := c.args

	// If running unit tests, we don't want to take the os.Args, see #155 and #2173.
	// For example, the following would fail:
	//   go test -c -o foo.test
	//   ./foo.test -test.run TestNoArgs
	if c.args == nil && !isTesting() {
		args = os.Args[1:]
	}

	// initialize the hidden command to be used for shell completion
	c.initCompleteCmd(args)

	var flags []string
	if c.TraverseChildren {
		cmd, flags, err = c.Traverse(args)
	} else {
		cmd, flags, err = c.Find(args)
	}
	if err != nil {
		// If found parse to a subcommand and then failed, talk about the subcommand
		if cmd != nil {
			c = cmd
		}
		if !c.SilenceErrors {
			c.PrintErrln(c.ErrPrefix(), err.Error())
			c.PrintErrf("Run '%v --help' for usage.\n", c.CommandPath())
		}
		return c, err
	}

	cmd.commandCalledAs.called = true
	if cmd.commandCalledAs.name == "" {
		cmd.commandCalledAs.name = cmd.Name()
	}

	// We have to pass global context to children command
	// if context is present on the parent command.
	if cmd.ctx == nil {
		cmd.ctx = c.ctx
	}

	err = cmd.execute(flags)
	if err != nil {
		// Always show help if requested, even if SilenceErrors is in
		// effect
		if errors.Is(err, flag.ErrHelp) {
			cmd.HelpFunc()(cmd, args)
			return cmd, nil
		}

		// If root command has SilenceErrors flagged,
		// all subcommands should respect it
		if !cmd.SilenceErrors && !c.SilenceErrors {
			c.PrintErrln(cmd.ErrPrefix(), err.Error())
		}

		// If root command has SilenceUsage flagged,
		// all subcommands should respect it
		if !cmd.SilenceUsage && !c.SilenceUsage {
			c.Println(cmd.UsageString())
		}
	}
	return cmd, err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) ExecuteC() (cmd *Command, err error) {
	if c.ctx == nil {
		c.ctx = context.Background()
	}

	// Regardless of what command execute is called on, run on Root only
	if c.HasParent() {
		return c.Root().ExecuteC()
	}

	// windows hook
	if preExecHookFn != nil {
		preExecHookFn(c)
	}

	// initialize help at the last point to allow for user overriding
	c.InitDefaultHelpCmd()

	args := c.args

	// If running unit tests, we don't want to take the os.Args, see #155 and #2173.
	// For example, the following would fail:
	//   go test -c -o foo.test
	//   ./foo.test -test.run TestNoArgs
	if c.args == nil && !isTesting() {
		args = os.Args[1:]
	}

	// initialize the __complete command to be used for shell completion
	c.initCompleteCmd(args)

	// initialize the default completion command
	c.InitDefaultCompletionCmd(args...)

	// Now that all commands have been created, let's make sure all groups
	// are properly created also
	c.checkCommandGroups()

	var flags []string
	if c.TraverseChildren {
		cmd, flags, err = c.Traverse(args)
	} else {
		cmd, flags, err = c.Find(args)
	}
	if err != nil {
		// If found parse to a subcommand and then failed, talk about the subcommand
		if cmd != nil {
			c = cmd
		}
		if !c.SilenceErrors {
			c.PrintErrln(c.ErrPrefix(), err.Error())
			c.PrintErrf("Run '%v --help' for usage.\n", c.CommandPath())
		}
		return c, err
	}

	cmd.commandCalledAs.called = true
	if cmd.commandCalledAs.name == "" {
		cmd.commandCalledAs.name = cmd.Name()
	}

	// We have to pass global context to children command
	// if context is present on the parent command.
	if cmd.ctx == nil {
		cmd.ctx = c.ctx
	}

	err = cmd.execute(flags)
	if err != nil {
		// Always show help if requested, even if SilenceErrors is in
		// effect
		if errors.Is(err, flag.ErrHelp) {
			cmd.HelpFunc()(cmd, args)
			return cmd, nil
		}

		// If root command has SilenceErrors flagged,
		// all subcommands should respect it
		if !cmd.SilenceErrors && !c.SilenceErrors {
			c.PrintErrln(cmd.ErrPrefix(), err.Error())
		}

		// If root command has SilenceUsage flagged,
		// all subcommands should respect it
		if !cmd.SilenceUsage && !c.SilenceUsage {
			c.Println(cmd.UsageString())
		}
	}
	return cmd, err
}
```


#### 📄 檔案: `completions.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:126, E:141, A:0) ➔ After(N:125, E:144, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 1, +Edges: 4, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • - [移除節點] `c.HasSubCommands (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.InitDefaultCompletionCmd` ──[CALLS]──> `c.Find (External/Pkg)`
  • + [新增呼叫邊] `Command.InitDefaultCompletionCmd` ──[CALLS]──> `subCmd.Name (External/Pkg)`
  • + [新增呼叫邊] `Command.InitDefaultCompletionCmd` ──[CALLS]──> `len (External/Pkg)`
  • + [新增呼叫邊] `Command.InitDefaultCompletionCmd` ──[CALLS]──> `c.RemoveCommand (External/Pkg)`
  • - [移除呼叫邊] `Command.InitDefaultCompletionCmd` ──[CALLS]──> `c.HasSubCommands (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.InitDefaultCompletionCmd()`
- **變更前簽章 (Before)**: `func Command.InitDefaultCompletionCmd()` (L730~L886)
- **變更後簽章 (After)**: `func Command.InitDefaultCompletionCmd(args ...string)` (L730~L912)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) InitDefaultCompletionCmd() {
	if c.CompletionOptions.DisableDefaultCmd || !c.HasSubCommands() {
		return
	}

	for _, cmd := range c.commands {
		if cmd.Name() == compCmdName || cmd.HasAlias(compCmdName) {
			// A completion command is already available
			return
		}
	}

	haveNoDescFlag := !c.CompletionOptions.DisableNoDescFlag && !c.CompletionOptions.DisableDescriptions

	completionCmd := &Command{
		Use:   compCmdName,
		Short: "Generate the autocompletion script for the specified shell",
		Long: fmt.Sprintf(`Generate the autocompletion script for %[1]s for the specified shell.
See each sub-command's help for details on how to use the generated script.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		Hidden:            c.CompletionOptions.HiddenDefaultCmd,
		GroupID:           c.completionCommandGroupID,
	}
	c.AddCommand(completionCmd)

	out := c.OutOrStdout()
	noDesc := c.CompletionOptions.DisableDescriptions
	shortDesc := "Generate the autocompletion script for %s"
	bash := &Command{
		Use:   "bash",
		Short: fmt.Sprintf(shortDesc, "bash"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

	source <(%[1]s completion bash)

To load completions for every new session, execute once:

#### Linux:

	%[1]s completion bash > /etc/bash_completion.d/%[1]s

#### macOS:

	%[1]s completion bash > $(brew --prefix)/etc/bash_completion.d/%[1]s

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:                  NoArgs,
		DisableFlagsInUseLine: true,
		ValidArgsFunction:     NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			return cmd.Root().GenBashCompletionV2(out, !noDesc)
		},
	}
	if haveNoDescFlag {
		bash.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	zsh := &Command{
		Use:   "zsh",
		Short: fmt.Sprintf(shortDesc, "zsh"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(%[1]s completion zsh)

To load completions for every new session, execute once:

#### Linux:

	%[1]s completion zsh > "${fpath[1]}/_%[1]s"

#### macOS:

	%[1]s completion zsh > $(brew --prefix)/share/zsh/site-functions/_%[1]s

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			if noDesc {
				return cmd.Root().GenZshCompletionNoDesc(out)
			}
			return cmd.Root().GenZshCompletion(out)
		},
	}
	if haveNoDescFlag {
		zsh.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	fish := &Command{
		Use:   "fish",
		Short: fmt.Sprintf(shortDesc, "fish"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

	%[1]s completion fish | source

To load completions for every new session, execute once:

	%[1]s completion fish > ~/.config/fish/completions/%[1]s.fish

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			return cmd.Root().GenFishCompletion(out, !noDesc)
		},
	}
	if haveNoDescFlag {
		fish.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	powershell := &Command{
		Use:   "powershell",
		Short: fmt.Sprintf(shortDesc, "powershell"),
		Long: fmt.Sprintf(`Generate the autocompletion script for powershell.

To load completions in your current shell session:

	%[1]s completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			if noDesc {
				return cmd.Root().GenPowerShellCompletion(out)
			}
			return cmd.Root().GenPowerShellCompletionWithDesc(out)

		},
	}
	if haveNoDescFlag {
		powershell.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	completionCmd.AddCommand(bash, zsh, fish, powershell)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) InitDefaultCompletionCmd(args ...string) {
	if c.CompletionOptions.DisableDefaultCmd {
		return
	}

	for _, cmd := range c.commands {
		if cmd.Name() == compCmdName || cmd.HasAlias(compCmdName) {
			// A completion command is already available
			return
		}
	}

	haveNoDescFlag := !c.CompletionOptions.DisableNoDescFlag && !c.CompletionOptions.DisableDescriptions

	// Special case to know if there are sub-commands or not.
	hasSubCommands := false
	for _, cmd := range c.commands {
		if cmd.Name() != ShellCompRequestCmd && cmd.Name() != helpCommandName {
			// We found a real sub-command (not 'help' or '__complete')
			hasSubCommands = true
			break
		}
	}

	completionCmd := &Command{
		Use:   compCmdName,
		Short: "Generate the autocompletion script for the specified shell",
		Long: fmt.Sprintf(`Generate the autocompletion script for %[1]s for the specified shell.
See each sub-command's help for details on how to use the generated script.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		Hidden:            c.CompletionOptions.HiddenDefaultCmd,
		GroupID:           c.completionCommandGroupID,
	}
	c.AddCommand(completionCmd)

	if !hasSubCommands {
		// If the 'completion' command will be the only sub-command,
		// we only create it if it is actually being called.
		// This avoids breaking programs that would suddenly find themselves with
		// a subcommand, which would prevent them from accepting arguments.
		// We also create the 'completion' command if the user is triggering
		// shell completion for it (prog __complete completion '')
		subCmd, cmdArgs, err := c.Find(args)
		if err != nil || subCmd.Name() != compCmdName &&
			!(subCmd.Name() == ShellCompRequestCmd && len(cmdArgs) > 1 && cmdArgs[0] == compCmdName) {
			// The completion command is not being called or being completed so we remove it.
			c.RemoveCommand(completionCmd)
			return
		}
	}

	out := c.OutOrStdout()
	noDesc := c.CompletionOptions.DisableDescriptions
	shortDesc := "Generate the autocompletion script for %s"
	bash := &Command{
		Use:   "bash",
		Short: fmt.Sprintf(shortDesc, "bash"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

	source <(%[1]s completion bash)

To load completions for every new session, execute once:

#### Linux:

	%[1]s completion bash > /etc/bash_completion.d/%[1]s

#### macOS:

	%[1]s completion bash > $(brew --prefix)/etc/bash_completion.d/%[1]s

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:                  NoArgs,
		DisableFlagsInUseLine: true,
		ValidArgsFunction:     NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			return cmd.Root().GenBashCompletionV2(out, !noDesc)
		},
	}
	if haveNoDescFlag {
		bash.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	zsh := &Command{
		Use:   "zsh",
		Short: fmt.Sprintf(shortDesc, "zsh"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(%[1]s completion zsh)

To load completions for every new session, execute once:

#### Linux:

	%[1]s completion zsh > "${fpath[1]}/_%[1]s"

#### macOS:

	%[1]s completion zsh > $(brew --prefix)/share/zsh/site-functions/_%[1]s

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			if noDesc {
				return cmd.Root().GenZshCompletionNoDesc(out)
			}
			return cmd.Root().GenZshCompletion(out)
		},
	}
	if haveNoDescFlag {
		zsh.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	fish := &Command{
		Use:   "fish",
		Short: fmt.Sprintf(shortDesc, "fish"),
		Long: fmt.Sprintf(`Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

	%[1]s completion fish | source

To load completions for every new session, execute once:

	%[1]s completion fish > ~/.config/fish/completions/%[1]s.fish

You will need to start a new shell for this setup to take effect.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			return cmd.Root().GenFishCompletion(out, !noDesc)
		},
	}
	if haveNoDescFlag {
		fish.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	powershell := &Command{
		Use:   "powershell",
		Short: fmt.Sprintf(shortDesc, "powershell"),
		Long: fmt.Sprintf(`Generate the autocompletion script for powershell.

To load completions in your current shell session:

	%[1]s completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.
`, c.Root().Name()),
		Args:              NoArgs,
		ValidArgsFunction: NoFileCompletions,
		RunE: func(cmd *Command, args []string) error {
			if noDesc {
				return cmd.Root().GenPowerShellCompletion(out)
			}
			return cmd.Root().GenPowerShellCompletionWithDesc(out)

		},
	}
	if haveNoDescFlag {
		powershell.Flags().BoolVar(&noDesc, compCmdNoDescFlagName, compCmdNoDescFlagDefault, compCmdNoDescFlagDesc)
	}

	completionCmd.AddCommand(bash, zsh, fish, powershell)
}
```


---

### 🔹 Commit #08: `4ba5566f`
- **完整 Hash**: `4ba5566f5704a9c0d205e1ef3efc4896156d33fa`
- **說明 (Ground Truth)**: fix(bash): nounset unbound file filter variable on empty extension (#2228)
- **變更檔案數**: 1

#### 📄 檔案: `bash_completionsV2.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:11, E:10, A:0) ➔ After(N:11, E:10, A:0)
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

### 🔹 函式: `genBashComp()`
- **變更前簽章 (Before)**: `func genBashComp(buf io.StringWriter, name string, includeDesc bool)` (L31~L467)
- **變更後簽章 (After)**: `func genBashComp(buf io.StringWriter, name string, includeDesc bool)` (L31~L467)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func genBashComp(buf io.StringWriter, name string, includeDesc bool) {
	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}

	WriteStringAndCheck(buf, fmt.Sprintf(`# bash completion V2 for %-36[1]s -*- shell-script -*-

__%[1]s_debug()
{
    if [[ -n ${BASH_COMP_DEBUG_FILE-} ]]; then
        echo "$*" >> "${BASH_COMP_DEBUG_FILE}"
    fi
}

# Macs have bash3 for which the bash-completion package doesn't include
# _init_completion. This is a minimal version of that function.
__%[1]s_init_completion()
{
    COMPREPLY=()
    _get_comp_words_by_ref "$@" cur prev words cword
}

# This function calls the %[1]s program to obtain the completion
# results and the directive.  It fills the 'out' and 'directive' vars.
__%[1]s_get_completion_results() {
    local requestComp lastParam lastChar args

    # Prepare the command to request completions for the program.
    # Calling ${words[0]} instead of directly %[1]s allows handling aliases
    args=("${words[@]:1}")
    requestComp="${words[0]} %[2]s ${args[*]}"

    lastParam=${words[$((${#words[@]}-1))]}
    lastChar=${lastParam:$((${#lastParam}-1)):1}
    __%[1]s_debug "lastParam ${lastParam}, lastChar ${lastChar}"

    if [[ -z ${cur} && ${lastChar} != = ]]; then
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go method.
        __%[1]s_debug "Adding extra empty parameter"
        requestComp="${requestComp} ''"
    fi

    # When completing a flag with an = (e.g., %[1]s -n=<TAB>)
    # bash focuses on the part after the =, so we need to remove
    # the flag part from $cur
    if [[ ${cur} == -*=* ]]; then
        cur="${cur#*=}"
    fi

    __%[1]s_debug "Calling ${requestComp}"
    # Use eval to handle any environment variables and such
    out=$(eval "${requestComp}" 2>/dev/null)

    # Extract the directive integer at the very end of the output following a colon (:)
    directive=${out##*:}
    # Remove the directive
    out=${out%%:*}
    if [[ ${directive} == "${out}" ]]; then
        # There is not directive specified
        directive=0
    fi
    __%[1]s_debug "The completion directive is: ${directive}"
    __%[1]s_debug "The completions are: ${out}"
}

__%[1]s_process_completion_results() {
    local shellCompDirectiveError=%[3]d
    local shellCompDirectiveNoSpace=%[4]d
    local shellCompDirectiveNoFileComp=%[5]d
    local shellCompDirectiveFilterFileExt=%[6]d
    local shellCompDirectiveFilterDirs=%[7]d
    local shellCompDirectiveKeepOrder=%[8]d

    if (((directive & shellCompDirectiveError) != 0)); then
        # Error code.  No completion.
        __%[1]s_debug "Received error from custom completion go code"
        return
    else
        if (((directive & shellCompDirectiveNoSpace) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                __%[1]s_debug "Activating no space"
                compopt -o nospace
            else
                __%[1]s_debug "No space directive not supported in this version of bash"
            fi
        fi
        if (((directive & shellCompDirectiveKeepOrder) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                # no sort isn't supported for bash less than < 4.4
                if [[ ${BASH_VERSINFO[0]} -lt 4 || ( ${BASH_VERSINFO[0]} -eq 4 && ${BASH_VERSINFO[1]} -lt 4 ) ]]; then
                    __%[1]s_debug "No sort directive not supported in this version of bash"
                else
                    __%[1]s_debug "Activating keep order"
                    compopt -o nosort
                fi
            else
                __%[1]s_debug "No sort directive not supported in this version of bash"
            fi
        fi
        if (((directive & shellCompDirectiveNoFileComp) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                __%[1]s_debug "Activating no file completion"
                compopt +o default
            else
                __%[1]s_debug "No file completion directive not supported in this version of bash"
            fi
        fi
    fi

    # Separate activeHelp from normal completions
    local completions=()
    local activeHelp=()
    __%[1]s_extract_activeHelp

    if (((directive & shellCompDirectiveFilterFileExt) != 0)); then
        # File extension filtering
        local fullFilter filter filteringCmd

        # Do not use quotes around the $completions variable or else newline
        # characters will be kept.
        for filter in ${completions[*]}; do
            fullFilter+="$filter|"
        done

        filteringCmd="_filedir $fullFilter"
        __%[1]s_debug "File filtering command: $filteringCmd"
        $filteringCmd
    elif (((directive & shellCompDirectiveFilterDirs) != 0)); then
        # File completion for directories only

        local subdir
        subdir=${completions[0]}
        if [[ -n $subdir ]]; then
            __%[1]s_debug "Listing directories in $subdir"
            pushd "$subdir" >/dev/null 2>&1 && _filedir -d && popd >/dev/null 2>&1 || return
        else
            __%[1]s_debug "Listing directories in ."
            _filedir -d
        fi
    else
        __%[1]s_handle_completion_types
    fi

    __%[1]s_handle_special_char "$cur" :
    __%[1]s_handle_special_char "$cur" =

    # Print the activeHelp statements before we finish
    __%[1]s_handle_activeHelp
}

__%[1]s_handle_activeHelp() {
    # Print the activeHelp statements
    if ((${#activeHelp[*]} != 0)); then
        if [ -z $COMP_TYPE ]; then
            # Bash v3 does not set the COMP_TYPE variable.
            printf "\n";
            printf "%%s\n" "${activeHelp[@]}"
            printf "\n"
            __%[1]s_reprint_commandLine
            return
        fi

        # Only print ActiveHelp on the second TAB press
        if [ $COMP_TYPE -eq 63 ]; then
            printf "\n"
            printf "%%s\n" "${activeHelp[@]}"

            if ((${#COMPREPLY[*]} == 0)); then
                # When there are no completion choices from the program, file completion
                # may kick in if the program has not disabled it; in such a case, we want
                # to know if any files will match what the user typed, so that we know if
                # there will be completions presented, so that we know how to handle ActiveHelp.
                # To find out, we actually trigger the file completion ourselves;
                # the call to _filedir will fill COMPREPLY if files match.
                if (((directive & shellCompDirectiveNoFileComp) == 0)); then
                    __%[1]s_debug "Listing files"
                    _filedir
                fi
            fi

            if ((${#COMPREPLY[*]} != 0)); then
                # If there are completion choices to be shown, print a delimiter.
                # Re-printing the command-line will automatically be done
                # by the shell when it prints the completion choices.
                printf -- "--"
            else
                # When there are no completion choices at all, we need
                # to re-print the command-line since the shell will
                # not be doing it itself.
                __%[1]s_reprint_commandLine
            fi
        elif [ $COMP_TYPE -eq 37 ] || [ $COMP_TYPE -eq 42 ]; then
            # For completion type: menu-complete/menu-complete-backward and insert-completions
            # the completions are immediately inserted into the command-line, so we first
            # print the activeHelp message and reprint the command-line since the shell won't.
            printf "\n"
            printf "%%s\n" "${activeHelp[@]}"

            __%[1]s_reprint_commandLine
        fi
    fi
}

__%[1]s_reprint_commandLine() {
    # The prompt format is only available from bash 4.4.
    # We test if it is available before using it.
    if (x=${PS1@P}) 2> /dev/null; then
        printf "%%s" "${PS1@P}${COMP_LINE[@]}"
    else
        # Can't print the prompt.  Just print the
        # text the user had typed, it is workable enough.
        printf "%%s" "${COMP_LINE[@]}"
    fi
}

# Separate activeHelp lines from real completions.
# Fills the $activeHelp and $completions arrays.
__%[1]s_extract_activeHelp() {
    local activeHelpMarker="%[9]s"
    local endIndex=${#activeHelpMarker}

    while IFS='' read -r comp; do
        [[ -z $comp ]] && continue

        if [[ ${comp:0:endIndex} == $activeHelpMarker ]]; then
            comp=${comp:endIndex}
            __%[1]s_debug "ActiveHelp found: $comp"
            if [[ -n $comp ]]; then
                activeHelp+=("$comp")
            fi
        else
            # Not an activeHelp line but a normal completion
            completions+=("$comp")
        fi
    done <<<"${out}"
}

__%[1]s_handle_completion_types() {
    __%[1]s_debug "__%[1]s_handle_completion_types: COMP_TYPE is $COMP_TYPE"

    case $COMP_TYPE in
    37|42)
        # Type: menu-complete/menu-complete-backward and insert-completions
        # If the user requested inserting one completion at a time, or all
        # completions at once on the command-line we must remove the descriptions.
        # https://github.com/spf13/cobra/issues/1508

        # If there are no completions, we don't need to do anything
        (( ${#completions[@]} == 0 )) && return 0

        local tab=$'\t'

        # Strip any description and escape the completion to handled special characters
        IFS=$'\n' read -ra completions -d '' < <(printf "%%q\n" "${completions[@]%%%%$tab*}")

        # Only consider the completions that match
        IFS=$'\n' read -ra COMPREPLY -d '' < <(IFS=$'\n'; compgen -W "${completions[*]}" -- "${cur}")

        # compgen looses the escaping so we need to escape all completions again since they will
        # all be inserted on the command-line.
        IFS=$'\n' read -ra COMPREPLY -d '' < <(printf "%%q\n" "${COMPREPLY[@]}")
        ;;

    *)
        # Type: complete (normal completion)
        __%[1]s_handle_standard_completion_case
        ;;
    esac
}

__%[1]s_handle_standard_completion_case() {
    local tab=$'\t'

    # If there are no completions, we don't need to do anything
    (( ${#completions[@]} == 0 )) && return 0

    # Short circuit to optimize if we don't have descriptions
    if [[ "${completions[*]}" != *$tab* ]]; then
        # First, escape the completions to handle special characters
        IFS=$'\n' read -ra completions -d '' < <(printf "%%q\n" "${completions[@]}")
        # Only consider the completions that match what the user typed
        IFS=$'\n' read -ra COMPREPLY -d '' < <(IFS=$'\n'; compgen -W "${completions[*]}" -- "${cur}")

        # compgen looses the escaping so, if there is only a single completion, we need to
        # escape it again because it will be inserted on the command-line.  If there are multiple
        # completions, we don't want to escape them because they will be printed in a list
        # and we don't want to show escape characters in that list.
        if (( ${#COMPREPLY[@]} == 1 )); then
            COMPREPLY[0]=$(printf "%%q" "${COMPREPLY[0]}")
        fi
        return 0
    fi

    local longest=0
    local compline
    # Look for the longest completion so that we can format things nicely
    while IFS='' read -r compline; do
        [[ -z $compline ]] && continue

        # Before checking if the completion matches what the user typed,
        # we need to strip any description and escape the completion to handle special
        # characters because those escape characters are part of what the user typed.
        # Don't call "printf" in a sub-shell because it will be much slower
        # since we are in a loop.
        printf -v comp "%%q" "${compline%%%%$tab*}" &>/dev/null || comp=$(printf "%%q" "${compline%%%%$tab*}")

        # Only consider the completions that match
        [[ $comp == "$cur"* ]] || continue

        # The completions matches.  Add it to the list of full completions including
        # its description.  We don't escape the completion because it may get printed
        # in a list if there are more than one and we don't want show escape characters
        # in that list.
        COMPREPLY+=("$compline")

        # Strip any description before checking the length, and again, don't escape
        # the completion because this length is only used when printing the completions
        # in a list and we don't want show escape characters in that list.
        comp=${compline%%%%$tab*}
        if ((${#comp}>longest)); then
            longest=${#comp}
        fi
    done < <(printf "%%s\n" "${completions[@]}")

    # If there is a single completion left, remove the description text and escape any special characters
    if ((${#COMPREPLY[*]} == 1)); then
        __%[1]s_debug "COMPREPLY[0]: ${COMPREPLY[0]}"
        COMPREPLY[0]=$(printf "%%q" "${COMPREPLY[0]%%%%$tab*}")
        __%[1]s_debug "Removed description from single completion, which is now: ${COMPREPLY[0]}"
    else
        # Format the descriptions
        __%[1]s_format_comp_descriptions $longest
    fi
}

__%[1]s_handle_special_char()
{
    local comp="$1"
    local char=$2
    if [[ "$comp" == *${char}* && "$COMP_WORDBREAKS" == *${char}* ]]; then
        local word=${comp%%"${comp##*${char}}"}
        local idx=${#COMPREPLY[*]}
        while ((--idx >= 0)); do
            COMPREPLY[idx]=${COMPREPLY[idx]#"$word"}
        done
    fi
}

__%[1]s_format_comp_descriptions()
{
    local tab=$'\t'
    local comp desc maxdesclength
    local longest=$1

    local i ci
    for ci in ${!COMPREPLY[*]}; do
        comp=${COMPREPLY[ci]}
        # Properly format the description string which follows a tab character if there is one
        if [[ "$comp" == *$tab* ]]; then
            __%[1]s_debug "Original comp: $comp"
            desc=${comp#*$tab}
            comp=${comp%%%%$tab*}

            # $COLUMNS stores the current shell width.
            # Remove an extra 4 because we add 2 spaces and 2 parentheses.
            maxdesclength=$(( COLUMNS - longest - 4 ))

            # Make sure we can fit a description of at least 8 characters
            # if we are to align the descriptions.
            if ((maxdesclength > 8)); then
                # Add the proper number of spaces to align the descriptions
                for ((i = ${#comp} ; i < longest ; i++)); do
                    comp+=" "
                done
            else
                # Don't pad the descriptions so we can fit more text after the completion
                maxdesclength=$(( COLUMNS - ${#comp} - 4 ))
            fi

            # If there is enough space for any description text,
            # truncate the descriptions that are too long for the shell width
            if ((maxdesclength > 0)); then
                if ((${#desc} > maxdesclength)); then
                    desc=${desc:0:$(( maxdesclength - 1 ))}
                    desc+="…"
                fi
                comp+="  ($desc)"
            fi
            COMPREPLY[ci]=$comp
            __%[1]s_debug "Final comp: $comp"
        fi
    done
}

__start_%[1]s()
{
    local cur prev words cword split

    COMPREPLY=()

    # Call _init_completion from the bash-completion package
    # to prepare the arguments properly
    if declare -F _init_completion >/dev/null 2>&1; then
        _init_completion -n =: || return
    else
        __%[1]s_init_completion -n =: || return
    fi

    __%[1]s_debug
    __%[1]s_debug "========= starting completion logic =========="
    __%[1]s_debug "cur is ${cur}, words[*] is ${words[*]}, #words[@] is ${#words[@]}, cword is $cword"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $cword location, so we need
    # to truncate the command-line ($words) up to the $cword location.
    words=("${words[@]:0:$cword+1}")
    __%[1]s_debug "Truncated words[*]: ${words[*]},"

    local out directive
    __%[1]s_get_completion_results
    __%[1]s_process_completion_results
}

if [[ $(type -t compopt) = "builtin" ]]; then
    complete -o default -F __start_%[1]s %[1]s
else
    complete -o default -o nospace -F __start_%[1]s %[1]s
fi

# ex: ts=4 sw=4 et filetype=sh
`, name, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder,
		activeHelpMarker))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func genBashComp(buf io.StringWriter, name string, includeDesc bool) {
	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}

	WriteStringAndCheck(buf, fmt.Sprintf(`# bash completion V2 for %-36[1]s -*- shell-script -*-

__%[1]s_debug()
{
    if [[ -n ${BASH_COMP_DEBUG_FILE-} ]]; then
        echo "$*" >> "${BASH_COMP_DEBUG_FILE}"
    fi
}

# Macs have bash3 for which the bash-completion package doesn't include
# _init_completion. This is a minimal version of that function.
__%[1]s_init_completion()
{
    COMPREPLY=()
    _get_comp_words_by_ref "$@" cur prev words cword
}

# This function calls the %[1]s program to obtain the completion
# results and the directive.  It fills the 'out' and 'directive' vars.
__%[1]s_get_completion_results() {
    local requestComp lastParam lastChar args

    # Prepare the command to request completions for the program.
    # Calling ${words[0]} instead of directly %[1]s allows handling aliases
    args=("${words[@]:1}")
    requestComp="${words[0]} %[2]s ${args[*]}"

    lastParam=${words[$((${#words[@]}-1))]}
    lastChar=${lastParam:$((${#lastParam}-1)):1}
    __%[1]s_debug "lastParam ${lastParam}, lastChar ${lastChar}"

    if [[ -z ${cur} && ${lastChar} != = ]]; then
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go method.
        __%[1]s_debug "Adding extra empty parameter"
        requestComp="${requestComp} ''"
    fi

    # When completing a flag with an = (e.g., %[1]s -n=<TAB>)
    # bash focuses on the part after the =, so we need to remove
    # the flag part from $cur
    if [[ ${cur} == -*=* ]]; then
        cur="${cur#*=}"
    fi

    __%[1]s_debug "Calling ${requestComp}"
    # Use eval to handle any environment variables and such
    out=$(eval "${requestComp}" 2>/dev/null)

    # Extract the directive integer at the very end of the output following a colon (:)
    directive=${out##*:}
    # Remove the directive
    out=${out%%:*}
    if [[ ${directive} == "${out}" ]]; then
        # There is not directive specified
        directive=0
    fi
    __%[1]s_debug "The completion directive is: ${directive}"
    __%[1]s_debug "The completions are: ${out}"
}

__%[1]s_process_completion_results() {
    local shellCompDirectiveError=%[3]d
    local shellCompDirectiveNoSpace=%[4]d
    local shellCompDirectiveNoFileComp=%[5]d
    local shellCompDirectiveFilterFileExt=%[6]d
    local shellCompDirectiveFilterDirs=%[7]d
    local shellCompDirectiveKeepOrder=%[8]d

    if (((directive & shellCompDirectiveError) != 0)); then
        # Error code.  No completion.
        __%[1]s_debug "Received error from custom completion go code"
        return
    else
        if (((directive & shellCompDirectiveNoSpace) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                __%[1]s_debug "Activating no space"
                compopt -o nospace
            else
                __%[1]s_debug "No space directive not supported in this version of bash"
            fi
        fi
        if (((directive & shellCompDirectiveKeepOrder) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                # no sort isn't supported for bash less than < 4.4
                if [[ ${BASH_VERSINFO[0]} -lt 4 || ( ${BASH_VERSINFO[0]} -eq 4 && ${BASH_VERSINFO[1]} -lt 4 ) ]]; then
                    __%[1]s_debug "No sort directive not supported in this version of bash"
                else
                    __%[1]s_debug "Activating keep order"
                    compopt -o nosort
                fi
            else
                __%[1]s_debug "No sort directive not supported in this version of bash"
            fi
        fi
        if (((directive & shellCompDirectiveNoFileComp) != 0)); then
            if [[ $(type -t compopt) == builtin ]]; then
                __%[1]s_debug "Activating no file completion"
                compopt +o default
            else
                __%[1]s_debug "No file completion directive not supported in this version of bash"
            fi
        fi
    fi

    # Separate activeHelp from normal completions
    local completions=()
    local activeHelp=()
    __%[1]s_extract_activeHelp

    if (((directive & shellCompDirectiveFilterFileExt) != 0)); then
        # File extension filtering
        local fullFilter="" filter filteringCmd

        # Do not use quotes around the $completions variable or else newline
        # characters will be kept.
        for filter in ${completions[*]}; do
            fullFilter+="$filter|"
        done

        filteringCmd="_filedir $fullFilter"
        __%[1]s_debug "File filtering command: $filteringCmd"
        $filteringCmd
    elif (((directive & shellCompDirectiveFilterDirs) != 0)); then
        # File completion for directories only

        local subdir
        subdir=${completions[0]}
        if [[ -n $subdir ]]; then
            __%[1]s_debug "Listing directories in $subdir"
            pushd "$subdir" >/dev/null 2>&1 && _filedir -d && popd >/dev/null 2>&1 || return
        else
            __%[1]s_debug "Listing directories in ."
            _filedir -d
        fi
    else
        __%[1]s_handle_completion_types
    fi

    __%[1]s_handle_special_char "$cur" :
    __%[1]s_handle_special_char "$cur" =

    # Print the activeHelp statements before we finish
    __%[1]s_handle_activeHelp
}

__%[1]s_handle_activeHelp() {
    # Print the activeHelp statements
    if ((${#activeHelp[*]} != 0)); then
        if [ -z $COMP_TYPE ]; then
            # Bash v3 does not set the COMP_TYPE variable.
            printf "\n";
            printf "%%s\n" "${activeHelp[@]}"
            printf "\n"
            __%[1]s_reprint_commandLine
            return
        fi

        # Only print ActiveHelp on the second TAB press
        if [ $COMP_TYPE -eq 63 ]; then
            printf "\n"
            printf "%%s\n" "${activeHelp[@]}"

            if ((${#COMPREPLY[*]} == 0)); then
                # When there are no completion choices from the program, file completion
                # may kick in if the program has not disabled it; in such a case, we want
                # to know if any files will match what the user typed, so that we know if
                # there will be completions presented, so that we know how to handle ActiveHelp.
                # To find out, we actually trigger the file completion ourselves;
                # the call to _filedir will fill COMPREPLY if files match.
                if (((directive & shellCompDirectiveNoFileComp) == 0)); then
                    __%[1]s_debug "Listing files"
                    _filedir
                fi
            fi

            if ((${#COMPREPLY[*]} != 0)); then
                # If there are completion choices to be shown, print a delimiter.
                # Re-printing the command-line will automatically be done
                # by the shell when it prints the completion choices.
                printf -- "--"
            else
                # When there are no completion choices at all, we need
                # to re-print the command-line since the shell will
                # not be doing it itself.
                __%[1]s_reprint_commandLine
            fi
        elif [ $COMP_TYPE -eq 37 ] || [ $COMP_TYPE -eq 42 ]; then
            # For completion type: menu-complete/menu-complete-backward and insert-completions
            # the completions are immediately inserted into the command-line, so we first
            # print the activeHelp message and reprint the command-line since the shell won't.
            printf "\n"
            printf "%%s\n" "${activeHelp[@]}"

            __%[1]s_reprint_commandLine
        fi
    fi
}

__%[1]s_reprint_commandLine() {
    # The prompt format is only available from bash 4.4.
    # We test if it is available before using it.
    if (x=${PS1@P}) 2> /dev/null; then
        printf "%%s" "${PS1@P}${COMP_LINE[@]}"
    else
        # Can't print the prompt.  Just print the
        # text the user had typed, it is workable enough.
        printf "%%s" "${COMP_LINE[@]}"
    fi
}

# Separate activeHelp lines from real completions.
# Fills the $activeHelp and $completions arrays.
__%[1]s_extract_activeHelp() {
    local activeHelpMarker="%[9]s"
    local endIndex=${#activeHelpMarker}

    while IFS='' read -r comp; do
        [[ -z $comp ]] && continue

        if [[ ${comp:0:endIndex} == $activeHelpMarker ]]; then
            comp=${comp:endIndex}
            __%[1]s_debug "ActiveHelp found: $comp"
            if [[ -n $comp ]]; then
                activeHelp+=("$comp")
            fi
        else
            # Not an activeHelp line but a normal completion
            completions+=("$comp")
        fi
    done <<<"${out}"
}

__%[1]s_handle_completion_types() {
    __%[1]s_debug "__%[1]s_handle_completion_types: COMP_TYPE is $COMP_TYPE"

    case $COMP_TYPE in
    37|42)
        # Type: menu-complete/menu-complete-backward and insert-completions
        # If the user requested inserting one completion at a time, or all
        # completions at once on the command-line we must remove the descriptions.
        # https://github.com/spf13/cobra/issues/1508

        # If there are no completions, we don't need to do anything
        (( ${#completions[@]} == 0 )) && return 0

        local tab=$'\t'

        # Strip any description and escape the completion to handled special characters
        IFS=$'\n' read -ra completions -d '' < <(printf "%%q\n" "${completions[@]%%%%$tab*}")

        # Only consider the completions that match
        IFS=$'\n' read -ra COMPREPLY -d '' < <(IFS=$'\n'; compgen -W "${completions[*]}" -- "${cur}")

        # compgen looses the escaping so we need to escape all completions again since they will
        # all be inserted on the command-line.
        IFS=$'\n' read -ra COMPREPLY -d '' < <(printf "%%q\n" "${COMPREPLY[@]}")
        ;;

    *)
        # Type: complete (normal completion)
        __%[1]s_handle_standard_completion_case
        ;;
    esac
}

__%[1]s_handle_standard_completion_case() {
    local tab=$'\t'

    # If there are no completions, we don't need to do anything
    (( ${#completions[@]} == 0 )) && return 0

    # Short circuit to optimize if we don't have descriptions
    if [[ "${completions[*]}" != *$tab* ]]; then
        # First, escape the completions to handle special characters
        IFS=$'\n' read -ra completions -d '' < <(printf "%%q\n" "${completions[@]}")
        # Only consider the completions that match what the user typed
        IFS=$'\n' read -ra COMPREPLY -d '' < <(IFS=$'\n'; compgen -W "${completions[*]}" -- "${cur}")

        # compgen looses the escaping so, if there is only a single completion, we need to
        # escape it again because it will be inserted on the command-line.  If there are multiple
        # completions, we don't want to escape them because they will be printed in a list
        # and we don't want to show escape characters in that list.
        if (( ${#COMPREPLY[@]} == 1 )); then
            COMPREPLY[0]=$(printf "%%q" "${COMPREPLY[0]}")
        fi
        return 0
    fi

    local longest=0
    local compline
    # Look for the longest completion so that we can format things nicely
    while IFS='' read -r compline; do
        [[ -z $compline ]] && continue

        # Before checking if the completion matches what the user typed,
        # we need to strip any description and escape the completion to handle special
        # characters because those escape characters are part of what the user typed.
        # Don't call "printf" in a sub-shell because it will be much slower
        # since we are in a loop.
        printf -v comp "%%q" "${compline%%%%$tab*}" &>/dev/null || comp=$(printf "%%q" "${compline%%%%$tab*}")

        # Only consider the completions that match
        [[ $comp == "$cur"* ]] || continue

        # The completions matches.  Add it to the list of full completions including
        # its description.  We don't escape the completion because it may get printed
        # in a list if there are more than one and we don't want show escape characters
        # in that list.
        COMPREPLY+=("$compline")

        # Strip any description before checking the length, and again, don't escape
        # the completion because this length is only used when printing the completions
        # in a list and we don't want show escape characters in that list.
        comp=${compline%%%%$tab*}
        if ((${#comp}>longest)); then
            longest=${#comp}
        fi
    done < <(printf "%%s\n" "${completions[@]}")

    # If there is a single completion left, remove the description text and escape any special characters
    if ((${#COMPREPLY[*]} == 1)); then
        __%[1]s_debug "COMPREPLY[0]: ${COMPREPLY[0]}"
        COMPREPLY[0]=$(printf "%%q" "${COMPREPLY[0]%%%%$tab*}")
        __%[1]s_debug "Removed description from single completion, which is now: ${COMPREPLY[0]}"
    else
        # Format the descriptions
        __%[1]s_format_comp_descriptions $longest
    fi
}

__%[1]s_handle_special_char()
{
    local comp="$1"
    local char=$2
    if [[ "$comp" == *${char}* && "$COMP_WORDBREAKS" == *${char}* ]]; then
        local word=${comp%%"${comp##*${char}}"}
        local idx=${#COMPREPLY[*]}
        while ((--idx >= 0)); do
            COMPREPLY[idx]=${COMPREPLY[idx]#"$word"}
        done
    fi
}

__%[1]s_format_comp_descriptions()
{
    local tab=$'\t'
    local comp desc maxdesclength
    local longest=$1

    local i ci
    for ci in ${!COMPREPLY[*]}; do
        comp=${COMPREPLY[ci]}
        # Properly format the description string which follows a tab character if there is one
        if [[ "$comp" == *$tab* ]]; then
            __%[1]s_debug "Original comp: $comp"
            desc=${comp#*$tab}
            comp=${comp%%%%$tab*}

            # $COLUMNS stores the current shell width.
            # Remove an extra 4 because we add 2 spaces and 2 parentheses.
            maxdesclength=$(( COLUMNS - longest - 4 ))

            # Make sure we can fit a description of at least 8 characters
            # if we are to align the descriptions.
            if ((maxdesclength > 8)); then
                # Add the proper number of spaces to align the descriptions
                for ((i = ${#comp} ; i < longest ; i++)); do
                    comp+=" "
                done
            else
                # Don't pad the descriptions so we can fit more text after the completion
                maxdesclength=$(( COLUMNS - ${#comp} - 4 ))
            fi

            # If there is enough space for any description text,
            # truncate the descriptions that are too long for the shell width
            if ((maxdesclength > 0)); then
                if ((${#desc} > maxdesclength)); then
                    desc=${desc:0:$(( maxdesclength - 1 ))}
                    desc+="…"
                fi
                comp+="  ($desc)"
            fi
            COMPREPLY[ci]=$comp
            __%[1]s_debug "Final comp: $comp"
        fi
    done
}

__start_%[1]s()
{
    local cur prev words cword split

    COMPREPLY=()

    # Call _init_completion from the bash-completion package
    # to prepare the arguments properly
    if declare -F _init_completion >/dev/null 2>&1; then
        _init_completion -n =: || return
    else
        __%[1]s_init_completion -n =: || return
    fi

    __%[1]s_debug
    __%[1]s_debug "========= starting completion logic =========="
    __%[1]s_debug "cur is ${cur}, words[*] is ${words[*]}, #words[@] is ${#words[@]}, cword is $cword"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $cword location, so we need
    # to truncate the command-line ($words) up to the $cword location.
    words=("${words[@]:0:$cword+1}")
    __%[1]s_debug "Truncated words[*]: ${words[*]},"

    local out directive
    __%[1]s_get_completion_results
    __%[1]s_process_completion_results
}

if [[ $(type -t compopt) = "builtin" ]]; then
    complete -o default -F __start_%[1]s %[1]s
else
    complete -o default -o nospace -F __start_%[1]s %[1]s
fi

# ex: ts=4 sw=4 et filetype=sh
`, name, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder,
		activeHelpMarker))
}
```


---

### 🔹 Commit #09: `6c3c1163`
- **完整 Hash**: `6c3c1163c6df19860515103199e880122ba49e80`
- **說明 (Ground Truth)**: feat: add CompletionFunc type to help with completions (#2220)
- **變更檔案數**: 2

#### 📄 檔案: `command.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:224, E:387, A:0) ➔ After(N:224, E:387, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:125, E:141, A:0) ➔ After(N:125, E:141, A:0)
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

### 🔹 函式: `FixedCompletions()`
- **變更前簽章 (Before)**: `func FixedCompletions(choices []string, directive ShellCompDirective)` (L128~L132)
- **變更後簽章 (After)**: `func FixedCompletions(choices []string, directive ShellCompDirective)` (L137~L141)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func FixedCompletions(choices []string, directive ShellCompDirective) func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective) {
	return func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective) {
		return choices, directive
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func FixedCompletions(choices []string, directive ShellCompDirective) CompletionFunc {
	return func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective) {
		return choices, directive
	}
}
```


---

### 🔹 Commit #10: `0745e557`
- **完整 Hash**: `0745e5576205cd05fada5bb2e01500d97e1a04be`
- **說明 (Ground Truth)**: completion: improve detection for flags that accept multiple values (#2210)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:125, E:141, A:0) ➔ After(N:125, E:141, A:0)
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

### 🔹 函式: `Command.getCompletions()`
- **變更前簽章 (Before)**: `func Command.getCompletions(args []string)` (L273~L528)
- **變更後簽章 (After)**: `func Command.getCompletions(args []string)` (L281~L539)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				if !flag.Changed ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo") {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				_, acceptsMultiple := flag.Value.(SliceValue)
				acceptsMultiple = acceptsMultiple ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo")

				if !flag.Changed || acceptsMultiple {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```


---

### 🔹 Commit #11: `5a138f14`
- **完整 Hash**: `5a138f143f25d616c6c195356a6560ed4fbbfdd4`
- **說明 (Ground Truth)**: Make Powershell completion script work in constrained mode (#2196)
- **變更檔案數**: 1

#### 📄 檔案: `powershell_completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:16, E:15, A:0) ➔ After(N:16, E:15, A:0)
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

### 🔹 函式: `genPowerShellComp()`
- **變更前簽章 (Before)**: `func genPowerShellComp(buf io.StringWriter, name string, includeDesc bool)` (L28~L286)
- **變更後簽章 (After)**: `func genPowerShellComp(buf io.StringWriter, name string, includeDesc bool)` (L28~L311)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func genPowerShellComp(buf io.StringWriter, name string, includeDesc bool) {
	// Variables should not contain a '-' or ':' character
	nameForVar := name
	nameForVar = strings.ReplaceAll(nameForVar, "-", "_")
	nameForVar = strings.ReplaceAll(nameForVar, ":", "_")

	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}
	WriteStringAndCheck(buf, fmt.Sprintf(`# powershell completion for %-36[1]s -*- shell-script -*-

function __%[1]s_debug {
    if ($env:BASH_COMP_DEBUG_FILE) {
        "$args" | Out-File -Append -FilePath "$env:BASH_COMP_DEBUG_FILE"
    }
}

filter __%[1]s_escapeStringWithSpecialChars {
`+"    $_ -replace '\\s|#|@|\\$|;|,|''|\\{|\\}|\\(|\\)|\"|`|\\||<|>|&','`$&'"+`
}

[scriptblock]${__%[2]sCompleterBlock} = {
    param(
            $WordToComplete,
            $CommandAst,
            $CursorPosition
        )

    # Get the current command line and convert into a string
    $Command = $CommandAst.CommandElements
    $Command = "$Command"

    __%[1]s_debug ""
    __%[1]s_debug "========= starting completion logic =========="
    __%[1]s_debug "WordToComplete: $WordToComplete Command: $Command CursorPosition: $CursorPosition"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $CursorPosition location, so we need
    # to truncate the command-line ($Command) up to the $CursorPosition location.
    # Make sure the $Command is longer then the $CursorPosition before we truncate.
    # This happens because the $Command does not include the last space.
    if ($Command.Length -gt $CursorPosition) {
        $Command=$Command.Substring(0,$CursorPosition)
    }
    __%[1]s_debug "Truncated command: $Command"

    $ShellCompDirectiveError=%[4]d
    $ShellCompDirectiveNoSpace=%[5]d
    $ShellCompDirectiveNoFileComp=%[6]d
    $ShellCompDirectiveFilterFileExt=%[7]d
    $ShellCompDirectiveFilterDirs=%[8]d
    $ShellCompDirectiveKeepOrder=%[9]d

    # Prepare the command to request completions for the program.
    # Split the command at the first space to separate the program and arguments.
    $Program,$Arguments = $Command.Split(" ",2)

    $RequestComp="$Program %[3]s $Arguments"
    __%[1]s_debug "RequestComp: $RequestComp"

    # we cannot use $WordToComplete because it
    # has the wrong values if the cursor was moved
    # so use the last argument
    if ($WordToComplete -ne "" ) {
        $WordToComplete = $Arguments.Split(" ")[-1]
    }
    __%[1]s_debug "New WordToComplete: $WordToComplete"


    # Check for flag with equal sign
    $IsEqualFlag = ($WordToComplete -Like "--*=*" )
    if ( $IsEqualFlag ) {
        __%[1]s_debug "Completing equal sign flag"
        # Remove the flag part
        $Flag,$WordToComplete = $WordToComplete.Split("=",2)
    }

    if ( $WordToComplete -eq "" -And ( -Not $IsEqualFlag )) {
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go method.
        __%[1]s_debug "Adding extra empty parameter"
        # PowerShell 7.2+ changed the way how the arguments are passed to executables,
        # so for pre-7.2 or when Legacy argument passing is enabled we need to use
`+"        # `\"`\" to pass an empty argument, a \"\" or '' does not work!!!"+`
        if ($PSVersionTable.PsVersion -lt [version]'7.2.0' -or
            ($PSVersionTable.PsVersion -lt [version]'7.3.0' -and -not [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -or
            (($PSVersionTable.PsVersion -ge [version]'7.3.0' -or [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -and
              $PSNativeCommandArgumentPassing -eq 'Legacy')) {
`+"             $RequestComp=\"$RequestComp\" + ' `\"`\"'"+`
        } else {
             $RequestComp="$RequestComp" + ' ""'
        }
    }

    __%[1]s_debug "Calling $RequestComp"
    # First disable ActiveHelp which is not supported for Powershell
    ${env:%[10]s}=0

    #call the command store the output in $out and redirect stderr and stdout to null
    # $Out is an array contains each line per element
    Invoke-Expression -OutVariable out "$RequestComp" 2>&1 | Out-Null

    # get directive from last line
    [int]$Directive = $Out[-1].TrimStart(':')
    if ($Directive -eq "") {
        # There is no directive specified
        $Directive = 0
    }
    __%[1]s_debug "The completion directive is: $Directive"

    # remove directive (last element) from out
    $Out = $Out | Where-Object { $_ -ne $Out[-1] }
    __%[1]s_debug "The completions are: $Out"

    if (($Directive -band $ShellCompDirectiveError) -ne 0 ) {
        # Error code.  No completion.
        __%[1]s_debug "Received error from custom completion go code"
        return
    }

    $Longest = 0
    [Array]$Values = $Out | ForEach-Object {
        #Split the output in name and description
`+"        $Name, $Description = $_.Split(\"`t\",2)"+`
        __%[1]s_debug "Name: $Name Description: $Description"

        # Look for the longest completion so that we can format things nicely
        if ($Longest -lt $Name.Length) {
            $Longest = $Name.Length
        }

        # Set the description to a one space string if there is none set.
        # This is needed because the CompletionResult does not accept an empty string as argument
        if (-Not $Description) {
            $Description = " "
        }
        @{Name="$Name";Description="$Description"}
    }


    $Space = " "
    if (($Directive -band $ShellCompDirectiveNoSpace) -ne 0 ) {
        # remove the space here
        __%[1]s_debug "ShellCompDirectiveNoSpace is called"
        $Space = ""
    }

    if ((($Directive -band $ShellCompDirectiveFilterFileExt) -ne 0 ) -or
       (($Directive -band $ShellCompDirectiveFilterDirs) -ne 0 ))  {
        __%[1]s_debug "ShellCompDirectiveFilterFileExt ShellCompDirectiveFilterDirs are not supported"

        # return here to prevent the completion of the extensions
        return
    }

    $Values = $Values | Where-Object {
        # filter the result
        $_.Name -like "$WordToComplete*"

        # Join the flag back if we have an equal sign flag
        if ( $IsEqualFlag ) {
            __%[1]s_debug "Join the equal sign flag back to the completion value"
            $_.Name = $Flag + "=" + $_.Name
        }
    }

    # we sort the values in ascending order by name if keep order isn't passed
    if (($Directive -band $ShellCompDirectiveKeepOrder) -eq 0 ) {
        $Values = $Values | Sort-Object -Property Name
    }

    if (($Directive -band $ShellCompDirectiveNoFileComp) -ne 0 ) {
        __%[1]s_debug "ShellCompDirectiveNoFileComp is called"

        if ($Values.Length -eq 0) {
            # Just print an empty string here so the
            # shell does not start to complete paths.
            # We cannot use CompletionResult here because
            # it does not accept an empty string as argument.
            ""
            return
        }
    }

    # Get the current mode
    $Mode = (Get-PSReadLineKeyHandler | Where-Object {$_.Key -eq "Tab" }).Function
    __%[1]s_debug "Mode: $Mode"

    $Values | ForEach-Object {

        # store temporary because switch will overwrite $_
        $comp = $_

        # PowerShell supports three different completion modes
        # - TabCompleteNext (default windows style - on each key press the next option is displayed)
        # - Complete (works like bash)
        # - MenuComplete (works like zsh)
        # You set the mode with Set-PSReadLineKeyHandler -Key Tab -Function <mode>

        # CompletionResult Arguments:
        # 1) CompletionText text to be used as the auto completion result
        # 2) ListItemText   text to be displayed in the suggestion list
        # 3) ResultType     type of completion result
        # 4) ToolTip        text for the tooltip with details about the object

        switch ($Mode) {

            # bash like
            "Complete" {

                if ($Values.Length -eq 1) {
                    __%[1]s_debug "Only one completion left"

                    # insert space after value
                    [System.Management.Automation.CompletionResult]::new($($comp.Name | __%[1]s_escapeStringWithSpecialChars) + $Space, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")

                } else {
                    # Add the proper number of spaces to align the descriptions
                    while($comp.Name.Length -lt $Longest) {
                        $comp.Name = $comp.Name + " "
                    }

                    # Check for empty description and only add parentheses if needed
                    if ($($comp.Description) -eq " " ) {
                        $Description = ""
                    } else {
                        $Description = "  ($($comp.Description))"
                    }

                    [System.Management.Automation.CompletionResult]::new("$($comp.Name)$Description", "$($comp.Name)$Description", 'ParameterValue', "$($comp.Description)")
                }
             }

            # zsh like
            "MenuComplete" {
                # insert space after value
                # MenuComplete will automatically show the ToolTip of
                # the highlighted value at the bottom of the suggestions.
                [System.Management.Automation.CompletionResult]::new($($comp.Name | __%[1]s_escapeStringWithSpecialChars) + $Space, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
            }

            # TabCompleteNext and in case we get something unknown
            Default {
                # Like MenuComplete but we don't want to add a space here because
                # the user need to press space anyway to get the completion.
                # Description will not be shown because that's not possible with TabCompleteNext
                [System.Management.Automation.CompletionResult]::new($($comp.Name | __%[1]s_escapeStringWithSpecialChars), "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
            }
        }

    }
}

Register-ArgumentCompleter -CommandName '%[1]s' -ScriptBlock ${__%[2]sCompleterBlock}
`, name, nameForVar, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder, activeHelpEnvVar(name)))
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func genPowerShellComp(buf io.StringWriter, name string, includeDesc bool) {
	// Variables should not contain a '-' or ':' character
	nameForVar := name
	nameForVar = strings.ReplaceAll(nameForVar, "-", "_")
	nameForVar = strings.ReplaceAll(nameForVar, ":", "_")

	compCmd := ShellCompRequestCmd
	if !includeDesc {
		compCmd = ShellCompNoDescRequestCmd
	}
	WriteStringAndCheck(buf, fmt.Sprintf(`# powershell completion for %-36[1]s -*- shell-script -*-

function __%[1]s_debug {
    if ($env:BASH_COMP_DEBUG_FILE) {
        "$args" | Out-File -Append -FilePath "$env:BASH_COMP_DEBUG_FILE"
    }
}

filter __%[1]s_escapeStringWithSpecialChars {
`+"    $_ -replace '\\s|#|@|\\$|;|,|''|\\{|\\}|\\(|\\)|\"|`|\\||<|>|&','`$&'"+`
}

[scriptblock]${__%[2]sCompleterBlock} = {
    param(
            $WordToComplete,
            $CommandAst,
            $CursorPosition
        )

    # Get the current command line and convert into a string
    $Command = $CommandAst.CommandElements
    $Command = "$Command"

    __%[1]s_debug ""
    __%[1]s_debug "========= starting completion logic =========="
    __%[1]s_debug "WordToComplete: $WordToComplete Command: $Command CursorPosition: $CursorPosition"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $CursorPosition location, so we need
    # to truncate the command-line ($Command) up to the $CursorPosition location.
    # Make sure the $Command is longer then the $CursorPosition before we truncate.
    # This happens because the $Command does not include the last space.
    if ($Command.Length -gt $CursorPosition) {
        $Command=$Command.Substring(0,$CursorPosition)
    }
    __%[1]s_debug "Truncated command: $Command"

    $ShellCompDirectiveError=%[4]d
    $ShellCompDirectiveNoSpace=%[5]d
    $ShellCompDirectiveNoFileComp=%[6]d
    $ShellCompDirectiveFilterFileExt=%[7]d
    $ShellCompDirectiveFilterDirs=%[8]d
    $ShellCompDirectiveKeepOrder=%[9]d

    # Prepare the command to request completions for the program.
    # Split the command at the first space to separate the program and arguments.
    $Program,$Arguments = $Command.Split(" ",2)

    $RequestComp="$Program %[3]s $Arguments"
    __%[1]s_debug "RequestComp: $RequestComp"

    # we cannot use $WordToComplete because it
    # has the wrong values if the cursor was moved
    # so use the last argument
    if ($WordToComplete -ne "" ) {
        $WordToComplete = $Arguments.Split(" ")[-1]
    }
    __%[1]s_debug "New WordToComplete: $WordToComplete"


    # Check for flag with equal sign
    $IsEqualFlag = ($WordToComplete -Like "--*=*" )
    if ( $IsEqualFlag ) {
        __%[1]s_debug "Completing equal sign flag"
        # Remove the flag part
        $Flag,$WordToComplete = $WordToComplete.Split("=",2)
    }

    if ( $WordToComplete -eq "" -And ( -Not $IsEqualFlag )) {
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go method.
        __%[1]s_debug "Adding extra empty parameter"
        # PowerShell 7.2+ changed the way how the arguments are passed to executables,
        # so for pre-7.2 or when Legacy argument passing is enabled we need to use
`+"        # `\"`\" to pass an empty argument, a \"\" or '' does not work!!!"+`
        if ($PSVersionTable.PsVersion -lt [version]'7.2.0' -or
            ($PSVersionTable.PsVersion -lt [version]'7.3.0' -and -not [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -or
            (($PSVersionTable.PsVersion -ge [version]'7.3.0' -or [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -and
              $PSNativeCommandArgumentPassing -eq 'Legacy')) {
`+"             $RequestComp=\"$RequestComp\" + ' `\"`\"'"+`
        } else {
             $RequestComp="$RequestComp" + ' ""'
        }
    }

    __%[1]s_debug "Calling $RequestComp"
    # First disable ActiveHelp which is not supported for Powershell
    ${env:%[10]s}=0

    #call the command store the output in $out and redirect stderr and stdout to null
    # $Out is an array contains each line per element
    Invoke-Expression -OutVariable out "$RequestComp" 2>&1 | Out-Null

    # get directive from last line
    [int]$Directive = $Out[-1].TrimStart(':')
    if ($Directive -eq "") {
        # There is no directive specified
        $Directive = 0
    }
    __%[1]s_debug "The completion directive is: $Directive"

    # remove directive (last element) from out
    $Out = $Out | Where-Object { $_ -ne $Out[-1] }
    __%[1]s_debug "The completions are: $Out"

    if (($Directive -band $ShellCompDirectiveError) -ne 0 ) {
        # Error code.  No completion.
        __%[1]s_debug "Received error from custom completion go code"
        return
    }

    $Longest = 0
    [Array]$Values = $Out | ForEach-Object {
        #Split the output in name and description
`+"        $Name, $Description = $_.Split(\"`t\",2)"+`
        __%[1]s_debug "Name: $Name Description: $Description"

        # Look for the longest completion so that we can format things nicely
        if ($Longest -lt $Name.Length) {
            $Longest = $Name.Length
        }

        # Set the description to a one space string if there is none set.
        # This is needed because the CompletionResult does not accept an empty string as argument
        if (-Not $Description) {
            $Description = " "
        }
        New-Object -TypeName PSCustomObject -Property @{
            Name = "$Name"
            Description = "$Description"
        }
    }


    $Space = " "
    if (($Directive -band $ShellCompDirectiveNoSpace) -ne 0 ) {
        # remove the space here
        __%[1]s_debug "ShellCompDirectiveNoSpace is called"
        $Space = ""
    }

    if ((($Directive -band $ShellCompDirectiveFilterFileExt) -ne 0 ) -or
       (($Directive -band $ShellCompDirectiveFilterDirs) -ne 0 ))  {
        __%[1]s_debug "ShellCompDirectiveFilterFileExt ShellCompDirectiveFilterDirs are not supported"

        # return here to prevent the completion of the extensions
        return
    }

    $Values = $Values | Where-Object {
        # filter the result
        $_.Name -like "$WordToComplete*"

        # Join the flag back if we have an equal sign flag
        if ( $IsEqualFlag ) {
            __%[1]s_debug "Join the equal sign flag back to the completion value"
            $_.Name = $Flag + "=" + $_.Name
        }
    }

    # we sort the values in ascending order by name if keep order isn't passed
    if (($Directive -band $ShellCompDirectiveKeepOrder) -eq 0 ) {
        $Values = $Values | Sort-Object -Property Name
    }

    if (($Directive -band $ShellCompDirectiveNoFileComp) -ne 0 ) {
        __%[1]s_debug "ShellCompDirectiveNoFileComp is called"

        if ($Values.Length -eq 0) {
            # Just print an empty string here so the
            # shell does not start to complete paths.
            # We cannot use CompletionResult here because
            # it does not accept an empty string as argument.
            ""
            return
        }
    }

    # Get the current mode
    $Mode = (Get-PSReadLineKeyHandler | Where-Object {$_.Key -eq "Tab" }).Function
    __%[1]s_debug "Mode: $Mode"

    $Values | ForEach-Object {

        # store temporary because switch will overwrite $_
        $comp = $_

        # PowerShell supports three different completion modes
        # - TabCompleteNext (default windows style - on each key press the next option is displayed)
        # - Complete (works like bash)
        # - MenuComplete (works like zsh)
        # You set the mode with Set-PSReadLineKeyHandler -Key Tab -Function <mode>

        # CompletionResult Arguments:
        # 1) CompletionText text to be used as the auto completion result
        # 2) ListItemText   text to be displayed in the suggestion list
        # 3) ResultType     type of completion result
        # 4) ToolTip        text for the tooltip with details about the object

        switch ($Mode) {

            # bash like
            "Complete" {

                if ($Values.Length -eq 1) {
                    __%[1]s_debug "Only one completion left"

                    # insert space after value
                    $CompletionText = $($comp.Name | __%[1]s_escapeStringWithSpecialChars) + $Space
                    if ($ExecutionContext.SessionState.LanguageMode -eq "FullLanguage"){
                        [System.Management.Automation.CompletionResult]::new($CompletionText, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
                    } else {
                        $CompletionText
                    }

                } else {
                    # Add the proper number of spaces to align the descriptions
                    while($comp.Name.Length -lt $Longest) {
                        $comp.Name = $comp.Name + " "
                    }

                    # Check for empty description and only add parentheses if needed
                    if ($($comp.Description) -eq " " ) {
                        $Description = ""
                    } else {
                        $Description = "  ($($comp.Description))"
                    }

                    $CompletionText = "$($comp.Name)$Description"
                    if ($ExecutionContext.SessionState.LanguageMode -eq "FullLanguage"){
                        [System.Management.Automation.CompletionResult]::new($CompletionText, "$($comp.Name)$Description", 'ParameterValue', "$($comp.Description)")
                    } else {
                        $CompletionText
                    }
                }
             }

            # zsh like
            "MenuComplete" {
                # insert space after value
                # MenuComplete will automatically show the ToolTip of
                # the highlighted value at the bottom of the suggestions.

                $CompletionText = $($comp.Name | __%[1]s_escapeStringWithSpecialChars) + $Space
                if ($ExecutionContext.SessionState.LanguageMode -eq "FullLanguage"){
                    [System.Management.Automation.CompletionResult]::new($CompletionText, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
                } else {
                    $CompletionText
                }
            }

            # TabCompleteNext and in case we get something unknown
            Default {
                # Like MenuComplete but we don't want to add a space here because
                # the user need to press space anyway to get the completion.
                # Description will not be shown because that's not possible with TabCompleteNext

                $CompletionText = $($comp.Name | __%[1]s_escapeStringWithSpecialChars)
                if ($ExecutionContext.SessionState.LanguageMode -eq "FullLanguage"){
                    [System.Management.Automation.CompletionResult]::new($CompletionText, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
                } else {
                    $CompletionText
                }
            }
        }

    }
}

Register-ArgumentCompleter -CommandName '%[1]s' -ScriptBlock ${__%[2]sCompleterBlock}
`, name, nameForVar, compCmd,
		ShellCompDirectiveError, ShellCompDirectiveNoSpace, ShellCompDirectiveNoFileComp,
		ShellCompDirectiveFilterFileExt, ShellCompDirectiveFilterDirs, ShellCompDirectiveKeepOrder, activeHelpEnvVar(name)))
}
```


---

### 🔹 Commit #12: `756ba6da`
- **完整 Hash**: `756ba6dad61458cbbf7abecfc502d230574c57d2`
- **說明 (Ground Truth)**: fix(completions): Complete map flags multiple times (#2174)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:125, E:141, A:0) ➔ After(N:125, E:141, A:0)
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

### 🔹 函式: `Command.getCompletions()`
- **變更前簽章 (Before)**: `func Command.getCompletions(args []string)` (L273~L527)
- **變更後簽章 (After)**: `func Command.getCompletions(args []string)` (L273~L528)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				if !flag.Changed ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") {
					// If the flag is not already present, or if it can be specified multiple times (Array or Slice)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				if !flag.Changed ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") ||
					strings.HasPrefix(flag.Value.Type(), "stringTo") {
					// If the flag is not already present, or if it can be specified multiple times (Array, Slice, or stringTo)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```


---

### 🔹 Commit #13: `371ae25d`
- **完整 Hash**: `371ae25d2c82e519feb48c82d142e6a696fd06dd`
- **說明 (Ground Truth)**: Fix deprecation comment for Command.SetOutput (#2172)
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:224, E:386, A:0) ➔ After(N:224, E:386, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #14: `a73b9c39`
- **完整 Hash**: `a73b9c391a9489d20f5ee1480e75d3b99fc8c7e2`
- **說明 (Ground Truth)**: Fix help text for runnable plugin command
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:223, E:383, A:0) ➔ After(N:224, E:386, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 3, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.Replace (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.UseLine` ──[CALLS]──> `strings.Replace (External/Pkg)`
  • + [新增呼叫邊] `Command.UseLine` ──[CALLS]──> `Command.Name`
  • + [新增呼叫邊] `Command.UseLine` ──[CALLS]──> `Command.displayName`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.UseLine()`
- **變更前簽章 (Before)**: `func Command.UseLine()` (L1442~L1456)
- **變更後簽章 (After)**: `func Command.UseLine()` (L1442~L1457)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) UseLine() string {
	var useline string
	if c.HasParent() {
		useline = c.parent.CommandPath() + " " + c.Use
	} else {
		useline = c.Use
	}
	if c.DisableFlagsInUseLine {
		return useline
	}
	if c.HasAvailableFlags() && !strings.Contains(useline, "[flags]") {
		useline += " [flags]"
	}
	return useline
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) UseLine() string {
	var useline string
	use := strings.Replace(c.Use, c.Name(), c.displayName(), 1)
	if c.HasParent() {
		useline = c.parent.CommandPath() + " " + use
	} else {
		useline = use
	}
	if c.DisableFlagsInUseLine {
		return useline
	}
	if c.HasAvailableFlags() && !strings.Contains(useline, "[flags]") {
		useline += " [flags]"
	}
	return useline
}
```


---

### 🔹 Commit #15: `df547f5f`
- **完整 Hash**: `df547f5fc6ee86071f73c36c16afd885bb4e3f28`
- **說明 (Ground Truth)**: Fix help text for plugins
- **變更檔案數**: 1

#### 📄 檔案: `command.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:222, E:380, A:0) ➔ After(N:223, E:383, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 11, -Edges: 8, ΔFuncs: 10, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Command.displayName` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.InitDefaultHelpFlag` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.InitDefaultHelpCmd` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.CommandPath` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.displayName` ──[CALLS]──> `Command.Name`
  • + [新增呼叫邊] `Command.Flags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.LocalNonPersistentFlags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.LocalFlags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.InheritedFlags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.PersistentFlags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.ResetFlags` ──[CALLS]──> `Command.displayName`
  • + [新增呼叫邊] `Command.updateParentsPflags` ──[CALLS]──> `Command.displayName`
  • - [移除呼叫邊] `Command.InitDefaultHelpFlag` ──[CALLS]──> `Command.Name`
  • - [移除呼叫邊] `Command.Flags` ──[CALLS]──> `Command.Name`
  • - [移除呼叫邊] `Command.LocalNonPersistentFlags` ──[CALLS]──> `Command.Name`
  • _... 以及其餘 5 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.InitDefaultHelpCmd()`
- **變更前簽章 (Before)**: `func Command.InitDefaultHelpCmd()` (L1229~L1275)
- **變更後簽章 (After)**: `func Command.InitDefaultHelpCmd()` (L1230~L1276)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) InitDefaultHelpCmd() {
	if !c.HasSubCommands() {
		return
	}

	if c.helpCommand == nil {
		c.helpCommand = &Command{
			Use:   "help [command]",
			Short: "Help about any command",
			Long: `Help provides help for any command in the application.
Simply type ` + c.Name() + ` help [path to command] for full details.`,
			ValidArgsFunction: func(c *Command, args []string, toComplete string) ([]string, ShellCompDirective) {
				var completions []string
				cmd, _, e := c.Root().Find(args)
				if e != nil {
					return nil, ShellCompDirectiveNoFileComp
				}
				if cmd == nil {
					// Root help command.
					cmd = c.Root()
				}
				for _, subCmd := range cmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == cmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
					}
				}
				return completions, ShellCompDirectiveNoFileComp
			},
			Run: func(c *Command, args []string) {
				cmd, _, e := c.Root().Find(args)
				if cmd == nil || e != nil {
					c.Printf("Unknown help topic %#q\n", args)
					CheckErr(c.Root().Usage())
				} else {
					cmd.InitDefaultHelpFlag()    // make possible 'help' flag to be shown
					cmd.InitDefaultVersionFlag() // make possible 'version' flag to be shown
					CheckErr(cmd.Help())
				}
			},
			GroupID: c.helpCommandGroupID,
		}
	}
	c.RemoveCommand(c.helpCommand)
	c.AddCommand(c.helpCommand)
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) InitDefaultHelpCmd() {
	if !c.HasSubCommands() {
		return
	}

	if c.helpCommand == nil {
		c.helpCommand = &Command{
			Use:   "help [command]",
			Short: "Help about any command",
			Long: `Help provides help for any command in the application.
Simply type ` + c.displayName() + ` help [path to command] for full details.`,
			ValidArgsFunction: func(c *Command, args []string, toComplete string) ([]string, ShellCompDirective) {
				var completions []string
				cmd, _, e := c.Root().Find(args)
				if e != nil {
					return nil, ShellCompDirectiveNoFileComp
				}
				if cmd == nil {
					// Root help command.
					cmd = c.Root()
				}
				for _, subCmd := range cmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == cmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
					}
				}
				return completions, ShellCompDirectiveNoFileComp
			},
			Run: func(c *Command, args []string) {
				cmd, _, e := c.Root().Find(args)
				if cmd == nil || e != nil {
					c.Printf("Unknown help topic %#q\n", args)
					CheckErr(c.Root().Usage())
				} else {
					cmd.InitDefaultHelpFlag()    // make possible 'help' flag to be shown
					cmd.InitDefaultVersionFlag() // make possible 'version' flag to be shown
					CheckErr(cmd.Help())
				}
			},
			GroupID: c.helpCommandGroupID,
		}
	}
	c.RemoveCommand(c.helpCommand)
	c.AddCommand(c.helpCommand)
}
```

### 🔹 函式: `Command.PersistentFlags()`
- **變更前簽章 (Before)**: `func Command.PersistentFlags()` (L1726~L1735)
- **變更後簽章 (After)**: `func Command.PersistentFlags()` (L1731~L1740)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) PersistentFlags() *flag.FlagSet {
	if c.pflags == nil {
		c.pflags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.pflags.SetOutput(c.flagErrorBuf)
	}
	return c.pflags
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) PersistentFlags() *flag.FlagSet {
	if c.pflags == nil {
		c.pflags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.pflags.SetOutput(c.flagErrorBuf)
	}
	return c.pflags
}
```

### 🔹 函式: `Command.CommandPath()`
- **變更前簽章 (Before)**: `func Command.CommandPath()` (L1426~L1434)
- **變更後簽章 (After)**: `func Command.CommandPath()` (L1427~L1432)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) CommandPath() string {
	if c.HasParent() {
		return c.Parent().CommandPath() + " " + c.Name()
	}
	if displayName, ok := c.Annotations[CommandDisplayNameAnnotation]; ok {
		return displayName
	}
	return c.Name()
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) CommandPath() string {
	if c.HasParent() {
		return c.Parent().CommandPath() + " " + c.Name()
	}
	return c.displayName()
}
```

### 🔹 函式: `Command.LocalNonPersistentFlags()`
- **變更前簽章 (Before)**: `func Command.LocalNonPersistentFlags()` (L1656~L1666)
- **變更後簽章 (After)**: `func Command.LocalNonPersistentFlags()` (L1661~L1671)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) LocalNonPersistentFlags() *flag.FlagSet {
	persistentFlags := c.PersistentFlags()

	out := flag.NewFlagSet(c.Name(), flag.ContinueOnError)
	c.LocalFlags().VisitAll(func(f *flag.Flag) {
		if persistentFlags.Lookup(f.Name) == nil {
			out.AddFlag(f)
		}
	})
	return out
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) LocalNonPersistentFlags() *flag.FlagSet {
	persistentFlags := c.PersistentFlags()

	out := flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
	c.LocalFlags().VisitAll(func(f *flag.Flag) {
		if persistentFlags.Lookup(f.Name) == nil {
			out.AddFlag(f)
		}
	})
	return out
}
```

### 🔹 函式: `Command.ResetFlags()`
- **變更前簽章 (Before)**: `func Command.ResetFlags()` (L1738~L1749)
- **變更後簽章 (After)**: `func Command.ResetFlags()` (L1743~L1754)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) ResetFlags() {
	c.flagErrorBuf = new(bytes.Buffer)
	c.flagErrorBuf.Reset()
	c.flags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
	c.flags.SetOutput(c.flagErrorBuf)
	c.pflags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
	c.pflags.SetOutput(c.flagErrorBuf)

	c.lflags = nil
	c.iflags = nil
	c.parentsPflags = nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) ResetFlags() {
	c.flagErrorBuf = new(bytes.Buffer)
	c.flagErrorBuf.Reset()
	c.flags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
	c.flags.SetOutput(c.flagErrorBuf)
	c.pflags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
	c.pflags.SetOutput(c.flagErrorBuf)

	c.lflags = nil
	c.iflags = nil
	c.parentsPflags = nil
}
```

### 🔹 函式: `Command.updateParentsPflags()`
- **變更前簽章 (Before)**: `func Command.updateParentsPflags()` (L1858~L1874)
- **變更後簽章 (After)**: `func Command.updateParentsPflags()` (L1863~L1879)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) updateParentsPflags() {
	if c.parentsPflags == nil {
		c.parentsPflags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
		c.parentsPflags.SetOutput(c.flagErrorBuf)
		c.parentsPflags.SortFlags = false
	}

	if c.globNormFunc != nil {
		c.parentsPflags.SetNormalizeFunc(c.globNormFunc)
	}

	c.Root().PersistentFlags().AddFlagSet(flag.CommandLine)

	c.VisitParents(func(parent *Command) {
		c.parentsPflags.AddFlagSet(parent.PersistentFlags())
	})
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) updateParentsPflags() {
	if c.parentsPflags == nil {
		c.parentsPflags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
		c.parentsPflags.SetOutput(c.flagErrorBuf)
		c.parentsPflags.SortFlags = false
	}

	if c.globNormFunc != nil {
		c.parentsPflags.SetNormalizeFunc(c.globNormFunc)
	}

	c.Root().PersistentFlags().AddFlagSet(flag.CommandLine)

	c.VisitParents(func(parent *Command) {
		c.parentsPflags.AddFlagSet(parent.PersistentFlags())
	})
}
```

### 🔹 函式: `Command.Flags()`
- **變更前簽章 (Before)**: `func Command.Flags()` (L1643~L1653)
- **變更後簽章 (After)**: `func Command.Flags()` (L1648~L1658)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) Flags() *flag.FlagSet {
	if c.flags == nil {
		c.flags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.flags.SetOutput(c.flagErrorBuf)
	}

	return c.flags
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) Flags() *flag.FlagSet {
	if c.flags == nil {
		c.flags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.flags.SetOutput(c.flagErrorBuf)
	}

	return c.flags
}
```

### 🔹 函式: `Command.LocalFlags()`
- **變更前簽章 (Before)**: `func Command.LocalFlags()` (L1669~L1693)
- **變更後簽章 (After)**: `func Command.LocalFlags()` (L1674~L1698)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) LocalFlags() *flag.FlagSet {
	c.mergePersistentFlags()

	if c.lflags == nil {
		c.lflags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.lflags.SetOutput(c.flagErrorBuf)
	}
	c.lflags.SortFlags = c.Flags().SortFlags
	if c.globNormFunc != nil {
		c.lflags.SetNormalizeFunc(c.globNormFunc)
	}

	addToLocal := func(f *flag.Flag) {
		// Add the flag if it is not a parent PFlag, or it shadows a parent PFlag
		if c.lflags.Lookup(f.Name) == nil && f != c.parentsPflags.Lookup(f.Name) {
			c.lflags.AddFlag(f)
		}
	}
	c.Flags().VisitAll(addToLocal)
	c.PersistentFlags().VisitAll(addToLocal)
	return c.lflags
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) LocalFlags() *flag.FlagSet {
	c.mergePersistentFlags()

	if c.lflags == nil {
		c.lflags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.lflags.SetOutput(c.flagErrorBuf)
	}
	c.lflags.SortFlags = c.Flags().SortFlags
	if c.globNormFunc != nil {
		c.lflags.SetNormalizeFunc(c.globNormFunc)
	}

	addToLocal := func(f *flag.Flag) {
		// Add the flag if it is not a parent PFlag, or it shadows a parent PFlag
		if c.lflags.Lookup(f.Name) == nil && f != c.parentsPflags.Lookup(f.Name) {
			c.lflags.AddFlag(f)
		}
	}
	c.Flags().VisitAll(addToLocal)
	c.PersistentFlags().VisitAll(addToLocal)
	return c.lflags
}
```

### 🔹 函式: `Command.InheritedFlags()`
- **變更前簽章 (Before)**: `func Command.InheritedFlags()` (L1696~L1718)
- **變更後簽章 (After)**: `func Command.InheritedFlags()` (L1701~L1723)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) InheritedFlags() *flag.FlagSet {
	c.mergePersistentFlags()

	if c.iflags == nil {
		c.iflags = flag.NewFlagSet(c.Name(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.iflags.SetOutput(c.flagErrorBuf)
	}

	local := c.LocalFlags()
	if c.globNormFunc != nil {
		c.iflags.SetNormalizeFunc(c.globNormFunc)
	}

	c.parentsPflags.VisitAll(func(f *flag.Flag) {
		if c.iflags.Lookup(f.Name) == nil && local.Lookup(f.Name) == nil {
			c.iflags.AddFlag(f)
		}
	})
	return c.iflags
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) InheritedFlags() *flag.FlagSet {
	c.mergePersistentFlags()

	if c.iflags == nil {
		c.iflags = flag.NewFlagSet(c.displayName(), flag.ContinueOnError)
		if c.flagErrorBuf == nil {
			c.flagErrorBuf = new(bytes.Buffer)
		}
		c.iflags.SetOutput(c.flagErrorBuf)
	}

	local := c.LocalFlags()
	if c.globNormFunc != nil {
		c.iflags.SetNormalizeFunc(c.globNormFunc)
	}

	c.parentsPflags.VisitAll(func(f *flag.Flag) {
		if c.iflags.Lookup(f.Name) == nil && local.Lookup(f.Name) == nil {
			c.iflags.AddFlag(f)
		}
	})
	return c.iflags
}
```

### 🔹 函式: `Command.InitDefaultHelpFlag()`
- **變更前簽章 (Before)**: `func Command.InitDefaultHelpFlag()` (L1186~L1198)
- **變更後簽章 (After)**: `func Command.InitDefaultHelpFlag()` (L1186~L1199)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) InitDefaultHelpFlag() {
	c.mergePersistentFlags()
	if c.Flags().Lookup("help") == nil {
		usage := "help for "
		if c.Name() == "" {
			usage += "this command"
		} else {
			usage += c.Name()
		}
		c.Flags().BoolP("help", "h", false, usage)
		_ = c.Flags().SetAnnotation("help", FlagSetByCobraAnnotation, []string{"true"})
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) InitDefaultHelpFlag() {
	c.mergePersistentFlags()
	if c.Flags().Lookup("help") == nil {
		usage := "help for "
		name := c.displayName()
		if name == "" {
			usage += "this command"
		} else {
			usage += name
		}
		c.Flags().BoolP("help", "h", false, usage)
		_ = c.Flags().SetAnnotation("help", FlagSetByCobraAnnotation, []string{"true"})
	}
}
```


---

### 🔹 Commit #16: `e63925d3`
- **完整 Hash**: `e63925d3216142ba2c8d7641d729c6c15f4433e7`
- **說明 (Ground Truth)**: Add env variable to suppress completion descriptions on create (#1938)
- **變更檔案數**: 2

#### 📄 檔案: `active_help.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:11, E:9, A:0) ➔ After(N:9, E:7, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 3, +Edges: 1, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `configEnvVar (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `strings.ToUpper (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `activeHelpEnvVarPrefixSubstRegexp` (MODULE_STATE)
  • + [新增呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `configEnvVar (External/Pkg)`
  • - [移除呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `strings.ToUpper (External/Pkg)`
  • - [移除呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`
  • - [移除呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `activeHelpEnvVar()`
- **變更前簽章 (Before)**: `func activeHelpEnvVar(name string)` (L62~L67)
- **變更後簽章 (After)**: `func activeHelpEnvVar(name string)` (L58~L60)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func activeHelpEnvVar(name string) string {
	// This format should not be changed: users will be using it explicitly.
	activeHelpEnvVar := strings.ToUpper(fmt.Sprintf("%s%s", name, activeHelpEnvVarSuffix))
	activeHelpEnvVar = activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString(activeHelpEnvVar, "_")
	return activeHelpEnvVar
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func activeHelpEnvVar(name string) string {
	return configEnvVar(name, activeHelpEnvVarSuffix)
}
```


#### 📄 檔案: `completions.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:118, E:132, A:0) ➔ After(N:125, E:141, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 9, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `strings.ToUpper (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `configEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `strconv.ParseBool (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `configEnvVar` (FUNCTION_DEF)
  • + [新增節點] `cmd.Root().Name (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `configEnvVarPrefixSubstRegexp` (MODULE_STATE)
  • + [新增節點] `getEnvConfig` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.initCompleteCmd` ──[CALLS]──> `strconv.ParseBool (External/Pkg)`
  • + [新增呼叫邊] `Command.initCompleteCmd` ──[CALLS]──> `getEnvConfig`
  • + [新增呼叫邊] `configEnvVar` ──[CALLS]──> `strings.ToUpper (External/Pkg)`
  • + [新增呼叫邊] `configEnvVar` ──[CALLS]──> `fmt.Sprintf (External/Pkg)`
  • + [新增呼叫邊] `configEnvVar` ──[CALLS]──> `configEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)`
  • + [新增呼叫邊] `getEnvConfig` ──[CALLS]──> `os.Getenv (External/Pkg)`
  • + [新增呼叫邊] `getEnvConfig` ──[CALLS]──> `configEnvVar`
  • + [新增呼叫邊] `getEnvConfig` ──[CALLS]──> `cmd.Root().Name (External/Pkg)`
  • _... 以及其餘 1 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Command.initCompleteCmd()`
- **變更前簽章 (Before)**: `func Command.initCompleteCmd(args []string)` (L194~L264)
- **變更後簽章 (After)**: `func Command.initCompleteCmd(args []string)` (L196~L271)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) initCompleteCmd(args []string) {
	completeCmd := &Command{
		Use:                   fmt.Sprintf("%s [command-line]", ShellCompRequestCmd),
		Aliases:               []string{ShellCompNoDescRequestCmd},
		DisableFlagsInUseLine: true,
		Hidden:                true,
		DisableFlagParsing:    true,
		Args:                  MinimumNArgs(1),
		Short:                 "Request shell completion choices for the specified command-line",
		Long: fmt.Sprintf("%[2]s is a special command that is used by the shell completion logic\n%[1]s",
			"to request completion choices for the specified command-line.", ShellCompRequestCmd),
		Run: func(cmd *Command, args []string) {
			finalCmd, completions, directive, err := cmd.getCompletions(args)
			if err != nil {
				CompErrorln(err.Error())
				// Keep going for multiple reasons:
				// 1- There could be some valid completions even though there was an error
				// 2- Even without completions, we need to print the directive
			}

			noDescriptions := (cmd.CalledAs() == ShellCompNoDescRequestCmd)
			noActiveHelp := GetActiveHelpConfig(finalCmd) == activeHelpGlobalDisable
			out := finalCmd.OutOrStdout()
			for _, comp := range completions {
				if noActiveHelp && strings.HasPrefix(comp, activeHelpMarker) {
					// Remove all activeHelp entries if it's disabled.
					continue
				}
				if noDescriptions {
					// Remove any description that may be included following a tab character.
					comp = strings.SplitN(comp, "\t", 2)[0]
				}

				// Make sure we only write the first line to the output.
				// This is needed if a description contains a linebreak.
				// Otherwise the shell scripts will interpret the other lines as new flags
				// and could therefore provide a wrong completion.
				comp = strings.SplitN(comp, "\n", 2)[0]

				// Finally trim the completion.  This is especially important to get rid
				// of a trailing tab when there are no description following it.
				// For example, a sub-command without a description should not be completed
				// with a tab at the end (or else zsh will show a -- following it
				// although there is no description).
				comp = strings.TrimSpace(comp)

				// Print each possible completion to the output for the completion script to consume.
				fmt.Fprintln(out, comp)
			}

			// As the last printout, print the completion directive for the completion script to parse.
			// The directive integer must be that last character following a single colon (:).
			// The completion script expects :<directive>
			fmt.Fprintf(out, ":%d\n", directive)

			// Print some helpful info to stderr for the user to understand.
			// Output from stderr must be ignored by the completion script.
			fmt.Fprintf(finalCmd.ErrOrStderr(), "Completion ended with directive: %s\n", directive.string())
		},
	}
	c.AddCommand(completeCmd)
	subCmd, _, err := c.Find(args)
	if err != nil || subCmd.Name() != ShellCompRequestCmd {
		// Only create this special command if it is actually being called.
		// This reduces possible side-effects of creating such a command;
		// for example, having this command would cause problems to a
		// cobra program that only consists of the root command, since this
		// command would cause the root command to suddenly have a subcommand.
		c.RemoveCommand(completeCmd)
	}
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) initCompleteCmd(args []string) {
	completeCmd := &Command{
		Use:                   fmt.Sprintf("%s [command-line]", ShellCompRequestCmd),
		Aliases:               []string{ShellCompNoDescRequestCmd},
		DisableFlagsInUseLine: true,
		Hidden:                true,
		DisableFlagParsing:    true,
		Args:                  MinimumNArgs(1),
		Short:                 "Request shell completion choices for the specified command-line",
		Long: fmt.Sprintf("%[2]s is a special command that is used by the shell completion logic\n%[1]s",
			"to request completion choices for the specified command-line.", ShellCompRequestCmd),
		Run: func(cmd *Command, args []string) {
			finalCmd, completions, directive, err := cmd.getCompletions(args)
			if err != nil {
				CompErrorln(err.Error())
				// Keep going for multiple reasons:
				// 1- There could be some valid completions even though there was an error
				// 2- Even without completions, we need to print the directive
			}

			noDescriptions := cmd.CalledAs() == ShellCompNoDescRequestCmd
			if !noDescriptions {
				if doDescriptions, err := strconv.ParseBool(getEnvConfig(cmd, configEnvVarSuffixDescriptions)); err == nil {
					noDescriptions = !doDescriptions
				}
			}
			noActiveHelp := GetActiveHelpConfig(finalCmd) == activeHelpGlobalDisable
			out := finalCmd.OutOrStdout()
			for _, comp := range completions {
				if noActiveHelp && strings.HasPrefix(comp, activeHelpMarker) {
					// Remove all activeHelp entries if it's disabled.
					continue
				}
				if noDescriptions {
					// Remove any description that may be included following a tab character.
					comp = strings.SplitN(comp, "\t", 2)[0]
				}

				// Make sure we only write the first line to the output.
				// This is needed if a description contains a linebreak.
				// Otherwise the shell scripts will interpret the other lines as new flags
				// and could therefore provide a wrong completion.
				comp = strings.SplitN(comp, "\n", 2)[0]

				// Finally trim the completion.  This is especially important to get rid
				// of a trailing tab when there are no description following it.
				// For example, a sub-command without a description should not be completed
				// with a tab at the end (or else zsh will show a -- following it
				// although there is no description).
				comp = strings.TrimSpace(comp)

				// Print each possible completion to the output for the completion script to consume.
				fmt.Fprintln(out, comp)
			}

			// As the last printout, print the completion directive for the completion script to parse.
			// The directive integer must be that last character following a single colon (:).
			// The completion script expects :<directive>
			fmt.Fprintf(out, ":%d\n", directive)

			// Print some helpful info to stderr for the user to understand.
			// Output from stderr must be ignored by the completion script.
			fmt.Fprintf(finalCmd.ErrOrStderr(), "Completion ended with directive: %s\n", directive.string())
		},
	}
	c.AddCommand(completeCmd)
	subCmd, _, err := c.Find(args)
	if err != nil || subCmd.Name() != ShellCompRequestCmd {
		// Only create this special command if it is actually being called.
		// This reduces possible side-effects of creating such a command;
		// for example, having this command would cause problems to a
		// cobra program that only consists of the root command, since this
		// command would cause the root command to suddenly have a subcommand.
		c.RemoveCommand(completeCmd)
	}
}
```


---

### 🔹 Commit #17: `a0a6ae02`
- **完整 Hash**: `a0a6ae020bb3899ff0276067863e50523f897370`
- **說明 (Ground Truth)**: Improve API to get flag completion function (#2063)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:121, E:134, A:0) ➔ After(N:118, E:132, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 4, +Edges: 3, -Edges: 5, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Command.GetFlagCompletionFunc` (FUNCTION_DEF)
  • - [移除節點] `c.Flags().Lookup (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `GetFlagCompletion` (FUNCTION_DEF)
  • - [移除節點] `c.Flags (External/Pkg)` (FUNCTION_DEF)
  • - [移除節點] `Command.GetFlagCompletionByName` (FUNCTION_DEF)
  • + [新增呼叫邊] `Command.GetFlagCompletionFunc` ──[CALLS]──> `c.Flag (External/Pkg)`
  • + [新增呼叫邊] `Command.GetFlagCompletionFunc` ──[CALLS]──> `flagCompletionMutex.RLock (External/Pkg)`
  • + [新增呼叫邊] `Command.GetFlagCompletionFunc` ──[CALLS]──> `flagCompletionMutex.RUnlock (External/Pkg)`
  • - [移除呼叫邊] `GetFlagCompletion` ──[CALLS]──> `flagCompletionMutex.RLock (External/Pkg)`
  • - [移除呼叫邊] `GetFlagCompletion` ──[CALLS]──> `flagCompletionMutex.RUnlock (External/Pkg)`
  • - [移除呼叫邊] `Command.GetFlagCompletionByName` ──[CALLS]──> `c.Flags().Lookup (External/Pkg)`
  • - [移除呼叫邊] `Command.GetFlagCompletionByName` ──[CALLS]──> `c.Flags (External/Pkg)`
  • - [移除呼叫邊] `Command.GetFlagCompletionByName` ──[CALLS]──> `GetFlagCompletion`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #18: `22953d88`
- **完整 Hash**: `22953d88453ec9343b4a78b9d67400a3326f3138`
- **說明 (Ground Truth)**: Replace all non-alphanumerics in active help env var program prefix (#1940)
- **變更檔案數**: 1

#### 📄 檔案: `active_help.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:10, E:9, A:0) ➔ After(N:11, E:9, A:0)
- **差分統計**: +Nodes: 2, -Nodes: 1, +Edges: 1, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)` (FUNCTION_DEF)
  • + [新增節點] `activeHelpEnvVarPrefixSubstRegexp` (MODULE_STATE)
  • - [移除節點] `strings.ReplaceAll (External/Pkg)` (FUNCTION_DEF)
  • + [新增呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString (External/Pkg)`
  • - [移除呼叫邊] `activeHelpEnvVar` ──[CALLS]──> `strings.ReplaceAll (External/Pkg)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `activeHelpEnvVar()`
- **變更前簽章 (Before)**: `func activeHelpEnvVar(name string)` (L59~L63)
- **變更後簽章 (After)**: `func activeHelpEnvVar(name string)` (L62~L67)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func activeHelpEnvVar(name string) string {
	// This format should not be changed: users will be using it explicitly.
	activeHelpEnvVar := strings.ToUpper(fmt.Sprintf("%s%s", name, activeHelpEnvVarSuffix))
	return strings.ReplaceAll(activeHelpEnvVar, "-", "_")
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func activeHelpEnvVar(name string) string {
	// This format should not be changed: users will be using it explicitly.
	activeHelpEnvVar := strings.ToUpper(fmt.Sprintf("%s%s", name, activeHelpEnvVarSuffix))
	activeHelpEnvVar = activeHelpEnvVarPrefixSubstRegexp.ReplaceAllString(activeHelpEnvVar, "_")
	return activeHelpEnvVar
}
```


---

### 🔹 Commit #19: `b711e876`
- **完整 Hash**: `b711e8760b73c6aa1b4aa1bef3a26da5926f175d`
- **說明 (Ground Truth)**: Don't complete --help flag when flag parsing disabled (#2061)
- **變更檔案數**: 1

#### 📄 檔案: `completions.go`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:121, E:134, A:0) ➔ After(N:121, E:134, A:0)
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

### 🔹 函式: `Command.getCompletions()`
- **變更前簽章 (Before)**: `func Command.getCompletions(args []string)` (L271~L516)
- **變更後簽章 (After)**: `func Command.getCompletions(args []string)` (L271~L525)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves.
	finalCmd.InitDefaultHelpFlag()
	finalCmd.InitDefaultVersionFlag()

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				if !flag.Changed ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") {
					// If the flag is not already present, or if it can be specified multiple times (Array or Slice)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func (c *Command) getCompletions(args []string) (*Command, []string, ShellCompDirective, error) {
	// The last argument, which is not completely typed by the user,
	// should not be part of the list of arguments
	toComplete := args[len(args)-1]
	trimmedArgs := args[:len(args)-1]

	var finalCmd *Command
	var finalArgs []string
	var err error
	// Find the real command for which completion must be performed
	// check if we need to traverse here to parse local flags on parent commands
	if c.Root().TraverseChildren {
		finalCmd, finalArgs, err = c.Root().Traverse(trimmedArgs)
	} else {
		// For Root commands that don't specify any value for their Args fields, when we call
		// Find(), if those Root commands don't have any sub-commands, they will accept arguments.
		// However, because we have added the __complete sub-command in the current code path, the
		// call to Find() -> legacyArgs() will return an error if there are any arguments.
		// To avoid this, we first remove the __complete command to get back to having no sub-commands.
		rootCmd := c.Root()
		if len(rootCmd.Commands()) == 1 {
			rootCmd.RemoveCommand(c)
		}

		finalCmd, finalArgs, err = rootCmd.Find(trimmedArgs)
	}
	if err != nil {
		// Unable to find the real command. E.g., <program> someInvalidCmd <TAB>
		return c, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Unable to find a command for arguments: %v", trimmedArgs)
	}
	finalCmd.ctx = c.ctx

	// These flags are normally added when `execute()` is called on `finalCmd`,
	// however, when doing completion, we don't call `finalCmd.execute()`.
	// Let's add the --help and --version flag ourselves but only if the finalCmd
	// has not disabled flag parsing; if flag parsing is disabled, it is up to the
	// finalCmd itself to handle the completion of *all* flags.
	if !finalCmd.DisableFlagParsing {
		finalCmd.InitDefaultHelpFlag()
		finalCmd.InitDefaultVersionFlag()
	}

	// Check if we are doing flag value completion before parsing the flags.
	// This is important because if we are completing a flag value, we need to also
	// remove the flag name argument from the list of finalArgs or else the parsing
	// could fail due to an invalid value (incomplete) for the flag.
	flag, finalArgs, toComplete, flagErr := checkIfFlagCompletion(finalCmd, finalArgs, toComplete)

	// Check if interspersed is false or -- was set on a previous arg.
	// This works by counting the arguments. Normally -- is not counted as arg but
	// if -- was already set or interspersed is false and there is already one arg then
	// the extra added -- is counted as arg.
	flagCompletion := true
	_ = finalCmd.ParseFlags(append(finalArgs, "--"))
	newArgCount := finalCmd.Flags().NArg()

	// Parse the flags early so we can check if required flags are set
	if err = finalCmd.ParseFlags(finalArgs); err != nil {
		return finalCmd, []string{}, ShellCompDirectiveDefault, fmt.Errorf("Error while parsing flags from args %v: %s", finalArgs, err.Error())
	}

	realArgCount := finalCmd.Flags().NArg()
	if newArgCount > realArgCount {
		// don't do flag completion (see above)
		flagCompletion = false
	}
	// Error while attempting to parse flags
	if flagErr != nil {
		// If error type is flagCompError and we don't want flagCompletion we should ignore the error
		if _, ok := flagErr.(*flagCompError); !(ok && !flagCompletion) {
			return finalCmd, []string{}, ShellCompDirectiveDefault, flagErr
		}
	}

	// Look for the --help or --version flags.  If they are present,
	// there should be no further completions.
	if helpOrVersionFlagPresent(finalCmd) {
		return finalCmd, []string{}, ShellCompDirectiveNoFileComp, nil
	}

	// We only remove the flags from the arguments if DisableFlagParsing is not set.
	// This is important for commands which have requested to do their own flag completion.
	if !finalCmd.DisableFlagParsing {
		finalArgs = finalCmd.Flags().Args()
	}

	if flag != nil && flagCompletion {
		// Check if we are completing a flag value subject to annotations
		if validExts, present := flag.Annotations[BashCompFilenameExt]; present {
			if len(validExts) != 0 {
				// File completion filtered by extensions
				return finalCmd, validExts, ShellCompDirectiveFilterFileExt, nil
			}

			// The annotation requests simple file completion.  There is no reason to do
			// that since it is the default behavior anyway.  Let's ignore this annotation
			// in case the program also registered a completion function for this flag.
			// Even though it is a mistake on the program's side, let's be nice when we can.
		}

		if subDir, present := flag.Annotations[BashCompSubdirsInDir]; present {
			if len(subDir) == 1 {
				// Directory completion from within a directory
				return finalCmd, subDir, ShellCompDirectiveFilterDirs, nil
			}
			// Directory completion
			return finalCmd, []string{}, ShellCompDirectiveFilterDirs, nil
		}
	}

	var completions []string
	var directive ShellCompDirective

	// Enforce flag groups before doing flag completions
	finalCmd.enforceFlagGroupsForCompletion()

	// Note that we want to perform flagname completion even if finalCmd.DisableFlagParsing==true;
	// doing this allows for completion of persistent flag names even for commands that disable flag parsing.
	//
	// When doing completion of a flag name, as soon as an argument starts with
	// a '-' we know it is a flag.  We cannot use isFlagArg() here as it requires
	// the flag name to be complete
	if flag == nil && len(toComplete) > 0 && toComplete[0] == '-' && !strings.Contains(toComplete, "=") && flagCompletion {
		// First check for required flags
		completions = completeRequireFlags(finalCmd, toComplete)

		// If we have not found any required flags, only then can we show regular flags
		if len(completions) == 0 {
			doCompleteFlags := func(flag *pflag.Flag) {
				if !flag.Changed ||
					strings.Contains(flag.Value.Type(), "Slice") ||
					strings.Contains(flag.Value.Type(), "Array") {
					// If the flag is not already present, or if it can be specified multiple times (Array or Slice)
					// we suggest it as a completion
					completions = append(completions, getFlagNameCompletions(flag, toComplete)...)
				}
			}

			// We cannot use finalCmd.Flags() because we may not have called ParsedFlags() for commands
			// that have set DisableFlagParsing; it is ParseFlags() that merges the inherited and
			// non-inherited flags.
			finalCmd.InheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
			// Try to complete non-inherited flags even if DisableFlagParsing==true.
			// This allows programs to tell Cobra about flags for completion even
			// if the actual parsing of flags is not done by Cobra.
			// For instance, Helm uses this to provide flag name completion for
			// some of its plugins.
			finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
				doCompleteFlags(flag)
			})
		}

		directive = ShellCompDirectiveNoFileComp
		if len(completions) == 1 && strings.HasSuffix(completions[0], "=") {
			// If there is a single completion, the shell usually adds a space
			// after the completion.  We don't want that if the flag ends with an =
			directive = ShellCompDirectiveNoSpace
		}

		if !finalCmd.DisableFlagParsing {
			// If DisableFlagParsing==false, we have completed the flags as known by Cobra;
			// we can return what we found.
			// If DisableFlagParsing==true, Cobra may not be aware of all flags, so we
			// let the logic continue to see if ValidArgsFunction needs to be called.
			return finalCmd, completions, directive, nil
		}
	} else {
		directive = ShellCompDirectiveDefault
		if flag == nil {
			foundLocalNonPersistentFlag := false
			// If TraverseChildren is true on the root command we don't check for
			// local flags because we can use a local flag on a parent command
			if !finalCmd.Root().TraverseChildren {
				// Check if there are any local, non-persistent flags on the command-line
				localNonPersistentFlags := finalCmd.LocalNonPersistentFlags()
				finalCmd.NonInheritedFlags().VisitAll(func(flag *pflag.Flag) {
					if localNonPersistentFlags.Lookup(flag.Name) != nil && flag.Changed {
						foundLocalNonPersistentFlag = true
					}
				})
			}

			// Complete subcommand names, including the help command
			if len(finalArgs) == 0 && !foundLocalNonPersistentFlag {
				// We only complete sub-commands if:
				// - there are no arguments on the command-line and
				// - there are no local, non-persistent flags on the command-line or TraverseChildren is true
				for _, subCmd := range finalCmd.Commands() {
					if subCmd.IsAvailableCommand() || subCmd == finalCmd.helpCommand {
						if strings.HasPrefix(subCmd.Name(), toComplete) {
							completions = append(completions, fmt.Sprintf("%s\t%s", subCmd.Name(), subCmd.Short))
						}
						directive = ShellCompDirectiveNoFileComp
					}
				}
			}

			// Complete required flags even without the '-' prefix
			completions = append(completions, completeRequireFlags(finalCmd, toComplete)...)

			// Always complete ValidArgs, even if we are completing a subcommand name.
			// This is for commands that have both subcommands and ValidArgs.
			if len(finalCmd.ValidArgs) > 0 {
				if len(finalArgs) == 0 {
					// ValidArgs are only for the first argument
					for _, validArg := range finalCmd.ValidArgs {
						if strings.HasPrefix(validArg, toComplete) {
							completions = append(completions, validArg)
						}
					}
					directive = ShellCompDirectiveNoFileComp

					// If no completions were found within commands or ValidArgs,
					// see if there are any ArgAliases that should be completed.
					if len(completions) == 0 {
						for _, argAlias := range finalCmd.ArgAliases {
							if strings.HasPrefix(argAlias, toComplete) {
								completions = append(completions, argAlias)
							}
						}
					}
				}

				// If there are ValidArgs specified (even if they don't match), we stop completion.
				// Only one of ValidArgs or ValidArgsFunction can be used for a single command.
				return finalCmd, completions, directive, nil
			}

			// Let the logic continue so as to add any ValidArgsFunction completions,
			// even if we already found sub-commands.
			// This is for commands that have subcommands but also specify a ValidArgsFunction.
		}
	}

	// Find the completion function for the flag or command
	var completionFn func(cmd *Command, args []string, toComplete string) ([]string, ShellCompDirective)
	if flag != nil && flagCompletion {
		flagCompletionMutex.RLock()
		completionFn = flagCompletionFunctions[flag]
		flagCompletionMutex.RUnlock()
	} else {
		completionFn = finalCmd.ValidArgsFunction
	}
	if completionFn != nil {
		// Go custom completion defined for this flag or command.
		// Call the registered completion function to get the completions.
		var comps []string
		comps, directive = completionFn(finalCmd, finalArgs, toComplete)
		completions = append(completions, comps...)
	}

	return finalCmd, completions, directive, nil
}
```


---

### 🔹 Commit #20: `8b1eba47`
- **完整 Hash**: `8b1eba47616566fc4d258a93da48d5d8741865f0`
- **說明 (Ground Truth)**: Fix linter errors (#2052)
- **變更檔案數**: 2

#### 📄 檔案: `command.go`
- **變更分類**: `ZERO_DELTA`
- **圖譜變更**: Before(N:219, E:377, A:0) ➔ After(N:219, E:377, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

#### 📄 檔案: `doc/md_docs.go`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:45, E:49, A:0) ➔ After(N:46, E:49, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 0, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `markdownExtension` (MODULE_STATE)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `GenMarkdownCustom()`
- **變更前簽章 (Before)**: `func GenMarkdownCustom(cmd *cobra.Command, w io.Writer, linkHandler func(string) string)` (L55~L115)
- **變更後簽章 (After)**: `func GenMarkdownCustom(cmd *cobra.Command, w io.Writer, linkHandler func(string) string)` (L57~L117)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func GenMarkdownCustom(cmd *cobra.Command, w io.Writer, linkHandler func(string) string) error {
	cmd.InitDefaultHelpCmd()
	cmd.InitDefaultHelpFlag()

	buf := new(bytes.Buffer)
	name := cmd.CommandPath()

	buf.WriteString("## " + name + "\n\n")
	buf.WriteString(cmd.Short + "\n\n")
	if len(cmd.Long) > 0 {
		buf.WriteString("### Synopsis\n\n")
		buf.WriteString(cmd.Long + "\n\n")
	}

	if cmd.Runnable() {
		buf.WriteString(fmt.Sprintf("```\n%s\n```\n\n", cmd.UseLine()))
	}

	if len(cmd.Example) > 0 {
		buf.WriteString("### Examples\n\n")
		buf.WriteString(fmt.Sprintf("```\n%s\n```\n\n", cmd.Example))
	}

	if err := printOptions(buf, cmd, name); err != nil {
		return err
	}
	if hasSeeAlso(cmd) {
		buf.WriteString("### SEE ALSO\n\n")
		if cmd.HasParent() {
			parent := cmd.Parent()
			pname := parent.CommandPath()
			link := pname + ".md"
			link = strings.ReplaceAll(link, " ", "_")
			buf.WriteString(fmt.Sprintf("* [%s](%s)\t - %s\n", pname, linkHandler(link), parent.Short))
			cmd.VisitParents(func(c *cobra.Command) {
				if c.DisableAutoGenTag {
					cmd.DisableAutoGenTag = c.DisableAutoGenTag
				}
			})
		}

		children := cmd.Commands()
		sort.Sort(byName(children))

		for _, child := range children {
			if !child.IsAvailableCommand() || child.IsAdditionalHelpTopicCommand() {
				continue
			}
			cname := name + " " + child.Name()
			link := cname + ".md"
			link = strings.ReplaceAll(link, " ", "_")
			buf.WriteString(fmt.Sprintf("* [%s](%s)\t - %s\n", cname, linkHandler(link), child.Short))
		}
		buf.WriteString("\n")
	}
	if !cmd.DisableAutoGenTag {
		buf.WriteString("###### Auto generated by spf13/cobra on " + time.Now().Format("2-Jan-2006") + "\n")
	}
	_, err := buf.WriteTo(w)
	return err
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func GenMarkdownCustom(cmd *cobra.Command, w io.Writer, linkHandler func(string) string) error {
	cmd.InitDefaultHelpCmd()
	cmd.InitDefaultHelpFlag()

	buf := new(bytes.Buffer)
	name := cmd.CommandPath()

	buf.WriteString("## " + name + "\n\n")
	buf.WriteString(cmd.Short + "\n\n")
	if len(cmd.Long) > 0 {
		buf.WriteString("### Synopsis\n\n")
		buf.WriteString(cmd.Long + "\n\n")
	}

	if cmd.Runnable() {
		buf.WriteString(fmt.Sprintf("```\n%s\n```\n\n", cmd.UseLine()))
	}

	if len(cmd.Example) > 0 {
		buf.WriteString("### Examples\n\n")
		buf.WriteString(fmt.Sprintf("```\n%s\n```\n\n", cmd.Example))
	}

	if err := printOptions(buf, cmd, name); err != nil {
		return err
	}
	if hasSeeAlso(cmd) {
		buf.WriteString("### SEE ALSO\n\n")
		if cmd.HasParent() {
			parent := cmd.Parent()
			pname := parent.CommandPath()
			link := pname + markdownExtension
			link = strings.ReplaceAll(link, " ", "_")
			buf.WriteString(fmt.Sprintf("* [%s](%s)\t - %s\n", pname, linkHandler(link), parent.Short))
			cmd.VisitParents(func(c *cobra.Command) {
				if c.DisableAutoGenTag {
					cmd.DisableAutoGenTag = c.DisableAutoGenTag
				}
			})
		}

		children := cmd.Commands()
		sort.Sort(byName(children))

		for _, child := range children {
			if !child.IsAvailableCommand() || child.IsAdditionalHelpTopicCommand() {
				continue
			}
			cname := name + " " + child.Name()
			link := cname + markdownExtension
			link = strings.ReplaceAll(link, " ", "_")
			buf.WriteString(fmt.Sprintf("* [%s](%s)\t - %s\n", cname, linkHandler(link), child.Short))
		}
		buf.WriteString("\n")
	}
	if !cmd.DisableAutoGenTag {
		buf.WriteString("###### Auto generated by spf13/cobra on " + time.Now().Format("2-Jan-2006") + "\n")
	}
	_, err := buf.WriteTo(w)
	return err
}
```

### 🔹 函式: `GenMarkdownTreeCustom()`
- **變更前簽章 (Before)**: `func GenMarkdownTreeCustom(cmd *cobra.Command, dir string, filePrepender, linkHandler func(string) string)` (L131~L156)
- **變更後簽章 (After)**: `func GenMarkdownTreeCustom(cmd *cobra.Command, dir string, filePrepender, linkHandler func(string) string)` (L133~L158)

#### ◀️ 變更前實作碼 (Before Implementation):
```
func GenMarkdownTreeCustom(cmd *cobra.Command, dir string, filePrepender, linkHandler func(string) string) error {
	for _, c := range cmd.Commands() {
		if !c.IsAvailableCommand() || c.IsAdditionalHelpTopicCommand() {
			continue
		}
		if err := GenMarkdownTreeCustom(c, dir, filePrepender, linkHandler); err != nil {
			return err
		}
	}

	basename := strings.ReplaceAll(cmd.CommandPath(), " ", "_") + ".md"
	filename := filepath.Join(dir, basename)
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	if _, err := io.WriteString(f, filePrepender(filename)); err != nil {
		return err
	}
	if err := GenMarkdownCustom(cmd, f, linkHandler); err != nil {
		return err
	}
	return nil
}
```

#### ▶️ 變更後實作碼 (After Implementation):
```
func GenMarkdownTreeCustom(cmd *cobra.Command, dir string, filePrepender, linkHandler func(string) string) error {
	for _, c := range cmd.Commands() {
		if !c.IsAvailableCommand() || c.IsAdditionalHelpTopicCommand() {
			continue
		}
		if err := GenMarkdownTreeCustom(c, dir, filePrepender, linkHandler); err != nil {
			return err
		}
	}

	basename := strings.ReplaceAll(cmd.CommandPath(), " ", "_") + markdownExtension
	filename := filepath.Join(dir, basename)
	f, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer f.Close()

	if _, err := io.WriteString(f, filePrepender(filename)); err != nil {
		return err
	}
	if err := GenMarkdownCustom(cmd, f, linkHandler); err != nil {
		return err
	}
	return nil
}
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/cobra show 746ef07158728502482cea9f880a6f4b21ef29a9
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff 746ef07158728502482cea9f880a6f4b21ef29a9~1 --file test_repos/cobra/completions.go
   ```
