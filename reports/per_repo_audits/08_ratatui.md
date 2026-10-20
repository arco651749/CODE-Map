# 🔬 CODE-Map 基準審查獨立驗證報告: `ratatui`
> **技術生態**: `Rust (終端 UI / 系統級緩衝繪製)`  
> **本地倉庫路徑**: `test_repos/ratatui`  
> **審查 Commit 數**: 20 Commits  
> **審查原始碼檔案數**: 34 Files  
> **報告生成時間**: 2026-10-20 21:41:04  

---

## 📊 驗證指標總評 (Scorecard - 去水分客觀指標)

| 指標項目 | 數值 / 統計 | 佔比 | 意義說明 |
| :--- | :---: | :---: | :--- |
| **結構性因果圖變動 (Structural Graph Delta)** | `33` / `34` | `97.1%` | 節點增減、呼叫電線接通/斷開、守衛狀態躍遷 |
| **函式體純文字變動 (Body-Level Semantic Delta)** | `1` / `34` | `2.9%` | 函式內部演算法或實作修改，但控制流拓樸不變 |
| **無語意圖譜變動 (Zero Delta)** | `0` / `34` | `0.0%` | 純型別宣告、註釋更動或格式微調 (非可執行邏輯) |
| **🏆 總體可執行邏輯變更捕獲率** | **`34` / `34`** | **`100.0%`** | 排除純型別/註釋後的總體捕獲命中率 |
| **AST 解析錯誤數 (Crash / Parse Error)** | `0` / `34` | `0.0%` | 全程零崩潰、語法解析完全通過 |

---

## 📋 逐條 Commit 形式化審查證明 (Ground Truth vs CODE-Map Proof)

