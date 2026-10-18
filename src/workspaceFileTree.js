/**
 * Workspace File Tree Plugin (範例模組)
 * 模擬具有資源回收桶按鈕、事件監聽與非同步刪除因果鏈的 UI 元件
 */

// 1. 宣告核心非同步業務函式 (模組可達作用域)
async function deleteItemToRecycleBin() {
    console.log("【Stage 1】彈出 In-DOM 模態確認對話框");
    await executeDeleteRPC();
    await notifyUserToast();
}

async function executeDeleteRPC() {
    console.log("【Stage 2】調用後端 RPC 刪除檔案至回收桶");
}

async function notifyUserToast() {
    console.log("【Stage 3】顯示檔案已移至回收桶之 Toast 提示");
}

// 2. 動態建立 UI 控制項並綁定事件
const btnDelete = document.createElement('button');
btnDelete.id = 'btnDelete';
btnDelete.className = 'nav-action-button';

// 3. 綁定 click 事件至處理函式
btnDelete.addEventListener('click', deleteItemToRecycleBin);

// 4. 外掛生命週期初始化函式
function init() {
    console.log("檔案樹外掛初始化就緒");
}
