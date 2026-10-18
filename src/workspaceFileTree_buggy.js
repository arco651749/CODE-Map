/**
 * Workspace File Tree Plugin (Buggy Commit 對照組)
 * 模擬「處理函式被深鎖在 init 內部閉包」以及「使用同步 confirm 阻塞 UI 主執行緒」之真實死穴
 */

// 1. 外部建立按鈕並綁定事件
const btnDelete = document.createElement('button');
btnDelete.id = 'btnDelete';
btnDelete.addEventListener('click', deleteItemToRecycleBin);

// 2. 外掛初始化函式
function init() {
    console.log("初始化檔案樹...");

    // 💥 致命死穴：deleteItemToRecycleBin 被宣告在 init() 內部閉包中！
    // 外部按鈕點擊時將引發 ReferenceError: deleteItemToRecycleBin is not defined
    function deleteItemToRecycleBin() {
        // ⚠️ 危害操作：使用了同步阻塞主執行緒的 confirm
        if (confirm("確定要將檔案丟進回收桶嗎？")) {
            console.log("正在執行刪除...");
        }
    }
}