### 🔹 Commit #01: `d1ef782b`
- **完整 Hash**: `d1ef782b48ddf0cb825c111d4d8b9adef572c0e1`
- **說明 (Ground Truth)**: fix(charts): clip rendering to buffer bounds (#2817)
- **變更檔案數**: 3

#### 📄 檔案: `ratatui-widgets/src/barchart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:219, E:534, A:0) ➔ After(N:226, E:550, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 16, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_barchart_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_barchart_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `BarChart::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `BarChart::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::new`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::render`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `data`
  • + [新增呼叫邊] `render_barchart_outside_buffer_is_noop` ──[CALLS]──> `BarChart::default`
  • _... 以及其餘 8 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BarChart::render()`
- **變更前簽章 (Before)**: `fn BarChart::render(self, area: Rect, buf: &mut Buffer)` (L705~L719)
- **變更後簽章 (After)**: `fn BarChart::render(self, area: Rect, buf: &mut Buffer)` (L705~L724)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);

        if inner.is_empty() || self.data.is_empty() || self.bar_width == 0 {
            return;
        }

        match self.direction {
            Direction::Horizontal => self.render_horizontal(buf, inner),
            Direction::Vertical => self.render_vertical(buf, inner),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);

        if inner.is_empty() || self.data.is_empty() || self.bar_width == 0 {
            return;
        }

        match self.direction {
            Direction::Horizontal => self.render_horizontal(buf, inner),
            Direction::Vertical => self.render_vertical(buf, inner),
        }
    }
```


#### 📄 檔案: `ratatui-widgets/src/chart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:182, E:329, A:0) ➔ After(N:189, E:347, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 18, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_chart_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_chart_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `Chart::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Chart::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Chart::new`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `Chart::render`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `vec! (Macro)`
  • + [新增呼叫邊] `render_chart_outside_buffer_is_noop` ──[CALLS]──> `assert_eq! (Macro)`
  • _... 以及其餘 10 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Chart::render()`
- **變更前簽章 (Before)**: `fn Chart::render(self, area: Rect, buf: &mut Buffer)` (L1002~L1157)
- **變更後簽章 (After)**: `fn Chart::render(self, area: Rect, buf: &mut Buffer)` (L1002~L1162)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let chart_area = self.block.inner_if_some(area);
        let Some(layout) = self.layout(chart_area) else {
            return;
        };
        let graph_area = layout.graph_area;

        // Sample the style of the entire widget. This sample will be used to reset the style of
        // the cells that are part of the components put on top of the grah area (i.e legend and
        // axis names).
        let original_style = buf[(area.left(), area.top())].style();

        self.render_x_labels(buf, &layout, chart_area, graph_area);
        self.render_y_labels(buf, &layout, chart_area, graph_area);

        if let Some(y) = layout.axis_x {
            for x in graph_area.left()..graph_area.right() {
                buf[(x, y)]
                    .set_symbol(symbols::line::HORIZONTAL)
                    .set_style(self.x_axis.style);
            }
        }

        if let Some(x) = layout.axis_y {
            for y in graph_area.top()..graph_area.bottom() {
                buf[(x, y)]
                    .set_symbol(symbols::line::VERTICAL)
                    .set_style(self.y_axis.style);
            }
        }

        if let Some(y) = layout.axis_x
            && let Some(x) = layout.axis_y
        {
            buf[(x, y)]
                .set_symbol(symbols::line::BOTTOM_LEFT)
                .set_style(self.x_axis.style);
        }

        Canvas::default()
            .background_color(self.style.bg.unwrap_or(Color::Reset))
            .x_bounds(self.x_axis.bounds)
            .y_bounds(self.y_axis.bounds)
            .paint(|ctx| {
                for dataset in &self.datasets {
                    ctx.marker(dataset.marker);

                    let color = dataset.style.fg.unwrap_or(Color::Reset);
                    ctx.draw(&Points {
                        coords: dataset.data,
                        color,
                    });
                    match dataset.graph_type {
                        GraphType::Line => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&CanvasLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    color,
                                });
                            }
                        }
                        GraphType::Bar => {
                            for (x, y) in dataset.data {
                                ctx.draw(&CanvasLine {
                                    x1: *x,
                                    y1: 0.0,
                                    x2: *x,
                                    y2: *y,
                                    color,
                                });
                            }
                        }
                        GraphType::Area => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&FilledLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    fill_to_y: dataset.fill_to_y,
                                    color,
                                });
                            }
                        }

                        GraphType::Scatter => {}
                    }
                }
            })
            .render(graph_area, buf);

        if let Some(Position { x, y }) = layout.title_x {
            let title = self.x_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(Position { x, y }) = layout.title_y {
            let title = self.y_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(legend_area) = layout.legend_area {
            buf.set_style(legend_area, original_style);
            Block::bordered().render(legend_area, buf);

            for (i, (dataset_name, dataset_style)) in self
                .datasets
                .iter()
                .filter_map(|ds| Some((ds.name.as_ref()?, ds.style())))
                .enumerate()
            {
                let name = dataset_name.clone().patch_style(dataset_style);
                name.render(
                    Rect {
                        x: legend_area.x + 1,
                        y: legend_area.y + 1 + i as u16,
                        width: legend_area.width - 2,
                        height: 1,
                    },
                    buf,
                );
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);

        self.block.as_ref().render(area, buf);
        let chart_area = self.block.inner_if_some(area);
        let Some(layout) = self.layout(chart_area) else {
            return;
        };
        let graph_area = layout.graph_area;

        // Sample the style of the entire widget. This sample will be used to reset the style of
        // the cells that are part of the components put on top of the grah area (i.e legend and
        // axis names).
        let original_style = buf[(area.left(), area.top())].style();

        self.render_x_labels(buf, &layout, chart_area, graph_area);
        self.render_y_labels(buf, &layout, chart_area, graph_area);

        if let Some(y) = layout.axis_x {
            for x in graph_area.left()..graph_area.right() {
                buf[(x, y)]
                    .set_symbol(symbols::line::HORIZONTAL)
                    .set_style(self.x_axis.style);
            }
        }

        if let Some(x) = layout.axis_y {
            for y in graph_area.top()..graph_area.bottom() {
                buf[(x, y)]
                    .set_symbol(symbols::line::VERTICAL)
                    .set_style(self.y_axis.style);
            }
        }

        if let Some(y) = layout.axis_x
            && let Some(x) = layout.axis_y
        {
            buf[(x, y)]
                .set_symbol(symbols::line::BOTTOM_LEFT)
                .set_style(self.x_axis.style);
        }

        Canvas::default()
            .background_color(self.style.bg.unwrap_or(Color::Reset))
            .x_bounds(self.x_axis.bounds)
            .y_bounds(self.y_axis.bounds)
            .paint(|ctx| {
                for dataset in &self.datasets {
                    ctx.marker(dataset.marker);

                    let color = dataset.style.fg.unwrap_or(Color::Reset);
                    ctx.draw(&Points {
                        coords: dataset.data,
                        color,
                    });
                    match dataset.graph_type {
                        GraphType::Line => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&CanvasLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    color,
                                });
                            }
                        }
                        GraphType::Bar => {
                            for (x, y) in dataset.data {
                                ctx.draw(&CanvasLine {
                                    x1: *x,
                                    y1: 0.0,
                                    x2: *x,
                                    y2: *y,
                                    color,
                                });
                            }
                        }
                        GraphType::Area => {
                            for data in dataset.data.windows(2) {
                                ctx.draw(&FilledLine {
                                    x1: data[0].0,
                                    y1: data[0].1,
                                    x2: data[1].0,
                                    y2: data[1].1,
                                    fill_to_y: dataset.fill_to_y,
                                    color,
                                });
                            }
                        }

                        GraphType::Scatter => {}
                    }
                }
            })
            .render(graph_area, buf);

        if let Some(Position { x, y }) = layout.title_x {
            let title = self.x_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(Position { x, y }) = layout.title_y {
            let title = self.y_axis.title.as_ref().unwrap();
            let width = graph_area
                .right()
                .saturating_sub(x)
                .min(title.width() as u16);
            buf.set_style(
                Rect {
                    x,
                    y,
                    width,
                    height: 1,
                },
                original_style,
            );
            buf.set_line(x, y, title, width);
        }

        if let Some(legend_area) = layout.legend_area {
            buf.set_style(legend_area, original_style);
            Block::bordered().render(legend_area, buf);

            for (i, (dataset_name, dataset_style)) in self
                .datasets
                .iter()
                .filter_map(|ds| Some((ds.name.as_ref()?, ds.style())))
                .enumerate()
            {
                let name = dataset_name.clone().patch_style(dataset_style);
                name.render(
                    Rect {
                        x: legend_area.x + 1,
                        y: legend_area.y + 1 + i as u16,
                        width: legend_area.width - 2,
                        height: 1,
                    },
                    buf,
                );
            }
        }
    }
```


#### 📄 檔案: `ratatui-widgets/src/sparkline.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:137, E:402, A:0) ➔ After(N:144, E:419, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 17, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_sparkline_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `render_sparkline_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `ratatui_core::buffer::Cell::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Sparkline::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Sparkline::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Rect::new (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `ratatui_core::buffer::Cell::new (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `render`
  • + [新增呼叫邊] `render_sparkline_outside_buffer_is_noop` ──[CALLS]──> `Sparkline::data`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Sparkline::render()`
- **變更前簽章 (Before)**: `fn Sparkline::render(self, area: Rect, buf: &mut Buffer)` (L390~L394)
- **變更後簽章 (After)**: `fn Sparkline::render(self, area: Rect, buf: &mut Buffer)` (L390~L399)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_sparkline(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_sparkline(inner, buf);
    }
```


---

### 🔹 Commit #02: `5a57af20`
- **完整 Hash**: `5a57af20a2260b31753780d791a6c1b0d56d33eb`
- **說明 (Ground Truth)**: fix(widgets): clip string rendering to buffer (#2815)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-core/src/widgets/widget.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:20, E:30, A:0) ➔ After(N:28, E:45, A:0)
- **差分統計**: +Nodes: 8, -Nodes: 0, +Edges: 17, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_string_widgets_outside_buffer` (FUNCTION_DEF)
  • + [新增節點] `buf.reset (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `self.as_str (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::with_lines (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_string_widgets_clip_to_buffer` (FUNCTION_DEF)
  • + [新增呼叫邊] `str::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `str::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `String::render` ──[CALLS]──> `String::render`
  • + [新增呼叫邊] `String::render` ──[CALLS]──> `self.as_str (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_string_widgets_outside_buffer` ──[CALLS]──> `render`
  • _... 以及其餘 12 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `str::render()`
- **變更前簽章 (Before)**: `fn str::render(self, area: Rect, buf: &mut Buffer)` (L85~L87)
- **變更後簽章 (After)**: `fn str::render(self, area: Rect, buf: &mut Buffer)` (L85~L91)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

### 🔹 函式: `String::render()`
- **變更前簽章 (Before)**: `fn String::render(self, area: Rect, buf: &mut Buffer)` (L95~L97)
- **變更後簽章 (After)**: `fn String::render(self, area: Rect, buf: &mut Buffer)` (L99~L101)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_stringn(area.x, area.y, self, area.width as usize, Style::new());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.as_str().render(area, buf);
    }
```


---

### 🔹 Commit #03: `7125ef2e`
- **完整 Hash**: `7125ef2ec3dbb12d10e12d75c72aee40cf9fecbb`
- **說明 (Ground Truth)**: fix(calendar): respect rendering bounds (#2819)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/calendar.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:111, E:145, A:0) ➔ After(N:121, E:172, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 27, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `days_area.bottom (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_stays_within_requested_rows` (FUNCTION_DEF)
  • + [新增節點] `Date::from_calendar_date(2026, Month::October, 8).expect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_calendar_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增呼叫邊] `Monthly::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Monthly::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `Monthly::render_monthly` ──[CALLS]──> `days_area.bottom (External/Unresolved)`
  • + [新增呼叫邊] `render_calendar_outside_buffer_is_noop` ──[CALLS]──> `Monthly::new`
  • + [新增呼叫邊] `render_calendar_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • _... 以及其餘 22 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Monthly::render_monthly()`
- **變更前簽章 (Before)**: `fn Monthly::render_monthly(&self, area: Rect, buf: &mut Buffer)` (L182~L230)
- **變更後簽章 (After)**: `fn Monthly::render_monthly(&self, area: Rect, buf: &mut Buffer)` (L187~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render_monthly(&self, area: Rect, buf: &mut Buffer) {
        let layout = Layout::vertical([
            Constraint::Length(self.show_month.is_some().into()),
            Constraint::Length(self.show_weekday.is_some().into()),
            Constraint::Fill(1),
        ]);
        let [month_header, days_header, days_area] = layout.areas(area);

        // Draw the month name and year
        if let Some(style) = self.show_month {
            Line::styled(
                format!("{} {}", self.display_date.month(), self.display_date.year()),
                style,
            )
            .alignment(Alignment::Center)
            .render(month_header, buf);
        }

        // Draw days of week
        if let Some(style) = self.show_weekday {
            Span::styled(" Su Mo Tu We Th Fr Sa", style).render(days_header, buf);
        }

        // Set the start of the calendar to the Sunday before the 1st (or the sunday of the first)
        let first_of_month = self.display_date.replace_day(1).unwrap();
        let offset = Duration::days(first_of_month.weekday().number_days_from_sunday().into());
        let mut curr_day = first_of_month - offset;

        let mut y = days_area.y;
        // go through all the weeks containing a day in the target month.
        while curr_day.month() != self.display_date.month().next() {
            let mut spans = Vec::with_capacity(14);
            for i in 0..7 {
                // Draw the gutter. Do it here so we can avoid worrying about
                // styling the ' ' in the format_date method
                if i == 0 {
                    spans.push(Span::styled(" ", Style::default()));
                } else {
                    spans.push(Span::styled(" ", self.default_bg()));
                }
                spans.push(self.format_date(curr_day));
                curr_day += Duration::DAY;
            }
            if buf.area.height > y {
                buf.set_line(days_area.x, y, &spans.into(), area.width);
            }
            y += 1;
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render_monthly(&self, area: Rect, buf: &mut Buffer) {
        let layout = Layout::vertical([
            Constraint::Length(self.show_month.is_some().into()),
            Constraint::Length(self.show_weekday.is_some().into()),
            Constraint::Fill(1),
        ]);
        let [month_header, days_header, days_area] = layout.areas(area);

        // Draw the month name and year
        if let Some(style) = self.show_month {
            Line::styled(
                format!("{} {}", self.display_date.month(), self.display_date.year()),
                style,
            )
            .alignment(Alignment::Center)
            .render(month_header, buf);
        }

        // Draw days of week
        if let Some(style) = self.show_weekday {
            Span::styled(" Su Mo Tu We Th Fr Sa", style).render(days_header, buf);
        }

        // Set the start of the calendar to the Sunday before the 1st (or the sunday of the first)
        let first_of_month = self.display_date.replace_day(1).unwrap();
        let offset = Duration::days(first_of_month.weekday().number_days_from_sunday().into());
        let mut curr_day = first_of_month - offset;

        let mut y = days_area.y;
        // go through all the weeks containing a day in the target month.
        while curr_day.month() != self.display_date.month().next() && y < days_area.bottom() {
            let mut spans = Vec::with_capacity(14);
            for i in 0..7 {
                // Draw the gutter. Do it here so we can avoid worrying about
                // styling the ' ' in the format_date method
                if i == 0 {
                    spans.push(Span::styled(" ", Style::default()));
                } else {
                    spans.push(Span::styled(" ", self.default_bg()));
                }
                spans.push(self.format_date(curr_day));
                curr_day += Duration::DAY;
            }
            buf.set_line(days_area.x, y, &spans.into(), days_area.width);
            y += 1;
        }
    }
```

### 🔹 函式: `Monthly::render()`
- **變更前簽章 (Before)**: `fn Monthly::render(self, area: Rect, buf: &mut Buffer)` (L174~L178)
- **變更後簽章 (After)**: `fn Monthly::render(self, area: Rect, buf: &mut Buffer)` (L174~L183)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_monthly(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_monthly(inner, buf);
    }
```


---

### 🔹 Commit #04: `8685c437`
- **完整 Hash**: `8685c437cd07f2a5decfe9750963e50cda23443c`
- **說明 (Ground Truth)**: fix(tabs): clip rendering to buffer bounds (#2816)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/tabs.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:97, E:203, A:0) ➔ After(N:104, E:217, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 14, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `render_tabs_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `render_tabs_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Tabs::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Tabs::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `new`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `Tabs::render`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `Tabs::new`
  • + [新增呼叫邊] `render_tabs_outside_buffer_is_noop` ──[CALLS]──> `assert_eq! (Macro)`
  • _... 以及其餘 6 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Tabs::render()`
- **變更前簽章 (Before)**: `fn Tabs::render(self, area: Rect, buf: &mut Buffer)` (L376~L381)
- **變更後簽章 (After)**: `fn Tabs::render(self, area: Rect, buf: &mut Buffer)` (L376~L386)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_tabs(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_tabs(inner, buf);
    }
```


---

### 🔹 Commit #05: `d16bdc64`
- **完整 Hash**: `d16bdc64a5a3bc93967d76b8b59624db88026636`
- **說明 (Ground Truth)**: fix(canvas): clip rendering to buffer bounds (#2821)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/canvas.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:108, E:141, A:0) ➔ After(N:114, E:163, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 22, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_canvas_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `render_canvas_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Canvas::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Canvas::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Context::new`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Canvas::render`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Canvas::paint`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Canvas::y_bounds`
  • + [新增呼叫邊] `render_canvas_outside_buffer_is_noop` ──[CALLS]──> `Canvas::x_bounds`
  • _... 以及其餘 13 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Canvas::render()`
- **變更前簽章 (Before)**: `fn Canvas::render(self, area: Rect, buf: &mut Buffer)` (L866~L935)
- **變更後簽章 (After)**: `fn Canvas::render(self, area: Rect, buf: &mut Buffer)` (L866~L940)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        self.block.as_ref().render(area, buf);
        let canvas_area = self.block.inner_if_some(area);
        if canvas_area.is_empty() {
            return;
        }

        buf.set_style(canvas_area, Style::default().bg(self.background_color));

        let width = canvas_area.width as usize;

        let Some(ref painter) = self.paint_func else {
            return;
        };

        // Create a blank context that match the size of the canvas
        let mut ctx = Context::new(
            canvas_area.width,
            canvas_area.height,
            self.x_bounds,
            self.y_bounds,
            self.marker,
        );
        // Paint to this context
        painter(&mut ctx);
        ctx.finish();

        // Retrieve painted points for each layer
        for layer in ctx.layers {
            for (index, layer_cell) in layer.contents.iter().enumerate() {
                let (x, y) = (
                    (index % width) as u16 + canvas_area.left(),
                    (index / width) as u16 + canvas_area.top(),
                );
                let cell = &mut buf[(x, y)];

                if let Some(symbol) = layer_cell.symbol {
                    cell.set_char(symbol);
                }
                if let Some(fg) = layer_cell.fg {
                    cell.set_fg(fg);
                }
                if let Some(bg) = layer_cell.bg {
                    cell.set_bg(bg);
                }
            }
        }

        // Finally draw the labels
        let left = self.x_bounds[0];
        let right = self.x_bounds[1];
        let top = self.y_bounds[1];
        let bottom = self.y_bounds[0];
        let width = (self.x_bounds[1] - self.x_bounds[0]).abs();
        let height = (self.y_bounds[1] - self.y_bounds[0]).abs();
        let resolution = {
            let width = f64::from(canvas_area.width - 1);
            let height = f64::from(canvas_area.height - 1);
            (width, height)
        };
        for label in ctx
            .labels
            .iter()
            .filter(|l| l.x >= left && l.x <= right && l.y <= top && l.y >= bottom)
        {
            let x = ((label.x - left) * resolution.0 / width) as u16 + canvas_area.left();
            let y = ((top - label.y) * resolution.1 / height) as u16 + canvas_area.top();
            buf.set_line(x, y, &label.line, canvas_area.right() - x);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        self.block.as_ref().render(area, buf);
        let canvas_area = self.block.inner_if_some(area);
        if canvas_area.is_empty() {
            return;
        }

        buf.set_style(canvas_area, Style::default().bg(self.background_color));

        let width = canvas_area.width as usize;

        let Some(ref painter) = self.paint_func else {
            return;
        };

        // Create a blank context that match the size of the canvas
        let mut ctx = Context::new(
            canvas_area.width,
            canvas_area.height,
            self.x_bounds,
            self.y_bounds,
            self.marker,
        );
        // Paint to this context
        painter(&mut ctx);
        ctx.finish();

        // Retrieve painted points for each layer
        for layer in ctx.layers {
            for (index, layer_cell) in layer.contents.iter().enumerate() {
                let (x, y) = (
                    (index % width) as u16 + canvas_area.left(),
                    (index / width) as u16 + canvas_area.top(),
                );
                let cell = &mut buf[(x, y)];

                if let Some(symbol) = layer_cell.symbol {
                    cell.set_char(symbol);
                }
                if let Some(fg) = layer_cell.fg {
                    cell.set_fg(fg);
                }
                if let Some(bg) = layer_cell.bg {
                    cell.set_bg(bg);
                }
            }
        }

        // Finally draw the labels
        let left = self.x_bounds[0];
        let right = self.x_bounds[1];
        let top = self.y_bounds[1];
        let bottom = self.y_bounds[0];
        let width = (self.x_bounds[1] - self.x_bounds[0]).abs();
        let height = (self.y_bounds[1] - self.y_bounds[0]).abs();
        let resolution = {
            let width = f64::from(canvas_area.width - 1);
            let height = f64::from(canvas_area.height - 1);
            (width, height)
        };
        for label in ctx
            .labels
            .iter()
            .filter(|l| l.x >= left && l.x <= right && l.y <= top && l.y >= bottom)
        {
            let x = ((label.x - left) * resolution.0 / width) as u16 + canvas_area.left();
            let y = ((top - label.y) * resolution.1 / height) as u16 + canvas_area.top();
            buf.set_line(x, y, &label.line, canvas_area.right() - x);
        }
    }
```


---

### 🔹 Commit #06: `2bcbd749`
- **完整 Hash**: `2bcbd749190a8b5e80405edaefdc34f407a6ca3a`
- **說明 (Ground Truth)**: fix(scrollbar): clip rendering to buffer bounds (#2818)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/scrollbar.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:120, E:292, A:0) ➔ After(N:127, E:309, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 17, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_scrollbar_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `orientation.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_scrollbar_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `Scrollbar::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Scrollbar::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `ScrollbarState::new`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `buf.clone (External/Unresolved)`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `ScrollbarState::position`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `Scrollbar::render`
  • + [新增呼叫邊] `render_scrollbar_outside_buffer_is_noop` ──[CALLS]──> `Scrollbar::new`
  • _... 以及其餘 9 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Scrollbar::render()`
- **變更前簽章 (Before)**: `fn Scrollbar::render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State)` (L526~L540)
- **變更後簽章 (After)**: `fn Scrollbar::render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State)` (L526~L545)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State) {
        if state.content_length == 0 || self.track_length_excluding_arrow_heads(area) == 0 {
            return;
        }

        if let Some(area) = self.scrollbar_area(area) {
            let areas = area.columns().flat_map(Rect::rows);
            let bar_symbols = self.bar_symbols(area, state);
            for (area, bar) in areas.zip(bar_symbols) {
                if let Some((symbol, style)) = bar {
                    buf.set_string(area.x, area.y, symbol, style);
                }
            }
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        if state.content_length == 0 || self.track_length_excluding_arrow_heads(area) == 0 {
            return;
        }

        if let Some(area) = self.scrollbar_area(area) {
            let areas = area.columns().flat_map(Rect::rows);
            let bar_symbols = self.bar_symbols(area, state);
            for (area, bar) in areas.zip(bar_symbols) {
                if let Some((symbol, style)) = bar {
                    buf.set_string(area.x, area.y, symbol, style);
                }
            }
        }
    }
```


---

### 🔹 Commit #07: `3c49d36f`
- **完整 Hash**: `3c49d36f46fd64c2fe12eed5d51bf029cc339865`
- **說明 (Ground Truth)**: fix(gauge): clip rendering to buffer bounds (#2820)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/gauge.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:87, E:112, A:0) ➔ After(N:97, E:150, A:0)
- **差分統計**: +Nodes: 10, -Nodes: 0, +Edges: 38, -Edges: 0, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `area.intersection (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_gauge_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert_ne! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `render_gauge_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `buf.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `area.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `render_line_gauge_clips_to_offset_buffer` (FUNCTION_DEF)
  • + [新增節點] `render_line_gauge_outside_buffer_is_noop` (FUNCTION_DEF)
  • + [新增節點] `ratatui_core::buffer::Cell::new (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Gauge::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `Gauge::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `LineGauge::render` ──[CALLS]──> `area.intersection (External/Unresolved)`
  • + [新增呼叫邊] `LineGauge::render` ──[CALLS]──> `area.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `render_gauge_outside_buffer_is_noop` ──[CALLS]──> `Rect::new (External/Unresolved)`
  • _... 以及其餘 33 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `LineGauge::render()`
- **變更前簽章 (Before)**: `fn LineGauge::render(self, area: Rect, buf: &mut Buffer)` (L425~L454)
- **變更後簽章 (After)**: `fn LineGauge::render(self, area: Rect, buf: &mut Buffer)` (L430~L464)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let gauge_area = self.block.inner_if_some(area);
        if gauge_area.is_empty() {
            return;
        }

        let ratio = self.ratio;
        let default_label = Line::from(format!("{:3.0}%", ratio * 100.0));
        let label = self.label.as_ref().unwrap_or(&default_label);
        let (col, row) = buf.set_line(gauge_area.left(), gauge_area.top(), label, gauge_area.width);
        let start = col + 1;
        if start >= gauge_area.right() {
            return;
        }

        let end = start
            + (f64::from(gauge_area.right().saturating_sub(start)) * self.ratio).floor() as u16;
        for col in start..end {
            buf[(col, row)]
                .set_symbol(self.filled_symbol)
                .set_style(self.filled_style);
        }
        for col in end..gauge_area.right() {
            buf[(col, row)]
                .set_symbol(self.unfilled_symbol)
                .set_style(self.unfilled_style);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let gauge_area = self.block.inner_if_some(area);
        if gauge_area.is_empty() {
            return;
        }

        let ratio = self.ratio;
        let default_label = Line::from(format!("{:3.0}%", ratio * 100.0));
        let label = self.label.as_ref().unwrap_or(&default_label);
        let (col, row) = buf.set_line(gauge_area.left(), gauge_area.top(), label, gauge_area.width);
        let start = col + 1;
        if start >= gauge_area.right() {
            return;
        }

        let end = start
            + (f64::from(gauge_area.right().saturating_sub(start)) * self.ratio).floor() as u16;
        for col in start..end {
            buf[(col, row)]
                .set_symbol(self.filled_symbol)
                .set_style(self.filled_style);
        }
        for col in end..gauge_area.right() {
            buf[(col, row)]
                .set_symbol(self.unfilled_symbol)
                .set_style(self.unfilled_style);
        }
    }
```

### 🔹 函式: `Gauge::render()`
- **變更前簽章 (Before)**: `fn Gauge::render(self, area: Rect, buf: &mut Buffer)` (L161~L166)
- **變更後簽章 (After)**: `fn Gauge::render(self, area: Rect, buf: &mut Buffer)` (L161~L171)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_gauge(inner, buf);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(buf.area);
        if area.is_empty() {
            return;
        }

        buf.set_style(area, self.style);
        self.block.as_ref().render(area, buf);
        let inner = self.block.inner_if_some(area);
        self.render_gauge(inner, buf);
    }
```


---

### 🔹 Commit #08: `91dc40fa`
- **完整 Hash**: `91dc40fae41d802a9683f799eae81ac4f43df313`
- **說明 (Ground Truth)**: fix(widgets): forward portable-atomic feature to ratatui-widgets (#2822)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/block/shadow.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:52, E:73, A:0) ➔ After(N:53, E:74, A:0)
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
  • + [新增節點] `Arc::from (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Shadow::custom` ──[CALLS]──> `Arc::from (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Shadow::custom()`
- **變更前簽章 (Before)**: `fn Shadow::custom(effect: F)` (L251~L257)
- **變更後簽章 (After)**: `fn Shadow::custom(effect: F)` (L256~L268)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn custom<F: CellEffect + 'static>(effect: F) -> Self {
        Self {
            effect: Effect::Custom(Arc::new(effect)),
            style: Style::default(),
            offset: Offset::new(1, 1),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn custom<F: CellEffect + 'static>(effect: F) -> Self {
        #[cfg(not(feature = "portable-atomic"))]
        let effect: Arc<dyn CellEffect> = Arc::new(effect);
        // portable-atomic's Arc does not implement CoerceUnsized on stable Rust, so erase the
        // concrete type through a Box first.
        #[cfg(feature = "portable-atomic")]
        let effect: Arc<dyn CellEffect> = Arc::from(Box::new(effect) as Box<dyn CellEffect>);
        Self {
            effect: Effect::Custom(effect),
            style: Style::default(),
            offset: Offset::new(1, 1),
        }
    }
```


---

### 🔹 Commit #09: `ad2e79e6`
- **完整 Hash**: `ad2e79e6b80311c094ad99146525537eb7789fc7`
- **說明 (Ground Truth)**: fix(rect): empty Rect never intersects (#2766)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-core/src/layout/rect.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:134, E:171, A:0) ➔ After(N:136, E:174, A:0)
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
  • + [新增節點] `intersects_empty` (FUNCTION_DEF)
  • + [新增節點] `intersects_single_cell` (FUNCTION_DEF)
  • + [新增呼叫邊] `Rect::intersects` ──[CALLS]──> `Rect::is_empty`
  • + [新增呼叫邊] `intersects_empty` ──[CALLS]──> `assert! (Macro)`
  • + [新增呼叫邊] `intersects_single_cell` ──[CALLS]──> `assert! (Macro)`

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Rect::intersects()`
- **變更前簽章 (Before)**: `fn Rect::intersects(self, other: Self)` (L336~L341)
- **變更後簽章 (After)**: `fn Rect::intersects(self, other: Self)` (L339~L346)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub const fn intersects(self, other: Self) -> bool {
        self.x < other.right()
            && self.right() > other.x
            && self.y < other.bottom()
            && self.bottom() > other.y
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub const fn intersects(self, other: Self) -> bool {
        !self.is_empty()
            && !other.is_empty()
            && self.x < other.right()
            && self.right() > other.x
            && self.y < other.bottom()
            && self.bottom() > other.y
    }
```


---

### 🔹 Commit #10: `a1a90d9d`
- **完整 Hash**: `a1a90d9d7efe2802ddbd324d34f4cd9108ad8cc9`
- **說明 (Ground Truth)**: fix(fill): reject empty symbols (#2736)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/fill.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:31, E:53, A:0) ➔ After(N:38, E:65, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 12, -Edges: 0, ΔFuncs: 3, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `self.symbol.is_empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Fill::default()
            .red (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `assert! (Macro)` (FUNCTION_DEF)
  • + [新增節點] `new_panics_on_empty_symbol` (FUNCTION_DEF)
  • + [新增節點] `symbol_panics_on_empty_symbol` (FUNCTION_DEF)
  • + [新增節點] `Fill::default (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `default_is_noop` (FUNCTION_DEF)
  • + [新增呼叫邊] `Fill::new` ──[CALLS]──> `assert! (Macro)`
  • + [新增呼叫邊] `Fill::symbol` ──[CALLS]──> `assert! (Macro)`
  • + [新增呼叫邊] `Fill::render` ──[CALLS]──> `self.symbol.is_empty (External/Unresolved)`
  • + [新增呼叫邊] `new_panics_on_empty_symbol` ──[CALLS]──> `Fill::new`
  • + [新增呼叫邊] `symbol_panics_on_empty_symbol` ──[CALLS]──> `Fill::symbol`
  • + [新增呼叫邊] `symbol_panics_on_empty_symbol` ──[CALLS]──> `Fill::new`
  • + [新增呼叫邊] `default_is_noop` ──[CALLS]──> `Buffer::with_lines (External/Unresolved)`
  • + [新增呼叫邊] `default_is_noop` ──[CALLS]──> `Fill::render`
  • _... 以及其餘 4 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Fill::symbol()`
- **變更前簽章 (Before)**: `fn Fill::symbol(mut self, symbol: S)` (L87~L90)
- **變更後簽章 (After)**: `fn Fill::symbol(mut self, symbol: S)` (L97~L102)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn symbol<S: Into<Cow<'a, str>>>(mut self, symbol: S) -> Self {
        self.symbol = symbol.into();
        self
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn symbol<S: Into<Cow<'a, str>>>(mut self, symbol: S) -> Self {
        let symbol = symbol.into();
        assert!(!symbol.is_empty(), "Fill symbol must not be empty");
        self.symbol = symbol;
        self
    }
```

### 🔹 函式: `Fill::new()`
- **變更前簽章 (Before)**: `fn Fill::new(symbol: S)` (L63~L68)
- **變更後簽章 (After)**: `fn Fill::new(symbol: S)` (L67~L74)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn new<S: Into<Cow<'a, str>>>(symbol: S) -> Self {
        Self {
            symbol: symbol.into(),
            style: Style::default(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn new<S: Into<Cow<'a, str>>>(symbol: S) -> Self {
        let symbol = symbol.into();
        assert!(!symbol.is_empty(), "Fill symbol must not be empty");
        Self {
            symbol,
            style: Style::default(),
        }
    }
```

### 🔹 函式: `Fill::render()`
- **變更前簽章 (Before)**: `fn Fill::render(self, area: Rect, buf: &mut Buffer)` (L100~L108)
- **變更後簽章 (After)**: `fn Fill::render(self, area: Rect, buf: &mut Buffer)` (L112~L120)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(*buf.area());
        if area.is_empty() {
            return;
        }
        for position in area.positions() {
            buf[position].set_symbol(&self.symbol).set_style(self.style);
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render(self, area: Rect, buf: &mut Buffer) {
        let area = area.intersection(*buf.area());
        if area.is_empty() || self.symbol.is_empty() {
            return;
        }
        for position in area.positions() {
            buf[position].set_symbol(&self.symbol).set_style(self.style);
        }
    }
```


---

### 🔹 Commit #11: `b45e20c1`
- **完整 Hash**: `b45e20c16291a9369affb7d963cda7f2ed97d701`
- **說明 (Ground Truth)**: fix(terminal)!: don't clear the whole screen when an inline viewport shrinks horizontally (#2670)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-core/src/terminal/resize.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:81, E:152, A:0) ➔ After(N:93, E:174, A:0)
- **差分統計**: +Nodes: 13, -Nodes: 1, +Edges: 38, -Edges: 16, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `terminal
                .insert_before(1, |buf| {
                    buf.set_string(0, 0, text, Style::default());
                })
                .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buf.set_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal
            .backend_mut()
            .set_cursor_position(Position { x: 4, y: 2 })
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Terminal::with_options(
            backend,
            TerminalOptions {
                viewport: Viewport::Inline(1),
            },
        )
        .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal
            .draw(|frame| {
                let area = frame.area();
                frame
                    .buffer_mut()
                    .set_string(area.x, area.y, "live", Style::default());
            })
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal.resize(Rect::new(0, 0, 5, 4)).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `frame.area (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `frame
                    .buffer_mut()
                    .set_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal
                .insert_before (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Style::default (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `frame
                    .buffer_mut (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `resize_inline_horizontal_shrink_keeps_rows_above_the_viewport` (FUNCTION_DEF)
  • + [新增節點] `resize_inline_resets_the_buffers_on_horizontal_shrink` (FUNCTION_DEF)
  • - [移除節點] `resize_inline_clears_screen_on_horizontal_shrink` (FUNCTION_DEF)
  • + [新增呼叫邊] `resize_inline_horizontal_shrink_keeps_rows_above_the_viewport` ──[CALLS]──> `TestBackend::new (External/Unresolved)`
  • _... 以及其餘 53 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Terminal::resize()`
- **變更前簽章 (Before)**: `fn Terminal::resize(&mut self, area: Rect)` (L23~L58)
- **變更後簽章 (After)**: `fn Terminal::resize(&mut self, area: Rect)` (L23~L71)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn resize(&mut self, area: Rect) -> Result<(), B::Error> {
        let (mut next_area, cursor_to_restore) = match self.viewport {
            Viewport::Inline(height) => {
                let offset_in_previous_viewport = self
                    .last_known_cursor_pos
                    .y
                    .saturating_sub(self.viewport_area.top());
                let (next_area, cursor_position) = compute_inline_size(
                    &mut self.backend,
                    height,
                    area.as_size(),
                    offset_in_previous_viewport,
                )?;
                (next_area, Some(cursor_position))
            }
            Viewport::Fixed(_) | Viewport::Fullscreen => (area, None),
        };

        // clear screen on horizontal shrink to avoid line wrapping issues
        if next_area.width < self.viewport_area.width {
            next_area.y = 0;
            // `clear_viewport` below already clears everything for `Fullscreen`.
            if !matches!(self.viewport, Viewport::Fullscreen) {
                self.backend.clear_region(ClearType::All)?;
            }
        }

        self.set_viewport_area(next_area);
        self.clear_viewport()?;
        if let Some(cursor_position) = cursor_to_restore {
            self.backend.set_cursor_position(cursor_position)?;
        }

        self.last_known_area = area;
        Ok(())
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn resize(&mut self, area: Rect) -> Result<(), B::Error> {
        let (mut next_area, cursor_to_restore) = match self.viewport {
            Viewport::Inline(height) => {
                let offset_in_previous_viewport = self
                    .last_known_cursor_pos
                    .y
                    .saturating_sub(self.viewport_area.top());
                let (next_area, cursor_position) = compute_inline_size(
                    &mut self.backend,
                    height,
                    area.as_size(),
                    offset_in_previous_viewport,
                )?;
                (next_area, Some(cursor_position))
            }
            Viewport::Fixed(_) | Viewport::Fullscreen => (area, None),
        };

        // Clear the screen on horizontal shrink to avoid line wrapping issues.
        //
        // Inline viewports are excluded: an inline viewport only owns the rows
        // from its origin down. The rows above it were written by
        // `insert_before`, which keeps no copy of them, so the application can
        // never repaint them. A full-screen erase either destroys that output
        // or, on terminals that move erased content into scrollback (Windows
        // Terminal, conhost), pushes a copy of the viewport into scrollback on
        // every resize event. The `clear_viewport` call below already erases
        // from the recomputed origin to the bottom of the screen, which covers
        // every row the inline viewport can legitimately own.
        if next_area.width < self.viewport_area.width {
            match self.viewport {
                Viewport::Inline(_) => {}
                Viewport::Fullscreen => next_area.y = 0,
                Viewport::Fixed(_) => {
                    next_area.y = 0;
                    self.backend.clear_region(ClearType::All)?;
                }
            }
        }

        self.set_viewport_area(next_area);
        self.clear_viewport()?;
        if let Some(cursor_position) = cursor_to_restore {
            self.backend.set_cursor_position(cursor_position)?;
        }

        self.last_known_area = area;
        Ok(())
    }
```


---

### 🔹 Commit #12: `67019321`
- **完整 Hash**: `67019321ab6aa49896708e203d6723dc592c0cdd`
- **說明 (Ground Truth)**: fix(core): prevent rendering artifacts around VS16 graphemes (#2686)
- **變更檔案數**: 4

#### 📄 檔案: `ratatui-core/src/buffer/diff.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:92, E:193, A:0) ➔ After(N:125, E:241, A:0)
- **差分統計**: +Nodes: 36, -Nodes: 3, +Edges: 51, -Edges: 3, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `assert_no_artifacts_for_both_widths` (FUNCTION_DEF)
  • + [新增節點] `(!uncertain_width).then_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `(i + reserved).min (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `columns
                .iter_mut()
                .enumerate (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buf.set_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.cell_width (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `buf.content[c].symbol (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Self::Glyph (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `expected_columns` (FUNCTION_DEF)
  • + [新增節點] `shifted_vs16_row_does_not_drift` (FUNCTION_DEF)
  • + [新增節點] `(cell.cell_width() as usize).max (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `VS16_WIDTHS` (MODULE_STATE)
  • + [新增節點] `has_uncertain_width` (FUNCTION_DEF)
  • + [新增節點] `contains_vs16` (FUNCTION_DEF)
  • + [新增節點] `self.columns[col + 1..end].fill (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 78 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BufferDiff::next()`
- **變更前簽章 (Before)**: `fn BufferDiff::next(&mut self)` (L94~L224)
- **變更後簽章 (After)**: `fn BufferDiff::next(&mut self)` (L90~L213)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn next(&mut self) -> Option<Self::Item> {
        let len = self.next.len().min(self.prev.len());

        // First, yield any pending trailing cells.
        if let Some(TrailingState {
            next_index,
            end,
            force,
            deferred,
        }) = &mut self.trailing
        {
            while *next_index < *end {
                let j = *next_index;
                // Advance past this cell; if it is wide, also skip its own trailing column
                // so the main loop does not emit a spurious EMPTY write over it.
                let cell_width = self.next[j].cell_width().max(1) as usize;
                *next_index += cell_width;
                *end = (*end).max(*next_index).min(len);

                if !is_skip(&self.next[j])
                    && (*force || self.prev[j].symbol() != self.next[j].symbol())
                {
                    let (tx, ty) = self.pos_of(j);
                    return Some((tx, ty, &self.next[j]));
                }
            }

            // Done with trailing cells; resume past the wide character, repainting its leading
            // cell first when the trailing cells were a pre-clear.
            self.pos = *end;
            let deferred = deferred.take();
            self.trailing = None;
            if let Some(i) = deferred {
                let (x, y) = self.pos_of(i);
                return Some((x, y, &self.next[i]));
            }
        }
        while self.pos < len {
            let i = self.pos;
            self.pos += 1;

            let current = &self.next[i];
            let previous = &self.prev[i];

            match current.diff_option {
                CellDiffOption::Skip => {}
                _ if is_skip(current) => {}

                CellDiffOption::ForcedWidth(width) => {
                    self.pos = self
                        .pos
                        .saturating_add(width.get().saturating_sub(1) as usize);
                    if current != previous {
                        let (x, y) = self.pos_of(i);
                        return Some((x, y, &self.next[i]));
                    }
                }
                CellDiffOption::None | CellDiffOption::AlwaysUpdate => {
                    // If the current cell is multi-width, ensure the trailing cells are
                    // explicitly cleared when they previously contained non-blank content.
                    // Some terminals do not reliably clear the trailing cell(s) when printing
                    // a wide grapheme, which can result in visual artifacts (e.g., leftover
                    // characters). Emitting an explicit update for the trailing cells avoids
                    // this.
                    let cell_width = current.cell_width() as usize;
                    if matches!(current.diff_option, CellDiffOption::None) && current == previous {
                        // Equal cells still need to account for multi-width skip.
                        self.pos += cell_width.saturating_sub(1);
                        continue;
                    }

                    let previous_width = previous.cell_width() as usize;
                    let previous_style_is_visible_on_blank = previous.bg != Color::Reset
                        || previous.modifier.intersects(VISIBLE_ON_BLANK);

                    // Clear stale styles from an unchanged wide glyph's trailing cells before
                    // repainting it.
                    if cell_width > 1
                        && current.symbol() == previous.symbol()
                        && current.style() != previous.style()
                        && previous_style_is_visible_on_blank
                    {
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + cell_width).min(len),
                            force: true,
                            deferred: Some(i),
                        });
                        return self.next();
                    }

                    // Work around terminals that fail to clear the trailing cell of certain
                    // emoji presentation sequences (those containing VS16 / U+FE0F).
                    // Only emit explicit clears for such sequences to avoid bloating diffs
                    // for standard wide characters (e.g., CJK), which terminals handle well.
                    let contains_vs16 =
                        cell_width > 1 && current.symbol().chars().any(|c| c == '\u{FE0F}');

                    if contains_vs16 {
                        let trailing_end = (i + cell_width).min(len);
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: trailing_end,
                            force: false,
                            deferred: None,
                        });
                    } else if cell_width > 1 {
                        self.pos += cell_width.saturating_sub(1);
                    } else if previous_width > cell_width && previous_style_is_visible_on_blank {
                        // The previous wide character's style is visible on blank cells, so the
                        // terminal may still show it on the trailing columns even after the
                        // character is replaced. Force-emit every cell in the trailing range to
                        // refresh the terminal regardless of whether the buffer content changed.
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + previous_width).min(len),
                            force: true,
                            deferred: None,
                        });
                    } else {
                        // single-width character, no position adjustment needed
                    }

                    let (x, y) = self.pos_of(i);
                    return Some((x, y, &self.next[i]));
                }
            }
        }

        None
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn next(&mut self) -> Option<Self::Item> {
        let len = self.next.len().min(self.prev.len());

        // First, yield any pending trailing cells.
        if let Some(TrailingState {
            next_index,
            end,
            force,
            deferred_leading_cell,
        }) = &mut self.trailing
        {
            while *next_index < *end {
                let j = *next_index;
                // Advance past this cell; if it is wide, also skip its own trailing column
                // so the main loop does not emit a spurious EMPTY write over it.
                let cell_width = self.next[j].cell_width().max(1) as usize;
                *next_index += cell_width;
                *end = (*end).max(*next_index).min(len);

                if !is_skip(&self.next[j])
                    && (*force || self.prev[j].symbol() != self.next[j].symbol())
                {
                    let (tx, ty) = self.pos_of(j);
                    return Some((tx, ty, &self.next[j]));
                }
            }

            // Resume after the wide glyph, repainting its deferred leading cell first.
            self.pos = *end;
            let deferred_leading_cell = deferred_leading_cell.take();
            self.trailing = None;
            if let Some(i) = deferred_leading_cell {
                let (x, y) = self.pos_of(i);
                return Some((x, y, &self.next[i]));
            }
        }
        while self.pos < len {
            let i = self.pos;
            self.pos += 1;

            let current = &self.next[i];
            let previous = &self.prev[i];

            match current.diff_option {
                CellDiffOption::Skip => {}
                _ if is_skip(current) => {}

                CellDiffOption::ForcedWidth(width) => {
                    self.pos = self
                        .pos
                        .saturating_add(width.get().saturating_sub(1) as usize);
                    if current != previous {
                        let (x, y) = self.pos_of(i);
                        return Some((x, y, &self.next[i]));
                    }
                }
                CellDiffOption::None | CellDiffOption::AlwaysUpdate => {
                    let cell_width = current.cell_width() as usize;
                    if matches!(current.diff_option, CellDiffOption::None) && current == previous {
                        // Equal cells still need to account for multi-width skip.
                        self.pos += cell_width.saturating_sub(1);
                        continue;
                    }

                    let previous_width = previous.cell_width() as usize;
                    let previous_style_is_visible_on_blank = previous.bg != Color::Reset
                        || previous.modifier.intersects(VISIBLE_ON_BLANK);

                    // Clear stale styles from an unchanged wide glyph's trailing cells before
                    // repainting it.
                    if cell_width > 1
                        && current.symbol() == previous.symbol()
                        && current.style() != previous.style()
                        && previous_style_is_visible_on_blank
                    {
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + cell_width).min(len),
                            force: true,
                            deferred_leading_cell: Some(i),
                        });
                        return self.next();
                    }

                    // Clear reserved columns first so they cannot overwrite the uncertain-width
                    // glyph.
                    let uncertain_width = cell_width > 1 && has_uncertain_width(current.symbol());

                    if uncertain_width {
                        let trailing_end = (i + cell_width).min(len);
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: trailing_end,
                            force: false,
                            deferred_leading_cell: Some(i),
                        });
                        // Recurses once and returns the deferred leading cell.
                        return self.next();
                    } else if cell_width > 1 {
                        self.pos += cell_width.saturating_sub(1);
                    } else if previous_width > cell_width && previous_style_is_visible_on_blank {
                        // The previous wide character's style is visible on blank cells, so the
                        // terminal may still show it on the trailing columns even after the
                        // character is replaced. Force-emit every cell in the trailing range to
                        // refresh the terminal regardless of whether the buffer content changed.
                        // This cell is narrow, so those columns stay adjacent and need no move.
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + previous_width).min(len),
                            force: true,
                            deferred_leading_cell: None,
                        });
                    } else {
                        // single-width character, no position adjustment needed
                    }

                    let (x, y) = self.pos_of(i);
                    return Some((x, y, &self.next[i]));
                }
            }
        }

        None
    }
```


#### 📄 檔案: `ratatui-crossterm/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:111, E:150, A:0) ➔ After(N:115, E:153, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 4, -Edges: 1, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `(!uncertain_width).then_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars().any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `CrosstermBackend::draw` ──[CALLS]──> `cell.symbol().chars().any (External/Unresolved)`
  • + [新增呼叫邊] `CrosstermBackend::draw` ──[CALLS]──> `cell.symbol().chars (External/Unresolved)`
  • + [新增呼叫邊] `CrosstermBackend::draw` ──[CALLS]──> `cell.symbol (External/Unresolved)`
  • + [新增呼叫邊] `CrosstermBackend::draw` ──[CALLS]──> `(!uncertain_width).then_some (External/Unresolved)`
  • - [移除呼叫邊] `CrosstermBackend::draw` ──[CALLS]──> `Some (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `CrosstermBackend::draw()`
- **變更前簽章 (Before)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L294)
- **變更後簽章 (After)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L297)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            let width = cell.cell_width();
            // A VS16 cluster's terminal cursor advance is not reliably predictable.
            let uncertain_width = width > 1 && cell.symbol().chars().any(|c| c == '\u{FE0F}');
            last = (!uncertain_width).then_some((Position { x, y }, width));
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```

### 🔹 函式: `draw_moves_cursor_after_wide_symbol_from_buffer_diff()`
- **變更前簽章 (Before)**: `fn draw_moves_cursor_after_wide_symbol_from_buffer_diff()` (L870~L888)
- **變更後簽章 (After)**: `fn draw_moves_cursor_after_wide_symbol_from_buffer_diff()` (L873~L892)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw_moves_cursor_after_wide_symbol_from_buffer_diff() {
        // End-to-end version of the report in #2651: the diff emits the trailing cell of a
        // VS16 emoji sequence on purpose, and the backend must reposition before writing it.
        let area = Rect::new(0, 0, 4, 1);
        let mut prev = Buffer::empty(area);
        prev.set_string(0, 0, "aaaa", Style::default());
        let mut next = Buffer::empty(area);
        next.set_string(0, 0, "\u{2764}\u{FE0F}bc", Style::default());

        let updates: Vec<_> = prev.diff(&next).into_iter().collect();
        assert_eq!(
            updates.iter().map(|(x, _, _)| *x).collect::<Vec<_>>(),
            [0, 1, 2, 3]
        );
        let output = draw_to_string(&updates);
        assert!(output.contains(&MoveTo(1, 0).to_string()));
        assert!(!output.contains(&MoveTo(2, 0).to_string()));
        assert!(!output.contains(&MoveTo(3, 0).to_string()));
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw_moves_cursor_after_wide_symbol_from_buffer_diff() {
        // End-to-end version of the report in #2651: the diff emits the trailing cell of a
        // VS16 emoji sequence on purpose, and the backend must reposition before writing it.
        let area = Rect::new(0, 0, 4, 1);
        let mut prev = Buffer::empty(area);
        prev.set_string(0, 0, "aaaa", Style::default());
        let mut next = Buffer::empty(area);
        next.set_string(0, 0, "\u{2764}\u{FE0F}bc", Style::default());

        let updates: Vec<_> = prev.diff(&next).into_iter().collect();
        assert_eq!(
            updates.iter().map(|(x, _, _)| *x).collect::<Vec<_>>(),
            [1, 0, 2, 3]
        );
        let output = draw_to_string(&updates);
        assert!(output.contains(&MoveTo(1, 0).to_string()));
        assert!(output.contains(&MoveTo(0, 0).to_string()));
        assert!(output.contains(&MoveTo(2, 0).to_string()));
        assert!(!output.contains(&MoveTo(3, 0).to_string()));
    }
```


#### 📄 檔案: `ratatui-termina/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:172, E:278, A:0) ➔ After(N:176, E:291, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 13, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `(!uncertain_width).then_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars().any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `moves_cursor_after_uncertain_width_symbol` (FUNCTION_DEF)
  • + [新增呼叫邊] `TerminaBackend::draw` ──[CALLS]──> `cell.symbol().chars().any (External/Unresolved)`
  • + [新增呼叫邊] `TerminaBackend::draw` ──[CALLS]──> `cell.symbol().chars (External/Unresolved)`
  • + [新增呼叫邊] `TerminaBackend::draw` ──[CALLS]──> `(!uncertain_width).then_some (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `backend`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `MockTerminal::new`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `backend.draw(content.into_iter()).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `TerminaBackend::draw`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `content.into_iter (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `MockTerminal::output`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `Csi::Cursor (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `cursor_position(Position::new(2, 0)).unwrap (External/Unresolved)`
  • _... 以及其餘 2 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TerminaBackend::draw()`
- **變更前簽章 (Before)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L190)
- **變更後簽章 (After)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L193)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            let width = cell.cell_width();
            // A VS16 cluster's terminal cursor advance is not reliably predictable.
            let uncertain_width = width > 1 && cell.symbol().chars().any(|c| c == '\u{FE0F}');
            last = (!uncertain_width).then_some((Position { x, y }, width));

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```


#### 📄 檔案: `ratatui-termion/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:127, E:143, A:0) ➔ After(N:130, E:148, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 1, +Edges: 6, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `(!uncertain_width).then_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_moves_cursor_after_uncertain_width_symbol` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars().any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.symbol().chars (External/Unresolved)` (FUNCTION_DEF)
  • - [移除節點] `Some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TermionBackend::draw` ──[CALLS]──> `cell.symbol().chars().any (External/Unresolved)`
  • + [新增呼叫邊] `TermionBackend::draw` ──[CALLS]──> `cell.symbol().chars (External/Unresolved)`
  • + [新增呼叫邊] `TermionBackend::draw` ──[CALLS]──> `(!uncertain_width).then_some (External/Unresolved)`
  • + [新增呼叫邊] `draw_moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `TermionBackend::new`
  • + [新增呼叫邊] `draw_moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `draw_to_string`
  • + [新增呼叫邊] `draw_moves_cursor_after_uncertain_width_symbol` ──[CALLS]──> `assert! (Macro)`
  • - [移除呼叫邊] `TermionBackend::draw` ──[CALLS]──> `Some (External/Unresolved)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TermionBackend::draw()`
- **變更前簽章 (Before)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L270)
- **變更後簽章 (After)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L273)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            let width = cell.cell_width();
            // A VS16 cluster's terminal cursor advance is not reliably predictable.
            let uncertain_width = width > 1 && cell.symbol().chars().any(|c| c == '\u{FE0F}');
            last = (!uncertain_width).then_some((Position { x, y }, width));
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```


---

### 🔹 Commit #13: `7babd829`
- **完整 Hash**: `7babd829c8552a92512762a07986e14b53648eb9`
- **說明 (Ground Truth)**: fix(buffer): clear trailing cells before wide glyph repaint (#2743)
- **變更檔案數**: 2

#### 📄 檔案: `ratatui-core/src/buffer/diff.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:85, E:166, A:0) ➔ After(N:92, E:193, A:0)
- **差分統計**: +Nodes: 7, -Nodes: 0, +Edges: 27, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `previous.style (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `previous.symbol (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `deferred.take (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `wide_glyph_foreground_change_does_not_clear_trailing_cell` (FUNCTION_DEF)
  • + [新增節點] `wide_glyph_style_change_clears_trailing_cell_before_repaint` (FUNCTION_DEF)
  • + [新增節點] `current.style (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `wide_glyph_style_change_resumes_after_repaint` (FUNCTION_DEF)
  • + [新增呼叫邊] `BufferDiff::next` ──[CALLS]──> `deferred.take (External/Unresolved)`
  • + [新增呼叫邊] `BufferDiff::next` ──[CALLS]──> `previous.symbol (External/Unresolved)`
  • + [新增呼叫邊] `BufferDiff::next` ──[CALLS]──> `current.style (External/Unresolved)`
  • + [新增呼叫邊] `BufferDiff::next` ──[CALLS]──> `previous.style (External/Unresolved)`
  • + [新增呼叫邊] `BufferDiff::next` ──[CALLS]──> `BufferDiff::next`
  • + [新增呼叫邊] `wide_glyph_style_change_clears_trailing_cell_before_repaint` ──[CALLS]──> `BufferDiff::new`
  • + [新增呼叫邊] `wide_glyph_style_change_clears_trailing_cell_before_repaint` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `wide_glyph_style_change_clears_trailing_cell_before_repaint` ──[CALLS]──> `prev.set_string (External/Unresolved)`
  • _... 以及其餘 19 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `BufferDiff::next()`
- **變更前簽章 (Before)**: `fn BufferDiff::next(&mut self)` (L92~L198)
- **變更後簽章 (After)**: `fn BufferDiff::next(&mut self)` (L94~L224)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn next(&mut self) -> Option<Self::Item> {
        let len = self.next.len().min(self.prev.len());

        // First, yield any pending trailing cells.
        if let Some(TrailingState {
            next_index,
            end,
            force,
        }) = &mut self.trailing
        {
            while *next_index < *end {
                let j = *next_index;
                // Advance past this cell; if it is wide, also skip its own trailing column
                // so the main loop does not emit a spurious EMPTY write over it.
                let cell_width = self.next[j].cell_width().max(1) as usize;
                *next_index += cell_width;
                *end = (*end).max(*next_index).min(len);

                if !is_skip(&self.next[j])
                    && (*force || self.prev[j].symbol() != self.next[j].symbol())
                {
                    let (tx, ty) = self.pos_of(j);
                    return Some((tx, ty, &self.next[j]));
                }
            }

            // Done with trailing cells; resume main loop past the wide character.
            self.pos = *end;
            self.trailing = None;
        }
        while self.pos < len {
            let i = self.pos;
            self.pos += 1;

            let current = &self.next[i];
            let previous = &self.prev[i];

            match current.diff_option {
                CellDiffOption::Skip => {}
                _ if is_skip(current) => {}

                CellDiffOption::ForcedWidth(width) => {
                    self.pos = self
                        .pos
                        .saturating_add(width.get().saturating_sub(1) as usize);
                    if current != previous {
                        let (x, y) = self.pos_of(i);
                        return Some((x, y, &self.next[i]));
                    }
                }
                CellDiffOption::None | CellDiffOption::AlwaysUpdate => {
                    // If the current cell is multi-width, ensure the trailing cells are
                    // explicitly cleared when they previously contained non-blank content.
                    // Some terminals do not reliably clear the trailing cell(s) when printing
                    // a wide grapheme, which can result in visual artifacts (e.g., leftover
                    // characters). Emitting an explicit update for the trailing cells avoids
                    // this.
                    let cell_width = current.cell_width() as usize;
                    if matches!(current.diff_option, CellDiffOption::None) && current == previous {
                        // Equal cells still need to account for multi-width skip.
                        self.pos += cell_width.saturating_sub(1);
                        continue;
                    }

                    let previous_width = previous.cell_width() as usize;

                    // Work around terminals that fail to clear the trailing cell of certain
                    // emoji presentation sequences (those containing VS16 / U+FE0F).
                    // Only emit explicit clears for such sequences to avoid bloating diffs
                    // for standard wide characters (e.g., CJK), which terminals handle well.
                    let contains_vs16 =
                        cell_width > 1 && current.symbol().chars().any(|c| c == '\u{FE0F}');

                    if contains_vs16 {
                        let trailing_end = (i + cell_width).min(len);
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: trailing_end,
                            force: false,
                        });
                    } else if cell_width > 1 {
                        self.pos += cell_width.saturating_sub(1);
                    } else if previous_width > cell_width
                        && (previous.bg != Color::Reset
                            || previous.modifier.intersects(VISIBLE_ON_BLANK))
                    {
                        // The previous wide character's style is visible on blank cells, so the
                        // terminal may still show it on the trailing columns even after the
                        // character is replaced. Force-emit every cell in the trailing range to
                        // refresh the terminal regardless of whether the buffer content changed.
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + previous_width).min(len),
                            force: true,
                        });
                    } else {
                        // single-width character, no position adjustment needed
                    }

                    let (x, y) = self.pos_of(i);
                    return Some((x, y, &self.next[i]));
                }
            }
        }

        None
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn next(&mut self) -> Option<Self::Item> {
        let len = self.next.len().min(self.prev.len());

        // First, yield any pending trailing cells.
        if let Some(TrailingState {
            next_index,
            end,
            force,
            deferred,
        }) = &mut self.trailing
        {
            while *next_index < *end {
                let j = *next_index;
                // Advance past this cell; if it is wide, also skip its own trailing column
                // so the main loop does not emit a spurious EMPTY write over it.
                let cell_width = self.next[j].cell_width().max(1) as usize;
                *next_index += cell_width;
                *end = (*end).max(*next_index).min(len);

                if !is_skip(&self.next[j])
                    && (*force || self.prev[j].symbol() != self.next[j].symbol())
                {
                    let (tx, ty) = self.pos_of(j);
                    return Some((tx, ty, &self.next[j]));
                }
            }

            // Done with trailing cells; resume past the wide character, repainting its leading
            // cell first when the trailing cells were a pre-clear.
            self.pos = *end;
            let deferred = deferred.take();
            self.trailing = None;
            if let Some(i) = deferred {
                let (x, y) = self.pos_of(i);
                return Some((x, y, &self.next[i]));
            }
        }
        while self.pos < len {
            let i = self.pos;
            self.pos += 1;

            let current = &self.next[i];
            let previous = &self.prev[i];

            match current.diff_option {
                CellDiffOption::Skip => {}
                _ if is_skip(current) => {}

                CellDiffOption::ForcedWidth(width) => {
                    self.pos = self
                        .pos
                        .saturating_add(width.get().saturating_sub(1) as usize);
                    if current != previous {
                        let (x, y) = self.pos_of(i);
                        return Some((x, y, &self.next[i]));
                    }
                }
                CellDiffOption::None | CellDiffOption::AlwaysUpdate => {
                    // If the current cell is multi-width, ensure the trailing cells are
                    // explicitly cleared when they previously contained non-blank content.
                    // Some terminals do not reliably clear the trailing cell(s) when printing
                    // a wide grapheme, which can result in visual artifacts (e.g., leftover
                    // characters). Emitting an explicit update for the trailing cells avoids
                    // this.
                    let cell_width = current.cell_width() as usize;
                    if matches!(current.diff_option, CellDiffOption::None) && current == previous {
                        // Equal cells still need to account for multi-width skip.
                        self.pos += cell_width.saturating_sub(1);
                        continue;
                    }

                    let previous_width = previous.cell_width() as usize;
                    let previous_style_is_visible_on_blank = previous.bg != Color::Reset
                        || previous.modifier.intersects(VISIBLE_ON_BLANK);

                    // Clear stale styles from an unchanged wide glyph's trailing cells before
                    // repainting it.
                    if cell_width > 1
                        && current.symbol() == previous.symbol()
                        && current.style() != previous.style()
                        && previous_style_is_visible_on_blank
                    {
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + cell_width).min(len),
                            force: true,
                            deferred: Some(i),
                        });
                        return self.next();
                    }

                    // Work around terminals that fail to clear the trailing cell of certain
                    // emoji presentation sequences (those containing VS16 / U+FE0F).
                    // Only emit explicit clears for such sequences to avoid bloating diffs
                    // for standard wide characters (e.g., CJK), which terminals handle well.
                    let contains_vs16 =
                        cell_width > 1 && current.symbol().chars().any(|c| c == '\u{FE0F}');

                    if contains_vs16 {
                        let trailing_end = (i + cell_width).min(len);
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: trailing_end,
                            force: false,
                            deferred: None,
                        });
                    } else if cell_width > 1 {
                        self.pos += cell_width.saturating_sub(1);
                    } else if previous_width > cell_width && previous_style_is_visible_on_blank {
                        // The previous wide character's style is visible on blank cells, so the
                        // terminal may still show it on the trailing columns even after the
                        // character is replaced. Force-emit every cell in the trailing range to
                        // refresh the terminal regardless of whether the buffer content changed.
                        self.trailing = Some(TrailingState {
                            next_index: i + 1,
                            end: (i + previous_width).min(len),
                            force: true,
                            deferred: None,
                        });
                    } else {
                        // single-width character, no position adjustment needed
                    }

                    let (x, y) = self.pos_of(i);
                    return Some((x, y, &self.next[i]));
                }
            }
        }

        None
    }
```


#### 📄 檔案: `ratatui-crossterm/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:102, E:129, A:0) ➔ After(N:111, E:150, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 0, +Edges: 21, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `Style::new()
                .fg(Color::Red)
                .add_modifier (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `output.find(&MoveTo(1, 0).to_string()).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `MoveTo(0, 0).to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `output.find('한').unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `output.find(' ').unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` (FUNCTION_DEF)
  • + [新增節點] `Style::new()
                .fg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `output.find (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `output.find(&MoveTo(0, 0).to_string()).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `CrosstermBackend::new`
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `prev.set_string (External/Unresolved)`
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `Style::new()
                .fg(Color::Red)
                .add_modifier (External/Unresolved)`
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `Style::new()
                .fg (External/Unresolved)`
  • + [新增呼叫邊] `draw_clears_trailing_cell_before_repainting_styled_wide_glyph` ──[CALLS]──> `next.set_string (External/Unresolved)`
  • _... 以及其餘 15 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #14: `a1b0b9ca`
- **完整 Hash**: `a1b0b9cad9d3033f0ab20d368f8b37dace933149`
- **說明 (Ground Truth)**: fix(backend): avoid overflow when tracking cursor position (#2735)
- **變更檔案數**: 3

#### 📄 檔案: `ratatui-crossterm/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:101, E:124, A:0) ➔ After(N:102, E:129, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `draw_moves_cursor_when_previous_width_overflows` (FUNCTION_DEF)
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `CrosstermBackend::new`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `forced.set_diff_option (External/Unresolved)`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `CellDiffOption::ForcedWidth (External/Unresolved)`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `draw_to_string`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `assert! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `CrosstermBackend::draw()`
- **變更前簽章 (Before)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L294)
- **變更後簽章 (After)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L294)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```


#### 📄 檔案: `ratatui-termina/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:168, E:266, A:0) ➔ After(N:172, E:278, A:0)
- **差分統計**: +Nodes: 4, -Nodes: 0, +Edges: 12, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `CellDiffOption::ForcedWidth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cursor_position(Position::new(0, 0)).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `forced.set_diff_option (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `moves_cursor_when_previous_width_overflows` (FUNCTION_DEF)
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `backend`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `MockTerminal::new`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `forced.set_diff_option (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `CellDiffOption::ForcedWidth (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `backend.draw(content.into_iter()).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `TerminaBackend::draw`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `content.into_iter (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `MockTerminal::output`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `Csi::Cursor (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `cursor_position(Position::new(0, 0)).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `moves_cursor_when_previous_width_overflows` ──[CALLS]──> `cursor_position`
  • _... 以及其餘 1 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TerminaBackend::draw()`
- **變更前簽章 (Before)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L190)
- **變更後簽章 (After)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L190)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```


#### 📄 檔案: `ratatui-termion/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:124, E:138, A:0) ➔ After(N:127, E:143, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `CellDiffOption::ForcedWidth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_moves_cursor_when_previous_width_overflows` (FUNCTION_DEF)
  • + [新增節點] `forced.set_diff_option (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `TermionBackend::new`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `forced.set_diff_option (External/Unresolved)`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `CellDiffOption::ForcedWidth (External/Unresolved)`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `draw_to_string`
  • + [新增呼叫邊] `draw_moves_cursor_when_previous_width_overflows` ──[CALLS]──> `assert! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TermionBackend::draw()`
- **變更前簽章 (Before)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L270)
- **變更後簽章 (After)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L270)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if p.x.checked_add(w) == Some(x) && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```


---

### 🔹 Commit #15: `13f6cfed`
- **完整 Hash**: `13f6cfedda004bc0d7369754587dc25376b30b14`
- **說明 (Ground Truth)**: fix(backend): account for symbol width when skipping cursor moves (#2721)
- **變更檔案數**: 3

#### 📄 檔案: `ratatui-crossterm/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:78, E:87, A:0) ➔ After(N:101, E:124, A:0)
- **差分統計**: +Nodes: 23, -Nodes: 0, +Edges: 37, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `CellDiffOption::ForcedWidth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_to_string` (FUNCTION_DEF)
  • + [新增節點] `prev.diff(&next).into_iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell.cell_width (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `String::from_utf8_lossy(&out).into_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prev.set_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `content.iter().copied (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `MoveTo(1, 0).to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_uses_forced_width_for_cursor_tracking` (FUNCTION_DEF)
  • + [新增節點] `forced.set_diff_option (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prev.diff(&next).into_iter().collect (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::empty (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_moves_cursor_after_wide_symbol` (FUNCTION_DEF)
  • + [新增節點] `content.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `CrosstermBackend::new(&mut out)
            .draw(content.iter().copied())
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • _... 以及其餘 45 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `CrosstermBackend::draw()`
- **變更前簽章 (Before)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L292)
- **變更後簽章 (After)**: `fn CrosstermBackend::draw(&mut self, content: I)` (L232~L294)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        let mut last_pos: Option<Position> = None;
        for (x, y, cell) in content {
            // Move the cursor if the previous location was not (x - 1, y)
            if !matches!(last_pos, Some(p) if x == p.x + 1 && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            last_pos = Some(Position { x, y });
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                queue!(self.writer, MoveTo(x, y))?;
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                let diff = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                };
                diff.queue(&mut self.writer)?;
                modifier = cell.modifier;
            }
            if cell.fg != fg || cell.bg != bg {
                queue!(
                    self.writer,
                    SetColors(CrosstermColors::new(
                        cell.fg.into_crossterm(),
                        cell.bg.into_crossterm(),
                    ))
                )?;
                fg = cell.fg;
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                let color = cell.underline_color.into_crossterm();
                queue!(self.writer, SetUnderlineColor(color))?;
                underline_color = cell.underline_color;
            }

            queue!(self.writer, Print(cell.symbol()))?;
        }

        #[cfg(feature = "underline-color")]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetUnderlineColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
        #[cfg(not(feature = "underline-color"))]
        return queue!(
            self.writer,
            SetForegroundColor(CrosstermColor::Reset),
            SetBackgroundColor(CrosstermColor::Reset),
            SetAttribute(CrosstermAttribute::Reset),
        );
    }
```


#### 📄 檔案: `ratatui-termina/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:162, E:235, A:0) ➔ After(N:168, E:266, A:0)
- **差分統計**: +Nodes: 6, -Nodes: 0, +Edges: 31, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `cell.cell_width (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cursor_position(Position::new(1, 0)).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `skips_cursor_move_after_wide_symbol_when_contiguous` (FUNCTION_DEF)
  • + [新增節點] `draws_cursor_move_after_wide_symbol` (FUNCTION_DEF)
  • + [新增節點] `skips_cursor_move_for_contiguous_cells` (FUNCTION_DEF)
  • + [新增節點] `cursor_position(Position::new(2, 0)).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `TerminaBackend::draw` ──[CALLS]──> `cell.cell_width (External/Unresolved)`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `backend`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `MockTerminal::new`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `backend.draw(content.into_iter()).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `TerminaBackend::draw`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `content.into_iter (External/Unresolved)`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `MockTerminal::output`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `Csi::Cursor (External/Unresolved)`
  • + [新增呼叫邊] `draws_cursor_move_after_wide_symbol` ──[CALLS]──> `cursor_position(Position::new(1, 0)).unwrap (External/Unresolved)`
  • _... 以及其餘 22 項拓樸變更_

ℹ️ **存量環境提醒**: 檔案內含 1 項既有技術債提醒 (非本次 Commit 引入，不予阻礙發布)

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TerminaBackend::draw()`
- **變更前簽章 (Before)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L187)
- **變更後簽章 (After)**: `fn TerminaBackend::draw(&mut self, content: I)` (L139~L190)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        let mut last_pos: Option<Position> = None;
        for (x, y, cell) in content {
            if !matches!(last_pos, Some(p) if x == p.x + 1 && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            last_pos = Some(Position { x, y });

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        #[cfg(feature = "underline-color")]
        let mut underline_color = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                let command = Csi::Cursor(cursor_position(Position { x, y })?);
                write!(string, "{command}").unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));

            let mut attributes = SgrAttributes::default();
            if cell.fg != fg {
                attributes.foreground = Some(cell.fg.into_termina());
                fg = cell.fg;
            }
            if cell.bg != bg {
                attributes.background = Some(cell.bg.into_termina());
                bg = cell.bg;
            }
            #[cfg(feature = "underline-color")]
            if cell.underline_color != underline_color {
                attributes.underline_color = Some(cell.underline_color.into_termina());
                underline_color = cell.underline_color;
            }
            if cell.modifier != modifier {
                attributes.modifiers = ModifierDiff {
                    from: modifier,
                    to: cell.modifier,
                }
                .into_termina();
                modifier = cell.modifier;
            }
            if !attributes.is_empty() {
                write!(string, "{}", Csi::Sgr(Sgr::Attributes(attributes))).unwrap();
            }

            string.push_str(cell.symbol());
        }

        write!(self.terminal, "{string}{}", Csi::Sgr(Sgr::Reset))
    }
```


#### 📄 檔案: `ratatui-termion/src/lib.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:112, E:119, A:0) ➔ After(N:124, E:138, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 0, +Edges: 19, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `draw_to_string` (FUNCTION_DEF)
  • + [新增節點] `cell.cell_width (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `String::from_utf8_lossy(&out).into_owned (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `termion::cursor::Goto(2, 1).to_string (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `content.iter().copied (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `TermionBackend::new(&mut out)
            .draw(content.iter().copied())
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `termion::cursor::Goto (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_moves_cursor_after_wide_symbol` (FUNCTION_DEF)
  • + [新增節點] `content.iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `String::from_utf8_lossy (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `draw_skips_cursor_move_after_wide_symbol_when_contiguous` (FUNCTION_DEF)
  • + [新增節點] `draw_skips_cursor_move_for_contiguous_cells` (FUNCTION_DEF)
  • + [新增呼叫邊] `TermionBackend::draw` ──[CALLS]──> `cell.cell_width (External/Unresolved)`
  • + [新增呼叫邊] `draw_to_string` ──[CALLS]──> `TermionBackend::new`
  • + [新增呼叫邊] `draw_to_string` ──[CALLS]──> `TermionBackend::new(&mut out)
            .draw(content.iter().copied())
            .unwrap (External/Unresolved)`
  • _... 以及其餘 16 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `TermionBackend::draw()`
- **變更前簽章 (Before)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L268)
- **變更後簽章 (After)**: `fn TermionBackend::draw(&mut self, content: I)` (L222~L270)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        let mut last_pos: Option<Position> = None;
        for (x, y, cell) in content {
            // Move the cursor if the previous location was not (x - 1, y)
            if !matches!(last_pos, Some(p) if x == p.x + 1 && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            last_pos = Some(Position { x, y });
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw<'a, I>(&mut self, content: I) -> io::Result<()>
    where
        I: Iterator<Item = (u16, u16, &'a Cell)>,
    {
        use std::fmt::Write;

        let mut string = String::with_capacity(content.size_hint().0 * 3);
        let mut fg = Color::Reset;
        let mut bg = Color::Reset;
        let mut modifier = Modifier::empty();
        // Position and width of the last cell written, used to skip redundant cursor moves.
        let mut last: Option<(Position, u16)> = None;
        for (x, y, cell) in content {
            // Move the cursor unless it already sits at (x, y), i.e. this cell directly follows
            // the previous one on the same row, accounting for the width of what was printed.
            if !matches!(last, Some((p, w)) if x == p.x + w && y == p.y) {
                write!(string, "{}", termion::cursor::Goto(x + 1, y + 1)).unwrap();
            }
            last = Some((Position { x, y }, cell.cell_width()));
            if cell.modifier != modifier {
                write!(
                    string,
                    "{}",
                    ModifierDiff {
                        from: modifier,
                        to: cell.modifier
                    }
                )
                .unwrap();
                modifier = cell.modifier;
            }
            if cell.fg != fg {
                write!(string, "{}", Fg(cell.fg)).unwrap();
                fg = cell.fg;
            }
            if cell.bg != bg {
                write!(string, "{}", Bg(cell.bg)).unwrap();
                bg = cell.bg;
            }
            string.push_str(cell.symbol());
        }
        write!(
            self.writer,
            "{string}{}{}{}",
            Fg(Color::Reset),
            Bg(Color::Reset),
            termion::style::Reset,
        )
    }
```


---

### 🔹 Commit #16: `1b73a281`
- **完整 Hash**: `1b73a281296aaafef10fba9d940f5af2f48223d3`
- **說明 (Ground Truth)**: fix(buffer): treat multi-grapheme cell symbols as single-width (#2697)
- **變更檔案數**: 2

#### 📄 檔案: `ratatui-core/src/buffer/cell.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:52, E:65, A:0) ➔ After(N:63, E:81, A:0)
- **差分統計**: +Nodes: 12, -Nodes: 1, +Edges: 17, -Edges: 1, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `graphemes.next().is_some (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `CellDiffOption::ForcedWidth (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `NonZeroU16::new(24).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `graphemes.next (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `width.get (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell_width_of_wide_grapheme` (FUNCTION_DEF)
  • + [新增節點] `graphemes.next().is_none (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `symbol.graphemes (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `"\u{1b}[s".repeat (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `cell_width_of_escape_sequence_symbol` (FUNCTION_DEF)
  • + [新增節點] `cell_width_of_forced_width_symbol` (FUNCTION_DEF)
  • + [新增節點] `is_single_grapheme` (FUNCTION_DEF)
  • - [移除節點] `w.get (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Cell::cell_width` ──[CALLS]──> `width.get (External/Unresolved)`
  • + [新增呼叫邊] `Cell::cell_width` ──[CALLS]──> `is_single_grapheme`
  • _... 以及其餘 16 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Cell::cell_width()`
- **變更前簽章 (Before)**: `fn Cell::cell_width(&self)` (L312~L317)
- **變更後簽章 (After)**: `fn Cell::cell_width(&self)` (L319~L330)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn cell_width(&self) -> u16 {
        match self.diff_option {
            CellDiffOption::ForcedWidth(w) => w.get(),
            _ => self.symbol().cell_width(),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn cell_width(&self) -> u16 {
        if let CellDiffOption::ForcedWidth(width) = self.diff_option {
            return width.get();
        }
        let symbol = self.symbol();
        let width = symbol.cell_width();
        if width > 1 && !is_single_grapheme(symbol) {
            1
        } else {
            width
        }
    }
```


#### 📄 檔案: `ratatui-core/src/buffer/diff.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:76, E:145, A:0) ➔ After(N:85, E:166, A:0)
- **差分統計**: +Nodes: 9, -Nodes: 0, +Edges: 21, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `prev.clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `next[(1, 0)].set_bg (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Buffer::filled (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `next[(10, 0)].set_symbol (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `prev[(10, 0)].set_symbol (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `identical_wide_glyph_hides_trailing_cell_changes` (FUNCTION_DEF)
  • + [新增節點] `long_symbol_does_not_hide_later_cells` (FUNCTION_DEF)
  • + [新增節點] `unchanged_long_symbol_does_not_hide_later_cells` (FUNCTION_DEF)
  • + [新增節點] `"\u{1b}[s".repeat (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `BufferDiff::new`
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `Buffer::filled (External/Unresolved)`
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `next[(10, 0)].set_symbol (External/Unresolved)`
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `"\u{1b}[s".repeat (External/Unresolved)`
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `BufferDiff::new(&prev, &next).collect (External/Unresolved)`
  • + [新增呼叫邊] `long_symbol_does_not_hide_later_cells` ──[CALLS]──> `assert_eq! (Macro)`
  • _... 以及其餘 15 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #17: `63db5f58`
- **完整 Hash**: `63db5f58b3cc520924acb46d5d8e318c852b7bfc`
- **說明 (Ground Truth)**: fix(gauge): include cell after label in filled area (#2579)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-widgets/src/gauge.rs`
- **變更分類**: `BODY_LEVEL_SEMANTIC_DELTA`
- **圖譜變更**: Before(N:87, E:112, A:0) ➔ After(N:87, E:112, A:0)
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

### 🔹 函式: `Gauge::render_gauge()`
- **變更前簽章 (Before)**: `fn Gauge::render_gauge(&self, gauge_area: Rect, buf: &mut Buffer)` (L170~L216)
- **變更後簽章 (After)**: `fn Gauge::render_gauge(&self, gauge_area: Rect, buf: &mut Buffer)` (L170~L216)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn render_gauge(&self, gauge_area: Rect, buf: &mut Buffer) {
        if gauge_area.is_empty() {
            return;
        }

        buf.set_style(gauge_area, self.gauge_style);

        // compute label value and its position
        // label is put at the center of the gauge_area
        let default_label = Span::raw(format!("{}%", f64::round(self.ratio * 100.0)));
        let label = self.label.as_ref().unwrap_or(&default_label);
        let clamped_label_width = gauge_area.width.min(label.width() as u16);
        let label_col = gauge_area.left() + (gauge_area.width - clamped_label_width) / 2;
        let label_row = gauge_area.top() + gauge_area.height / 2;

        // the gauge will be filled proportionally to the ratio
        let filled_width = f64::from(gauge_area.width) * self.ratio;
        let end = if self.use_unicode {
            gauge_area.left() + filled_width.floor() as u16
        } else {
            gauge_area.left() + filled_width.round() as u16
        };
        for y in gauge_area.top()..gauge_area.bottom() {
            // render the filled area (left to end)
            for x in gauge_area.left()..end {
                // Use full block for the filled part of the gauge and spaces for the part that is
                // covered by the label. Note that the background and foreground colors are swapped
                // for the label part, otherwise the gauge will be inverted
                if x < label_col || x > label_col + clamped_label_width || y != label_row {
                    buf[(x, y)]
                        .set_symbol(symbols::block::FULL)
                        .set_fg(self.gauge_style.fg.unwrap_or(Color::Reset))
                        .set_bg(self.gauge_style.bg.unwrap_or(Color::Reset));
                } else {
                    buf[(x, y)]
                        .set_symbol(" ")
                        .set_fg(self.gauge_style.bg.unwrap_or(Color::Reset))
                        .set_bg(self.gauge_style.fg.unwrap_or(Color::Reset));
                }
            }
            if self.use_unicode && self.ratio < 1.0 {
                buf[(end, y)].set_symbol(get_unicode_block(filled_width % 1.0));
            }
        }
        // render the label
        buf.set_span(label_col, label_row, label, clamped_label_width);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn render_gauge(&self, gauge_area: Rect, buf: &mut Buffer) {
        if gauge_area.is_empty() {
            return;
        }

        buf.set_style(gauge_area, self.gauge_style);

        // compute label value and its position
        // label is put at the center of the gauge_area
        let default_label = Span::raw(format!("{}%", f64::round(self.ratio * 100.0)));
        let label = self.label.as_ref().unwrap_or(&default_label);
        let clamped_label_width = gauge_area.width.min(label.width() as u16);
        let label_col = gauge_area.left() + (gauge_area.width - clamped_label_width) / 2;
        let label_row = gauge_area.top() + gauge_area.height / 2;

        // the gauge will be filled proportionally to the ratio
        let filled_width = f64::from(gauge_area.width) * self.ratio;
        let end = if self.use_unicode {
            gauge_area.left() + filled_width.floor() as u16
        } else {
            gauge_area.left() + filled_width.round() as u16
        };
        for y in gauge_area.top()..gauge_area.bottom() {
            // render the filled area (left to end)
            for x in gauge_area.left()..end {
                // Use full block for the filled part of the gauge and spaces for the part that is
                // covered by the label. Note that the background and foreground colors are swapped
                // for the label part, otherwise the gauge will be inverted
                if x < label_col || x >= label_col + clamped_label_width || y != label_row {
                    buf[(x, y)]
                        .set_symbol(symbols::block::FULL)
                        .set_fg(self.gauge_style.fg.unwrap_or(Color::Reset))
                        .set_bg(self.gauge_style.bg.unwrap_or(Color::Reset));
                } else {
                    buf[(x, y)]
                        .set_symbol(" ")
                        .set_fg(self.gauge_style.bg.unwrap_or(Color::Reset))
                        .set_bg(self.gauge_style.fg.unwrap_or(Color::Reset));
                }
            }
            if self.use_unicode && self.ratio < 1.0 {
                buf[(end, y)].set_symbol(get_unicode_block(filled_width % 1.0));
            }
        }
        // render the label
        buf.set_span(label_col, label_row, label, clamped_label_width);
    }
```


---

### 🔹 Commit #18: `c64fac0d`
- **完整 Hash**: `c64fac0dfa6d908417982813ec04a325d5ccc469`
- **說明 (Ground Truth)**: chore(clippy): fix new Rust lints (#2728)
- **變更檔案數**: 2

#### 📄 檔案: `ratatui-core/src/buffer/diff.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:76, E:145, A:0) ➔ After(N:76, E:145, A:0)
- **差分統計**: +Nodes: 0, -Nodes: 0, +Edges: 2, -Edges: 2, ΔFuncs: 2, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增呼叫邊] `empty_buffers_yield_no_diffs` ──[CALLS]──> `assert_eq! (Macro)`
  • + [新增呼叫邊] `identical_buffers_yield_no_diffs` ──[CALLS]──> `assert_eq! (Macro)`
  • - [移除呼叫邊] `empty_buffers_yield_no_diffs` ──[CALLS]──> `assert! (Macro)`
  • - [移除呼叫邊] `identical_buffers_yield_no_diffs` ──[CALLS]──> `assert! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `identical_buffers_yield_no_diffs()`
- **變更前簽章 (Before)**: `fn identical_buffers_yield_no_diffs()` (L229~L233)
- **變更後簽章 (After)**: `fn identical_buffers_yield_no_diffs()` (L229~L233)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn identical_buffers_yield_no_diffs() {
        let buf = Buffer::with_lines(["hello"]);
        let diff: Vec<_> = BufferDiff::new(&buf, &buf).collect();
        assert!(diff.is_empty());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn identical_buffers_yield_no_diffs() {
        let buf = Buffer::with_lines(["hello"]);
        let diff: Vec<_> = BufferDiff::new(&buf, &buf).collect();
        assert_eq!(diff, Vec::new());
    }
```

### 🔹 函式: `empty_buffers_yield_no_diffs()`
- **變更前簽章 (Before)**: `fn empty_buffers_yield_no_diffs()` (L221~L226)
- **變更後簽章 (After)**: `fn empty_buffers_yield_no_diffs()` (L221~L226)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn empty_buffers_yield_no_diffs() {
        let rect = Rect::new(0, 0, 5, 1);
        let buf = Buffer::empty(rect);
        let diff: Vec<_> = BufferDiff::new(&buf, &buf).collect();
        assert!(diff.is_empty());
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn empty_buffers_yield_no_diffs() {
        let rect = Rect::new(0, 0, 5, 1);
        let buf = Buffer::empty(rect);
        let diff: Vec<_> = BufferDiff::new(&buf, &buf).collect();
        assert_eq!(diff, Vec::new());
    }
```


#### 📄 檔案: `ratatui-widgets/src/barchart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:220, E:535, A:0) ➔ After(N:219, E:534, A:0)
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
  • - [移除節點] `assert! (Macro)` (FUNCTION_DEF)
  • - [移除呼叫邊] `constructors_ignore_empty_groups` ──[CALLS]──> `assert! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `constructors_ignore_empty_groups()`
- **變更前簽章 (Before)**: `fn constructors_ignore_empty_groups()` (L761~L770)
- **變更後簽章 (After)**: `fn constructors_ignore_empty_groups()` (L761~L770)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn constructors_ignore_empty_groups() {
        assert!(BarChart::new(Vec::<Bar>::new()).data.is_empty());
        assert!(BarChart::horizontal(Vec::<Bar>::new()).data.is_empty());

        let chart = BarChart::grouped([
            BarGroup::new(Vec::<Bar>::new()),
            BarGroup::new([Bar::new(1)]),
        ]);
        assert_eq!(chart.data, vec![BarGroup::new([Bar::new(1)])]);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn constructors_ignore_empty_groups() {
        assert_eq!(BarChart::new(Vec::<Bar>::new()).data, Vec::new());
        assert_eq!(BarChart::horizontal(Vec::<Bar>::new()).data, Vec::new());

        let chart = BarChart::grouped([
            BarGroup::new(Vec::<Bar>::new()),
            BarGroup::new([Bar::new(1)]),
        ]);
        assert_eq!(chart.data, vec![BarGroup::new([Bar::new(1)])]);
    }
```


---

### 🔹 Commit #19: `a52adf36`
- **完整 Hash**: `a52adf36ceb9de73c635bbef981e7a193a225a47`
- **說明 (Ground Truth)**: fix(canvas): ignore non-finite coordinates (#2722)
- **變更檔案數**: 3

#### 📄 檔案: `ratatui-widgets/src/canvas.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:105, E:136, A:0) ➔ After(N:108, E:141, A:0)
- **差分統計**: +Nodes: 3, -Nodes: 0, +Edges: 5, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `y.is_finite (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `get_point_rejects_non_finite_coordinates` (FUNCTION_DEF)
  • + [新增節點] `x.is_finite (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Painter::get_point` ──[CALLS]──> `x.is_finite (External/Unresolved)`
  • + [新增呼叫邊] `Painter::get_point` ──[CALLS]──> `y.is_finite (External/Unresolved)`
  • + [新增呼叫邊] `get_point_rejects_non_finite_coordinates` ──[CALLS]──> `Context::new`
  • + [新增呼叫邊] `get_point_rejects_non_finite_coordinates` ──[CALLS]──> `Painter::from`
  • + [新增呼叫邊] `get_point_rejects_non_finite_coordinates` ──[CALLS]──> `assert_eq! (Macro)`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Painter::get_point()`
- **變更前簽章 (Before)**: `fn Painter::get_point(&self, x: f64, y: f64)` (L449~L463)
- **變更後簽章 (After)**: `fn Painter::get_point(&self, x: f64, y: f64)` (L449~L463)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn get_point(&self, x: f64, y: f64) -> Option<(usize, usize)> {
        let [left, right] = self.context.x_bounds;
        let [bottom, top] = self.context.y_bounds;
        if x < left || x > right || y < bottom || y > top {
            return None;
        }
        let width = right - left;
        let height = top - bottom;
        if width <= 0.0 || height <= 0.0 {
            return None;
        }
        let x = ((x - left) * (self.resolution.0 - 1.0) / width).round() as usize;
        let y = ((top - y) * (self.resolution.1 - 1.0) / height).round() as usize;
        Some((x, y))
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn get_point(&self, x: f64, y: f64) -> Option<(usize, usize)> {
        let [left, right] = self.context.x_bounds;
        let [bottom, top] = self.context.y_bounds;
        if !x.is_finite() || !y.is_finite() || x < left || x > right || y < bottom || y > top {
            return None;
        }
        let width = right - left;
        let height = top - bottom;
        if width <= 0.0 || height <= 0.0 {
            return None;
        }
        let x = ((x - left) * (self.resolution.0 - 1.0) / width).round() as usize;
        let y = ((top - y) * (self.resolution.1 - 1.0) / height).round() as usize;
        Some((x, y))
    }
```


#### 📄 檔案: `ratatui-widgets/src/canvas/line.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:43, E:62, A:0) ➔ After(N:48, E:76, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 14, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `[self.x1, self.y1, self.x2, self.y2]
            .iter()
            .any (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Canvas::default()
            .marker(Marker::Dot)
            .x_bounds([0.0, 10.0])
            .y_bounds([10.0, 0.0])
            .paint (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `non_finite_endpoint_draws_nothing` (FUNCTION_DEF)
  • + [新增節點] `[self.x1, self.y1, self.x2, self.y2]
            .iter (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `coordinate.is_finite (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `Line::draw` ──[CALLS]──> `[self.x1, self.y1, self.x2, self.y2]
            .iter()
            .any (External/Unresolved)`
  • + [新增呼叫邊] `Line::draw` ──[CALLS]──> `[self.x1, self.y1, self.x2, self.y2]
            .iter (External/Unresolved)`
  • + [新增呼叫邊] `Line::draw` ──[CALLS]──> `coordinate.is_finite (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `FilledLine::new`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Canvas::default()
            .marker(Marker::Dot)
            .x_bounds([0.0, 10.0])
            .y_bounds([10.0, 0.0])
            .paint (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Canvas::default()
            .marker(Marker::Dot)
            .x_bounds([0.0, 10.0])
            .y_bounds (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Canvas::default()
            .marker(Marker::Dot)
            .x_bounds (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Canvas::default()
            .marker (External/Unresolved)`
  • + [新增呼叫邊] `non_finite_endpoint_draws_nothing` ──[CALLS]──> `Canvas::default (External/Unresolved)`
  • _... 以及其餘 4 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Line::draw()`
- **變更前簽章 (Before)**: `fn Line::draw(&self, painter: &mut Painter)` (L48~L63)
- **變更後簽章 (After)**: `fn Line::draw(&self, painter: &mut Painter)` (L48~L69)

#### ◀️ 變更前實作碼 (Before Implementation):
```
fn draw(&self, painter: &mut Painter) {
        let (x_bounds, y_bounds) = painter.bounds();
        let Some((world_x1, world_y1, world_x2, world_y2)) =
            clip_line(x_bounds, y_bounds, self.x1, self.y1, self.x2, self.y2)
        else {
            return;
        };
        let Some((x1, y1)) = painter.get_point(world_x1, world_y1) else {
            return;
        };
        let Some((x2, y2)) = painter.get_point(world_x2, world_y2) else {
            return;
        };

        draw_line(painter, x1, y1, x2, y2, self.color);
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
fn draw(&self, painter: &mut Painter) {
        if [self.x1, self.y1, self.x2, self.y2]
            .iter()
            .any(|coordinate| !coordinate.is_finite())
        {
            return;
        }
        let (x_bounds, y_bounds) = painter.bounds();
        let Some((world_x1, world_y1, world_x2, world_y2)) =
            clip_line(x_bounds, y_bounds, self.x1, self.y1, self.x2, self.y2)
        else {
            return;
        };
        let Some((x1, y1)) = painter.get_point(world_x1, world_y1) else {
            return;
        };
        let Some((x2, y2)) = painter.get_point(world_x2, world_y2) else {
            return;
        };

        draw_line(painter, x1, y1, x2, y2, self.color);
    }
```


#### 📄 檔案: `ratatui-widgets/src/chart.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:181, E:321, A:0) ➔ After(N:182, E:329, A:0)
- **差分統計**: +Nodes: 1, -Nodes: 0, +Edges: 8, -Edges: 0, ΔFuncs: 0, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `nan_data_point_with_reversed_bounds` (FUNCTION_DEF)
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Chart::y_axis`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Chart::x_axis`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Chart::new`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `vec! (Macro)`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Axis::bounds`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Axis::default (External/Unresolved)`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Buffer::empty (External/Unresolved)`
  • + [新增呼叫邊] `nan_data_point_with_reversed_bounds` ──[CALLS]──> `Chart::render`

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

---

### 🔹 Commit #20: `ff3891ab`
- **完整 Hash**: `ff3891abc6f0844f1aff1283af4391176b3eb0af`
- **說明 (Ground Truth)**: fix(terminal): make insert_before a no-op when the terminal has no rows (#2723)
- **變更檔案數**: 1

#### 📄 檔案: `ratatui-core/src/terminal/inline.rs`
- **變更分類**: `STRUCTURAL_GRAPH_DELTA`
- **圖譜變更**: Before(N:102, E:189, A:0) ➔ After(N:107, E:201, A:0)
- **差分統計**: +Nodes: 5, -Nodes: 0, +Edges: 12, -Edges: 0, ΔFuncs: 1, ΔTrans: 0
- **驗收裁決**: `🟢 READY_TO_SHIP` (通過: `True`)

##### 🌲 語意控制樹變更差分 (Semantic UIA-Diff):
```text
🌲 **UIA 語意控制樹變更差分 (Semantic UIA-Diff):**
---
  _無任何 UI 控制項變更_

🛡️ **形式化守衛狀態遷移 (Invariant Transitions):**
  • _無狀態躍遷變動_

🔗 **結構性拓樸圖變更明細 (Structural Graph Delta):**
  • + [新增節點] `insert_before_is_noop_when_terminal_has_no_rows` (FUNCTION_DEF)
  • + [新增節點] `terminal.backend().scrollback().clone (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal
            .insert_before(2, |buf| buf.set_string(0, 0, "aaaaa", Style::default()))
            .unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `Terminal::with_options(backend, options).unwrap (External/Unresolved)` (FUNCTION_DEF)
  • + [新增節點] `terminal.backend().scrollback (External/Unresolved)` (FUNCTION_DEF)
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `TestBackend::new (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `Viewport::Inline (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `Terminal::with_options(backend, options).unwrap (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `Terminal::with_options (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `terminal.backend().scrollback().clone (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `terminal.backend().scrollback (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `terminal.backend (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `terminal
            .insert_before(2, |buf| buf.set_string(0, 0, "aaaaa", Style::default()))
            .unwrap (External/Unresolved)`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `Terminal::insert_before`
  • + [新增呼叫邊] `insert_before_is_noop_when_terminal_has_no_rows` ──[CALLS]──> `buf.set_string (External/Unresolved)`
  • _... 以及其餘 2 項拓樸變更_

**最終驗收裁決: 🟢 READY_TO_SHIP**
```

##### 🔍 函式實作原始碼變更對照 (Function Implementation Semantic Diff):
## 🔍 函式實作語意變更對照包 (Function Implementation Semantic Diff)

### 🔹 函式: `Terminal::insert_before()`
- **變更前簽章 (Before)**: `fn Terminal::insert_before(&mut self, height: u16, draw_fn: F)` (L109~L120)
- **變更後簽章 (After)**: `fn Terminal::insert_before(&mut self, height: u16, draw_fn: F)` (L111~L123)

#### ◀️ 變更前實作碼 (Before Implementation):
```
pub fn insert_before<F>(&mut self, height: u16, draw_fn: F) -> Result<(), B::Error>
    where
        F: FnOnce(&mut Buffer),
    {
        match self.viewport {
            #[cfg(feature = "scrolling-regions")]
            Viewport::Inline(_) => self.insert_before_scrolling_regions(height, draw_fn),
            #[cfg(not(feature = "scrolling-regions"))]
            Viewport::Inline(_) => self.insert_before_no_scrolling_regions(height, draw_fn),
            _ => Ok(()),
        }
    }
```

#### ▶️ 變更後實作碼 (After Implementation):
```
pub fn insert_before<F>(&mut self, height: u16, draw_fn: F) -> Result<(), B::Error>
    where
        F: FnOnce(&mut Buffer),
    {
        match self.viewport {
            Viewport::Inline(_) if self.last_known_area.height == 0 => Ok(()),
            #[cfg(feature = "scrolling-regions")]
            Viewport::Inline(_) => self.insert_before_scrolling_regions(height, draw_fn),
            #[cfg(not(feature = "scrolling-regions"))]
            Viewport::Inline(_) => self.insert_before_no_scrolling_regions(height, draw_fn),
            _ => Ok(()),
        }
    }
```


---

## 🤖 外部模型 / 人類架構師 Review 指引 (How to Re-verify)

另一台 LLM 或審查者若要獨立覆核本報告的真實性，可直接在終端執行以下標準命令實地檢核：

1. **查看 Commit 原始變更 (Git Ground Truth)**:
   ```powershell
   git -C test_repos/ratatui show d1ef782b48ddf0cb825c111d4d8b9adef572c0e1
   ```
2. **透過 CODE-Map CLI 獨立重現語意差分**:
   ```powershell
   python.exe -X utf8 codemap.py --git-diff d1ef782b48ddf0cb825c111d4d8b9adef572c0e1~1 --file test_repos/ratatui/ratatui-widgets/src/barchart.rs
   ```
