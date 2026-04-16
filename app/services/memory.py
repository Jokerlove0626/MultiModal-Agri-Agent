class MemoryManager:
    def __init__(self):
        self.chat_history = {}

    def get_recent_history(self, session_id: str, limit: int = 4) -> list:
        """获取最近的历史记录（滑动窗口）"""
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []
        return self.chat_history[session_id][-limit:]

    def save_interaction(self, session_id: str, user_query: str, ai_answer: str):
        """保存一轮完整的对话"""
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []
        self.chat_history[session_id].append({"role": "user", "content": user_query})
        self.chat_history[session_id].append({"role": "assistant", "content": ai_answer})
        
    def has_history(self, session_id: str) -> bool:
        """判断是否有历史记录"""
        return session_id in self.chat_history and len(self.chat_history[session_id]) > 0