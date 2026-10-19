using System;
using System.Threading;

namespace CloudDesk.Client
{
    public class FileExplorerWindow
    {
        public void InitializeControls()
        {
            // WPF / WinUI 控制項事件綁定
            btnDeleteFile.Click += OnDeleteFileClicked;
        }

        private void OnDeleteFileClicked(object sender, EventArgs e)
        {
            // 危害 1: 在 UI 執行緒直接調用同步休眠造成介面凍結
            Thread.Sleep(3000);

            // 危害 2: 呼叫未完成實作的例外
            throw new NotImplementedException("雲端檔案刪除邏輯尚未實作完成");
        }

        public static void Main(string[] args)
        {
            var window = new FileExplorerWindow();
            window.InitializeControls();
        }
    }
}
